# brew
## 安装 
安装 Homebrew，参见 https://brew.sh
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
## 配置
brew --config
```
HOMEBREW_VERSION: 2.1.5
ORIGIN: https://github.com/Homebrew/brew
HEAD: db58b9f41b70a331dbe9b8371527a23e8ddcc718
Last commit: 2 days ago
Core tap ORIGIN: https://mirrors.ustc.edu.cn/homebrew-core.git
Core tap HEAD: ed7e53bb86c861663a2988544dc05a65eaeaaea0
Core tap last commit: 76 minutes ago
HOMEBREW_PREFIX: /usr/local
HOMEBREW_DEV_CMD_RUN: 1
CPU: quad-core 64-bit haswell
Homebrew Ruby: 2.3.7 => /usr/local/Homebrew/Library/Homebrew/vendor/portable-ruby/2.3.7/bin/ruby
Clang: 10.0 build 1000
Git: 2.6.2 => /usr/local/bin/git
Curl: 7.54.0 => /usr/bin/curl
Java: 1.8.0_112, 1.8.0_40, 1.7.0_71, 1.7.0_67
macOS: 10.13.5-x86_64
CLT: 10.1.0.0.1.1539992718
Xcode: N/A
XQuartz: 2.7.7 => /opt/X11
```
## brew 镜像设置
[Homebrew有比较快的源（mirror）吗？](https://www.zhihu.com/question/31360766)
[替换及重置Homebrew默认源](https://lug.ustc.edu.cn/wiki/mirrors/help/brew.git)
```
# 替换brew.git:
cd "$(brew --repo)"
git remote set-url origin https://mirrors.ustc.edu.cn/brew.git

# 替换homebrew-core.git:
cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git
```

## Failed to upgrade vendor Ruby