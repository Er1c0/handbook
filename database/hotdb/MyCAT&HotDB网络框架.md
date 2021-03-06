[TOC]
#1.三种IO类型
系统I/O 可分为阻塞型, 非阻塞同步型以及非阻塞异步型. 

   阻塞型I/O意味着控制权只到调用操作结束了才会回到调用者手里. 结果调用者被阻塞了, 这段时间了做不了任何其它事情. 更郁闷的是,在等待IO结果的时间里,调用者所在线程此时无法腾出手来去响应其它的请求，这真是太浪费资源了。拿read()操作来说吧, 调用此函数的代码会一直僵在此处直至它所读的socket缓存中有数据到来.
   
   相比之下，非阻塞同步是会立即返回控制权给调用者的。调用者不需要等等，它从调用的函数获取两种结果：要么此次调用成功进行了;要么系统返回错误标识告诉调用者当前资源不可用，你再等等或者再试度看吧。比如read()操作, 如果当前socket无数据可读，则立即返回EWOULBLOCK/EAGAIN，告诉调用read()者"数据还没准备好，你稍后再试".
   
   在非阻塞异步调用中，稍有不同。调用函数在立即返回时，还告诉调用者，这次请求已经开始了。系统会使用另外的资源或者线程来完成这次调用操作，并在完成的时候知会调用者（比如通过回调函数）。拿Windows的ReadFile()或者POSIX的aio_read()来说,调用它之后，函数立即返回，操作系统在后台同时开始读操作。
   在以上三种IO形式中，理论上，非阻塞异步是性能最高、伸缩性最好的。

>同步和异步是相对于应用和内核的交互方式而言的，同步需要主动去询问，而异步的时候内核在IO事件发生的时候通知应用程序，而阻塞和非阻塞仅仅是系统在调用系统调用的时候函数的实现方式而已。

对于JAVA的API来说：
    - java.net.Socket就是典型的阻塞型IO
    - java NIO非阻塞同步
    - java AIO非阻塞异步

   MyCAT起源于Cobar，Cobar前端为NIO后端为BIO，后端就是通过java.net.Socket进行读写，所以Cobar后端每次进行读写都会造成线程阻塞，后端能支持的连接总数就成为瓶颈所在。
   MyCAT在基于Cobar改版时，直接采用了Java 7的AIO，前后端都实现了非阻塞异步。由于Linux并没有真正实现AIO，实际测试下来，AIO并不比NIO快，反而性能上比NIO还要慢。所以MyCAT在2014年下半年，做了一次网络通信框架的大调整，改为同时支持AIO和NIO，通过启动参数让用户来选择哪种方式。虽然现在AIO比NIO慢，但是MyCAT仍然保留了AIO实现，就是为了等Linux真正实现AIO后，可以直接支持。
#2.Reactor和Proactor

**MyCAT同时实现了NIO和AIO，为了便于读者更清楚理解代码实现，先介绍NIO和AIO分布对应的两种设计模式：Reactor和Proactor**


一般情况下，I/O 复用机制需要事件分享器(event demultBossiplexor). 事件分享器的作用，即将那些读写事件源分发给各读写事件的处理者，就像送快递的在楼下喊: 谁的什么东西送了, 快来拿吧。开发人员在开始的时候需要在分享器那里注册感兴趣的事件，并提供相应的处理者(event handlers)，或者是回调函数; 事件分享器在适当的时候会将请求的事件分发给这些handler或者回调函数.


涉及到事件分享器的两种模式称为：Reactor和Proactor. Reactor模式是基于同步I/O的，而Proactor模式是和异步I/O相关的. 在Reactor模式中，事件分离者等待某个事件或者可应用或个操作的状态发生（比如文件描述符可读写，或者是socket可读写）,事件分离者就把这个事件传给事先注册的事件处理函数或者回调函数，由后者来做实际的读写操作。


而在Proactor模式中，事件处理者(或者代由事件分离者发起)直接发起一个异步读写操作(相当于请求)，而实际的工作是由操作系统来完成的。发起时，需要提供的参数包括用于存放读到数据的缓存区，读的数据大小，或者用于存放外发数据的缓存区，以及这个请求完后的回调函数等信息。事件分离者得知了这个请求，它默默等待这个请求的完成，然后转发完成事件给相应的事件处理者或者回调。举例来说，在Windows上事件处理者投递了一个异步IO操作(称有overlapped的技术)，事件分离者等IOCompletion事件完成. 这种异步模式的典型实现是基于操作系统底层异步API的，所以我们可称之为“系统级别”的或者“真正意义上”的异步，因为具体的读写是由操作系统代劳的。


Reactor与Proactor两种模式的场景区别：

下面是Reactor的做法：

1. 等待事件响应 (Reactor job)
2. 分发 "Ready-to-Read" 事件给用户句柄 ( Reactor job)
3. 读数据 (user handler job)
4. 处理数据( user handler job)

下面再来看看真正意义的异步模式Proactor是如何做的：

