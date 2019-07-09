[TOC]
# 安装部署
## 官网操作和主要命令
比较人性化，非常简单，按着官网操作即可
- https://about.gitlab.com/downloads/

sudo gitlab-ctl restart #重启
sudo gitlab-ctl reconfigure   #重新初始化配置
gitlab-ctl  tail  #查看日志
### 手工安装
可以直接下载安装包(只能翻墙下载) https://packages.gitlab.com/gitlab/gitlab-ce
ubuntu的安装命令（后面是我下载的包名）： sudo dpkg -i gitlab-ce_8.9.6-ce.0_amd64.deb
```
Ubuntu软件包格式为deb，安装方法如下：

    sudo  dpkg  -i  package.deb

dpkg的详细使用方法，网上有很多，下面简单列了几个：

dpkg -i package.deb 安装包
dpkg -r package 删除包
dpkg -P package 删除包（包括配置文件）
dpkg -L package 列出与该包关联的文件
dpkg -l package 显示该包的版本
dpkg –unpack package.deb  解开 deb 包的内容
dpkg -S keyword 搜索所属的包内容
dpkg -l 列出当前已安装的包
dpkg -c package.deb 列出 deb 包的内容
dpkg –configure package 配置包
 

（根据Ubuntu中文论坛上介绍，使用apt-get方法安装的软件，所有下载的deb包都缓存到了/var/cache/apt/archives目录下了，所以可以把常用的deb包备份出来，甚至做成ISO工具包、刻盘，以后安装Ubuntu时就可以在没有网络环境的情况下进行了）
```
## 升级
查看当前版本：http://自己的域名/help
查看：https://about.gitlab.com/update/

由于网络原因，只能通过手工安装，先翻墙下载，下载地址
https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/doc/update/README.md#upgrading-from-a-non-omnibus-installation-to-an-omnibus-installation

上传到服务器后执行
```
root@AY120810031731bef8123:~#  dpkg -i gitlab-ce_8.13.8-ce.0_amd64.deb
(正在读取数据库 ... 系统当前共安装有 139867 个文件和目录。)
正预备替换 gitlab-ce 8.9.6-ce.0 (使用 gitlab-ce_8.13.8-ce.0_amd64.deb) ...
gitlab preinstall: Automatically backing up only the GitLab SQL database (excluding everything else!)
Dumping database ...
Dumping PostgreSQL database gitlabhq_production ... [DONE]
done
Dumping repositories ...
[SKIPPED]
Dumping uploads ...
[SKIPPED]
Dumping builds ...
[SKIPPED]
Dumping artifacts ...
[SKIPPED]
Dumping lfs objects ...
[SKIPPED]
Dumping container registry images ...
[DISABLED]
Creating backup archive: 1481186831_gitlab_backup.tar ... done
Uploading backup archive to remote storage  ... skipped
Deleting tmp directories ... done
done
Deleting old backups ... skipping
正在解压缩将用于更替的包文件 gitlab-ce ...
```


## 查看默认配置
cat /opt/gitlab/embedded/cookbooks/gitlab/attributes/default.rb|grep port  #查看各端口的配置
或者(一般修改这个文件)  /etc/gitlab/gitlab.rb 

## 运行状态检查
### 启停过程
```
[root@ip-172-31-28-245 attributes]# sudo gitlab-ctl  stop
ok: down: logrotate: 0s, normally up
ok: down: nginx: 1s, normally up
ok: down: postgresql: 0s, normally up
ok: down: redis: 0s, normally up
ok: down: sidekiq: 0s, normally up
ok: down: unicorn: 0s, normally up
[root@ip-172-31-28-245 attributes]# sudo gitlab-ctl  start
ok: run: logrotate: (pid 18256) 0s
ok: run: nginx: (pid 18258) 0s
ok: run: postgresql: (pid 18261) 0s
ok: run: redis: (pid 18263) 0s
ok: run: sidekiq: (pid 18265) 0s
ok: run: unicorn: (pid 18267) 0s
```
### 端口占用情况
```
[root@ip-172-31-28-245 attributes]#  netstat -anp|grep LISTEN
tcp        0      0 0.0.0.0:80                  0.0.0.0:*                   LISTEN      18044/nginx         
tcp        0      0 127.0.0.1:8080              0.0.0.0:*                   LISTEN      18025/unicorn maste 
unix  2      [ ACC ]     STREAM     LISTENING     13400  18025/unicorn maste /var/opt/gitlab/gitlab-rails/sockets/gitlab.socket
unix  2      [ ACC ]     STREAM     LISTENING     12594  2185/redis-server 1 /var/opt/gitlab/redis/redis.socket
unix  2      [ ACC ]     STREAM     LISTENING     12585  2183/postgres       /tmp/.s.PGSQL.5432

```

