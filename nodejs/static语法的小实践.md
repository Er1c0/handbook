# static静态方法
```
class User {
  constructor() {
    User.staticMethod();
  }

  static staticMethod() {
      console.log("called staticMethod!");
  }
}
let u = new User();
try{
    u.staticMethod();
}catch(e){
    console.log(e);//TypeError: u.staticMethod is not a function
}
User.staticMethod();
u.constructor.staticMethod();
```

static是为类定义静态方法的关键字。不能在类实例上调用静态方法。

参考：

-[js call static method from class](https://stackoverflow.com/questions/43614131/js-call-static-method-from-class/43614217)
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/static



