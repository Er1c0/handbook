# ssh-keygen
ssh-keygen命令用于为“ssh”生成、管理和转换认证密钥，它支持RSA和DSA两种认证密钥
[ssh-keygen介绍](https://www.cnblogs.com/kerrycode/p/9410928.html)
[SSH-KEYGEN - GENERATE A NEW SSH KEY](https://www.ssh.com/ssh/keygen/)

# openssh介绍
[openssh](https://www.ssh.com/ssh/openssh)
[wiki OpenSSH](https://en.wikipedia.org/wiki/OpenSSH):Not to be confused with OpenSSL

# 扩展阅读:SSL和SSH和OpenSSH，OpenSSL有什么区别
[SSL和SSH和OpenSSH，OpenSSL有什么区别](https://www.cnblogs.com/foohack/p/4103212.html)
[SSH、OpenSSH、SSL、OpenSSL](https://www.jianshu.com/p/6ab9700a69bb)

- SSL
    + Secure Sockets Layer的缩写，是为网络通信提供安全及数据完整性的一种安全协议，在传输层对网络连接进行加密,只是一种协议.
    + 通讯链路的附加层,可以包含很多协议。https, ftps,wss(Web Socket Secure 的简称, 它是 WebSocket 的加密版本)
- OpenSSL
    + SSL的开源实现(具体的实现方式,一个C语言函数库)
    + 绝大部分HTTPS请求等价于：HTTP + OpenSSL
- SSH
    + Secure Shell的缩写，意为“安全外壳协议”，是一种可以为远程登录提供安全保障的协议.
    + 使用SSH，可以把所有传输的数据进行加密，“中间人”攻击方式就不可能实现，能防止DNS欺骗和IP欺骗
    + 还有一个额外的好处就是传输的数据是经过压缩的，所以可以加快传输的速度。SSH有很多功能，它既可以代替telnet，又可以为ftp、pop、甚至ppp提供一个安全的“通道”。
    + SSH是由客户端和服务端的软件组成的，有两个不兼容的版本分别是：1.x和2.x。用SSH 2.x的客户程序是不能连接到SSH 1.x的服务程序上去的。OpenSSH 2.x同时支持SSH 1.x和2.x。
    + SSH的安全验证是如何工作的从客户端来看，SSH提供两种级别的安全验证。
        * 第一种级别（基于口令的安全验证）只要你知道自己帐号和口令，就可以登录到远程主机。所有传输的数据都会被加密，但是不能保证你正在连接的服务器就是你想连接的服务器。可能会有别的服务器在冒充真正的服务器，也就是受到“中间人”这种方式的攻击。
        * 第二种级别（基于密匙的安全验证）需要依靠密匙，也就是你必须为自己创建一对密匙，并把公用密匙放在需要访问的服务器上。如果你要连接到SSH服务器上，客户端软件就会向服务器发出请求，请求用你的密匙进行安全验证。服务器收到请求之后，先在你在该服务器的家目录下寻找你的公用密匙，然后把它和你发送过来的公用密匙进行比较。如果两个密匙一致，服务器就用公用密匙加密“质询”（challenge）并把它发送给客户端软件。客户端软件收到“质询”之后就可以用你的私人密匙解密再把它发送给服务器。
        * 与第一种级别相比，第二种级别不需要在网络上传送口令。第二种级别不仅加密所有传送的数据，而且“中间人”这种攻击方式也是不可能的（因为他没有你的私人密匙）
- OpenSSH
    + 是SSH协议的免费开源实现
    + OpenSSH的加密就是通过OpenSSL完成的
    + 从编译依赖上看：openssh依赖于openssl，没有openssl的话openssh就编译不过去，也运行不了。
    + 正宗的openssh为 [OpenBSD](https://www.openssh.com/)
    + github上的[Portable OpenSSH](https://github.com/openssh/openssh-portable)
# ssh秘钥变更导致git pull失败
gitlab主机的ssh秘钥变更导致git pull失败
```
root@ml179:~/build_project/gitbook# git pull
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ECDSA key sent by the remote host is
SHA256:Q0epvJ/OXBoINj+KGKALtWfd5glW8h3QnF+oX3rchJ0.
Please contact your system administrator.
Add correct host key in /root/.ssh/known_hosts to get rid of this message.
Offending ECDSA key in /root/.ssh/known_hosts:1
  remove with:
  ssh-keygen -f "/root/.ssh/known_hosts" -R gitlab.lingxi.co
ECDSA host key for gitlab.lingxi.co has changed and you have requested strict checking.
Host key verification failed.
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```
ssh-keygen -f "/root/.ssh/known_hosts" -R gitlab.lingxi.co