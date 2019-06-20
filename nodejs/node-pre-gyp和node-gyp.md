# node-pre-gyp
[官网](https://github.com/mapbox/node-pre-gyp)

node-pre-gyp是一个分发nodejs二进制程序包的工具，负责将预编译好的二进制程序直接下载到用户目录。它介于npm与node-gyp之间，只在相应平台二进制包不存在时才调用node-gyp编译。

node-pre-gyp存在的意义是什么呢？一些简单的nodejs C++扩展直接从源代码编译安装问题不大，但复杂的扩展编译环境难搭建、编译耗时长，因而从源代码安装非常麻烦。node-pre-gyp能够将预编译好的二进制包直接下载到用户目录，只在必要的时候才调用node-gyp从源代码编译，大大加快了nodejs C++扩展的安装速度。

node-pre-gyp需要开发者将各平台编译好的二进制包上传到网络上，并在package.json的binary字段指明二进制包的位置。然而，很多开发者选择将二进制包上传到aws上，导致国内无法正常下载（被墙）。幸好，可以在npm中设置--{module_name}_binary_host_mirror选项来指定二进制包的位置。例如，安装v8-profiler可以使用如下命令安装：
```
npm install v8-profiler --profiler_binary_host_mirror=https://npm.taobao.org/mirrors/node-inspector/
```


https://npm.taobao.org/mirrors/canvas-prebuilt

```
 npm install phantomjs --phantomjs_cdnurl=http://npm.taobao.org/mirrors/phantomjs
  npm install chromedriver --chromedriver_cdnurl=http://npm.taobao.org/mirrors/chromedriver
  npm install operadriver --operadriver_cdnurl=http://npm.taobao.org/mirrors/operadriver
```

## 问题 _binary_host_mirror 和_cdnurl 的区别

```
module.js:549
    throw err;
    ^

Error: Cannot find module '../build/Release/canvas.node'
    at Function.Module._resolveFilename (module.js:547:15)
    at Function.Module._load (module.js:474:25)
    at Module.require (module.js:596:17)
    at require (internal/module.js:11:18)
    at Object.<anonymous> (/root/jfjun-mg-ty-yansh3/node_modules/node-echarts/node_modules/canvas-prebuilt/canvas/lib/bindings.js:3:18)
    at Module._compile (module.js:652:30)
    at Object.Module._extensions..js (module.js:663:10)
    at Module.load (module.js:565:32)
    at tryModuleLoad (module.js:505:12)
    at Function.Module._load (module.js:497:3)
    at Module.require (module.js:596:17)
    at require (internal/module.js:11:18)
    at Object.<anonymous> (/root/jfjun-mg-ty-yansh3/node_modules/node-echarts/node_modules/canvas-prebuilt/canvas/lib/canvas.js:13:14)
    at Module._compile (module.js:652:30)
```

参见：canvas-prebuilt的package.json
```
  "binary": {
    "module_name": "canvas-prebuilt",
    "module_path": "canvas/build/Release",
    "host": "https://github.com/chearon/node-canvas-prebuilt/releases/download/",
    "remote_path": "v{version}"
  },
 "homepage": "https://github.com/chearon/node-canvas-prebuilt",
  "scripts": {
    "install": "node-pre-gyp install",
    "test": "echo No test needed"
  },
```

**NOTE:** the `canvas-prebuilt` package is deprecated. As of version 2,
[`canvas`](https://github.com/Automattic/node-canvas) itself bundles prebuilt
versions from this repo. Install by running
```
npm install --save canvas
```
…and use `canvas` as usual.

在canvas工程的package.json中可以看到
```
  "binary": {
    "module_name": "canvas",
    "module_path": "build/Release",
    "host": "https://github.com/node-gfx/node-canvas-prebuilt/releases/download/",
    "remote_path": "v{version}",
    "package_name": "{module_name}-v{version}-{node_abi}-{platform}-{libc}-{arch}.tar.gz"
  },
  "scripts": {
    "install": "node-pre-gyp install --fallback-to-build",
  }

```