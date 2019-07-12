# install类命令
原理：
一个package是:
- a) a folder containing a program described by a package.json file
- b) a gzipped tarball containing (a)
- c) a url that resolves to (b)
- d) a <name>@<version> that is published on the registry (see npm-registry) with (c)
- e) a <name>@<tag> (see npm-dist-tag) that points to (d)
- f) a <name> that has a “latest” tag satisfying (e)
- g) a <git remote url> that resolves to (a)
  - github
  - gitlab
  - bitbucket

总结起来：
- 文件形式
  - 支持文件夹，要包含package.json
  - 支持文件夹打包后的tar文件
- 文件来源
  - 本地:文件夹、tar文件
  - 远程：https、git
- 标签方式：
  - tar文件标签:<name>@<version>  <name>@<tag> <name>
  - git标签:#4727d357ea、#feature\/branch

在package.json中，可以写成下列方式:
**github URLs：**
```
{
  "name": "foo",
  "version": "0.0.0",
  "dependencies": {
    "express": "expressjs/express",
    "mocha": "mochajs/mocha#4727d357ea",
    "module": "user/repo#feature\/branch"
  }
}
```
如果不是github，但是git协议，可以写成下列方式:
格式为：
```
<protocol>://[<user>[:<password>]@]<hostname>[:<port>][:][/]<path>[#<commit-ish> | #semver:<semver>]
```
样例如下：
```
git+ssh://git@github.com:npm/cli.git#v1.0.27
git+ssh://git@github.com:npm/cli#semver:^5.0
git+https://isaacs@github.com/npm/cli.git
git://github.com/npm/cli.git#v1.0.27
```
比如我们公司的私有仓储用的gitlab，可以写成下列方式1：
其中后缀.git加不加都可以执行
```
npm install git+ssh://git@gitlab.lingxi.co/lcz/jfjun-model.git
```
方式2，必须支持https协议才行
```
npm install git+https://lcz:password@gitlab.lingxi.co/lcz/jfjun-model.git
```

