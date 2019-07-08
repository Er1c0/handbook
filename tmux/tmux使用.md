https://harttle.land/2015/11/06/tmux-startup.html


# 创建一个新的会话
tmux new -s myname
# 依附某个会话
tmux a -t myname
#  重命名一个session 
ctrl+b $
# 退出当前Session的快捷键是<prefix>d
ctrl+b+d

tmux list-sessions
