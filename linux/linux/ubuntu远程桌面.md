# 概念
## 安装
sudo apt-get install x11vnc
## 设置密码
x11vnc -storepasswd
## 修改配置文件
sudu vim /lib/systemd/system/x11vnc.service
```
[Unit]
Description=Start x11vnc at startup.
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/x11vnc -auth guess -forever -loop -noxdamage -repeat -rfbauth /home/<USERNAME>/.vnc/passwd -rfbport 5900 -shared

[Install]
WantedBy=multi-user.target
```
## 启动服务
```
sudo systemctl daemon-reload
sudo systemctl enable x11vnc.service
sudo systemctl start x11vnc.service
```
## 访问
通过mac，直接在浏览器输入
```
vnc://ip:port
```

# 参考
- [Ubuntu16.04安装x11VNC远程桌面](https://blog.csdn.net/songbaiyao/article/details/72858087)
- [输入正确的密码，依然无法登陆ubuntu系统](https://blog.csdn.net/chen_chun_guang/article/details/7712189)
# 其它问题

## 输入正确的密码，依然无法登陆ubuntu系统

进入home目录，删除.Xauthor*文件：
```
root@kevin:/home# find -name .Xauthor*
./kevin/.Xauthority-c
./kevin/.Xauthority-l
./kevin/.Xauthority

root@kevin:/home#rm -rf .Xauthor*
```