## Introduction
**Welcome.**

![products]([rfed-logo-horiz](https://raw.githubusercontent.com/rancherfederal/branding/main/rancherfederal/rfed-logo-horiz.svg))

####
This training platform is open-source. And can be found at https://github.com/hobbyfarm/hobbyfarm.

####
The good news is that all the fields are clickable and do not require copying and pasting. This will create great success.

####
We are building 3 vms:
* **ubuntu1** ( Ubuntu 22.04 ) - Control Plane/etcd/Worker
* **ubuntu2** ( Ubuntu 22.04 ) - Control Plane/etcd/Worker
* **sles** ( SLES 15 - SP4 ) - Control Plane/etcd/Worker


Keep in mind the Operating System does not matter and our solutions can run on any Operating System

####

---
## RKE2 - Install - First Node

If you are in an AirGapped or connection limited environment check out our [docs](https://docs.rke2.io/). For speed, we are completing an online installation.

#### sudo

We need to sudo and create an account and directory.

```ctr:node1
sudo -i
```

#### rke2 install

```ctr:node1
curl -sfL https://get.rke2.io | INSTALL_RKE2_CHANNEL=v1.25 sh - 
systemctl enable --now rke2-server.service
```

server install options https://docs.rke2.io/install/configuration#configuring-the-linux-installation-script

#### config.yaml

Next we create a config yaml on ubuntu1.

```file:yaml:/etc/rancher/rke2/config.yaml:node1
token: RancherRodeo123456!
```

### on to the second node

---

## RKE2 - Install -  Node

#### sudo

We need to sudo and create an account and directory.

```ctr:node2
sudo -i
mkdir -p /etc/rancher/rke2/
```

#### yaml

Next we create a config yaml on ubuntu.

```file:yaml:/etc/rancher/rke2/config.yaml:node2
token: RancherRodeo123456!
server: https://${vminfo:rocky:public_ip}:9345
```

#### rke2 install

Great. We have all the files setup. We can now install rke2 and start it.

```ctr:node2
curl -sfL https://get.rke2.io | INSTALL_RKE2_CHANNEL=v1.25 sh - 
systemctl enable --now rke2-agent.service
```

#### watch - rocky

While this is starting we can watch from the rocky.

```ctr:node1
watch -n 5 kubectl get node -o wide
```

### On to sles

---

## RKE2 - Install - sles

#### sudo

We need to sudo and create an account and directory.

```ctr:node3
sudo -i
mkdir -p /etc/rancher/rke2/
```

#### yaml

Next we create a config yaml on sles.

```file:yaml:/etc/rancher/rke2/config.yaml:node3
token: RancherRodeo123456!
server: https://${vminfo:rocky:public_ip}:9345
```

#### rke2 install

Great. We have all the files setup. We can now install rke2 and start it.

```ctr:node3
curl -sfL https://get.rke2.io | INSTALL_RKE2_CHANNEL=v1.25 INSTALL_RKE2_TYPE=agent sh - 
systemctl enable --now rke2-agent.service
```

#### watch - rocky

While this is starting we can click on the rocky tab to watch.

### We now have a 3 node cluster!

We should talk about the STIG next.

---