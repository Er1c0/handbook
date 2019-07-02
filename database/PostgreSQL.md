### PostgreSQL服务端和客户端安装
我的本机是Ubuntu，参照http://www.postgresql.org/download/linux/ubuntu/
**查看版本**
```
# sudo lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:  Ubuntu 12.04.1 LTS
Release:  12.04
Codename: precise
```
**Add PostgreSQL Apt Repository**
Create the file /etc/apt/sources.list.d/pgdg.list ,增加一行
```
deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main
```
**Import the repository signing key, and update the package lists**
```
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
  sudo apt-key add -
sudo apt-get update
```
**Install postgresql client**
```
apt-get install postgresql-client-9.4 # client libraries and client binaries
```

## 问题1:psql: 无法联接到服务器: 没有那个文件或目录
psql: 无法联接到服务器: 没有那个文件或目录
  服务器是否在本地运行并且在 Unix 域套接字
  "/var/run/postgresql/.s.PGSQL.5432"上准备接受联接?

http://stackoverflow.com/questions/13868730/socket-file-var-pgsql-socket-s-pgsql-5432-missing-in-mountain-lion-os-x-ser
```
mkdir /var/run/postgresql
ln -s /tmp/.s.PGSQL.5432  /var/run/postgresql/.s.PGSQL.5432
```

# 参考
[PostgreSQL新手入门(1)](http://developer.51cto.com/art/201312/425171.htm):如何创建用户，登录
# 与mysql比较
[PostgreSQL与MySQL比较 ](http://blog.chinaunix.net/uid-354915-id-3506732.html):泛泛的概念性东西
[PostgreSQL与MySQL命令的使用比较](http://netocool.blog.51cto.com/61250/98648):
