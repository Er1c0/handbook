# 几个Mongodb库比较

- mongorito 基本处于停滞状态
- [mongoose](https://github.com/Automattic/mongoose) 仍然非常活跃
- [node-mongodb-native](https://github.com/mongodb/node-mongodb-native) 仍然非常活跃,其[说明文档](http://mongodb.github.io/node-mongodb-native/3.3/api/Collection.html)

## Difference between MongoDB and Mongoose：

就nodejs而言，`mongodb`是与mongodb实例交互的原生驱动程序，而mongoose是mongodb的对象建模工具。
Mongoose是构建在mongodb驱动程序之上，为程序员提供了一种对数据建模的工具。

使用Mongoose，用户可以为特定集合中的文档定义模式，它为MongoDB中的数据创建和管理提供便利。缺点方面，学习mongoose可能需要些时间，并且处理那些相当复杂的模式方面有些限制。

但是，如果你的集合模式不可预测，或者你想要在Node.js中有类似Mongo-shell的体验，那就继续使用MongoDB驱动吧。这是最简单的选择。缺点是你必须编写更大量的代码来验证数据，并且错误的风险更高。

- https://stackoverflow.com/questions/28712248/difference-between-mongodb-and-mongoose 
- https://medium.com/@bugwheels94/performance-difference-in-mongoose-vs-mongodb-60be831c69ad: 使用了benchmark进行测试
- [Mongodb-native over mongoose?](https://dev.to/tojacob/mongodb-native-over-mongoose--3n9e):
  - [Kevin Isom](https://github.com/Kevnz):我使用mongojs或者mongodb.如果你使用的是无模式的数据库，那为什么要引入模式呢？为了校验？实际上，在访问db/(model之前就应该检验了，或者在api入口，或者在离开浏览器之前。因此，校验应该再客户端和服务器之前共享，而不是在数据库级别)
  - [Perry Donham](https://dev.to/perrydbucs):1.我在课程中推广Mongoose作为设计工具。抽象通常作为契约，使用Mongoose模式，我可以创建并强化与数据库接口的契约。这个模式也能帮我思考数据的结构及其关系。2.如果应用需要存储任意对象，我可能只使用没有mongoose抽象的MongoDB，但是依我的经营，这种要求非常罕见。

## mongoose和node-mongodb-native的关系
在mongoose官网中，有这么一段:

> Mongoose is built on top of the official MongoDB Node.js driver. Each mongoose model keeps a reference to a native MongoDB driver collection. The collection object can be accessed using YourModel.collection. However, using the collection object directly bypasses all mongoose features, including hooks, validation, etc. The one notable exception that YourModel.collection still buffers commands. As such, YourModel.collection.find() will not return a cursor.

Mongoose建立在MongoDB官方Node.js驱动程序之上。每个mongoose模型都保留对原生MongoDB驱动程序集合的引用。 可以使用YourModel.collection访问集合对象。 但是，使用集合对象直接绕过所有的mongoose功能，包括钩子，验证等.一个值得注意的例外是**YourModel.collection仍然缓冲命令**。因此YourModel.collection.find（）不会返回游标。

另外YourModel.db 返回的是原生的链接对象，对应功能可参见[node-mongodb-native/3.3/api/Db](http://mongodb.github.io/node-mongodb-native/3.3/api/Db.html)

# mongodb驱动测试代码
```
const MongoClient = require('mongodb').MongoClient;

const url = 'mongodb://test:test@localhost/test';
let client = await MongoClient.connect(url, { useNewUrlParser: true });
const db = client.db();
let collection = db.collection('formdatas1');
if (!collection) {
collection = await db.createCollection('formdatas1');
}
await collection.save({ a: 1 })
// Find some documents
let ret = await collection.find({}).toArray();
console.log("list = ", ret);
let one = await collection.findOne({});
console.log("one=", one);
```
# mongoose


## mongodb的运行器
- mongodb-topology-manager
  - 允许以编程方式启动MongoDB实例、Replicaset或Sharded群集
- mongodb-memory-server
  - 以编程方式启动真实的Mongodb Server，以便在开发期间进行测试和模拟。
  - 默认情况下讲数据保存在内存中。
  - 在启动时下载最新的Mongo二进制包，保存在cache目录。首次启动会占用些时间。

## 构造数据
- dookie
  - 允许使用额外的语法糖(扩展json、变量、导入、继承等)在Json或yaml中编写mongodb测试装置
- Seedgoose 
  - 以递归方式变量你的模型，为您设置智能ID引用跟踪

## mongoose_inherit_to_diff_collection
[The model.discriminator() function](http://mongoosejs.com/docs/discriminators.html)
Discriminators are a schema inheritance mechanism. They enable you to have multiple models with overlapping schemas on top of the same underlying MongoDB collection.
鉴别器是一种schema继承模式，它们使您能够在同一底层MongoDB集合之上具有重叠模式的多个模型。

Suppose you wanted to track different types of events in a single collection. Every event will have a timestamp, but events that represent clicked links should have a URL. You can achieve this using the model.discriminator() function. This function takes 2 parameters, a model name and a discriminator schema. It returns a model whose schema is the union of the base schema and the discriminator schema.

假设你想跟踪不同类型的事件在用一个collection上。每个event有个时间戳，但是表达点击的事件有个url。你就通过 model.discriminator使用这个功能,2个参数，model名称和discriminator模式。返回一个模型，它的模式是基本模式和鉴别模式的联合体
# How to inherit a mongoose model and store it in a different collection
[How to inherit a mongoose model and store it in a different collection](http://stackoverflow.com/questions/34980337/how-to-inherit-a-mongoose-model-and-store-it-in-a-different-collection)


# 案例
## MongoNetworkError: connection 0 to xxx closed 数据库连接关闭
如下日志，可能原因是数据库宕机了
```
(node:8266) UnhandledPromiseRejectionWarning: MongoNetworkError: connection 0 to dds-bp1ad70ef34be93433270.mongodb.rds.aliyuncs.com:3717 closed
    at Socket.<anonymous> (/root/test/mongodb-performance/node_modules/mongodb-core/lib/connection/connection.js:352:9)
    at Object.onceWrapper (events.js:272:13)
    at Socket.emit (events.js:180:13)
    at TCP._handle.close [as _onclose] (net.js:541:12)
(node:8266) UnhandledPromiseRejectionWarning: Unhandled promise rejection. This error originated either by throwing inside of an async function without a catch block, or by rejecting a promise which was not handled with .catch(). (rejection id: 1)
(node:8266) [DEP0018] DeprecationWarning: Unhandled promise rejections are deprecated. In the future, promise rejections that are not handled will terminate the Node.js process with a non-zero exit code.
```