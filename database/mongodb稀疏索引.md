# mongodb的稀疏索引/部分索引

特殊应用场景:动态表单使用mongdb存储，解决动态表单动态索引的效率问题。绝配！

**:(**:这个方法不行，mongodb本身有使用限制

- 单个collection的最大索引数为64个
- 一个database能创建的最大collection数也有限制（这个上限比较高，一般不会触发）

# 阅读材料：
- [Partial Indexes](https://docs.mongodb.com/manual/core/index-partial/)
- [Sparse Indexes](https://docs.mongodb.com/manual/core/index-sparse/)
  - [稀疏索引](http://www.mongoing.com/docs/core/index-sparse.html):中文社区的翻译文档，两年前翻译的文档
- [MongoDB索引原理](http://www.mongoing.com/archives/2797):作者为阿里巴巴技术专家，分布式、Redis、NoSQL。这篇文章原理介绍的很详细，值得细读
- 
