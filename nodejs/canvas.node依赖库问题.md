# 问题
启动node app.js时报问题"Incompatible library version"
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

```
Error: dlopen(/Users/lcz/git/jfjun_v5/jfjun-mg-base/node_modules/node --version/canvas/build/Release/canvas.node, 1): Library not loaded: @loader_path/libintl.8.dylib
  Referenced from: /Users/lcz/git/jfjun_v5/jfjun-mg-base/node_modules/canvas-prebuilt/canvas/build/Release/canvas.node
  Reason: image not found
```