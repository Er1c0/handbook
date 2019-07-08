[TOC]
# 阅读
[大数据架构的未来](http://www.mongoing.com/blog/post/the-future-of-big-data-architecture)
[MongoDB 3.0新增特性一览](http://blog.sina.com.cn/s/blog_48c95a190102vedr.html)
[MongoDB 倾向于将数据都放在一个 Collection 下吗？](https://segmentfault.com/q/1010000000589390)
[Hadoop Map/Reduce vs built-In Map/Reduce](http://stackoverflow.com/questions/9287585/hadoop-map-reduce-vs-built-in-map-reduce)
[Using MongoDB with Hadoop & Spark: Part 1 - Introduction & Setup](https://www.mongodb.com/blog/post/using-mongodb-hadoop-spark-part-1-introduction-setup?jmp=docs&_ga=1.46654882.46421289.1462274693)
# Mac安装MongoDb

参考：http://www.cnblogs.com/junqilian/p/4109580.html
```
brew update #要几分钟，取决于网络速度
brew install mongodb # 安装，大小154M
  mongod -f /usr/local/etc/mongod.conf #启动
```

```
>mongo
MongoDB shell version: 3.0.4
connecting to: test
Server has startup warnings: 
2015-07-03T12:56:05.722+0800 I CONTROL  [initandlisten] 
2015-07-03T12:56:05.722+0800 I CONTROL  [initandlisten] ** WARNING: soft rlimits too low. Number of files is 256, should be at least 1000
```

参见官方手册：https://docs.mongodb.org/manual/administration/install-on-linux/

参数配置：https://docs.mongodb.org/manual/reference/configuration-options/

如果远端密码访问：
https://docs.mongodb.org/manual/reference/configuration-options/
```
net:
  port: 27017
#  bindIp: 127.0.0.1 #默认是0.0.0.0
security:
  authorization: enabled
```

# Ubuntu安装MongoDb
官方手册：https://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/

重要！！ 配置文件/etc/mongod.conf

重启：
```
sudo service mongod stop
sudo service mongod start
```
## 更重要，与ubuntu提供的工具包冲突？！！

`mongodb-org`包是MongoDB公司官方维护和支持的，并且与最新的MongoDB发布版本保持更新。
由Ubuntu提供的`mongodb`并不是MongoDB公司维护的，并且与`mongodb-org`冲突。检查Ubuntu的`mongodb`是否安装在系统上，运行`sudo apt list --installed | grep mongodb`,在正式安装前，您可以使用`sudo apt remove mongodb`和`sudo apt purge mongodb`来删除和清除mongodb包。

- mongodb-org 一个元包，自动包含了下列四个组件包
- mongodb-org-server 包含mongod、初始脚本和一个配置文件(/etc/mongod.conf)
- mongodb-org-mongos 包含mongos
- mongodb-org-shell 包含mongo
- mongodb-org-tools 包含下列工具：`mongoimport bsondump, mongodump, mongoexport, mongofiles, mongorestore, mongostat, and mongotop`



## MongoDb数据文件迁移记录
数据文件默认是系统盘，大小有限制，需要迁移到专门的数据盘
1.打开/etc/mongod.conf查看dbPath的路径
2.停止
3.把数据目录拷贝到数据盘
4.chown -R mongodb:mongodb mongodb
5.启动

# 基本操作
[MongoDB基本使用](http://www.cnblogs.com/TankMa/archive/2011/06/08/2074947.html):整理的很全面

## 用户管理
### 创建用户管理员
参见：http://docs.mongodb.org/manual/tutorial/add-user-administrator/
创建系统的用户管理员
```
use admin
db.auth('root','xxx')
db.createUser(
  {
    user: "sa",
    pwd: "sa!QAZ2wsx",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
  }
);
db.createUser(
  {
    user: "root",
    pwd: "root_jfjun88",
    roles: [ { role: "root", db: "admin" } ]
  }
);
> show databases
admin  0.078GB
local  0.078GB
> show collections;
system.indexes
system.users
system.version
> db.system.users.find();
```
创建单个数据库的用户管理员
```
use jfjun
db.createUser(
  {
    user: "test1",
    pwd: "test1",
    roles: [ { role: "userAdmin", db: "jfjun" } ]
  }
);
```
### 创建使用用户
创建一个库的使用用户  http://docs.mongodb.org/manual/tutorial/manage-users-and-roles/#create-user-defined-role
查看哪些角色和角色的权限


```
show roles  --显示角色数量
db.getRole( "readWrite", { showPrivileges: true } ) --显示权限细节
```

可以访问所有库数据的超级用户
```
use admin
db.createUser(
  {
    user: "root",
    pwd: "12345678",
    roles: [ { role: "root", db: "admin" } ]
  }
);
```
mongo  -u root -p 12345678 120.26.68.22:27017/admin
单个库的读写权限
```
use jfjun
db.createUser(
  {
    user: "root",
    pwd: "12345678",
    roles: [ { role: "root", db: "jfjun" } ]
  }
);
show users;
```
然后可以通过用户名和密码访问
mongo  -u jfjun -p jfjun12qw 120.26.68.22:27017/jfjun

### 权限说明
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
### 删除用户
```
db.auth("test1","test1")
show users;
db.dropUser('test1');
```
### 修改用户密码
[参见官网文档](https://docs.mongodb.org/manual/tutorial/manage-users-and-roles/#modify-password-for-existing-user)
先用admin登录，然后执行下列
use jfjun_fp_dev1 --切换到对应database
db.changeUserPassword("reporting", "SOh3TbYhxuLiW8ypJPxmt1oOfL")
db.updateUser('test',{pwd:'lingxilingxi'});

## 重启
```bash
/usr/bin/mongod -f /etc/mongodb.conf --shutdown
/usr/bin/mongod --fork -f /etc/mongodb.conf #-fork flag to your mongod invocation will keep it running in the background
```
## 创建表和索引
[给MongoDB添加索引](http://blog.163.com/ji_1006/blog/static/10612341201311243825985/)
db.createCollection("brother1s") --- 创建表
db.brother1s.ensureIndex({"name":1},{"unique":true})--创建索引
## 导入导出数据
参见官方文档：
http://docs.mongodb.org/manual/reference/program/mongoexport/
参见中文：http://chenzhou123520.iteye.com/blog/1641319

mongoexport --db watchdog --collection accounts --out accounts.json
--fields <field1[,field2]>
json格式的导入导出
mongoimport 和mongorestore --help没有列出batchSize 的帮助，

```bash
mongoexport --db=jfjun_web --collection=brothers --username=web1 --password=web1  --out brothers.json
mongoimport --db=jfjun_web   --collection=brothers  --username=web1 --password=web1 brothers.json
```

csv格式的
```
mongoexport --db=jfjun_web --collection=brothers --username=web1 --password=web1 type=csv --fields=name,displayName,img,detail,http,industry,createTime,updateTime --out brothers.csv
mongoimport --db=jfjun_web   --collection=brothers  brothers.json #--username=web1 --password=web1 

```


```
mongo  -u test -p lingxi 120.26.68.22:27017/watchdog
mongo  -u test -p lingxi 192.168.1.119:27017/watchdog
# 导出整个库
mongodump \
--db=watchdog --username=test --password=lingxi --host=192.168.1.119:27017 \
-o my
# 导入整个库
mongorestore \
--drop   \
--db=watchdog --username=test --password=lingxi --host=120.26.68.22:27017 \
my/*
```
## 最简单的增删改查
输入help可以看到基本操作命令：
- show dbs:显示数据库列表 
- show collections：显示当前数据库中的集合（类似关系数据库中的表） 
- show users：显示用户
- use <db name>：切换当前数据库，这和MS-SQL里面的意思一样 
- db.help()：显示数据库操作命令，里面有很多的命令 
- db.foo.help()：显示集合操作命令，同样有很多的命令，foo指的是当前数据库下，一个叫foo的集合，并非真正意义上的命令 
- db.foo.find()：对于当前数据库中的foo集合进行数据查找（由于没有条件，会列出所有数据） 
- db.foo.find( { a : 1 } )：对于当前数据库中的foo集合进行查找，条件是数据中有一个属性叫a，且a的值为1


```sql
db.person.find();
db.person.insert({"name":"jack","age":20});
db.person.update({"name":"jack"},{"name":"jack","age":30});
db.person.remove({"name":"jack"});
db.person.count();
```

mongo命令打开的是一个javascript shell,所以可以直接用js语法

```sql
var p={"name":"jack","age":20};
db.person.insert(p);
p.name="marry";
db.person.insert(p);
db.person.find();
```
## 修改字段命名
db.test.update({}, {$rename : {"oldname" : "newname"}}, false, true)

## 数组操作
### 查询数组中的一个元素
```
db.getCollection('balancesheets').find({_id:ObjectId("56cea0699a3bec4b54a7d7fc"),'balances.subject':'1002'},{'balances.$':1})
```
### 添加数组中的一个元素
```

```

### 更新数组中一个元素的某个字段
```
db.getCollection('fixedassets').update({_id:ObjectId("571050e4791c6a5a5b492bd1"),"items.key":"123"},
{$set:{"items.$.abc":"test"}}，{multi:true})
```
说明： 若document的数组中有多个满足条件的子元素，只能更新一个子元素的值
参见：http://stackoverflow.com/questions/4669178/how-to-update-multiple-array-elements-in-mongodb 给出的方法，只能查找遍历修改，然后再保存对象

### 更新数组中一个元素
```
db.getCollection('fixedassets').update({_id:ObjectId("571050e4791c6a5a5b492bd1"),"items._id":ObjectId("571050e4791c6a5a5b492bd2")},
{$set:{"items.$":{
    "_id" : ObjectId("571050e4791c6a5a5b492bd2"),
    "initVal" : 41699.15,
    "depreciationPeriod" : 36,
    "residualVal" : 2084.96,
    "abc" : "test1"
}}})
```
### 删除数组中一个元素
这个语句只会置为null，不会删除这个元素
```
db.getCollection('fixedassets').update({_id:ObjectId("571050e4791c6a5a5b492bd1"),"items._id":ObjectId("571050e4791c6a5a5b492bd2")},
{$unset:{"items.$":""}})
```



# 查询
## 一般查询语法
http://www.nonb.cn/blog/mongodb-advanced-queries.html
WHERE查询
// i.e., select * from things where x=3 and y="foo"
db.things.find( { x : 3, y : "foo" } );

存储数组元素
db.things.insert({colors : ["blue", "black"]})
db.things.insert({colors : ["yellow", "orange", "red"]})
//查询结果
db.things.find({colors : {$ne : "red"}})
{"_id": ObjectId("4dc9acea045bbf04348f9691"), "colors": ["blue","black"]}
 

对比操作符
$ne 不等于
db.collection.find({ "field" : { $gt: value } } );   // greater than  : field > value
db.collection.find({ "field" : { $lt: value } } );   // less than  :  field < value
db.collection.find({ "field" : { $gte: value } } );  // greater than or equal to : field >= value
db.collection.find({ "field" : { $lte: value } } );  // less than or equal to : field <= 
 

$all 全部属于
db.things.find( { a: { $all: [ 2, 3 ] } } )
 

$exists 字段存在
db.things.find( { a : { $exists : true } } )
db.things.find( { a : { $exists : false } } )
true返回存在字段a的数据，false返回不存在字度a的数据。
 

$mod 取模运算
db.things.find( { a : { $mod : [ 10 , 1 ] } } )
条件相当于a % 10 == 1 即a除以10余数为1的。

$in 属于
db.things.find({j:{$in: [2,4,6]}})
条件相当于j等于[2,4,6]中的任何一个。
 

$nin 不属于
db.things.find({j:{$nin: [2,4,6]}})
条件相当于 j 不等于 [2,4,6] 中的任何一个。
 

$or 或 （注意：MongoDB 1.5.3后版本可用）
db.foo.find( { $or : [ { a : 1 } , { b : 2 } ] } )
符合条件a=1的或者符合条件b=2的数据都会查询出来。
 

$size 数量，尺寸
db.things.find( { a : { $size: 1 } } )
条件相当于a的值的数量是1（a必须是数组，一个值的情况不能算是数量为1的数组）。
 

$type 字段类型
db.things.find( { a : { $type : 2 } } )
条件是a类型符合的话返回数据。
 

limit() skip()
这两个ME想连起来讲，他们就是你实现数据库分页的好帮手。
limit()控制返回结果数量，如果参数是0，则当作没有约束，limit()将不起作用。
skip()控制返回结果跳过多少数量，如果参数是0，则当作没有约束，skip()将不起作用，或者说跳过了0条。
例如：
 db.test.find().skip(5).limit(5)
结果就是取第6条到第10条数据。
snapshot()   （没有尝试）
count()   条数
返回结果集的条数。
db.test.count()
在加入skip()和limit()这两个操作时，要获得实际返回的结果数，需要一个参数true，否则返回的是符合查询条件的结果总数。
例子如下：
$elemMatch
如果对象有一个元素是数组，那么$elemMatch可以匹配内数组内的元素：
 t.find( { x : { $elemMatch : { a : 1, b : { $gt : 1 } } } } ) 
{ "_id" : ObjectId("4b5783300334000000000aa9"), 
"x" : [ { "a" : 1, "b" : 3 }, 7, { "b" : 99 }, { "a" : 11 } ]
}
$elemMatch : { a : 1, b : { $gt : 1 } } 所有的条件都要匹配上才行。
注意，上面的语句和下面是不一样的。
 t.find( { "x.a" : 1, "x.b" : { $gt : 1 } } )
$elemMatch是匹配{ "a" : 1, "b" : 3 }，而后面一句是匹配{ "b" : 99 }, { "a" : 11 } 
1)  查询嵌入对象的值

db.postings.find( { "author.name" : "joe" } );
注意用法是author.name，用一个点就行了。更详细的可以看这个链接： dot notation
举个例子：
 db.blog.save({ title : "My First Post", author: {name : "Jane", id : 1}})
如果我们要查询 authors name 是Jane的, 我们可以这样：
 db.blog.findOne({"author.name" : "Jane"})
如果不用点，那就需要用下面这句才能匹配：
db.blog.findOne({"author" : {"name" : "Jane", "id" : 1}})
下面这句：
db.blog.findOne({"author" : {"name" : "Jane"}})
是不能匹配的，因为mongodb对于子对象，他是精确匹配。

## 聚合
http://www.cnblogs.com/shanyou/archive/2012/08/05/2624073.html
```
db.system.js.save( { _id : "Sum" ,
value : function(key,values)
{
    var total = 0;
    for(var i = 0; i < values.length; i++)
        total += values[i];
    return total;
}});
db.system.js.save( { _id : "Count" ,
value : function(key,values)
{
    return values.length;
}});
```

```
use jfjun_web
db.accessinfos.runCommand(
{
mapreduce : "accessinfos",
map:function()
{
        emit(
        {key0:this.statTime,
        key1:this.userAgent},
        // Values
        this.ip);
}, 
reduce:function(key,values)
{
    var result = Count(key, values);
    return result;
},
out : { inline : 1 } });
```

### mapreduce的注意点
https://docs.mongodb.org/manual/reference/method/db.collection.mapReduce/#mapreduce-map-mtd

map：
The map function may optionally call emit(key,value) any number of times to create an output document associating key with value.
**一个map函数可以调用任意次数的emit**

reduce：
can invoke the reduce function more than once for the same key
The reduce function can access the variables defined in the scope parameter.

#  概念
mongodb中有三元素：

- 数据库，
- 集合，就是对应关系数据库中的“表”
- 文档，对应“行”；

部署：MongoDB使用的是memory-mapped file
MongoDB高度事务性的系统：例如银行或会计系统。传统的关系型数据库目前还是更适用于需要大量原子性复杂事务的应用程序。

# 客户端
http://docs.mongodb.org/ecosystem/tools/administration-interfaces/ 
Robomongo ，开源软件，只有10M
另外还有个[mongo-express](https://github.com/andzdroid/mongo-express)，是用nodejs和express写的

# 网上培训课程-MongoDB实战
http://www.dataguru.cn/article-7129-1.html
# 系统运维
## journal太大
参考1：http://lostquery.com/questions/313/how-do-i-shrink-the-mongodb-journal-files
参考2：http://stackoverflow.com/questions/19533019/is-it-safe-to-delete-the-journal-file-of-mongodb
修改/etc/mongod.conf 的storage.smallFiles参数为空
## 只允许本地访问
bind_ip = 127.0.0.1
## 性能优化
[MongoDB 性能优化五个简单步骤](http://blog.oneapm.com/apm-tech/183.html)

## transparent huge pages

https://docs.mongodb.com/manual/tutorial/transparent-huge-pages/
## mongodump 和 Replic Set 
https://docs.mongodb.com/manual/reference/program/mongodump/

- 如果在--host前有the replica set name,将会读取主库，
  + <replSetName>/<hostname1><:port>,<hostname2><:port>,<...>
- 如果没有包含replica set name，会读取最近节点

## copyDatabase
https://docs.mongodb.com/manual/reference/method/db.copyDatabase/#db.copyDatabase
在copy时要保证有足够的磁盘空间，db.stats()表示数据库的统计信息


```
mongo $DB -u "test" -p "lingxi" --eval "db.dropDatabase();db.copyDatabase('jfjun_cw4', '$DB', 'dds-bp1aa90ef5a8a7f41.mongodb.rds.aliyuncs.com:3717', 'jfjunR', 'lingxi');"
```
尝试了copydb,但是没有成功：
```
mynonce = db.runCommand( { copydbgetnonce : 1, fromhost: 'dds-bp1aa90ef5a8a7f41.mongodb.rds.aliyuncs.com:3717' } ).nonce

hex_md5('7337108a719dd4fc' + 'jfjunR' + hex_md5('jfjunR'+":mongo:"+'lingxi'))
db.runCommand({
   copydb: 1,
   fromdb: "jfjun_cw4",
   todb: "jfjun_ml_test",
   fromhost: "dds-bp1aa90ef5a8a7f41.mongodb.rds.aliyuncs.com:3717",
   username: 'jfjunR',
   slaveOk:true,
   nonce: "7337108a719dd4fc",
   key: "28e2c60ea360baed61c18deab294dd1d"
})
```
报错：
```
{
  "ok" : 0,
  "errmsg" : "unable to login { ok: 0.0, errmsg: \"auth failed\", code: 18, codeName: \"AuthenticationFailed\" }"
}
```

但是看文档 说是只是从secondary 拷贝数据的
https://docs.mongodb.com/v2.2/tutorial/copy-databases-between-instances/#considerations
https://docs.mongodb.com/v2.2/reference/command/copydb/
- 并发
  - 源数据库不产生 point-in-time snapshots，可能会产生有分歧的数据
  - 目标数据库不加锁，可能同时会有其他操作
- 如果远端服务需要授权，需要先请求一个one-time password ，然后生成key
- 索引
  + 执行foreground builds of indexes ，会锁定数据库，阻止其它操作
  + 可以通过db.currentOp()查看当前操作

# 小工具
## 根据ObjectId获取时间
https://steveridout.github.io/mongo-object-time/

# 参考文章:
- [MongoDB权限访问控制](https://www.jianshu.com/p/ca08e63fd587)