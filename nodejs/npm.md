# npm

## 常用命令
- `npm config ls` 查看本地配置
- `npm config ls -l` 是查看所有的key
- `npm config delete <key>` 是删除某个key
    + `config prefix` 参考：https://docs.npmjs.com/misc/config
        * The location to install global items. If set on the command line, then it forces non-global commands to run in the specified folder. 是一个位置
- `npm set registry <url>` 设置仓储url,另外也可以通过`nrm use taobao`命令修改
    + 用`npm set `修改的参数，可以通过`npm config ls`检查是否生效
- `npm adduser --registry <url>` 
- `npm publish` 版本发布，默认是发布整个工程，也可以通过package.json中 files参数控制发布哪些文件？如`files:["src"]`

## npm私有仓储:verdaccio
[verdaccio](https://www.npmjs.com/package/verdaccio)

使用说明
```
npm install --global verdaccio #安装
verdaccio  # 启动服务
npm set registry http://localhost:4873/ # 设置配置
```

- **E2E testing**:Verdaccio has proved to be a lightweight registry that can be booted in a couple of seconds, fast enough for any CI.
- **Link multiple registries** 多个仓储
- **Override public packages** 覆盖公共报
- **Cache npmjs.org registry** 当公共仓储不可用时，做缓存
- **Use private packages** 使用私有包

## npm私有仓储：sinopia
[Sinopia 搭建npm 私有仓库](https://juejin.im/post/5c2712355188255e9b621c48)
sinopia是一个零配置的私有的带缓存功能的npm包管理工具，使用sinopia，你不用安装CouchDB或MYSQL之类的数据库，Sinopia有自己的迷你数据库，如果要下载的包不存在，它将自动去你配置的npm地址上去下载，而且硬盘中只缓存你现在过的包，以节省空间。

安装部署
```
npm i sinopia -g
sinopia
```
配置文件：vim /root/.config/sinopia/config.yaml
所有参数参见[conf/full.yaml](https://github.com/rlidwka/sinopia/blob/3f55fb4c0c6685e8b22796cce7b523bdbfb4019e/conf/full.yaml)

```
pm2 info sinopia
 Describing process with id 18 - name sinopia
┌───────────────────┬─────────────────────────────────────────────┐
│ status            │ online                                      │
│ name              │ sinopia                                     │
│ version           │ 0.33.2                                      │
│ restarts          │ 0                                           │
│ uptime            │ 9D                                          │
│ script path       │ /root/.nvm/versions/node/v8.2.1/bin/sinopia │
│ script args       │ N/A                                         │
│ error log path    │ /root/.pm2/logs/sinopia-error.log           │
│ out log path      │ /root/.pm2/logs/sinopia-out.log             │
│ pid path          │ /root/.pm2/pids/sinopia-18.pid              │
│ interpreter       │ node                                        │
│ interpreter args  │ N/A                                         │
│ script id         │ 18                                          │
│ exec cwd          │ /root                                       │
│ exec mode         │ fork_mode                                   │
│ node.js version   │ 8.2.1                                       │
│ node env          │ N/A                                         │
│ watch & reload    │ ✘                                           │
│ unstable restarts │ 0                                           │
│ created at        │ 2019-06-07T15:51:50.445Z                    │
└───────────────────┴─────────────────────────────────────────────┘
 Revision control metadata
┌──────────────────┬──────────────────────────────────────────┐
│ revision control │ git                                      │
│ remote url       │ https://github.com/creationix/nvm.git    │
│ repository root  │ /root/.nvm                               │
│ last update      │ 2019-06-07T15:51:50.539Z                 │
│ revision         │ 0a95e77000515c1156be593642dd4e452f2f098e │
│ comment          │ v0.33.2                                  │
│ branch           │ HEAD                                     │
└──────────────────┴──────────────────────────────────────────┘
 Code metrics value
┌────────────────────────┬──────┐
│ Active requests        │ 0    │
│ Active handles         │ 4    │
│ Event Loop Latency     │ 0.49 │
│ Event Loop Latency p95 │ 1.29 │
└────────────────────────┴──────┘
 Add your own code metrics: http://bit.ly/code-metrics
 Use `pm2 logs sinopia [--lines 1000]` to display logs
 Use `pm2 env 18` to display environement variables
 Use `pm2 monit` to monitor CPU and Memory usage sinopia
```


## 问题:publish Failed
错误日志：
```
npm ERR! publish Failed PUT 413
npm ERR! code E413
npm ERR! 413 Payload Too Large
```
参考：[unable to publish to sinopia 413](https://github.com/rlidwka/sinopia/issues/83)

所有参数参见[conf/full.yaml](https://github.com/rlidwka/sinopia/blob/3f55fb4c0c6685e8b22796cce7b523bdbfb4019e/conf/full.yaml)
在配置文件(/root/.config/sinopia/config.yaml)中增加max_body_size即可解决
```
# maximum size of uploaded json document
# increase it if you have "request entity too large" errors
max_body_size: 30mb
listen: 0.0.0.0:4884
```


# 问题:publish Failed PUT 413:request entity too large
```
npm notice === Tarball Details ===
npm notice name:          jfjun-mg-base
npm notice version:       0.3.150
npm notice package size:  9.6 MB
npm notice unpacked size: 18.7 MB
npm notice shasum:        5c80835aadd732097723119839d27cacfb97d834
npm notice integrity:     sha512-AAdDssXY0b3GR[...]TzjjpH8D2V/ww==
npm notice total files:   102
npm notice
npm ERR! publish Failed PUT 413
npm ERR! code E413
npm ERR! request entity too large : jfjun-mg-base

npm ERR! A complete log of this run can be found in:
```
通过修改nginx参数：
```
server {
    listen 80;
    client_max_body_size 1024m;
}
```

