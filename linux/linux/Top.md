http://os.51cto.com/art/201108/285581.htm

# Linux top命令简介

top 命令是最流行的性能监视工具之一，我们必需了解。它是一个优秀的交互式工具，用于监视性能。它提供系统整体性能，但报告进程信息才是 top 命令的长处。top 命令交互界面如下图所视：
top 界面分为两个部份，光标上面部份显示关于系统整体性能，光标下面部份显示各进程信息。光标所在处是用来输入操作命令的。

Linux top命令界面
第一行显示的内容和uptime命令一样，【l】可以显示和隐藏这个区域：

top界面第一行|uptime
top：   这个没有什么意思，只是个名称而以

01：47：56 ：     系统当前时间

up 1:26   ：   系统开机到现在经过了多少时间

2 users  ：            当前2用户在线

load average:0.00,0.00,0.00：        系统1分钟、5分钟、15分钟的CPU负载信息

第二行：

top界面第二行
Tasks：英文意思是工作;任务;差事。

38 total：很好理解，就是当前有38个任务，也就是38个进程。

1 running：1个进程正在运行

37 sleeping：37个进程睡眠

0 stopped：停止的进程数

0 zombie：僵死的进程数

Cpu(s)：表示这一行显示CPU总体信息

0.0%us：用户态进程占用CPU时间百分比，不包含renice值为负的任务占用的CPU的时间。

0.7%sy：内核占用CPU时间百分比

0.0%ni：renice值为负的任务的用户态进程的CPU时间百分比。nice是优先级的意思

99.3%id：空闲CPU时间百分比

0.0%wa：等待I/O的CPU时间百分比

0.0%hi：CPU硬中断时间百分比

0.0%si：CPU软中断时间百分比

0.0%st：我不知道

第三行：

TOP界面第三行
Men：内存的意思

256412k total：物理内存总量

30156k used：使用的物理内存量

226256 free：空闲的物理内存量

8176k buffers：用作内核缓存的物理内存量

Swap：交换空间

337356k total：交换区总量

0k used：使用的交换区量

337356k free：空闲的交换区量

12160k cached：缓冲交换区总量

第四行：

top界面第四行
PID：进程的ID

USER：进程所有者

PR：进程的优先级别，越小越优先被执行

NInice：值

VIRT：进程占用的虚拟内存

RES：进程占用的物理内存

SHR：进程使用的共享内存

S：进程的状态。S表示休眠，R表示正在运行，Z表示僵死状态，N表示该进程优先值为负数

%CPU：进程占用CPU的使用率

%MEM：进程使用的物理内存和总内存的百分比

TIME+：该进程启动后占用的总的CPU时间，即占用CPU使用时间的累加值。

COMMAND：进程启动命令名称

Linux top命令操作指令

下面我列出一些常用的linux top命令操作指令：

q：退出top命令

<Space>：立即刷新

s：设置刷新时间间隔

c：显示命令完全模式

t:：显示或隐藏进程和CPU状态信息

m：显示或隐藏内存状态信息

l：显示或隐藏uptime信息

f：增加或减少进程显示标志

S：累计模式，会把已完成或退出的子进程占用的CPU时间累计到父进程的MITE+

P：按%CPU使用率排行

T：按MITE+排行

M：按%MEM排行

u：指定显示用户进程

r：修改进程renice值

kkill：进程

i：只显示正在运行的进程

W：保存对top的设置到文件~/.toprc，下次启动将自动调用toprc文件的设置。

h：帮助命令。

原文：http://www.itwhy.org/2011/07-05/437.html

# 【编辑推荐】

Linux系统监控工具之top详解
为Linux管理员节省时间的十条命令行
实例解说Linux命令行uniq
# edit you top mode 
~/.toprc
G
```
RCfile for "top with windows"       # shameless braggin'
Id:a, Mode_altscr=0, Mode_irixps=1, Delay_time=3.000, Curwin=0
Def fieldscur=AEHIOQTWKNMbcdfgjplrsuvyzX
    winflags=65081, sortindx=10, maxtasks=0
    summclr=1, msgsclr=1, headclr=3, taskclr=2
Job fieldscur=ABcefgjlrstuvyzMKNHIWOPQDX
    winflags=62777, sortindx=0, maxtasks=0
    summclr=6, msgsclr=6, headclr=7, taskclr=6
Mem fieldscur=ANOPQRSTUVbcdefgjlmyzWHIKX
    winflags=62777, sortindx=13, maxtasks=0
    summclr=5, msgsclr=5, headclr=4, taskclr=5
Usr fieldscur=ABDECGfhijlopqrstuvyzMKNWX
    winflags=62777, sortindx=4, maxtasks=0
    summclr=3, msgsclr=3, headclr=2, taskclr=3
```