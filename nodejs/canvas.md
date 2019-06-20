# 说明
包地址:https://www.npmjs.com/package/canvas
node-canvas is a Cairo-backed Canvas implementation for Node.js.
```
npm install canvas 
```
安装卡死了，可以使用源码安装

```
npm install --build-from-source -g canvas
```
可以使用 npm install --build-from-sourc 进行编译安装：但是依赖 cairo需要先安装
```
sudo apt-get install build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev
```

## 异常：node-pre-gyp: Permission denied
```
> canvas@2.5.0 install /root/.nvm/versions/node/v9.11.1/lib/node_modules/canvas
> node-pre-gyp install --fallback-to-build

sh: 1: node-pre-gyp: Permission denied
npm ERR! file sh
npm ERR! code ELIFECYCLE
npm ERR! errno ENOENT
npm ERR! syscall spawn
npm ERR! canvas@2.5.0 install: `node-pre-gyp install --fallback-to-build`
npm ERR! spawn ENOENT
npm ERR!
npm ERR! Failed at the canvas@2.5.0 install script.
npm ERR! This is probably not a problem with npm. There is likely additional logging output above.

npm ERR! A complete log of this run can be found in:
npm ERR!     /root/.npm/_logs/2019-06-19T14_34_59_468Z-debug.log
```

参考：https://github.com/jansmolders86/mediacenterjs/issues/191


## 问题：Using request for node-pre-gyp https download
并非卡死，而是确实在下载，只是时间比较长：

```
> canvas@2.5.0 install /root/jfjun-mg-test-chris/node_modules/canvas
> node-pre-gyp install --fallback-to-build

node-pre-gyp WARN Using request for node-pre-gyp https download
```
