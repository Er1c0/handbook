# 总览

- box add:导入box
- box list:查看box
- box remove:删除box
- init:初始化，创建一个Vagrantfile
- up:启动
- status:查看状态
- ssh:SSH连接
- reload:重载
- halt:关闭
- suspend:暂停
- destroy:删除

# 快照 vagrant snapshot 

- list 
- save [options] [vm-name] `<name>`:
  - 样例1：vagrant snapshot save -f lab1 base1.0
  - 样例2：vagrant snapshot save base2.0
-  delete [options] [vm-name] `<name>`:
  - 样例1: vagrant snapshot delete base2.0
- push 
- pop 

# 状态 status

