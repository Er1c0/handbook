
很不错的文档，整理的基本
[《Unix & Linux 大学教程》 - 第十三章 学习笔记](http://su1216.iteye.com/blog/1631238)
# Ubuntu
## 基础
### 查看版本和内核
```bash
uname -r #内核
cat /etc/issue # 查看内核版本
sudo lsb_release -a #查看版本,有些主机没有安装lsb_release命令，c适用于所有的linux，Centos、UbuntuRedhat、SuSE、Debian等发行版。
```

### 用户管理

（1）创建用户命令两条：
adduser
useradd
（2）用户删除命令：
userdel

二、两个用户创建命令之间的区别
adduser： 会自动为创建的用户指定主目录、系统shell版本，会在创建时输入用户密码。
useradd：需要使用参数选项指定上述基本设置，如果不使用任何参数，则创建的用户无密码、无主目录、没有指定shell版本。



### Ubuntu安装JDK
[How to Install JAVA 8 (JDK 8u45) on Ubuntu & LinuxMint Via PPA](http://tecadmin.net/install-oracle-java-8-jdk-8-ubuntu-via-ppa/)

```bash
apt-get install python-software-properties  #先安装add-apt-repository命令
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
```

配置java环境

```bash
sudo apt-get install oracle-java8-set-default
```


### Ubuntu安装nodejs
上面最新版本为v0.10.37
```
sudo add-apt-repository ppa:chris-lea/node.js 
sudo apt-get update
sudo apt-get install 
```

如果需要安装最新版本：
打开官方网站：https://nodejs.org/dist/latest/ 选择最新版本
可以参考：https://github.com/nodeschool/discussions/issues/1439
```
wget http://nodejs.org/dist/latest/node-v4.2.1-linux-x64.tar.gz 
tar -C /usr/local --strip-components 1 -xzf node-v4.2.1-linux-x64.tar.gz
ls -l /usr/local/bin/node
ls -l /usr/local/bin/npm
```

一个小问题：执行node命令竟然失败了
```
root@iZ23t589u79Z:/usr/local/bin# node -v 
-bash: /usr/bin/node: No such file or directory
root@iZ23t589u79Z:/usr/local/bin# which node
/usr/local/bin/node
root@iZ23t589u79Z:/usr/local/bin# ln /usr/local/bin/node  /usr/bin/node
root@iZ23t589u79Z:/usr/local/bin# node -v
v4.2.1
```

### Ubuntu PPA
PPA，这是一个存储库，由Canonical（Ubuntu背后的公司）提供，其允许开发者和爱好者给Ubuntu用户提供软件的最新版本。最初PPA只是限于编程者和测试者使用，但在2007年底Canonical把PPA开放给了所有人。[参考](http://article.yeeyan.org/view/213582/193672)
Personal Package Archives (PPA) allow you to upload Ubuntu source packages to be built and published as an apt repository by Launchpad

### How to add ppa repositories? 
http://askubuntu.com/questions/217179/how-to-add-ppa-repositories?lq=1
所有可用的ppa
http://www.ubuntuupdates.org/ppas

### ubuntu安装mongodb
官网的安装步骤非常详细
https://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/
### ubuntu安装nginx
参照http://www.ubuntuupdates.org/ppa/nginx?dist=precise
```
sudo add-apt-repository ppa:nginx/stable 
sudo apt-get update
sudo apt-get install 
```
## 问题
### 修改主机名称
root用户默认登录后显示，所以在会话中就立即知道是那台主机
```
root@iZ237bnk0qqZ:~# echo $PS1
${debian_chroot:+($debian_chroot)}\u@\h:\w\$
```


```
hostname #查看主机名
hostname xx #临时修改主机名，重新登录后可以看到。主机重启后恢复原值
vi /etc/hostanme # 永久修改主机名
```

# 环境设置
```
cd
cat .bashrc
可以看到
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
alias p='ps -efa|grep '
alias n='netstat -an |grep '
```

## history用法

https://linuxtoy.org/archives/history-command-usage-examples.html

## 修改apt-get的源
/etc/apt/sources.list:
例如在[Qt5-default package not found](http://askubuntu.com/questions/468432/qt5-default-package-not-found)例子中增加 deb http://http.debian.net/debian jessie main

注意，执行完后一定要执行，sudo apt-get update

## 开机自动重启方法
linux ubuntu开机自动运行程序方法rc.local
文件
/etc/rc.local 

# 工具
## /proc/meminfo之谜
参见：http://www.tuicool.com/articles/muqIBvy