# 概念与原理
## git、github、gitlab
参考：[git github gitlab之间是什么关系](http://www.phperz.com/article/14/0705/3314.html)
Git - 版本控制工具

- 开源的分布式版本控制和源代码管理系统
- Linus Torvalds 开发
- 点到点，而不是集中式

Github-一个网站，提供给用户空间创建git仓储，保存用户的一些数据文档或者代码等

- 目前已经成为开源代码库，成为了管理软件开发以及发现已有代码的首选方法
- 独特卖点在于从另外一个项目进行分支的简易性，“fork”-“pull request”

GitLab - 基于Git的项目管理软件

- Github的山塞版，但是开源，可以私有部署

## 功能
官方文档简介：

- Manage **git repositories** with fine grained **access controls** that keep your code secure. 
- Perform **code reviews** and enhance collaboration with **merge requests**. 
- Each project can also have an **issue tracker** and a **wiki**.

[GitLab Documentation](http://doc.gitlab.com/ce/):社区版本的官方文档

### 系统管理
Admin用户--》admin area--》可以分别对Projects、Users、Groups进行管理

- Overview 静态统计、project\用户展示
- Projects 特性开关管理、重命名、空间迁移、归档、删除等
- Users 创建、删除、重置密码、block等
- Groups 创建、删除、重命名
- deploy keys  配置key后可以SSH自动登录  
- Logs 可以在线观看后台日志
- Messages 可以在停机维护前广播消息，适合很多人的团队，对小团队可以忽略
- hooks 当创建用户或工程等事件发送时，发送http post到指定的URL
- Background Jobs 后台任务处理，用[sidekiq](http://sidekiq.org/)做异步任务处理
- Applications  待研究System OAuth applications
- Service templates  待研究

### 工程视图
- project 当前的活动事件，可以进入project编辑页面，进行project参数设置
- Files 文件列表
- Commits 可以显示提交日志，比较、分支、tag,如果对git命令熟悉，可以忽略这个视图
- NetWork 图形化方式显示代码提交情况
- Graphs 可以量化每个人的代码提交次数
- MileStones 可以自定义里程碑，可以方便得看里程碑的进度完成情况
    - 可以在里程碑里拖拽issues,参见[官网](https://about.gitlab.com/2014/06/22/gitlab-7-dot-0-released/)
- Issues 问题管理，比较便捷；提交代码是可以关联issue，方便把问题与代码关联起来
    - 支持直接拖拽图片，参见[官网](https://about.gitlab.com/2014/06/22/gitlab-7-dot-0-released/)
    - [git commit -m "Awesome commit message (Fix #20, Fixes #21 and Closes #22)"](http://doc.gitlab.com/ce/customization/issue_closing.html)
- MergeRequest  合并分支，小团队可以忽略
- Members 成员管理
- Labels label管理
- wiki  (标题不支持中文)

### Hooks
有系统级的，也有project级
通过 Web hook可以达到网站自动化部署的目的
[Git系列-WebHook-简单自动部署](http://blog.ikaros.club/2014/10/24/gitlab-webhook/)
[node-gitlab-hook](https://github.com/rolfn/node-gitlab-hook):github上的开源项目，还增加了逆向代理转发功能

参考文档[gitlab简介、搭建与维护](http://www.tuicool.com/articles/bYbi2mJ)

## 架构
![gitlab架构图](http://img0.tuicool.com/F3AjA3V.png)
### 组件
- 前端：Nginx，用于页面及Git tool走http或https协议
- 后端：Gitlab服务，采用Ruby on Rails框架，通过unicorn实现后台服务及多进程
- SSHD：开启sshd服务，用于用户上传ssh key进行版本克隆及上传。注：用户上传的ssh key是保存到git账户中
- 数据库：目前仅支持MySQL和PostgreSQL
- Redis：用于存储用户session和任务，任务包括新建仓库、发送邮件等等
- Sidekiq：Rails框架自带的，订阅redis中的任务并执行

### 官方架构文档
http://doc.gitlab.com/ce/development/architecture.html

### 关键信息

**上传附件和图片的保存目录** 
/opt/gitlab/embedded/service/gitlab-rails/public/uploads

**主程序安装目录**
/opt/gitlab/embedded/bin是执行文件目录，如：
/opt/gitlab/embedded/bin/postgres -D /var/opt/gitlab/postgresql/data
/opt/gitlab/embedded/bin/redis-server 127.0.0.1:0
nginx: master process /opt/gitlab/embedded/sbin/nginx -p /var/opt/gitlab/nginx

**资源目录**
/var/opt/gitlab    
    ├── backups
    ├── bootstrapped
    ├── git-data
    ├── gitlab-rails
    ├── gitlab-shell
    ├── logrotate
    ├── nginx
    ├── postgresql
    └── redis

cat /etc/passwd 
```bash
gitlab-www:x:498:499::/var/opt/gitlab/nginx:/bin/false
git:x:497:498::/var/opt/gitlab:/bin/sh
gitlab-redis:x:496:497::/var/opt/gitlab/redis:/bin/nologin
gitlab-psql:x:495:496::/var/opt/gitlab/postgresql:/bin/sh
```

![gitlab_diagram_overview](http://doc.gitlab.com/ce/development/gitlab_diagram_overview.png)

麻雀虽小，五脏俱全，这是个大型网站的典型结构，[参见这篇文章的p17](http://www.slideshare.net/kigster/12step-program-for-scaling-web-applications-on-postgresql)

### 进程体系
ps -ef|grep 547|grep -v grep| awk '{print $2}'| (while read arg; do  ps -ef|grep -v grep |grep  $arg; done)
其中的547是gitlab-ctl  start启动程序的进程号

启动过程(sudo gitlab-ctl start)：
(Root用户)runsvdir -P /opt/gitlab/service log

  + runsv redis
    * svlogd -tt /var/log/gitlab/redis
    * (**gitlab-redis用户**)/opt/gitlab/embedded/bin/redis-server 127.0.0.1:0
  + runsv sidekiq
    * svlogd -tt /var/log/gitlab/sidekiq
    * (**git用户**)sidekiq 3.3.0 gitlab-rails [0 of 25 busy]
  + runsv logrotate
    * svlogd -tt /var/log/gitlab/logrotate
    * /bin/sh ./run
  + runsv unicorn
    * svlogd -tt /var/log/gitlab/unicorn
    * /bin/sh ./run(非常驻，设置变量如rails_app=gitlab-rails)
    * /bin/bash /opt/gitlab/embedded/bin/gitlab-unicorn-wrapper
      - (**git用户**,但父进程是PID 1)unicorn master -D -E production -c /var/opt/gitlab/gitlab-rails/etc/unicorn.rb /opt/gitlab/embedded/service/gitlab-rails/config.ru
        + unicorn worker[0] -D -E production -c /var/opt/gitlab/gitlab-rails/etc/unicorn.rb /opt/gitlab/embedded/service/gitlab-rails/config.ru
        + unicorn worker[1] -D -E production -c /var/opt/gitlab/gitlab-rails/etc/unicorn.rb /opt/gitlab/embedded/service/gitlab-rails/config.ru
  + runsv postgresql
    * svlogd -tt /var/log/gitlab/postgresql
    * (**gitlab-psql用户**)/opt/gitlab/embedded/bin/postgres -D /var/opt/gitlab/postgresql/data
  + runsv nginx
    * svlogd -tt /var/log/gitlab/postgresql
    * nginx: master process /opt/gitlab/embedded/sbin/nginx -p /var/opt/gitlab/nginx
      - (**gitlab-www用户**)nginx: worker process 

### 日志体系
[Log system](http://doc.gitlab.com/ce/logs/logs.html)

|文件名|路径|说明|
|---|----|---|
|production.log| /var/log/gitlab/gitlab-rails/production.log|contains information about all performed requests|
|application.log| /var/log/gitlab/gitlab-rails/application.log| helps you discover events happening in your instance such as user creation, project removing and so on|
|githost.log| /var/log/gitlab/gitlab-rails/githost.log |contains all failed requests from GitLab to git repository. In majority of cases this file will be useful for developers only.|
|satellites.log| /var/log/gitlab/gitlab-rails/satellites.log|write actions to git repository|
|sidekiq.log|/var/log/gitlab/gitlab-rails/sidekiq.log |background jobs for processing tasks |
|gitlab-shell.log| /var/log/gitlab/gitlab-shell/gitlab-shell|ssh access to git repositories|
|unicorn_stderr.log|/var/log/gitlab/unicorn/unicorn_stderr.log |unicorn processes|

### 其它培训教程
[Gitlab使用流程](http://wenku.baidu.com/link?url=n7rQLoo7d2Ztkae8IWjm-T9XUwxJD4snOYfVrAqapE5Q_GGQRkzEAvDsZEzzxv8pCcmyLTRsGXFOMV8Cj5O_-plr4lkSbZA_LUxMo8RMN-a):中文版，截图比较多
[Introduction to Gitlab](http://www.slideshare.net/roidelapluie/gitlab-intro):超简洁
[GitFlow, SourceTree and GitLab](http://www.slideshare.net/mailtoshinu/gitflow-sourcetree-and-gitlab?related=1):GitFlow小团队较少用，SourceTree是图形工具，目前用的也较少；GitLab部分介绍还可以
[GitLab—the new workbench项目协作平台](http://www.slideshare.net/tblanlan/gitlabthe-new-workbench):好像是淘宝的人写的，版本比较老

# psql

启动命令
```
/opt/gitlab/embedded/bin/postgres -D /var/opt/gitlab/postgresql/data
#-D DATADIR         database directory 
```
PostgreSQL有两个配置文件修改的情况比较多，第一是认证文件 pg_hba.conf，另一个是配置文件 postgresql.conf
pg_hba.conf是客户端认证配置文件，定义如何认证客户端

[PostgreSQL pg_hba.conf 文件简析](http://www.cnblogs.com/hiloves/archive/2011/08/20/2147043.html)
```
# If you want to allow non-local connections, you need to add more
# "host" records. In that case you will also need to make PostgreSQL listen
# on a non-local interface via the listen_addresses configuration parameter,
# or via the -i or -h command line switches.
#


# TYPE  DATABASE    USER        CIDR-ADDRESS          METHOD

# "local" is for Unix domain socket connections only
local   all         all                               peer map=gitlab
```

关于 method peer，参见官网[Peer Authentication](http://www.postgresql.org/docs/9.1/static/auth-methods.html#AUTH-PEER)
The peer authentication method works by obtaining the client's operating system user name from the kernel and using it as the allowed database user name (with optional user name mapping). This method is only supported on local connections.

map=gitlab的定义在pg_ident.conf文件
```
# This file is read on server startup and when the postmaster receives
# a SIGHUP signal.  If you edit the file on a running system, you have
# to SIGHUP the postmaster for the changes to take effect.  You can
# use "pg_ctl reload" to do that.

# MAPNAME       SYSTEM-USERNAME         PG-USERNAME
gitlab  git  gitlab
gitlab  gitlab-ci  gitlab_ci
# Default to a 1-1 mapping between system usernames and Postgres usernames
gitlab  /^(.*)$  \1
```


## 登录
```
su - gitlab-psql
/opt/gitlab/embedded/bin/psql gitlabhq_production
```


database的配置文件在/opt/gitlab/embedded/service/gitlab-rails/config/database.yml
```
cat /opt/gitlab/embedded/service/gitlab-rails/config/database.yml
# This file is managed by gitlab-ctl. Manual changes will be
# erased! To change the contents below, edit /etc/gitlab/gitlab.rb
# and run `sudo gitlab-ctl reconfigure`.

production:
  adapter: postgresql
  encoding: unicode
  database: gitlabhq_production
  pool: 10
  username: 'gitlab'
  password: 
  host: 
  port: 5432
  socket: 
  sslmode: 
  sslrootcert: 
```
### 字符集
```
show client_encoding;
show server_encoding;
set client_encoding to 'GBK';
```
## 控制台命令
- \password命令（设置密码）
- \q命令（退出）
- \h：查看SQL命令的解释，比如\h select。
- \?：查看psql命令列表。
- \l：列出所有数据库。
- \c [database_name]：连接其他数据库。
- \d：列出当前数据库的所有表格。
- \d [table_name]：列出某一张表格的结构。
- \du：列出所有用户。
- \e：打开文本编辑器。
- \conninfo：列出当前数据库和连接的信息。

```
gitlabhq_production-# \l
                                         List of databases
        Name         |    Owner    | Encoding | Collate |  Ctype  |        Access privileges        
---------------------+-------------+----------+---------+---------+---------------------------------
 gitlabhq_production | gitlab      | UTF8     | C.UTF-8 | C.UTF-8 | 
 postgres            | gitlab-psql | UTF8     | C.UTF-8 | C.UTF-8 | 
 template0           | gitlab-psql | UTF8     | C.UTF-8 | C.UTF-8 | =c/"gitlab-psql"               +
                     |             |          |         |         | "gitlab-psql"=CTc/"gitlab-psql"
 template1           | gitlab-psql | UTF8     | C.UTF-8 | C.UTF-8 | =c/"gitlab-psql"               +
                     |             |          |         |         | "gitlab-psql"=CTc/"gitlab-psql"
(4 rows)

gitlabhq_production-# \du
                              List of roles
  Role name  |                   Attributes                   | Member of 
-------------+------------------------------------------------+-----------
 gitlab      |                                                | {}
 gitlab-psql | Superuser, Create role, Create DB, Replication | {}

```

## 业务相关命令
```sql
select id,title,project_id,author_id,created_at,state,milestone_id,iid from issues order by project_id,iid;
select id,name,path,description from projects;
select id,name from users;

select t1.id,t1.title,t2.name project,t3.name as author,t4.name as assignee,t1.created_at,t1.state,t1.milestone_id,t1.iid from issues t1,projects t2,users t3 where t1.project_id= t2.id and t1.author_id=t3.id  order by t1.project_id,t1.iid;--显示问题列表

select t1.id,t1.title,t2.name project,t3.name as author,t4.name as assignee,t1.created_at,t1.state,t5.title as milestone,t1.iid from issues t1
left join projects t2 on t1.project_id= t2.id 
left join users t3 on t1.author_id=t3.id
left join users t4 on t1.assignee_id = t4.id
left join milestones t5 on t1.milestone_id = t5.id
where t2.name='jfjun-fp'
order by t1.project_id,t1.iid; --因为有空字段的存在，不能使用内连接，必须要左链接，

select * from labels;--issue的标签定义
select * from label_link;--issue的标签

--合并显示某个issue的标签,参考http://stackoverflow.com/questions/43870/how-to-concatenate-strings-of-a-string-field-in-a-postgresql-group-by-query

select id,array_to_string(array_agg(tag), '#') as tag from (select t2.title tag,t3.title,t3.id from 
label_links t1,
labels t2 ,
issues t3 
where t1.label_id=t2.id and 
t1.target_type='Issue' 
and t1.target_id = t3.id
and t3.project_id = 12) tt1 GROUP BY id;


--把issue和标签合并在一起
select ttt1.* ,ttt2.tag from (select t1.id,t1.title,t2.name project,t3.name as author,t4.name as assignee,t1.created_at,t1.state,t5.title as milestone,t1.iid from issues t1
left join projects t2 on t1.project_id= t2.id 
left join users t3 on t1.author_id=t3.id
left join users t4 on t1.assignee_id = t4.id
left join milestones t5 on t1.milestone_id = t5.id
where t2.name='jfjun-fp'
order by t1.project_id,t1.iid) ttt1,
(select id,array_to_string(array_agg(tag), '#') as tag from (select t2.title tag,t3.title,t3.id from 
label_links t1,
labels t2 ,
issues t3 
where t1.label_id=t2.id and 
t1.target_type='Issue' 
and t1.target_id = t3.id
and t3.project_id = 12) tt1 GROUP BY id ) ttt2
where ttt1.id = ttt2.id ;

```


```
select count(1) from  application_settings ;
select count(1) from  broadcast_messages   ;
select count(1) from  deploy_keys_projects ;
select count(1) from  emails               ;
select count(1) from  events               ;
select count(1) from  forked_project_links ;
select count(1) from  identities           ;
select count(1) from  issues               ;
select count(1) from  keys                 ;
select count(1) from  label_links          ;
select count(1) from  labels               ;
select count(1) from  members              ;
select count(1) from  merge_request_diffs  ;
select count(1) from  merge_requests       ;
select count(1) from  milestones           ;
select count(1) from  namespaces           ;
select count(1) from  notes                ;
select count(1) from  oauth_access_grants  ;
select count(1) from  oauth_access_tokens  ;
select count(1) from  oauth_applications   ;
select count(1) from  project_import_data  ;
select count(1) from  projects             ;
select count(1) from  protected_branches   ;
select count(1) from  schema_migrations    ;--
select count(1) from  services             ;
select count(1) from  snippets             ;
select count(1) from  subscriptions        ;
select count(1) from  taggings             ;
select count(1) from  tags                 ;
select count(1) from  users                ;
select count(1) from  users_star_projects  ;
select count(1) from  web_hooks            ;


select * from  application_settings limit 1;
select * from  broadcast_messages   limit 1;
select * from  deploy_keys_projects limit 1;
select * from  emails               limit 1;
select * from  events               limit 1;
select * from  forked_project_links limit 1;
select * from  identities           limit 1;
select * from  issues               limit 1;
select * from  keys                 limit 1;
select * from  label_links          limit 1;
select * from  labels               limit 1;
select * from  members              limit 1;
select * from  merge_request_diffs  limit 1;
select * from  merge_requests       limit 1;
select * from  milestones           limit 1;
select * from  namespaces           limit 1;
select * from  notes                limit 1;
select * from  oauth_access_grants  limit 1;
select * from  oauth_access_tokens  limit 1;
select * from  oauth_applications   limit 1;
select * from  project_import_data  limit 1;
select * from  projects             limit 1;
select * from  protected_branches   limit 1;
select * from  schema_migrations    limit 1;
select * from  services             limit 1;
select * from  snippets             limit 1;
select * from  subscriptions        limit 1;
select * from  taggings             limit 1;
select * from  tags                 limit 1;
select * from  users                limit 1;
select * from  users_star_projects  limit 1;
select * from  web_hooks            limit 1;
```

[官网Database settings](https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/doc/settings/database.md) 仅供参考
### 把A工程的issue迁移到B工程 
```sql
--找工程id
select * from projects;
--查找工程的id
select id, title ,project_id,author_id,iid from issues where project_id=2;  order by iid;
--把A工程的issue迁移到B工程 
update issues set project_id=12,iid=18 where project_id=2 and iid=96;
```

### 把A工程的标签，迁移到B工程
```sql
insert into labels (title,color,project_id,created_at,updated_at)
(SELECT title,color,project_id,created_at,updated_at
    FROM labels  
   WHERE project_id =2) ;--从某个工程迁移出来
update labels set project_id=12 where id >=37;    
```
# 高级应用：API

curl --header "PRIVATE-TOKEN: QVy1PB7sTxfy4pqfZM1U" "http://example.com/api/v3/projects"
[官方GitLab API](http://doc.gitlab.com/ce/api/README.html)
[Gitlab API: How to generate the private token](http://stackoverflow.com/questions/23640961/gitlab-api-how-to-generate-the-private-token)

curl http://gitlab.lingxi.co/api/v3/session --data 'login=lichangzhen&password=xxx'

{
  "name": "李昌振",
  "username": "lichangzhen",
  "id": 4,
  "state": "active",
  "avatar_url": "http://gitlab.lingxi.co/uploads/user/avatar/4/%E6%9D%8E%E6%98%8C%E6%8C%AF-%E5%B7%A5%E5%8D%A1%E7%9B%B8%E7%89%87_min.jpg",
  "created_at": "2015-07-14T06:11:24.120Z",
  "is_admin": true,
  "bio": null,
  "skype": "",
  "linkedin": "",
  "twitter": "",
  "website_url": "",
  "email": "changzhen.li@lingxi.co",
  "theme_id": 2,
  "color_scheme_id": 1,
  "projects_limit": 20,
  "current_sign_in_at": "2015-07-24T12:35:20.894Z",
  "identities": [],
  "can_create_group": true,
  "can_create_project": true,
  "private_token": "2Tm3Yb8qQ8irejJvCteZ"
}
curl --header "PRIVATE-TOKEN: 2Tm3Yb8qQ8irejJvCteZ" "http://gitlab.lingxi.co//api/v3/projects/1/repository/commits?"


# git
以git用户登录，如何"劫持"ssh上来得git命令
 /var/opt/gitlab/.ssh/authorized_keys
git clone git@host:repo.git==>ssh git@host 'git-upload-pack repo.git'
git push==>ssh git@host 'git-receive-pack repo.git'

[GitLab Shell](https://gitlab.com/gitlab-org/gitlab-shell/blob/master/README.md)


监控ssh和gitlab日志
```
#sudo /usr/sbin/sshd -ddd
debug1: trying public key file /var/opt/gitlab/.ssh/authorized_keys
debug2: user_key_allowed: check options: 'command="/opt/gitlab/embedded/service/gitlab-shell/bin/gitlab-shell key-1",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-rsa AAAAB3Nz.......
```

```
#cat /var/opt/gitlab/.ssh/authorized_keys
command="/opt/gitlab/embedded/service/gitlab-shell/bin/gitlab-shell key-1",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1C3D0D/xwGqk5AhIL/MSqU2PTdOjm/mQ78yIlO/UmtY7SPgDOjBG5dDHJj5QAPEc5RPaR73VS3LvRb4mLvIzF3jJxcmUYwLg1espGJQTwNGxFOkx21rizdJ1THboRUfJzcZHWPoDz4DhgR4MUcQ8HBXk8vswocSEznMV8RTaMNlUhCOKzFV1GVpEDmqEfs2ufmA8oq4yxwGixdT7vXVRrZUbi738TN/4BtgnesJ7U/tkfT6ZIBAllH4ES0X2ADUThlF/XGg8I8RS3QkI5ryQyiRNkgm2iwxxmW7rP6ed4gJp754IizaBsdd3D3tPpaMRN/wgID/Q3lS8un76AM9TR lcz@lichangzhendeMacBook-Pro.local
```

如果gitlab服务正常
```
==> /var/log/gitlab/gitlab-shell/gitlab-shell.log <==
I, [2015-07-24T01:53:48.252534 #31063]  INFO -- : gitlab-shell: executing git command <git-upload-pack /var/opt/gitlab/git-data/repositories/root/test.git> for user with key key-1.
I, [2015-07-24T02:07:42.170402 #32046]  INFO -- : gitlab-shell: executing git command <git-receive-pack /var/opt/gitlab/git-data/repositories/root/test.git> for user with key key-1.
```

如果gitlab服务异常
```
==> /var/log/gitlab/gitlab-shell/gitlab-shell.log <==
W, [2015-07-24T01:49:54.719962 #30920]  WARN -- : Failed to connect to internal API <GET http://127.0.0.1:8080/api/v3/internal/discover?key_id=1>: #<Errno::ECONNREFUSED: Connection refused - connect(2) for "127.0.0.1" port 8080>
```

更为详细的日志
```
==> /var/log/gitlab/gitlab-rails/production.log <==
Started POST "/api/v3/internal/allowed" for 127.0.0.1 at 2015-07-24 02:07:42 +0000

==> /var/log/gitlab/gitlab-shell/gitlab-shell.log <==
I, [2015-07-24T02:07:42.170402 #32046]  INFO -- : gitlab-shell: executing git command <git-receive-pack /var/opt/gitlab/git-data/repositories/root/test.git> for user with key key-1.

==> /var/log/gitlab/gitlab-rails/production.log <==
Started POST "/api/v3/internal/allowed" for 127.0.0.1 at 2015-07-24 02:07:42 +0000

==> /var/log/gitlab/sidekiq/current <==
2015-07-24_02:07:42.58254 2015-07-24T02:07:42.582Z 30942 TID-bwa8o PostReceive JID- INFO: start

==> /var/log/gitlab/gitlab-rails/production.log <==
Started GET "/api/v3/internal/broadcast_message" for 127.0.0.1 at 2015-07-24 02:07:42 +0000

==> /var/log/gitlab/sidekiq/current <==
2015-07-24_02:07:42.66394 2015-07-24T02:07:42.663Z 30942 TID-bwa8o PostReceive JID- INFO: done: 0.081 sec
```


参考
[Gitolite](http://www.slideshare.net/chenryn/add-mailinglist-command-to-gitolite): 讲解了ssh与git的原理

# Redis
[在Ubuntu中安装Redis](http://blog.fens.me/linux-redis-install/):介绍了基本使用
[超强、超详细Redis数据库入门教程](http://www.jb51.net/article/56448.htm):配置和原理讲的不错
redis是一个开源的、使用C语言编写的、支持网络交互的、可基于内存也可持久化的Key-Value数据库。

**gitlab调用Redis的配置**
```
/opt/gitlab/embedded/service/gitlab-rails/config# cat  resque.yml
production: unix:/var/opt/gitlab/redis/redis.socket
```
**gitlab内嵌的redis命令**，在/opt/gitlab/embedded/bin目录：
./redis-benchmark //用于进行redis性能测试的工具
./redis-check-dump //用于修复出问题的dump.rdb文件
./redis-cli //redis的客户端
./redis-server //redis的服务端
./redis-check-aof //用于修复出问题的AOF文件
./redis-sentinel //用于集群管理

**Redis的HOME**:/var/opt/gitlab/redis
```
/var/opt/gitlab/redis# tree -L 3
.
├── dump.rdb
├── redis.conf
└── redis.socket
```

可以看到 **redis.conf配置文件**

```
# Accept connections on the specified port, default is 6379.
# If port 0 is specified Redis will not listen on a TCP socket.
port 0 

# Specify the path for the unix socket that will be used to listen for
# incoming connections. There is no default, so Redis will not listen
# on a unix socket when not specified.
unixsocket /var/opt/gitlab/redis/redis.socket

# The filename where to dump the DB
dbfilename dump.rdb 

# The working directory.
dir /var/opt/gitlab/redis

# AOF and RDB persistence can be enabled at the same time without problems.
# If the AOF is enabled on startup Redis will load the AOF, that is the file
# with the better durability guarantees.
appendonly no
```

dump.rdb是快照文件，可以看出持久化采用的是RDB方式，是将redis某一时刻的数据持久化到磁盘中，是一种快照式的持久化方法;如果采用AOF(Append Only File，即只允许追加不允许改写的文件)的话，默认文件是appendonly.aof

如果redis不监听端口，还怎么与外界通信呢”，其实redis还支持通过unix socket方式来接收请求。可以通过unixsocket配置项来指定unix socket文件的路径。


**客户端连接**
/opt/gitlab/embedded/bin/redis-cli -s /var/opt/gitlab/redis/redis.socket 
keys * #列出所有的key,支持正则表达式
get XXX
DBSIZE #显示key的数量
help @generic
help @server

# sidekiq
GitLab uses sidekiq library for async job processing.
[The Basics of sidekiq](https://github.com/mperham/sidekiq/wiki/The-Basics)
Sidekiq is a framework for background job processing. It allows you to scale your application by performing work in the background. This requires three parts:

- Client --runs in your web application process (typically a Rails unicorn or passenger process) and allows you to push jobs into the background for processing. 
- Redis--provides data storage for Sidekiq. It holds all the job data along with runtime and historical data to power Sidekiq's Web UI.
- Server-- process pulls jobs from the queue in Redis and processes them.


# logrotate
```
root     21024     1  0 Jul14 ?        00:00:06 runsvdir -P /opt/gitlab/service log
root     21045 21024  0 Jul14 ?        00:00:00 runsv redis
root     21126 21024  0 Jul14 ?        00:00:00 runsv postgresql
root     21183 21024  0 Jul14 ?        00:00:00 runsv unicorn
root     21204 21024  0 Jul14 ?        00:00:00 runsv sidekiq
root     21234 21024  0 Jul14 ?        00:00:00 runsv logrotate
root     30381 21024  0 Jul14 ?        00:00:00 runsv nginx
root     21046 21045  0 Jul14 ?        00:00:00 svlogd -tt /var/log/gitlab/redis
root     21127 21126  0 Jul14 ?        00:00:00 svlogd -tt /var/log/gitlab/postgresql
root     21184 21183  0 Jul14 ?        00:00:00 svlogd -tt /var/log/gitlab/unicorn
root     21205 21204  0 Jul14 ?        00:00:00 svlogd -tt /var/log/gitlab/sidekiq
root     21235 21234  0 Jul14 ?        00:00:00 svlogd -tt /var/log/gitlab/logrotate
root     30382 30381  0 Jul14 ?        00:00:00 svlogd -tt /var/log/gitlab/nginx
```
man logrotate
logrotate is designed to ease administration of systems that generate large numbers of log files.  It allows automatic rotation, compression, removal, and mailing of log
       files.  Each log file may be handled daily, weekly, monthly, or when it grows too large.

另外 ： svlogd -tt /var/log/gitlab/sidekiq
[svlogd](http://manpages.ubuntu.com/manpages/hardy/man8/svlogd.8.html):
[runsv](http://manpages.ubuntu.com/manpages/hardy/man8/runsvdir.8.html):
[runsvdir](http://manpages.ubuntu.com/manpages/hardy/man8/runsvdir.8.html):
# unicorn
gitlab 默认使用的是 unicorn 作为内部的 app server，再用 nginx 做代理转发

GitLab uses [Unicorn](http://unicorn.bogomips.org/), a pre-forking Ruby web server, to handle web requests (web browsers and Git HTTP clients). Unicorn is a daemon written in Ruby and C that can load and run a Ruby on Rails application

[Deploying Rails Applications with Unicorn](https://devcenter.heroku.com/articles/rails-unicorn)：文中介绍，可以找到gitlab对应的配置文件是 **/var/opt/gitlab/gitlab-rails/etc/unicorn.rb**

关于Ruby on Rails，可参考百度[ROR](http://baike.baidu.com/link?url=8XqzVTyMgxnR2tLd5fbYfZVBUIrFLtW3QCwWzGJuM9Vyi47g3MoCRLBgd9zHpPP1-Yg5Lwm3AUCFJLWuGz3efq)

运行中发现unicorn比较耗内存，网上有人用[Puma 替换 Unicorn 跑 Gitlab](http://icyleaf.com/2014/01/moving-unicorn-to-puma-on-gitlab/):也是ruby写的，占用资源较少


说明：
**unicorn:**在/bin/sh ./run( 即/opt/gitlab/service/unicorn/run文件)，设置变量如rails_app=gitlab-rails,/opt/gitlab/embedded/bin/gitlab-unicorn-wrapper是个脚本，这个脚本先cd /opt/gitlab/embedded/service/${rails_app}，然后再该目录下执行其它操作
查看/opt/gitlab/embedded/service/gitlab-rails/config/gitlab.yml文件，
可以看到关键配置：
- gitlab
  + email_enabled
  + default_projects_features
- ldap
- omniauth
- backup
- gitlab_shell
- git


# 部署与运维问题
## 重要的事重复三篇
[Omnibus GitLab](https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/README.md):关于安装及部署过程的各种场景，非常非常重要

## 系统优化-内存清理
[系统优化](http://doc.gitlab.com/ce/operations/README.html):Sidekiq\Redis\Unicorn的内存清理

## 系统备份
[Backup restore](http://doc.gitlab.com/ce/raketasks/backup_restore.html):按着说明进行操作即可
Maintenance
## 【问题】上传图片或者附件时，图片的URL不正确
如下，ip-172-31-28-245.ap-northeast-1.compute.internal非真实地ip地址，是不能正常加载的
<img src="http://ip-172-31-28-245.ap-northeast-1.compute.internal/root/test/uploads/8a40102eac9333c12836a41588f20fae/%E9%83%A8%E7%BD%B2%E7%A8%8B%E5%BA%8F%E5%92%8C%E7%8B%AC%E7%AB%8B%E8%87%AA%E6%B5%8B%E7%A8%8B%E5%BA%8F.jpg" alt="部署程序和独立自测程序">
方法：
**1、改变主机名**
[Changing the Hostname of Your Linux Instance](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-hostname.html)

**2、然后执行sudo gitlab-ctl reconfigure，进行生效**
```
Recipe: gitlab::users
  * template[/var/opt/gitlab/.gitconfig] action create
    - update content in file /var/opt/gitlab/.gitconfig from f4c858 to 9d94a5
    --- /var/opt/gitlab/.gitconfig  2015-07-14 03:51:16.000000000 +0000
    +++ /tmp/chef-rendered-template20150723-2933-cnnj1j 2015-07-23 10:02:53.000000000 +0000
    @@ -4,7 +4,7 @@
     
     [user]
             name = GitLab
    -        email = gitlab@ip-172-31-28-245.ap-northeast-1.compute.internal
    +        email = gitlab@52.68.78.183
     [core]
             autocrlf = input
Recipe: gitlab::gitlab-rails
  * template[/var/opt/gitlab/gitlab-rails/etc/gitlab.yml] action create
    - update content in file /var/opt/gitlab/gitlab-rails/etc/gitlab.yml from 5bd69f to c3bd17
    --- /var/opt/gitlab/gitlab-rails/etc/gitlab.yml 2015-07-20 07:48:04.000000000 +0000
    +++ /tmp/chef-rendered-template20150723-2933-1reygbm  2015-07-23 10:02:53.000000000 +0000
    @@ -10,7 +10,7 @@
       ## GitLab settings
       gitlab:
         ## Web server settings (note: host is the FQDN, do not include http://)
    -    host: ip-172-31-28-245.ap-northeast-1.compute.internal
    +    host: 52.68.78.183
         port: 80
         https: false
Recipe: gitlab::nginx
 * template[/var/opt/gitlab/nginx/conf/gitlab-http.conf] action create
    - update content in file /var/opt/gitlab/nginx/conf/gitlab-http.conf from 739978 to c806f8
    --- /var/opt/gitlab/nginx/conf/gitlab-http.conf 2015-07-20 07:48:05.000000000 +0000
    +++ /tmp/chef-rendered-template20150723-2933-1ci1svy  2015-07-23 10:02:54.000000000 +0000
    @@ -39,7 +39,7 @@
     
     server {
       listen *:80;
    -  server_name ip-172-31-28-245.ap-northeast-1.compute.internal;
    +  server_name 52.68.78.183;
       server_tokens off; ## Don't show the nginx version number, a security best practice
       root /opt/gitlab/embedded/service/gitlab-rails/public;
```
## 【问题】修改nginx端口
https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/doc/settings/nginx.md#setting-the-nginx-listen-port

```
  * template[/var/opt/gitlab/gitlab-rails/etc/gitlab.yml] action create
    - update content in file /var/opt/gitlab/gitlab-rails/etc/gitlab.yml from 5bd69f to 08adb0
    --- /var/opt/gitlab/gitlab-rails/etc/gitlab.yml 2015-07-14 04:04:41.000000000 +0000
    +++ /tmp/chef-rendered-template20150715-1836-1ayq2q9    2015-07-15 04:57:41.000000000 +0000
    @@ -11,7 +11,7 @@
       gitlab:
         ## Web server settings (note: host is the FQDN, do not include http://)
         host: ip-172-31-28-245.ap-northeast-1.compute.internal
    -    port: 80
    +    port: 8090
         https: false
     
         # Uncommment this line below if your ssh host is different from HTTP/HTTPS one
  * template[/var/opt/gitlab/nginx/conf/gitlab-http.conf] action create
    - update content in file /var/opt/gitlab/nginx/conf/gitlab-http.conf from 739978 to 6b3a16
    --- /var/opt/gitlab/nginx/conf/gitlab-http.conf 2015-07-14 04:04:42.000000000 +0000
    +++ /tmp/chef-rendered-template20150715-1836-15a7jdj    2015-07-15 04:57:43.000000000 +0000
    @@ -38,7 +38,7 @@
     
     
     server {
    -  listen *:80;
    +  listen *:8090;
       server_name ip-172-31-28-245.ap-northeast-1.compute.internal;
       server_tokens off; ## Don't show the nginx version number, a security best practice
       root /opt/gitlab/embedded/service/gitlab-rails/public;
```

## 【问题】修改外部显示的URL
默认是根据hostname显示主机url,如果是云主机或者通过nginx采用二级域名映射，可以参考[configuration](https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/doc/settings/configuration.md)
```
external_url "http://gitlab.example.com" 
```
## 【问题】unicorn比较耗内存，可以减少worker个数
部署成功后，发现有时可以登录，有时不行。重装，然后折腾了半天，检查日志发现是内存不足
ActionView::Template::Error (Cannot allocate memory - node):
    52:     = render 'profile', user: @user
    53:     = render 'projects', projects: @projects, contributed_projects: @contributed_projects
    54: 
    55: :coffeescript
    56:   $(".user-calendar").load("#{user_calendar_path}")
  app/views/users/show.html.haml:55:in `_app_views_users_show_html_haml___3560521860722670995_41535680'
  app/controllers/users_controller.rb:15:in `show'

[Unicorn settings](https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/doc/settings/unicorn.md) 

修改/etc/gitlab/gitlab.rb 然后执行 sudo gitlab-ctl reconfigure 
unicorn['worker_processes'] = 3
unicorn['worker_timeout'] = 60


## 【问题】解决amazon免费主机，虚拟内存不足的情况
[amazon ec2 ubuntu with gitlab and nginx - cant load?](http://serverfault.com/questions/602416/amazon-ec2-ubuntu-with-gitlab-and-nginx-cant-load)
[How To Add Swap on Ubuntu 12.04](https://www.digitalocean.com/community/tutorials/how-to-add-swap-on-ubuntu-12-04):验证过了，在Centos6上也是同样ok

# 使用问题
## 受保护的分支
执行 git push -f origin HEAD 报下面错误
remote: GitLab: You are not allowed to force push code to a protected branch on this project.

参考：https://about.gitlab.com/2014/11/26/keeping-your-code-protected/
Project-->Setting -->Protected Branches
会看到分支情况，点击 unprotected,就可以关闭开关
![](https://about.gitlab.com/images/protected_branches.png)
