# 三个点three dots(...)使用说明
## 数组或对象扩展运算符

假如有下面对象:
```
const bob = {
    name: 'bob Oprea',
    occupation: 'Software developer',
    age: 31,
    website: 'https://bob.rocks'
};
```
如果你想创建一个新的对象，使用不同的name和website，但是相同的occupation和age,你就可以使用下面语法:
```
const bill = {
    ...bob,
    name: 'Bill Gates',
    website: 'https://microsoft.com'
};
```
你仅指定所需的属性并使用扩展运算符就能完成这个操作。这种扩展操作可以视作，逐个提取所有单个属性并将它们传递给新对象。

数组扩展样例如下:
```
const numbers1 = [1, 2, 3, 4, 5];
const numbers2 = [ ...numbers1, 1, 2, 6,7,8]; // this will be [1, 2, 3, 4, 5, 1, 2, 6, 7, 8]
```

## 剩余参数，Rest运算符
当使用在函数签名中时，称为rest运算符。可以可以完全替换参数，也可以与函数的其它参数一起使用。

rest operator使开发人员能够创建可以获取无限数量参数的函数，称为可变函数(variadic function)
```
function sum(...numbers) {
    return numbers.reduce((accumulator, current) => {
        return accumulator += current
    });
};
sum(1, 2) // 3
sum(1, 2, 3, 4, 5) // 15
```
最简单的解释就是，rest operator接收函数的参数，然后转存到一个真实的数组中，这个数组你稍后就会用到：
你可能会争辩下面连个替代方法：
  
- 直接让用户传递一个数组。这个技术是可行的，但是非常的不UX。因为用户期望通过简单数据调用sum函数，而不是给一个数字列表
- 也可以使用arguments，但是arguments只是个像数组的对象(只有length属性和索引元素)，并不是一个真正的数组。数组的一些方法比如reduce等，是不能直接使用的。

# 参考:
- [What do the three dots (…) mean in JavaScript?](https://medium.com/@oprearocks/what-do-the-three-dots-mean-in-javascript-bc5749439c9a)
- [Arguments 对象](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Functions/arguments)
- [展开语法(Spread syntax)](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/Spread_syntax)