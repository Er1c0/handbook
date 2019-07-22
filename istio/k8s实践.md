```
$sudo kubeadm init --config kubeadm-master.config
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of machines by running the following on each node
as root:

  kubeadm join 11.11.11.111:6443 --token d2ia57.lri6xuh89mlb2l1s --discovery-token-ca-cert-hash sha256:c099bfc4b574a5d1966c55e7788d46c3ec8d0894df92458e50671dad8e03fc90
```