1. 等待事件响应  (Proactor job)
2. 读数据 (Proactor job)
3. 分发 "Read-Completed" 事件给用户句柄 (Proactor job)
4. 处理数据(user handler job)

从上面可以看出，Reactor和Proactor模式的主要区别就是真正的读取和写入操作是有谁来完成的，Reactor中需要应用程序自己读取或者写入数据，而Proactor模式中，应用程序不需要进行实际的读写过程，它只需要从缓存区读取或者写入即可，操作系统会读取缓存区或者写入缓存区到真正的IO设备.

最后结合下面的两张图更容易理解（这是[别人的图](http://blog.csdn.net/caiwenfeng_for_23/article/details/8458299)，非原创）：
![Reactor-map](http://img.my.csdn.net/uploads/201301/02/1357085735_7579.png)

![Proactor-map](http://img.my.csdn.net/uploads/201301/02/1357085756_3746.png)

可以看到两者图中都有分离器，在JAVA NIO框架中分离器的逻辑需要用户通过selector自己完成
在JAVA AIO框架中，分离器有系统API自动完成，AsynchronousChannelGroup就代替了分离的作用

#3.支持AIO和NIO的框架
前面已经讲了，MyCAT可以通过系统参数选择是使用AIO还是NIO，那么在代码里面是如何做到同时支持两种架构的呢。可以看下面的类图：
![MyCAT-io-class-map][]

- SocketConnector 发起连接请求类，如MyCAT与MySQL数据库的连接，都是由MyCAT主动发起连接请求
- SocketAcceptor 接收连接请求类，如MyCAT启动9066和8066分别侦听管理员和应用程序的连接请求
- SocketWR 读写操作类，SocketConnector和SocketAcceptor只负责socket建立，当socket连接建立后进行字节的读写操作则由SocketWR来完成。

这几个接口分别处理网络通道的四种不同类型的事件：
- Connect客户端连接服务端事件
- Accept 服务端接收客户端连接事件
- Read   读事件
- Write  写事件
这四种事件在AIO和NIO的实现差别如下：

| 操作  | NIO          | AIO         |
|------|---------------|-------------|
| Connect | 注册OP_CONNECT事件，通过seletor线程循环检查事件是否就绪| 通过AIO的connect函数进行连接调用并注册CompletionHandler句柄，事件发生后回调         |
| Accept | 注册OP_ACCEPT事件，通过seletor线程循环检查事件是否就绪| 通过AIO的accept函数进行连接准备调用并注册CompletionHandler句柄，事件发生后回调         |
| read | 注册OP_READ事件，通过seletor线程循环检查事件是否就绪| 通过AIO的read函数传递缓存读内容的buffer，并注册CompletionHandler句柄，事件发生后回调，回调时读入的内容已经写入buffer         |
| write | 1.若通道空闲当前线程直接写，否则缓存队列，注册OP_Write事件；2.通过seletor线程循环检查写事件是否就绪| 通过AIO的write函数传递要写的buffer，并注册CompletionHandler句柄，事件发生后回调，回调时buffer内容已经写入到通道了        |

上面的类图看起来有些复杂，因为把NIO和AIO放在一起了，那么我们分开来讲

**NIO主要类调用** 
![NIO-read-write][]

**AIO主要类调用-服务端**
![AIO-read-write-server][]
**AIO主要类调用-客户端**
![AIO-read-write-client][]

看起来好像是AIO的调用比NIO多吧，其实NIO比AIO要略麻烦些，因为AIO的调用关系全画了，NIO对链接建立过程进行简化，否则一个图上画不开了：）

#4.MyCAT的NIO实现

[Selector](http://http://ifeve.com/selectors/)（选择器）是Java NIO中能够检测一到多个NIO通道，并能够知晓通道是否为诸如读写事件做好准备的组件。这样，一个单独的线程可以管理多个channel，从而管理多个网络连接。
Selector可以监听四种不同类型的事件：
- Connect
- Accept
- Read
- Write

这四种事件用SelectionKey的四个常量来表示：
- SelectionKey.OP_CONNECT
- SelectionKey.OP_ACCEPT
- SelectionKey.OP_READ
- SelectionKey.OP_WRITE

前面已经说了，NIO采用的Reactor模式：例如汽车是乘客访问的主体（Reactor），乘客上车后，到售票员（acceptor）处登记，之后乘客便可以休息睡觉去了，当到达乘客所要到达的目的地后，售票员将其唤醒即可。
典型的Reactor场景
![Reactor][]

在高性能IO框架中，大都是采用多Reactor模式,即多个dispatcher，如下图所示：
![Reactor-multi][]

上图是服务端采用多Reactor模式的典型场景，MyCAT也采用多Reactor模式，另外MyCAT不仅做服务端，也要作为客户端去连接后端MySQL Server，所以实际场景如下图所示，
![Reactor-multi-proxy][]

多Reactor区分说明：
通常Reactor实现为一个线程,内部维护一个Selector
```java
   while(true){
    int sel=selector.select(timeout);
    processRegister();
    if(sel>0)
      processSelected(); 
  }
```

##4.1.NIOConnector类分析

NIOConnector处理的是Connect事件，是客户端连接服务端事件，就是MyCAT作为客户端去主动连接MySQL Server的操作。
###NIOConnector类声明和关键成员变量
```java
public final class NIOConnector extends Thread implements SocketConnector {

  private final Selector selector;
  private final BlockingQueue<AbstractConnection> connectQueue;
  private final NIOReactorPool reactorPool;
}

```
可以看到NIOConnector是一个线程，三个主要的成员变量
- selector 事件选择器
- connectQueue 需要建立连接的对象，临时放在这个队列里
- reactorPool  当连接建立后，从reactorPool中分配一个NIOReactor，处理Read和Write事件

###postConnect函数

```java
  public void postConnect(AbstractConnection c) {
    connectQueue.offer(c);
    selector.wakeup();
  }
```
postConnect函数的作用，是把需要建立的连接放到connectQueue队列中，然后再唤醒selector。
postConnect是在新建连接或者心跳时被XXXXConnectionFactory触发的。
![postConnect][]


###connect函数

```java  
private void connect(Selector selector) {
    AbstractConnection c = null;
    while ((c = connectQueue.poll()) != null) {
      try {
        SocketChannel channel = (SocketChannel) c.getChannel();
        channel.register(selector, SelectionKey.OP_CONNECT, c);
        channel.connect(new InetSocketAddress(c.host, c.port));
      } catch (Throwable e) {
        c.close(e.toString());
      }
    }
  }}
```
connect函数的目的就是处理postConnect函数操作的connectQueue队列：
1. 判断connectQueue中是否新的连接请求
2. 建立一个SocketChannel
3. 在selector中进行注册OP_CONNECT
4. 发起SocketChannel.connect()操作


###run函数
```java
  public void run() {
    for (;;) {
                 .....
        selector.select(1000L);
        connect(selector);
        Set<SelectionKey> keys = selector.selectedKeys();
        try {
          for (SelectionKey key : keys) {
            Object att = key.attachment();
            if (att != null && key.isValid() && key.isConnectable()) {
              finishConnect(key, att);
            } else {
              key.cancel();
            }
          }
        } finally {
          keys.clear();
        }
                 .....
    }
  }
```
NIOConnector继承Thread实现run()函数，这是一个无限循环体，包含了两个主要循环操作
- 调用connect函数中，判断connectQueue中是否新的连接请求，如有则在selector中进行注册，然后发起连接
- selector监听事件，然后在finishConnect函数中对事件进行处理。在NIOConnector类中，只注册了OP_CONNECT事件，所以只对OP_CONNECT事件进行处理。

###finishConnect函数

在NIOConnector类中，只处理OP_CONNECT事件，当连接建立完毕后，Read和Write事件如何处理呢？可以在finishConnect函数看到，当连接建立完毕后，从reactorPool中获得一个NIOReactor，然后把连接传递到NIOReactor，然后后续的Read和Write事件就交给NIOReactor处理了。
```java
  private void finishConnect(SelectionKey key, Object att) {
    BackendAIOConnection c = (BackendAIOConnection) att;
                 .....
        NIOReactor reactor = reactorPool.getNextReactor();
        reactor.postRegister(c);
                 .....
  }
```

##4.2.NIOAcceptor类分析

NIOAcceptor处理的是Accept事件，是服务端接收客户端连接事件，就是MyCAT作为服务端去处理前端业务程序发过来的连接请求。

###NIOAcceptor类声明和关键成员变量
```java
public final class NIOAcceptor extends Thread  implements SocketAcceptor{

  private final Selector selector;
  private final ServerSocketChannel serverChannel;
  private final NIOReactorPool reactorPool;
}
```
可以看到NIOAcceptor的主体结构，与NIOConnector比较像，也是一个线程，也有三个主要的成员变量（其它非主要变量就不在这儿一一列出了）
- selector 事件选择器
- serverChannel 监听新进来的TCP连接的通道
- reactorPool  当连接建立后，从reactorPool中分配一个NIOReactor，处理Read和Write事件

###NIOAcceptor的构造函数

监听通道在NIOAcceptor构造函数里启动,然后注册到实际进行任务处理的Dispather线程的Selector中
```java
  public NIOAcceptor(String name, String bindIp,int port, 
      FrontendConnectionFactory factory, NIOReactorPool reactorPool)
      throws IOException {

    this.selector = Selector.open();
    this.serverChannel = ServerSocketChannel.open();
    this.serverChannel.configureBlocking(false);
    /** 设置TCP属性 */
    serverChannel.setOption(StandardSocketOptions.SO_REUSEADDR, true);
    serverChannel.setOption(StandardSocketOptions.SO_RCVBUF, 1024 * 16 * 2);
    // backlog=100
    serverChannel.bind(new InetSocketAddress(bindIp, port), 100);
    this.serverChannel.register(selector, SelectionKey.OP_ACCEPT);
  }
```
###run函数
```java
  public void run() {
    for (;;) {
      try {
        selector.select(1000L);
        Set<SelectionKey> keys = selector.selectedKeys();
        try {
          for (SelectionKey key : keys) {
            if (key.isValid() && key.isAcceptable()) {
              accept();
            } else {
              key.cancel();
            }
          }
        } finally {
          keys.clear();
        }
      } catch (Throwable e) {
        LOGGER.warn(getName(), e);
      }
    }
  }
```
NIOAcceptor继承Thread实现run()函数，与NIOConnector的run()类似,也是一个无限循环体：
selector不断监听连接事件，然后在accept()函数中对事件进行处理。
在NIOAcceptor类中，只注册了OP_ACCEPT事件，所以只对OP_ACCEPT事件进行处理。

###accept函数
```java
  private void accept() {
      channel = serverChannel.accept();
      channel.configureBlocking(false);
      FrontendConnection c = factory.make(channel);

                 .....      
      NIOReactor reactor = reactorPool.getNextReactor();
      reactor.postRegister(c);
                 .....
  }
```
NIOAcceptor的accept（）与NIOConnector的finishConnect()类似，当连接建立完毕后，从reactorPool中获得一个NIOReactor，然后把连接传递到NIOReactor，然后后续的Read和Write事件就交给NIOReactor处理了。

##4.3.NIOSocketWR和NIOReactor分析
======

NIOConnector和NIOAcceptor分布完成连接的建立，真正的内容的读写是由NIOSocketWR和NIOReactor共同完成的。可以参见下图
![NIO-read-write][]

###先说一下NIOSocketWR和NIOReactor的关系

下面是NIOSocketWR的类声明和主要成员变量，可以看到NIOSocketWR针对的某一条链路

```java
public class NIOSocketWR extends SocketWR {
  private SelectionKey processKey;
  private final AbstractConnection con;
  private final SocketChannel channel;
}
```

在来看一下NIOReactor的内部类RW的类声明和主要成员变量，可以看到NIOReactor包含一个selector，是一个dispatcher，用来负责多个链路事件的事件分发。

```java
private final class RW implements Runnable {
  private final Selector selector;
  private final ConcurrentLinkedQueue<AbstractConnection> registerQueue;
}

```
###NIOReactor.postRegister()

 NIOConnector和NIOAcceptor建立连接后，调用NIOReactor.postRegister进行注册
```java
  final void postRegister(AbstractConnection c) {
    reactorR.registerQueue.offer(c);
    reactorR.selector.wakeup();
  }
```
NIOReactor.postRegister并没有直接注册，而是把AbstractConnection对象加入缓冲队列,然后wakeup selector等待注册。
`直接注册不可吗? 不是不可以`,是效率问题，至少加两次锁,锁竞争激烈
- Channel本身的regLock,竞争几乎没有 
- Selector内部的key集合,竞争激烈
更好的方式就是采用上面这种方式，先放入缓冲队列，等待selector单线程进行注册。

###NIOReactor.RW.run()

```java
public void run() {
  Set<SelectionKey> keys = null;
  for (;;) {
    try {
      selector.select(500L);
      register(selector);
      keys = selector.selectedKeys();
      for (SelectionKey key : keys) {
        AbstractConnection con = null;
        try {
          Object att = key.attachment();
          if (att != null && key.isValid()) {
            con = (AbstractConnection) att;
            if (key.isReadable()) {
              con.asynRead();
            }
            if (key.isWritable()) {
              con.doNextWriteCheck();
            }
          } else {
            key.cancel();
          }
        } catch (Throwable e) {

        }
      }
    } catch (Throwable e) {
      LOGGER.warn(name, e);
    } finally {
      if (keys != null) {
        keys.clear();
      }    
    }
  }
}
```

NIOReactor在内部类RW中继承Thread实现run()函数，这是一个无限循环体，包含了三个主要循环操作
- 注册事件，这儿只是注册OP_READ事件。OP_WRITE事件的注册放在NIOSocketWR.doNextWriteCheck()函数中，doNextWriteCheck既被selector线程调用，`也会被其它的业务线程调用，此时就会存在lock竞争的问题，所以对于OP_WRITE事件也建议用队列缓存的方式`，不过对于MyCAT的流量场景，大部分写操作是由业务线程直接写入，只有在网络繁忙时，业务线程不能一次全部写完，才会通过OP_WRITE注册方式进行候补写。所以此处可以考虑优化，但是性能上到底有多大提升，是否值得，优化前倒需要斟酌下。
- selector监听事件，如果是读事件，就调用con.asynRead()函数，进行字节的读取。对于asynRead中如何提取MySQL协议包，就属于网络框架讨论的内容，可以参考其它章节。
- selector监听到写事件，调用AbstractConnection.doNextWriteCheck()进行写事件的处理，在AbstractConnection.doNextWriteCheck()中，又调用NIOSocketWR.doNextWriteCheck()进行处理的。

###NIOSocketWR.doNextWriteCheck()

NIOSocketWR.doNextWriteCheck()的调用关系如下

![doNextWriteCheck][]
调用者有两个
1. selector循环写事件侦听
2. 其它业务线程触发的写操作

```java
  public void doNextWriteCheck() {
    if (!writing.compareAndSet(false, true)) {
      return;
    }
    try {
      boolean noMoreData = write0();
      writing.set(false);
      if (noMoreData && con.writeQueue.isEmpty()) {
        if ((processKey.isValid() && (processKey.interestOps() & SelectionKey.OP_WRITE) != 0)) {
          disableWrite();
        }
      } else {
        if ((processKey.isValid() && (processKey.interestOps() & SelectionKey.OP_WRITE) == 0)) {
          enableWrite(false);
        }
      }
    } catch (IOException e) {
      .....
    }
  }
```
1. 先判断是否正在写，如果正在写，退出（之前已经把写内容放到缓冲队列，那么此处是否可以优化呢，即`当发送缓冲队列为空的时候,可以直接往channel写数据，不能写再放缓冲队列`，理论上可以优化，但是写代码时要注意，因为必需要保证协议包的顺序，还要考虑到前一次写时，是否有buffer没有写完，若前一次写入时，最后一个buffer没有写完，记得退回缓冲队列；MyCAT当前的实现方式是增加了一个变量专门存放上次未写完的buffer）
2. write0()方法是只要buffer中还有，就不停写入；直到写完所有buffer，或者写入时，返回写入字节为零，表示网络繁忙，就回临时退出写操作。
3. 没有完全写入并且缓冲队列为空,取消注册写事件
4. 没有完全写入或者缓冲队列有代写对象,继续注册写时间
5. 特别说明，`writing.set(false)`必须要在`boolean noMoreData = write0()`之前和`if (noMoreData && con.writeQueue.isEmpty())`之后，否则会导致当网络流量较低时，消息包缓存在内存中迟迟发不出去的现象。

#5.与Cobar原有NIO细节比较

##5.1.Cobar的NIO
Cobar后端是采用BIO，前端采用NIO；Cobar的BIO这儿就不必提了，对于原有NIO实现，跟MyCAT相比，读方式差不多，写的差别比较大。

**NIOReactor.postWrite()**

这儿传入的参数，不是要写的buffer，而是一个连接对象，只是注册这个对象有内容需要写。要写的buffer，在连接对象自己的缓存队列中
这种方式与MyCAT差不多，连接对象自己维护写队列。

```java

  final void postWrite(NIOConnection c) {
    reactorW.writeQueue.offer(c);
  }

```
**NIOReactor.W内部类**

专门负责缓冲队列写，不停循环遍历，等待其它业务线程放入写数据
```java
  private final class W implements Runnable {
    private final BlockingQueue<NIOConnection> writeQueue;
    private W() {
      this.writeQueue = new LinkedBlockingQueue<NIOConnection>();
    }
    public void run() {
      NIOConnection c = null;
      for (;;) {
        try {
          if ((c = writeQueue.take()) != null) {
             c.writeByQueue();
          }
        } catch (Throwable e) {}
      }
    }
  }

```

**NIOReactor.R内部类,为一个seletor**
同时处理读事件和写事件。但是主要负责的是读，只有在网络非常繁忙等极少数情况下，小概率走到读分支

```java
  private final class R implements Runnable {
    private final Selector selector;
    @Override
    public void run() {
      final Selector selector = this.selector;
      for (;;) {
        try {
          selector.select(1000L);
          register(selector);
          Set<SelectionKey> keys = selector.selectedKeys();
            for (SelectionKey key : keys) {
              Object att = key.attachment();
              if (att != null && key.isValid()) {
                int readyOps = key.readyOps();
                if ((readyOps & SelectionKey.OP_READ) != 0) {
                  read((NIOConnection) att);
                } else if ((readyOps & SelectionKey.OP_WRITE) != 0) {
                   c.writeByEvent();
                } else {
                  key.cancel();
                }
              } else {
                key.cancel();
              }
            }
        } catch (Throwable e) {
        }
      }
    }
  }
```

**基于队列的写和基于事件的写**

- 队列写：所有的写请求，放到缓存队列，由独立W线程进行写。如果未写完（比如网络繁忙），则注册写事件，然后会再seleltor发现写事件
- 事件写：R线程中，seletor探测到写事件后，进行写操作。如果写完了，则立即取消注册写事件，避免继续触发导致循环 
- 总结：主要是W线程进行写，只有在网络繁忙时，才会注册写事件，等待网络写就绪后，R线程就会立即发现写事件，然后R线程再写一部分。


```java
  @Override
  public void writeByQueue() throws IOException {
    if (isClosed.get()) {
      return;
    }
    final ReentrantLock lock = this.writeLock;
    lock.lock();
    try {
      // 满足以下两个条件时，切换到基于事件的写操作。
      // 1.当前key对写事件不该兴趣。
      // 2.write0()返回false。
      if ((processKey.interestOps() & SelectionKey.OP_WRITE) == 0
          && !write0()) {
        enableWrite();
      }
    } finally {
      lock.unlock();
    }
  }

  @Override
  public void writeByEvent() throws IOException {
    if (isClosed.get()) {
      return;
    }
    final ReentrantLock lock = this.writeLock;
    lock.lock();
    try {
      // 满足以下两个条件时，切换到基于队列的写操作。
      // 1.write0()返回true。
      // 2.发送队列的buffer为空。
      if (write0() && writeQueue.size() == 0) {
        disableWrite();
      }
    } finally {
      lock.unlock();
    }
  }
    /**
   * 打开写事件
   */
  private void enableWrite() {
    final Lock lock = this.keyLock;
    lock.lock();
    try {
      SelectionKey key = this.processKey;
      key.interestOps(key.interestOps() | SelectionKey.OP_WRITE);
    } finally {
      lock.unlock();
    }
    processKey.selector().wakeup();
  }

  /**
   * 关闭写事件
   */
  private void disableWrite() {
    final Lock lock = this.keyLock;
    lock.lock();
    try {
      SelectionKey key = this.processKey;
      key.interestOps(key.interestOps() & OP_NOT_WRITE);
    } finally {
      lock.unlock();
    }
  }

```

##5.2.比较MyCAT和Cobar两种写方式

- Cobar的写：业务线程把写请求放到缓冲队列，然后由独立写线程W负责，当W在写的时候，网络慢等原因导致未写完，
 然后注册写事件，由R线程(selector)进行候补写
- MyCAT的写：业务线程先通过加锁或者AtomicBoolean判断当前channel是否正在写数据，如空闲则由当前线程直接写，否则入缓冲队列交给其他线程写；在写的时候，网络慢等原因导致未写完，
 然后注册写事件，由NIOReactor线程(selector)进行候补写；
- MyCAT采用这种方式的显著优点：尽可能减少系统调用和线程切换；

#6.MyCAT的AIO实现
##6.1.JAVA AIO体系
从代码风格上比较，NIO和AIO的差别，就是Reactor和Proactor两种模式差别，对于典型的读场景，来回顾下他们的区分：
Reactor的做法：
1. 等待事件响应 (Reactor job)
2. 分发 "Ready-to-Read" 事件给用户句柄 ( Reactor job)
3. 读数据 (user handler job)
4. 处理数据( user handler job)

Proactor的做法：
1. 等待事件响应  (Proactor job)
2. 读数据 (Proactor job)
3. 分发 "Read-Completed" 事件给用户句柄 (Proactor job)
4. 处理数据(user handler job)

可以看到两者最大的区别，就是到了AIO，用户只管专心负责对读到的数据进行处理，如何读的过程过程就全交给系统层面去完成。
同样对于写操作，在AIO方式中，应用层只管把要写的buffer传递出去，等到系统写完，再回调应用层做其它动作。
而在NIO方式中，应用层要自己控制buffer写入channel的过程。

首先看下AIO引入的新的类和接口：

```java
 java.nio.channels.AsynchronousChannel
```
- 标记一个channel支持异步IO操作。

```java
 java.nio.channels.AsynchronousServerSocketChannel
```
- ServerSocket的aio版本，创建TCP服务端，绑定地址，监听端口等。

```java
 java.nio.channels.AsynchronousSocketChannel
```
- 面向流的异步socket channel，表示一个连接。 
```java
  java.nio.channels.AsynchronousChannelGroup
```
- 异步channel的分组管理，目的是为了资源共享。一个AsynchronousChannelGroup绑定一个线程池，这个线程池执行两个任务：处理IO事件和派发CompletionHandler。AsynchronousServerSocketChannel创建的时候可以传入一个 AsynchronousChannelGroup，那么通过AsynchronousServerSocketChannel创建的 AsynchronousSocketChannel将同属于一个组，共享资源。
```java
 java.nio.channels.CompletionHandler
```
- 异步IO操作结果的回调接口，用于定义在IO操作完成后所作的回调工作。
AIO的API允许两种方式来处理异步操作的结果：返回的Future模式或者注册CompletionHandler，
MyCAT采用的是CompletionHandler的方式，这些handler的调用是由 AsynchronousChannelGroup的线程池派发的。

AsynchronousChannelGroup实际上扮演Proactor的角色，业务逻辑通过CompletionHandler接口实现。在整个JAVA AIO体系中，主要由四个地方需要注册CompletionHandler，分别对应Accept、Connect、Read、Write四个不同的事件。

AsynchronousServerSocketChannel类的accept
```java
 public abstract <A> void accept(A attachment,
                                    CompletionHandler<AsynchronousSocketChannel,? super A> handler)
```

AsynchronousSocketChannel类的

```java
    public abstract <A> void connect(SocketAddress remote,
                                     A attachment,
                                     CompletionHandler<Void,? super A> handler)
    public final <A> void read(ByteBuffer dst,
                               A attachment,
                               CompletionHandler<Integer,? super A> handler)
    public final <A> void write(ByteBuffer dst,
                               A attachment,
                               CompletionHandler<Integer,? super A> handler)
```

  
  在Mycat工程中，有四个类实现CompletionHandler接口，分别满足上面四个事件的注册。
##6.2.AIOAcceptor
NIOAcceptor负责作为服务端接受客户端的请求，通过AsynchronousServerSocketChannel.accept() 进行写accept事件的注册。
###类声明
虽然CompletionHandler定义为CompletionHandler<V,A> ，根据AsynchronousServerSocketChannel.accept()的参数定义，对AIOAcceptor而言，V已经固定为AsynchronousSocketChannel，A可以自定义.
```java
public final class AIOAcceptor implements SocketAcceptor,
    CompletionHandler<AsynchronousSocketChannel, Long> {
  private final AsynchronousServerSocketChannel serverChannel;
  private final FrontendConnectionFactory factory;
  public AIOAcceptor(String name, String ip, int port,
      FrontendConnectionFactory factory, AsynchronousChannelGroup group)
      throws IOException {
    ...
    this.factory = factory;
    serverChannel = AsynchronousServerSocketChannel.open(group);
    // backlog=100
    serverChannel.bind(new InetSocketAddress(ip, port), 100);
  }
}
```

跟NIOAcceptor一样，AIO也要启动一个监听通道serverChannel，绑定一个侦听端口。

###启动方法start

```java
  public void start() {
    this.pendingAccept();
  }；
   private void pendingAccept() {
    if (serverChannel.isOpen()) {
      serverChannel.accept(ID_GENERATOR.getId(), this);
    }
}
```

AIO的启动方法方法非常简单，就是调用AsynchronousServerSocketChannel的accept方法，把用户定义的CompletionHandler即AIOAcceptor传递就可以了。由AsynchronousChannelGroup担任proactor角色，当连接建立时，回调AIOAcceptor的completed或者failed方法

###completed方法

```java
  @Override
  public void completed(AsynchronousSocketChannel result, Long id) {
    accept(result, id);
    // next pending waiting
    pendingAccept();
  }
  private void accept(NetworkChannel channel, Long id) {
    try {
      ....
      FrontendConnection. c = factory.make(channel);
      NIOProcessor processor = MycatServer.getInstance().nextProcessor();
      c.setProcessor(processor);
      c.register();
    } catch (Throwable e) {
      closeChannel(channel);
    }
  }
```

completed方法的内容跟NIOAccepter的accept()函数的作用差不多，就对建立连接后的socket做下一步操作，而AIO比NIO还要略微简单些（NIO还要做一次sub reactor的再分配。），AIO只要调用FrontendConnection.register()向就可以了。
另外,AsynchronousServerSocketChannel的accept方法注册的completionHandler只能被一次连接接入事件调用，并且不能同时注册多个pending的completionHandler，否则会抛出AcceptPendingException。所以当completionHandler被回调时，为了服务器能继续接入新的连接，要继续调用AsynchronousServerSocketChannel的accept方法注册一个新的completionHandler，用于下一个新连接的接入准备，所以completed方法还要继续调用pendingAccept()方法


##6.3.AIOConnector

###类声明
AIOConnector实现CompletionHandler<V,A>,用作在connect事件的用户句柄。根据AsynchronousSocketChannel.connect()的参数定义，对AIOAcceptor而言，V已经固定为Void，A可以自定义.
```java
public final class AIOConnector implements SocketConnector,
    CompletionHandler<Void, AbstractConnection>{}
```


###被谁调用
在启动时初始化数据源、HeartBeat和前端执行Query需要新建连接时，通过BackendConnnectionFactory的make方法中，调用connnect进行handler设置：
```java
      ((AsynchronousSocketChannel) channel).connect(
          new InetSocketAddress(dsc.getIp(), dsc.getPort()),
          detector, (CompletionHandler) MycatServer.getInstance()
              .getConnector());
```

###completed方法

```java
  @Override
  public void completed(Void result, AbstractConnection attachment) {
    finishConnect(attachment);
  }

  private void finishConnect(AbstractConnection c) {
    try {
      if (c.finishConnect()) {
        NIOProcessor processor = MycatServer.getInstance()
            .nextProcessor();
        c.setProcessor(processor);
        c.register();
      }
    } catch (Throwable e) {}
  }
```

与AIOAcceptor的completed方法比较像，对建立连接后的socket做下一步操作，只要调用AbstractConnection.register()向就可以了。

##6.4.AIOSocketWR和AIOReadHandler
AIOSocketWR实现了SocketWR接口的asynRead方法，该方法的调用关系如下图
![asynRead][]
1、前端链路接入后，先发发送握手数据包，然后调用asynRead()等待读应答握手应答
2、后端链路接入后，调用asynRead()等待握手数据包的到来
3、AIOReadHandler被回调时，继续下一次读

###AIOSocketWR的asynRead方法
这个方法很简单，就是调用channel的read方法，把AIOReadHandler句柄传递过去
```java
  @Override
  public void asynRead() {
    ByteBuffer theBuffer = con.readBuffer;
    if (theBuffer == null) {
      theBuffer = con.processor.getBufferPool().allocate();
      con.readBuffer = theBuffer;
      channel.read(theBuffer, this, aioReadHandler);
    } else if (theBuffer.hasRemaining()) {
      channel.read(theBuffer, this, aioReadHandler);
    } else {
      throw new java.lang.IllegalArgumentException("full buffer to read ");
    }
  }
```

###AIOReadHandler
AIOReadHandler实现CompletionHandler<V,A>,用作在read事件的用户句柄回调。根据AsynchronousSocketChannel.read()的参数定义，对AIOReadHandler而言，V已经固定为Integer类型表示读的字节数，A可以自定义.

```java
class AIOReadHandler implements CompletionHandler<Integer, AIOSocketWR> {
  @Override
  public void completed(final Integer i, final AIOSocketWR wr) {
    if (i > 0) {
      try {
        wr.con.onReadData(i);
        wr.con.asynRead();
      } catch (IOException e) {
        wr.con.close("handle err:" + e);
      }
    } else if (i == -1) {
      wr.con.close("client closed");
    }
  }
}
```
AIOReadHandler的completed方法主要做两件事
1、读buffer中的内容
2、继续注册下一次读的回调句柄

##6.5.AIOSocketWR和AIOWriteHandler
AIOSocketWR实现了SocketWR接口的doNextWriteCheck方法，doNextWriteCheck又调用asynWrite，该方法的调用有两类：
![asynWrite][]

1.业务线程发起写请求操作，当显式调用AbstactConnection时，若空闲直接，否则放入写队列等待
```java
  public void doNextWriteCheck() {
    if (!writing.compareAndSet(false, true)) {
      return;
    }
    boolean noMoreData = this.write0();
    if (noMoreData) {
      if (!con.writeQueue.isEmpty()) {
        this.write0();
      }
    }
  }
  private boolean write0() {
    ByteBuffer theBuffer = con.writeBuffer;
    if (theBuffer == null || !theBuffer.hasRemaining()) {// writeFinished,但要区分bufer是否NULL，不NULL，要回收
      if (theBuffer != null) {
        con.recycle(theBuffer);
        con.writeBuffer = null;
      }
      ByteBuffer buffer = con.writeQueue.poll();
      if (buffer != null) {
        if (buffer.limit() == 0) {
          con.recycle(buffer);
          con.writeBuffer = null;
          con.close("quit cmd");
          return true;
        } else {
          con.writeBuffer = buffer;
          asynWrite(buffer);
          return false;
        }
      } else {
        writing.set(false);
        return true;
      }
    } else {
      theBuffer.compact();
      asynWrite(theBuffer);
      return false;
    }
  }
  private void asynWrite(ByteBuffer buffer) {
    buffer.flip();
    this.channel.write(buffer, this, aioWriteHandler);
  }
```
2.CompletionHandler回调句柄中，对返回的Integer仅作计数和判断用，不像read那样，读出n bytes进行handle出来。异步写的逻辑是，不断循环，发现buffer没有写完，则compact后继续写；如果buffer已经写完，则recycle；然后从writeQueue中取出其他的buffer继续，如果队列中也没有buffer，则不再循环。
```java
  protected void onWriteFinished(int result) {
    con.netOutBytes += result;
    con.processor.addNetOutBytes(result);
    con.lastWriteTime = TimeUtil.currentTimeMillis();
    boolean noMoreData = this.write0();
    if (noMoreData) {
      this.doNextWriteCheck();
    }
  }
```


[MyCAT-io-class-map]:http://img.blog.csdn.net/20150423105956655 "MyCAT 类图"
[Reactor]:http://img.blog.csdn.net/20150422131451747  "Reactor模式"
[Reactor-multi]:http://img.blog.csdn.net/20150423105035039 "多Reactor模式"
[Reactor-multi-proxy]:http://img.blog.csdn.net/20150423105103961  "既做服务端又做客户端的多Reactor模式"
[postConnect]:http://img.blog.csdn.net/20150423105634416 " postConnect函数调用关系"
[NIO-read-write]:http://img.blog.csdn.net/20150423105130980 "NIO 读写调用"
[doNextWriteCheck]:http://img.blog.csdn.net/20150423105604901 "NIOSocketWR.doNextWriteCheck()的调用关系"
[asynRead]:http://img.blog.csdn.net/20150423105455216 "asynRead方法的调用关系"
[asynWrite]:http://img.blog.csdn.net/20150423105540665 "asynWrite方法的调用关系"
[AIO-read-write-server]: http://img.blog.csdn.net/20150423105315928 "AIO读写调用关系-服务端"
[AIO-read-write-client]: http://img.blog.csdn.net/20150423105232897 "AIO读写调用关系-客户端"
