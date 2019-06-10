# 案例：npm install失败

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
