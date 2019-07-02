# mongoose_inherit_to_diff_collection
[The model.discriminator() function](http://mongoosejs.com/docs/discriminators.html)
Discriminators are a schema inheritance mechanism. They enable you to have multiple models with overlapping schemas on top of the same underlying MongoDB collection.
鉴别器是一种schema继承模式，它们使您能够在同一底层MongoDB集合之上具有重叠模式的多个模型。

Suppose you wanted to track different types of events in a single collection. Every event will have a timestamp, but events that represent clicked links should have a URL. You can achieve this using the model.discriminator() function. This function takes 2 parameters, a model name and a discriminator schema. It returns a model whose schema is the union of the base schema and the discriminator schema.

假设你想跟踪不同类型的事件在用一个collection上。每个event有个时间戳，但是表达点击的事件有个url。你就通过 model.discriminator使用这个功能,2个参数，model名称和discriminator模式。返回一个模型，它的模式是基本模式和鉴别模式的联合体
# How to inherit a mongoose model and store it in a different collection
[How to inherit a mongoose model and store it in a different collection](http://stackoverflow.com/questions/34980337/how-to-inherit-a-mongoose-model-and-store-it-in-a-different-collection)

