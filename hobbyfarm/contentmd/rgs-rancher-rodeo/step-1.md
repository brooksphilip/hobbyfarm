### Welcome to the Rancher Government Solutions Rodeo.

In this scenario, we will be walking through installing Rancher and deploying several workloads to a cluster provisioned by Rancher.

We will be using two virtual machines today, `cluster01` and `rancher01` which are located in the tabs in the panel to the right. `rancher01` will run a Kubernetes cluster and Rancher, and `cluster01` will run a Kubernetes cluster and the corresponding user workloads.

Note that there are two separate Kubernetes clusters at play here, the Rancher Kubernetes Cluster is dedicated to running Rancher, while the Workload Cluster is managed by Rancher and runs on a separate virtual machine.

#### This scenario will NOT be following the general HA installation instructions available here: [High Availability (HA) Install](https://ranchermanager.docs.rancher.com/pages-for-subheaders/install-upgrade-on-a-kubernetes-cluster). We reccomend that any production supported cluster follow best practices and be deployed using a 3 or 5 node cluster. 
