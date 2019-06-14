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