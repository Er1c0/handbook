# util_promisify_original 把callback转换为promise
- [Using filesystem in node.js with async / await](https://stackoverflow.com/questions/40593875/using-filesystem-in-node-js-with-async-await)
- [util_promisify_original](https://nodejs.org/dist/latest-v8.x/docs/api/util.html#util_util_promisify_original)
    + 采用常见的错误优先回调样式的函数(即把（err，val）=> 回调作为最后一个参数)，并返回返回promises的版本。
```
const util = require('util');
const fs = require('fs');
const stat = util.promisify(fs.stat);
stat('.').then((stats) => {
  // Do something with `stats`
}).catch((error) => {
  // Handle the error.
});

或者
async function callStat() {
  const stats = await stat('.');
  console.log(`This directory is owned by ${stats.uid}`);
}
```

# How to handle "unhandled Promise rejections" 如何处理未处理的Promise拒绝

```
async function one() {
    await Promise.reject('err');
}
async function one() {
  try {    
    await Promise.reject('err');
  } catch (e) {
     // e caught here
  }
}
```

```
function one() {
  return Promise.reject('error');
}

function two() {
  one().catch(e => {
     // error caught
  });
```
下面代码是不能catch异常的
```
function two() {
    try {
        one();
    } catch (e) {
        console.log(e);   // uncaught
    }
}
```
In both examples, function one returns a rejected Promise. When you call one() even with a try/catch block around it, you aren't capturing the error from the Promise; instead, the rejected promise is left unhandled. You must use .catch on the Promise or use await to capture the Error. If you use await in function two, it must also be an async function.

在上面两个示例中，函数`one`返回一个被拒绝的Promise。当你调用`one()`时，即使周围有一个try/catch块，你仍然不能捕获来自Promise的异常，被拒绝的Promise未得到处理。你必须在Promise上使用`.catch`或使用await来捕获`Error`.如果你使用`await`在函数二中，它必须也是异步函数

