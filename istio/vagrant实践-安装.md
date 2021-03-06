# 入门简介

[Vagrant 入门指南](https://linux.cn/article-9587-1.html)

- 构建和管理虚拟机环境的工具
  + 使用 Ruby 开发，基于 VirtualBox 等虚拟机管理软件的接口
- 方便建立起来一个虚拟环境，而且可以模拟多台虚拟机，这样我们平时还可以在开发机模拟分布式系统
- 新员工加入,有了 Vagrant，只需要直接将已经打包好的 package（里面包括开发工具，代码库，配置好的服务器等）拿过来就可以工作


# 在Ubuntu16安装

## 方法1使用apt
参考[install-vagrant-ubuntu-16-04](http://www.codebind.com/linux-tutorials/install-vagrant-ubuntu-16-04/)

这种方式安装的版本较低，为1.8.1
```bash
sudo apt-get install virtualbox #需要先安装 virtualbox
sudo apt-get install vagrant
vagrant #校验
```


## 方法2 官网安装
参考[vagrant安装和使用](https://yq.aliyun.com/articles/392388/)
参考 [官方文档](https://www.vagrantup.com/intro/getting-started/install.html)
```bash
wget https://download.virtualbox.org/virtualbox/6.0.10/virtualbox-6.0_6.0.10-132072~Ubuntu~xenial_amd64.deb
wget https://releases.hashicorp.com/vagrant/2.2.5/vagrant_2.2.5_x86_64.deb
sudo dpkg -i vagrant_2.2.5_x86_64.deb
dpkg -l |grep virtualbox # 查看版本 如果卸载用sudo apt-get remove virtualbox
dpkg -l |grep vagrant # 查看版本
```
# 简单使用
[在官网搜索box](https://app.vagrantup.com/boxes/search)
导入box,启动你的第一个虚拟机
**```bash**
vagrant init centos/7  #会自动创建一个Vagrantfile，并且自动从官方仓储中下载centos/7
vagrant up
```
说明，vagrant命令执行时，需要在包含Vagrantfile文件的目录下运行,否则会报[A Vagrant environment or target machine is required to run this command](https://stackoverflow.com/questions/34745295/a-vagrant-environment-or-target-machine-is-required)


# 共享文件夹

默认情况下，Vagrant会共享项目目录(就是Vagrantfile所在目录)到虚拟机的/vagrant.
[how to map a folder in my VM to my local machine](https://askubuntu.com/questions/323082/how-to-map-a-folder-in-my-vm-to-my-local-machine)

例如启动时有一个语句:Rsyncing folder: xxx => /vagrant
```
==> lab1: Setting hostname...
==> lab1: Configuring and enabling network interfaces...
==> lab1: Rsyncing folder: /home/lingxi/lcz/ => /vagrant
==> lab1: Machine already provisioned. Run `vagrant provision` or use the `--provision`
==> lab1: flag to force provisioning. Provisioners marked to run always will still run.
==> lab1: Running provisioner: shell...
    lab1: Running: inline script
    lab1: hello from lab1
```