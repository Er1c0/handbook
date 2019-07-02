
[TOC]
# MyCAT线程模型
![MyCAT线程模型](http://img.blog.csdn.net/20150423225645338)
## 线程介绍
### Timer
Timer单线程仅仅负责调度，任务的具体动作交给timerExecutor。
### TimerExecutor线程池，
默认大小N=2
任务通过timer单线程和timerExecutor线程池共同完成。这个1+N的设计方式是沿用Cobar的设计，比较巧妙的，真心赞！
### NIOConnect主动连接事件分离器
一个线程，负责作为客户端连接MySQL的主动连接事件。
### Server被动连接事件分离器
一个线程，负责作为服务端接收来自业务系统的连接事件。
### Manager被动连接事件分离器
一个线程，负责作为服务端接收来自管理系统的连接事件。
### NIOReactor读写事件分离器
默认个数N=processor size，通道建立连接后处理NIO读写事件。
由于写是采用通道空闲时其它线程直接写，只有写繁忙时才会注册写事件，再由NIOReactor分发，所以NIOReactor主要处理读操作。
### BusinessExecutor线程池
默认大小N=processor size，任务队列采用的是LinkedTransferQueue，所有的NIOReactor把读出的数据交给BusinessExecutor做下一步的业务操作。
全局只有一个BusinessExecutor线程池，所有链接通道随机分成多个组，然后每组的多个通道共享一个Reactor，所有的Reactor读取且解码后的数据下一步处理操作，又共享一个BusinessExecutor线程池。
## 一个SQL请求的线程切换
![一个SQL请求的线程切换mycat](http://img.blog.csdn.net/20150427221938647)

## MyCAT的线程快照
```
jstack 34179|grep prio
"Attach Listener" #32 daemon prio=9 os_prio=31 tid=0x00007f8f8ba15800 nid=0x2f07 waiting on condition [0x0000000000000000]
"Timer1" #31 daemon prio=5 os_prio=31 tid=0x00007f8f8c0d1000 nid=0x7703 waiting on condition [0x0000000126510000]
"Timer0" #30 daemon prio=5 os_prio=31 tid=0x00007f8f8c0d0000 nid=0x7607 waiting on condition [0x000000012640d000]
"DestroyJavaVM" #29 prio=5 os_prio=31 tid=0x00007f8f8b01c000 nid=0x1303 waiting on condition [0x0000000000000000]
"BusinessExecutor7" #28 daemon prio=5 os_prio=31 tid=0x00007f8f8b1e5800 nid=0x6f03 waiting on condition [0x000000012630a000]
"BusinessExecutor6" #27 daemon prio=5 os_prio=31 tid=0x00007f8f8a3ab800 nid=0x6d03 waiting on condition [0x0000000126207000]
"BusinessExecutor5" #26 daemon prio=5 os_prio=31 tid=0x00007f8f8a3b3000 nid=0x6b03 waiting on condition [0x0000000126104000]
"BusinessExecutor4" #25 daemon prio=5 os_prio=31 tid=0x00007f8f89c04800 nid=0x6903 waiting on condition [0x0000000126001000]
"BusinessExecutor3" #24 daemon prio=5 os_prio=31 tid=0x00007f8f89937800 nid=0x6703 waiting on condition [0x0000000125efe000]
"BusinessExecutor2" #23 daemon prio=5 os_prio=31 tid=0x00007f8f8a443800 nid=0x6503 waiting on condition [0x0000000125dfb000]
"BusinessExecutor1" #22 daemon prio=5 os_prio=31 tid=0x00007f8f8a43c000 nid=0x6303 waiting on condition [0x0000000125cf8000]
"BusinessExecutor0" #21 daemon prio=5 os_prio=31 tid=0x00007f8f8a3ae000 nid=0x6103 waiting on condition [0x0000000125bf5000]
"$_MyCatServer" #20 prio=5 os_prio=31 tid=0x00007f8f8c098000 nid=0x5f03 runnable [0x0000000125af2000]
"$_MyCatManager" #19 prio=5 os_prio=31 tid=0x00007f8f8a8ce800 nid=0x5d03 runnable [0x00000001259ef000]
"$_NIOConnector" #18 prio=5 os_prio=31 tid=0x00007f8f89956800 nid=0x5b03 runnable [0x00000001256ec000]
"$_NIOREACTOR-3-RW" #17 prio=5 os_prio=31 tid=0x00007f8f898b9000 nid=0x5903 runnable [0x00000001255e9000]
"$_NIOREACTOR-2-RW" #16 prio=5 os_prio=31 tid=0x00007f8f8a914800 nid=0x5703 runnable [0x00000001254e6000]
"$_NIOREACTOR-1-RW" #15 prio=5 os_prio=31 tid=0x00007f8f8a8d9800 nid=0x5503 runnable [0x00000001253e3000]
"$_NIOREACTOR-0-RW" #14 prio=5 os_prio=31 tid=0x00007f8f8a8d9000 nid=0x5303 runnable [0x00000001252e0000]
"Log4jWatchdog" #13 daemon prio=5 os_prio=31 tid=0x00007f8f8a305000 nid=0x5107 waiting on condition [0x00000001251cd000]
"net.sf.ehcache.CacheManager@512ddf17" #11 daemon prio=5 os_prio=31 tid=0x00007f8f8a32d000 nid=0x4f03 in Object.wait() [0x00000001250ca000]
"MyCatTimer" #10 daemon prio=5 os_prio=31 tid=0x00007f8f8a162800 nid=0x4d03 in Object.wait() [0x0000000124fab000]
"Thread-0" #9 prio=5 os_prio=31 tid=0x00007f8f8b082000 nid=0x4b03 waiting on condition [0x0000000124cf1000]
"Service Thread" #8 daemon prio=9 os_prio=31 tid=0x00007f8f8a801000 nid=0x4703 runnable [0x0000000000000000]
"C1 CompilerThread2" #7 daemon prio=9 os_prio=31 tid=0x00007f8f8b025800 nid=0x4503 waiting on condition [0x0000000000000000]
"C2 CompilerThread1" #6 daemon prio=9 os_prio=31 tid=0x00007f8f8b025000 nid=0x4303 waiting on condition [0x0000000000000000]
"C2 CompilerThread0" #5 daemon prio=9 os_prio=31 tid=0x00007f8f8b023800 nid=0x4103 waiting on condition [0x0000000000000000]
"Signal Dispatcher" #4 daemon prio=9 os_prio=31 tid=0x00007f8f8b022000 nid=0x3017 runnable [0x0000000000000000]
"Finalizer" #3 daemon prio=8 os_prio=31 tid=0x00007f8f8a00e800 nid=0x2d03 in Object.wait() [0x0000000122b34000]
"Reference Handler" #2 daemon prio=10 os_prio=31 tid=0x00007f8f8a00d800 nid=0x2b03 in Object.wait() [0x0000000122a31000]
"VM Thread" os_prio=31 tid=0x00007f8f8b001000 nid=0x2903 runnable 
"GC task thread#0 (ParallelGC)" os_prio=31 tid=0x00007f8f8980d800 nid=0x2103 runnable 
"GC task thread#1 (ParallelGC)" os_prio=31 tid=0x00007f8f8980e000 nid=0x2303 runnable 
"GC task thread#2 (ParallelGC)" os_prio=31 tid=0x00007f8f8980f000 nid=0x2503 runnable 
"GC task thread#3 (ParallelGC)" os_prio=31 tid=0x00007f8f8980f800 nid=0x2703 runnable 
"VM Periodic Task Thread" os_prio=31 tid=0x00007f8f8a840800 nid=0x4903 waiting on condition 
```
# Cobar线程介绍
![Cobar线程模型](http://img.blog.csdn.net/20150427221459096)
## 线程介绍
### Timer
Timer单线程仅仅负责调度，任务的具体动作交给timerExecutor。
### TimerExecutor线程池，
默认大小N=2，任务通过timer单线程和timerExecutor线程池共同完成。这个1+N的设计方式是比较巧妙的，真心赞！
但是timerExecutor跟aioExecutor大小默认一样，不太合理，定时任务没有那么大的运算量。
### Server被动连接事件分离器
一个线程，负责作为服务端接收来自业务系统的连接事件
### Manager被动连接事件分离器
一个线程，负责作为服务端接收来自管理系统的连接事件
### R读写事件分离器
客户端与Server连接后，由R线程负责读写事件（写事件大部分有W线程负责，只有在网络繁忙时才会由小部分写事件是由R线程完成的）。
### Handler和Executor线程池
R线程接收到读事件后解码出一个完整的MySQL协议包，下一步由Handler线程池进行SQL解析、路由计算。然后执行任务从Handler线程池转移到Executor线程池，以阻塞方式发送给后端MySQL Server。Executor收到MySQL Server应答后，会由最后一个Executor线程进行聚合，然后交给W线程
### W线程
W线程不停遍历LinkedBlockingQueue检查是否有写任务，若有则写入Socket Channel。当Channel繁忙时，W线程会注册OP_WRITE事件，通过R线程进行候补写操作。
下面是一个SQL请求执行过程的线程切换，可以看到Cobar的线程上下文切换还是比较多的。
### ManageExecutor线程池
Cobar对来自Manager的请求和来自Server的请求做了分离，来自管理系统会专门由ManageExecutor线程池处理。
### InitExecutor线程池
用来进行后端链路初始化。
## Cobar为什么那么多个线程池？
可以发现Cobar有下面这么多个线程池
- TimerExecutor线程池(一个)
- InitExecutor线程池(一个)
- ManageExecutor线程池(一个)
- Handler线程池(N个)
- Executor线程池(N个)

注意上面的**个数单位是线程池，不是线程**！所以看起来有些眼花缭乱吧？
我不是Cobar的原作者，只能猜测最什么设计这么多线程池？那就是因为**后端采用了BIO**！

- 因为后端BIO，所以每一个请求到后端查询，都要阻塞一个线程，前端NIO(Reactor-R线程)必须要把执行任务交给Executor线程池。
- 由于存在聚合要求，前端NIO的一个SQL请求可能会对应多个后端请求，所以有时可能会阻塞多个Executor线程。为此增加了Handler做中间SQL解析、路由计算，路由计算完毕后再交给Executor执行。 
- 由于后端是阻塞方式，在时，会导致Executor无空闲线程，为了避免管理端口输入名命令无任何响应的现象，为此增加一个ManageExecutor线程池，专门处理ManageExecutor线程。
- 在后端BIO时，除了读写是阻塞方式外，链路建立过程也是阻塞方式，若同时链路建立请求多，也会阻塞大量线程。为避免业务、管理的相互干扰，为此增加了一个InitExecutor线程池专门做后端链路建立。
- 所以如果后端BIO改为NIO，并优化逻辑执行过程，避免业务执行线程sleep或长时间阻塞，尽量通过Reactor线程直接计算，就可以大大降低线程上下文切换的损耗，上述各眼花缭乱的线程池就可以合并为一个业务线程池。 
 
## 一个SQL请求的线程切换
![一个SQL请求的线程切换mycat](http://img.blog.csdn.net/20150427221803252)

### Cobar的线程快照
```
Cobar>jstack 10631|grep prio
"Processor0-E6" daemon prio=5 tid=7f931f057000 nid=0x11abcf000 waiting on condition [11abce000]
"Processor1-E6" daemon prio=5 tid=7f931f056000 nid=0x11aacc000 waiting on condition [11aacb000]
"TimerExecutor3" daemon prio=5 tid=7f931e206000 nid=0x119d22000 waiting on condition [119d21000]
"CobarServer" prio=5 tid=7f931d961000 nid=0x119c1f000 runnable [119c1e000]
"CobarManager" prio=5 tid=7f931f150800 nid=0x119b1c000 runnable [119b1b000]
"TimerExecutor2" daemon prio=5 tid=7f931d8c7800 nid=0x119a19000 waiting on condition [119a18000]
"TimerExecutor1" daemon prio=5 tid=7f931f14f800 nid=0x119916000 waiting on condition [119915000]
"InitExecutor1" daemon prio=5 tid=7f931f156800 nid=0x119813000 waiting on condition [119812000]
"InitExecutor0" daemon prio=5 tid=7f931f155800 nid=0x119710000 waiting on condition [11970f000]
"CobarConnector" prio=5 tid=7f931e203800 nid=0x11960d000 runnable [11960c000]
"TimerExecutor0" daemon prio=5 tid=7f931e201000 nid=0x11950a000 waiting on condition [119509000]
"Processor1-W" prio=5 tid=7f931d8c4800 nid=0x119407000 waiting on condition [119406000]
"Processor1-R" prio=5 tid=7f931d82c800 nid=0x119304000 runnable [119303000]
"Processor0-W" prio=5 tid=7f931d0ab800 nid=0x119201000 waiting on condition [119200000]
"Processor0-R" prio=5 tid=7f931d0aa800 nid=0x1190fe000 runnable [1190fd000]
"CobarTimer" daemon prio=5 tid=7f931e17f000 nid=0x118fde000 in Object.wait() [118fdd000]
"Low Memory Detector" daemon prio=5 tid=7f931e0ab800 nid=0x118b3b000 runnable [00000000]
"C2 CompilerThread1" daemon prio=9 tid=7f931e0aa800 nid=0x118a38000 waiting on condition [00000000]
"C2 CompilerThread0" daemon prio=9 tid=7f931e0aa000 nid=0x118935000 waiting on condition [00000000]
"Signal Dispatcher" daemon prio=9 tid=7f931e0a9000 nid=0x118832000 runnable [00000000]
"Surrogate Locker Thread (Concurrent GC)" daemon prio=5 tid=7f931e0a8800 nid=0x11872f000 waiting on condition [00000000]
"Finalizer" daemon prio=8 tid=7f931f037000 nid=0x116d52000 in Object.wait() [116d51000]
"Reference Handler" daemon prio=10 tid=7f931f036000 nid=0x116c4f000 in Object.wait() [116c4e000]
"VM Thread" prio=9 tid=7f931e094800 nid=0x116b4c000 runnable 
"Gang worker#0 (Parallel GC Threads)" prio=9 tid=7f931f001800 nid=0x113005000 runnable 
"Gang worker#1 (Parallel GC Threads)" prio=9 tid=7f931d001000 nid=0x113108000 runnable 
"Gang worker#2 (Parallel GC Threads)" prio=9 tid=7f931d001800 nid=0x11320b000 runnable 
"Gang worker#3 (Parallel GC Threads)" prio=9 tid=7f931d002000 nid=0x11330e000 runnable 
"Concurrent Mark-Sweep GC Thread" prio=9 tid=7f931f002000 nid=0x1167c7000 runnable 
"VM Periodic Task Thread" prio=10 tid=7f931d811800 nid=0x118c3e000 waiting on condition 
"Exception Catcher Thread" prio=10 tid=7f931f001000 nid=0x10ff01000 runnable 
```

# MyCAT与Cobar的比较
## MyCAT比Cobar减少了线程切换
Cobar的后端采用BIO通信，后端读与后端因为线程阻塞了，不存在线程切换，没有可比性，所以我们只比较NIO和业务逻辑部分。
Cobar的线程模型中存在着大量的上下文切换,MyCAT的线程调度尽量减少了线程间的切换，以写为例
Cobar是业务线程先把写请求交给专门的W线程，W线程再写过程中发现通道繁忙时再交给R线程；MyCAT对写的做法是业务线程发现通道空闲直接写，只有再通道繁忙时再交给Reactor线程。

## 减少线程切换与业务可能停顿的矛盾
MyCAT几乎已经达到了线程简化的最高境界，有一个看似可行的方法：可以配置多个NIOReactor，尽可能所有读、解码、业务处理都在Reactor线程中完成，而不必把任务交给BusinessExecutor线程池，从而减少线程的上下文切换，提高处理效率。
但是，不管配置几个Reactor，还是要求多个通道共享一个Reactor，（为什么？因为Reactor最多十几个、几十个，并发的链接通道可能上万个！）如果Reactor在读和解码请求后顺序处理业务逻辑，那么在处理业务逻辑过程中，Reactor就无法响应其它通道的事件了，这个时候如果正好有共享同一个Reactor的其它通道的请求过来，就会出现停顿的现象。

那么如何做呢，就需要具体问题具体分析，要对业务逻辑进行归类：
- 对于业务较重的，比如大结果集排序，则送到BusinessExecutor线程池进行下一步处理；
- 于业务较轻的，比如单库直接转发的情况，则由Reactor直接完成，不再送线程池，减少上下文切换。

### 特别说明ER分片机制
如果涉到ER分片，MyCAT目前的机制：计算路由时以阻塞同步方式调用FetchStoreNodeOfChildTableHandler，若由Reactor直接进行路由计算，会导致其它通道停顿现象。`把ER分片同步改异步是个看似可行的方法，但这个改造工作量较大，会造成原来完整路由计算逻辑的碎片化`。
即使ER分片同步改异步了，每次子表操作都要遍历父表对性能损耗较大，即使采用缓存也不能最终解决问题。**个人觉得，ER分片这个功能比较鸡肋，建议生产部署时绕开这个功能，直接通过关联字段分片或表设计时增加冗余字段.**

## 数据验证
1. 试sql从收到请求到下推的总时长，如果时间可容忍，则不必切换到线程池(**此处可忽略ER分片**)。
2. 对于manager端口的命令，若存在执行时间比较的，也需要改为线程池来执行。
3. 对于收到的应答，大部分都不必切换到线程池。
3. 对于大量数据排序，只有在排序时，构造执行任务，切换到线程池完成。

# HotDB线程介绍
HotDB与MyCAT比较相近，不同点是Hotdb的BusinessExecutor线程池有多个，每个Reactor对应一个BusinessExecutor线程池；这是沿用Cobar的思路，是为了降低多Reactor对同一个线程池队列的竞争
