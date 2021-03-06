# 用户管理
## 用户登录鉴权

鉴权的两种方式：

**（一）登陆时鉴权**
```
mongo --port 27017 -u "myUserAdmin" -p "abc123" --authenticationDatabase "admin"
```
**（二）登陆后鉴权**
```
mongo --port 27017
use admin
db.auth("myUserAdmin", "abc123" )
```

## 创建用户
感觉有点啰嗦：

- 首先选择在哪个数据库上创建用户，
- 每个用户必须要设置角色列表，
- 角色必须要指定应用到哪个数据库

[创建系统的用户管理员](http://docs.mongodb.org/manual/tutorial/add-user-administrator/)
```
use admin #改用户创建在哪个数据库上，即对应authenticationDatabase是哪个
db.auth('root','xxx')
db.createUser(
  {
    user: "sa",
    pwd: "sa!QAZ2wsx",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
  }
);
```
创建单个数据库的用户管理员
```
use jfjun
db.createUser(
  {
    user: "test1",
    pwd: "test1",
    roles: [ { role: "readWrite", db: "jfjun" } ]
  }
);
```
mongo  -u test1 -p test1 localhost:27017/jfjun
## 查看角色
查看哪些角色和角色的权限
```
db.system.users.find();
show users;
show roles;  --显示角色数量
db.getRole( "readWrite", { showPrivileges: true } ) --显示权限细节
```

## 权限说明
名词解释：

- Read：允许用户读取指定数据库
- readWrite：允许用户读写指定数据库
- dbAdmin：允许用户在指定数据库中执行管理函数，如索引创建、删除，查看统计或访问system.profile
- userAdmin：允许用户向system.users集合写入，可以找指定数据库里创建、删除和管理用户
- clusterAdmin：只在admin数据库中可用，赋予用户所有分片和复制集相关函数的管理权限。
- readAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读权限
- readWriteAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读写权限
- userAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的userAdmin权限
- dbAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的dbAdmin权限。
- root：只在admin数据库中可用。超级账号，超级权限

Built-In Roles（内置角色）：

1. 数据库用户角色：read、readWrite;
2. 数据库管理角色：dbAdmin、dbOwner、userAdmin；
3. 集群管理角色：clusterAdmin、clusterManager、clusterMonitor、hostManager；
4. 备份恢复角色：backup、restore；
5. 所有数据库角色：readAnyDatabase、readWriteAnyDatabase、userAdminAnyDatabase、dbAdminAnyDatabase
6. 超级用户角色：root  // 这里还有几个角色间接或直接提供了系统超级用户的访问（dbOwner 、userAdmin、userAdminAnyDatabase）
7. 内部角色：__system

[MongoDB设置访问权限、设置用户](http://www.cnblogs.com/zengen/archive/2011/04/23/2025722.html)
[MongoDB的授权登录处理](https://www.cnblogs.com/wingjay/p/3954430.html)
[Manage Users and Roles](https://docs.mongodb.com/manual/tutorial/manage-users-and-roles/)
## 删除用户
```
db.auth("test1","test1")
db.dropUser('test1');
```
## 修改用户密码
[参见官网文档](https://docs.mongodb.org/manual/tutorial/manage-users-and-roles/#modify-password-for-existing-user)
先用admin登录，然后执行下列
use jfjun_fp_dev1 --切换到对应database
db.changeUserPassword("reporting", "SOh3TbYhxuLiW8ypJPxmt1oOfL")
db.updateUser('test',{pwd:'lingxilingxi'});