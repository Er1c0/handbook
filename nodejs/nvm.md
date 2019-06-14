# nvm常用命令
- nvm ls
- nvm use `版本号`
- nvm alias default `版本号` 

# 错误场景

## npm版本:nvm is not compatible with the npm config "prefix" option

```
(base) root@ops2:/home/gitlab-runner/jfjun-mg-base# . ~/.nvm/nvm.sh
nvm is not compatible with the npm config "prefix" option: currently set to "/root/.tnvm/versions/alinode/v3.11.0"
Run `npm config delete prefix` or `nvm use --delete-prefix v8.16.0 --silent` to unset it.
```
npm config delete prefix 命令解释：

- `npm config delete <key>` 是删除某个key
- `npm config ls -l` 是查看所有的key
- `config prefix` 参考：https://docs.npmjs.com/misc/config
    + The location to install global items. If set on the command line, then it forces non-global commands to run in the specified folder. 是一个位置
    