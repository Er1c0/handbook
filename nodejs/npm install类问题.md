# 案例1：由于package-lock.json导致的install失败

```
>npm install jfjun-service-mg
npm ERR! code ETARGET
npm ERR! notarget No matching version found for jfjun-service-mg@0.0.32
npm ERR! notarget In most cases you or one of your dependencies are requesting
npm ERR! notarget a package version that doesn't exist.

npm ERR! A complete log of this run can be found in:
npm ERR!     /Users/lcz/.npm/_logs/2019-06-10T02_40_08_239Z-debug.log
```

错误日志如下,
```
6 http fetch GET 304 http://npm.lingxi.co:80/jfjun-service-mg 219ms (from cache)
7 silly pacote tag manifest for jfjun-service-mg@latest fetched in 261ms
8 silly install loadIdealTree
9 silly install cloneCurrentTreeToIdealTree
10 silly install loadShrinkwrap
11 silly registry:manifest no matching version for jfjun-service-mg@0.0.32 in the cache. Forcing revalidation
12 http fetch GET 304 http://npm.lingxi.co:80/jfjun-service-mg 44ms (from cache)
13 silly fetchPackageMetaData error for jfjun-service-mg@0.0.32 No matching version found for jfjun-service-mg@0.0.32
14 verbose type version
15 verbose stack jfjun-service-mg: No matching version found for jfjun-service-mg@0.0.32
```
根据错误可以看到，是对应的版本号找不到，为什么呢？发现有一个package-lock.json，里面已经写死了版本号,删除后该文件就可以重新安装了

# 案例2：node依赖库不一致问题 
错误如下：
```
internal/modules/cjs/loader.js:683
  return process.dlopen(module, path.toNamespacedPath(filename));
                 ^

Error: The module '/home/gitlab-runner/jfjun-mg-base/node_modules/node-echarts/node_modules/canvas-prebuilt/canvas/build/Release/canvas.node'
was compiled against a different Node.js version using
NODE_MODULE_VERSION 57. This version of Node.js requires
NODE_MODULE_VERSION 59. Please try re-compiling or re-installing
the module (for instance, using `npm rebuild` or `npm install`).
```
参考: [recompiling-node-dependencies-using-another-node-version](https://stackoverflow.com/questions/43158417/recompiling-node-dependencies-using-another-node-version)

最简单的方式：删除node_modules文件夹，然后重新安装


# 案例3：启动时报"Incompatible library version"

```
Reason: Incompatible library version: canvas.node requires version 52.0.0 or later, but libpng16.16.dylib provides version 47.0.0
```
解决方法
```
brew reinstall libpng
```

```
Error: dlopen(/Users/lcz/git/jfjun_v5/jfjun-mg-base/node_modules/canvas-prebuilt/canvas/build/Release/canvas.node, 1): Library not loaded: @loader_path/libpangocairo-1.0.0.dylib
  Referenced from: /Users/lcz/git/jfjun_v5/jfjun-mg-base/node_modules/canvas-prebuilt/canvas/build/Release/canvas.node
  Reason: Incompatible library version: canvas.node requires version 4201.0.0 or later, but libpangocairo-1.0.0.dylib provides version 4001.0.0
    at Object.Module._extensions..node (module.js:598:18)
    at Module.load (module.js:503:32)
```

解决方法:升级[pango](http://zoomadmin.com/HowToInstall/UbuntuPackage/libpangocairo-1.0-0)
```
/Users/lcz/>brew install pango
Error: pango 1.40.4 is already installed
To upgrade to 1.42.4_1, run `brew upgrade pango`.
/Users/lcz/>brew upgrade pango
==> Upgrading 1 outdated package:
pango 1.40.4 -> 1.42.4_1
==> Upgrading pango
==> Installing dependencies for pango: freetype, fontconfig, pcre, gdbm, openssl, readline, sqlite, xz, python, glib, pixman, cairo, fribidi, graphite2, icu4c and harfbuzz
==> Installing pango dependency: freetype
```
还报错
```
Error: dlopen(/Users/lcz/git/jfjun_v5/jfjun-mg-base/node_modules/node --version/canvas/build/Release/canvas.node, 1): Library not loaded: @loader_path/libintl.8.dylib
  Referenced from: /Users/lcz/git/jfjun_v5/jfjun-mg-base/node_modules/canvas-prebuilt/canvas/build/Release/canvas.node
  Reason: image not found
```


**上述问题最终通过把node切换到最新版本，然后重新安装"canvas-prebuilt"后接解决**
[How to resolve the canvas-prebuilt Node.js version incompatibility issue?](https://stackoverflow.com/questions/47301017/how-to-resolve-the-canvas-prebuilt-node-js-version-incompatibility-issue)

```
nvm use v8.14.0
node uninstall canvas-prebuilt
npm install canvas-prebuilt
```

## ubuntu上的处理方法
现象如下：
```
module.js:682
  return process.dlopen(module, path._makeLong(filename));
                 ^

Error: libpangocairo-1.0.so.0: cannot open shared object file: No such file or directory
    at Object.Module._extensions..node (module.js:682:18)
    at Module.load (module.js:566:32)
```

参考[How To Install "libpangocairo-1.0-0" Package on Ubuntu](http://zoomadmin.com/HowToInstall/UbuntuPackage/libpangocairo-1.0-0)
```
sudo apt-get install -y libpangocairo-1.0-0
```

```
  return process.dlopen(module, path._makeLong(filename));
                 ^

Error: libgif.so.4: cannot open shared object file: No such file or directory
    at Object.Module._extensions..node (module.js:682:18)
```
参考[How to install libgif-dev on Ubuntu 14.04 (Trusty Tahr)](https://www.howtoinstall.co/en/ubuntu/trusty/libgif-dev)
```
sudo apt-get install libgif-dev
```