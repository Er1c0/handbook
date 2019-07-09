- [问题](#%E9%97%AE%E9%A2%98)
  - [gitlab-runner失联了](#gitlab-runner%E5%A4%B1%E8%81%94%E4%BA%86)
  - [git-runner配置](#git-runner%E9%85%8D%E7%BD%AE)
# 问题
## gitlab-runner失联了
参考:[gitlab-runner 失联了](https://www.jianshu.com/p/6063c1a2fa47)

常用命令:

- gitlab-runner list #显示所有配置的runner
- gitlab-runner status # 获得一个service的状态
- gitlab-runner restart|start|stop #重启、启动、停止

完整命令说明如下：
```
# gitlab-runner --help
NAME:
   gitlab-runner - a GitLab Runner

USAGE:
   gitlab-runner [global options] command [command options] [arguments...]

VERSION:
   11.10.1 (1f513601)

AUTHOR:
   GitLab Inc. <support@gitlab.com>

COMMANDS:
     exec                  execute a build locally
     list                  List all configured runners
     run                   run multi runner service
     register              register a new runner
     install               install service
     uninstall             uninstall service
     start                 start service
     stop                  stop service
     restart               restart service
     status                get status of a service
     run-single            start single runner
     unregister            unregister specific runner
     verify                verify all registered runners
     artifacts-downloader  download and extract build artifacts (internal)
     artifacts-uploader    create and upload build artifacts (internal)
     cache-archiver        create and upload cache artifacts (internal)
     cache-extractor       download and extract cache artifacts (internal)
     cache-init            changed permissions for cache paths (internal)
     health-check          check health for a specific address
     help, h               Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --cpuprofile value           write cpu profile to file [$CPU_PROFILE]
   --debug                      debug mode [$DEBUG]
   --log-format value           Choose log format (options: runner, text, json) [$LOG_FORMAT]
   --log-level value, -l value  Log level (options: debug, info, warn, error, fatal, panic) [$LOG_LEVEL]
   --help, -h                   show help
   --version, -v                print the version
```

## git-runner配置
通过`git-runner list`命令可以看到` ConfigFile=/etc/gitlab-runner/config.toml`
样例文件内容为:
```
concurrent = 1
check_interval = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "mg_ci_111"
  url = "http://gitlab.lingxi.co/"
  token = "Co1UmjA6zWzBmcLss4t3"
  executor = "shell"
  [runners.custom_build_dir]
  [runners.cache]
    [runners.cache.s3]
    [runners.cache.gcs]
```

参数说明:
- concurrent 并发数
- log_level 日志级别，比命令行的参数级别低:--debug, -l or --log-level
- log_format 日志格式如：runner、text、json等，命令参数为 --log-format
- check_interval 新任务的检查周期，默认为3秒