# 几个Mongodb库比较

mongorito 基本处于停滞状态
mongoose 仍然活跃


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

