# pod如何理解?

- pod是容器载体，一个或多个容器作为一个单元方便管理。
- 还有就是docker和kubernetets是两家公司，作为一个编排部署的工具，不可能直接去管理别人公司开发的东西，然后把docker放在了pod里，在kubernetes集群环境下，直接管理我的pod。然后对docker容器操作。


**pod带来的好处:**

- Pod做为一个可以独立运行的服务单元，简化了应用部署的难度，以更高的抽象层次为应用部署管提供了极大的方便。
- Pod做为最小的应用实例可以独立运行，因此可以方便的进行部署、水平扩展和收缩、方便进行调度管理与资源的分配。
- Pod中的容器共享相同的数据和网络地址空间，Pod之间也进行了统一的资源管理与分配。


**pod的配置文件：**
apiVersion、kind、metadata、spec以及status。其中apiVersion和kind是比较固定的，status是运行时的状态，所以最重要的就是metadata和spec两个部分

样例:
```yml
apiVersion: v1
kind: Pod
metadata:
  name: first-pod
  labels:
    app: bash
    tir: backend
spec:
  containers:
  - name: bash-container
    image: docker.io/busybox
    command: ['sh', '-c', 'echo Hello Kubernetes! && sleep 3600']
```

# 参考:

- [Kubernetes |Pod 深入理解与实践](https://www.jianshu.com/p/d867539a15cf)