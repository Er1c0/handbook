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


## npm私有仓储
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

