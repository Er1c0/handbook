# gitlbab持续集成

官方入门：http://docs.gitlab.com/ce/ci/quick_start/README.html

特性介绍(软文性质):
https://about.gitlab.com/features/gitlab-ci-cd/

文档汇总:
https://docs.gitlab.com/ce/ci/

## 架构
GitLab CI 是gitlab的一部分，除了gitlab的所有特性之外，它管理工程构建project/builds,并提供一个友好的用户接口
GitLab Runner 一个处理构建的应用。可以独立部署，并且通过api与gitlab CI一起工作
为了运行测试，你至少需要一个gitlab实例和一个gitlab Runner 

GitLab Runner 用go编写
## 概念：
- Runners  
  + 运行你的yaml文件，一个runner是一个隔离的虚拟机
  + 专用runner vs  共享runner(服务于所有工程)
  + 理想的，runner不要安装在gitlab的主机上，我们建议每个runner在一个专门主机上
- Pipeline
  + 一个pipeline 按批处理 stages (batches)执行的一组builds(独立运行的job)。
  + 在同一个stage的builds并发执行(依赖于并发runner的个数)
  + 如果都成功了，pipeline移到下一个stage；只要一个失败，下一个stage就不会执行
  
## 介绍
- GitLab提供了CI服务，仅需要增加一个.gitlab-ci.yml文件到仓储根目录，并配置你的project去调用一个runner。这样每次merge或者push就会自动触发CI pipeline；
- 默认的，pipeline会执行三个stage：Build、test、deploy， 如果stage没有job定义会被直接跳过。
- 如果运行正常（无非零值返回），会有个好看的绿色检查标志关联commit，

简而言之,需要两件事

1. Add .gitlab-ci.yml to the root directory of your repository
1. Configure a Runner

## 创建一个最简单的shell runner
### 安装GitlabRunner
```
# Linux x86-64
sudo wget -O /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64

# 授权执行权限
sudo chmod +x /usr/local/bin/gitlab-runner

# 创建Ci用户
sudo useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash

# 安装，作为一个server启动,为了共享权限，改为user=root
sudo gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner
sudo gitlab-runner start
```

### 注册一个shell runner
首先，在gitlab 上获取token定义：Admin Area->Overview->Runners 可以看到对应的url和token

参考：https://docs.gitlab.com/runner/register/index.html

1. 启动注册命令，可以注册多个
```
sudo gitlab-runner register
```
2. 输入gitlab的url
```
Please enter the gitlab-ci coordinator URL (e.g. https://gitlab.com )
https://gitlab.com
```
3. 输入token
```
Please enter the gitlab-ci token for this runner
xxx
```
4. 输入描述
```
Please enter the gitlab-ci description for this runner
[hostame] my-runner
```
5. 输入tags，tags用来关联不同的runner
```
Please enter the gitlab-ci tags for this runner (comma separated):
my-tag,another-tag
```
6. 选择runner executor
```
Please enter the executor: ssh, docker+machine, docker-ssh+machine, kubernetes, docker, parallels, virtualbox, docker-ssh, shell:
shell
```
7. 然后可以在Admin Area->Overview->Runners看到注册后的runner

## 在project上激活runner
project->Settings -> CI/CD -> runner

## 在对应的project上，增加.gitlab-ci.yml文件
```
stages:
  - test
  - deploy_production

test:
  stage: test
  tags:
    - ai-test-by-shell
  script:
    - cd /home/gitlab-runner/jfjun-OCR-template-images
    - git pull
    - cd -
    - export PATH="/root/anaconda3/bin:$PATH"
    - PYTHONPATH=. python -m unittest tests/ocr_regression_test.py


deploy_production:
  stage: deploy_production
  tags:
    - ai-test-by-shell
  script:
    - ssh root@host "export PATH=\"/anaconda3/bin:$PATH\" &&
          cd ~/project/jfjun-OCR-template &&
          git pull &&
          ./start_task.sh production "
  only:
    - master

```
样例2：
```
stages:
  - deploy_prod

deploy_prod:
   stage: deploy_prod
   tags:
     - mg_ci_111
   script:
     - . ~/.bashrc && cd /root/gitlab-runner/jfjun-model/ && git checkout szjy && git pull
     - nrm use lingxi
     - npm publish
     - ssh root@localhost  ". ~/.bashrc && cd /root/jfjun-core0/ && npm update jfjun-model-szjy && npm run gulp pm2"
   only:
     - szjy

```

## 通过docker创建runner
1、先安装docker

2、用root用户操作下列命令（sudo -i）

-使用一个配置卷到gitlab-runner的容器，用来进行配置和其它资源
-如果打算使用docker作为创建runner的方法，还需要mount your docker socket
```
docker run -d --name gitlab-runner --restart always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  gitlab/gitlab-runner:latest
```
-  -d (--detach)在后端原型
-  --name 容器的名称
-  -v 绑定一个逻辑卷

- docker ps 显示容器列表
- docker rm  删除一个容器
- docker stop 停止一个容器
- docker images 显示镜像列表

## 使用docker as a service
如下，在连接mongo时，host的值是mongo
```
services:
  - mongo:3.3
```

辅助文档：
[Configuration of your builds with .gitlab-ci.yml](http://doc.gitlab.com/ce/ci/yaml/README.html)
[Shared Runners](https://about.gitlab.com/2016/04/05/shared-runners/)