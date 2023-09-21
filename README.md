### Welcome to the Rancher Government Solutions Rodeo.

In this scenario, we will be walking through installing Rancher and deploying several workloads to a cluster provisioned by Rancher.

<br>

We will be using two virtual machines today, `cluster01` and `rancher01` which are located in the tabs in the panel to the right. `rancher01` will run a Kubernetes cluster and Rancher, and `cluster01` will run a Kubernetes cluster and the corresponding user workloads.
<br>
<br>

Note that there are two separate Kubernetes clusters at play here, the Rancher Kubernetes Cluster is dedicated to running Rancher, while the Workload Cluster is managed by Rancher and runs on a separate virtual machine.

#### This scenario will NOT be following the general HA installation instructions available here: [High Availability (HA) Install](https://ranchermanager.docs.rancher.com/pages-for-subheaders/install-upgrade-on-a-kubernetes-cluster). We reccomend that any production supported cluster follow best practices and be deployed using a 3 or 5 node cluster. 
### Rancher can run on any Kubernetes cluster and distribution, that is certified to be standard compliant by the Cloud Native Computing Foundation (CNCF).

#### We recommend using a [RKE2](https://rke2.io/) Kubernetes cluster. RKE2 is a CNCF certified Kubernetes distribution, which is easy and fast to install and upgrade with a focus on security. You can run it in your datacenter, in the cloud as well as on edge devices. It works great on a single-node as well in large, highly available setups.

#### In this Rodeo we want to create a single node Kubernetes cluster on the `Rancher01` VM in order to install Rancher into it. 

```ctr:Rancher01
sudo bash -c 'curl -sfL https://get.rke2.io | \
  INSTALL_RKE2_CHANNEL="v1.24" \
  sh -'
```

Create a configuration for RKE2

```ctr:Rancher01
sudo mkdir -p /etc/rancher/rke2
sudo bash -c 'echo "write-kubeconfig-mode: \"0600\"" > /etc/rancher/rke2/config.yaml'
```

After that you can enable and start the RKE2 systemd service:

```ctr:Rancher01
sudo systemctl enable rke2-server.service
sudo systemctl start rke2-server.service
```

The service start will block until your cluster is up and running. This should take about 1 minute.

You can access the RKE2 logs with:

```ctr:Rancher01
sudo journalctl -u rke2-server
```

#### Creating a highly available, multi-node Kubernetes cluster for a highly available Rancher installation would not be much more complicated. You can run the same installation script with a couple more options on multiple nodes.

#### You can find more information on this in the [RKE2 documentation](https://docs.rke2.io/).
RKE2 now created a new Kubernetes cluster. In order to interact with its API, we can use the Kubernetes CLI `kubectl`.

To install `kubectl` run:

```ctr:Rancher01
echo 'export PATH=$PATH:/var/lib/rancher/rke2/bin/' >> ~/.bashrc
source ~/.bashrc
```

We also have to ensure that `kubectl` can connect to our Kubernetes cluster. For this, `kubectl` uses standard Kubeconfig files which it looks for in a `KUBECONFIG` environment variable or in a `~/.kube/config` file in the user's home directory.

RKE2 writes the Kubeconfig of a cluster to `/etc/rancher/rke2/rke2.yaml`.

We can copy the `/etc/rancher/rke2/rke2.yaml` file to our `~/.kube/config` file so that `kubectl` can interact with our cluster:

```ctr:Rancher01
mkdir -p ~/.kube
sudo cp /etc/rancher/rke2/rke2.yaml ~/.kube/config
sudo chown ec2-user: ~/.kube/config
sudo chmod 600 ~/.kube/config

```

In order to test that we can properly interact with our cluster, we can execute two commands.

To list all the nodes in the cluster and check their status:

```ctr:Rancher01
kubectl get nodes
```

The cluster should have one node, and the status should be "Ready".

To list all the Pods in all Namespaces of the cluster:

```ctr:Rancher01
kubectl get pods --all-namespaces
```

All Pods should have the status "Running" OR "Completed".
#### Installing Rancher into our new Kubernetes cluster is easily done with Helm. Helm is a very popular package manager for Kubernetes. It is used as the installation tool for Rancher when deploying Rancher onto a Kubernetes cluster. In order to use Helm, we have to download the Helm CLI.

```ctr:Rancher01
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 \
  | bash
```

After a successful installation of Helm, we should check our installation to ensure that we are ready to install Rancher.

```ctr:Rancher01
helm version --client
```

Helm uses the same kubeconfig as kubectl in the previous step.

We can check that this works by listing the Helm charts that are already installed in our cluster:

```ctr:Rancher01
helm ls --all-namespaces
```
#### cert-manager is a Kubernetes add-on to automate the management and issuance of TLS certificates from various issuing sources.

The following set of steps will install cert-manager which will be used to manage the TLS certificates for Rancher.

First, we'll add the helm repository for Jetstack

```ctr:Rancher01
helm repo add jetstack https://charts.jetstack.io
```

Now, we can install cert-manager:

```ctr:Rancher01
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --version v1.11.0 \
  --set installCRDs=true \
  --create-namespace
```

Once the helm chart has installed, you can monitor the rollout status of both `cert-manager` and `cert-manager-webhook`

```ctr:Rancher01
kubectl -n cert-manager rollout status deploy/cert-manager
```

You should eventually receive output similar to:

`Waiting for deployment "cert-manager" rollout to finish: 0 of 1 updated replicas are available...`

`deployment "cert-manager" successfully rolled out`

```ctr:Rancher01
kubectl -n cert-manager rollout status deploy/cert-manager-webhook
```

You should eventually receive output similar to:

`Waiting for deployment "cert-manager-webhook" rollout to finish: 0 of 1 updated replicas are available...`

`deployment "cert-manager-webhook" successfully rolled out`
#### We will now install Rancher in HA mode onto our `Rancher01` Kubernetes cluster. The following command will add `rancher-latest` as a helm repository.

```ctr:Rancher01
helm repo add rancher-latest https://releases.rancher.com/server-charts/latest
```

Finally, we can install Rancher using our `helm install` command.

```ctr:Rancher01
helm install rancher rancher-latest/rancher \
  --namespace cattle-system \
  --set hostname=rancher.${vminfo:rancher01:public_ip}.sslip.io \
  --set replicas=1 \
  --version 2.7.4 \
  --create-namespace
```

### It's That Easy!
#### Before we access Rancher, we need to make sure that `cert-manager` has signed a certificate using the `dynamiclistener-ca` in order to make sure our connection to Rancher does not get interrupted. The following bash script will check for the certificate we are looking for.

```ctr:Rancher01
while true; do curl -kv https://rancher.${vminfo:Rancher01:public_ip}.sslip.io 2>&1 | grep -q "dynamiclistener-ca"; if [ $? != 0 ]; then echo "Rancher isn't ready yet"; sleep 5; continue; fi; break; done; echo "Rancher is Ready";
```
***Note:*** Rancher may not immediately be available at the link below, as it may be starting up still. Please continue to refresh until Rancher is available.
<br>
<br>
#### Access Rancher Server at [https://rancher.${vminfo:Rancher01:public_ip}.sslip.io](https://rancher.${vminfo:Rancher01:public_ip}.sslip.io).
<br>
<br>
For this Rodeo, Rancher is installed with a self-signed certificate from a CA that is not automatically trusted by your browser. Because of this, you will see a certificate warning in your browser. You can safely skip this warning. Some Chromium based browsers may not show a skip button. If this is the case, just click anywhere on the error page and type "thisisunsafe" (without quotes). This will force the browser to bypass the warning and accept the certificate.
<br>
<br>
In order to retrieve the bootstrap password run the supplied command on the initial Rancher UI screen. Then Please follow instructions on the UI to generate password for default `admin` user when prompted.
<br>
<br>
Make sure to agree to the Terms & Conditions.
<br>
<br>
When prompted, the **Rancher Server URL** should be `rancher.${vminfo:Rancher01:public_ip}.sslip.io`, which is the hostname you used to access the server.
<br>
<br>
You will see the Rancher UI, with the `local` cluster in it. The `local` cluster is the cluster where Rancher itself runs, and **should not be used for deploying your demo workloads.**
<br>
<br>
In the top left corner of the UI, you can find a "burger menu" button, which opens up the global navigation menu. There you can access global applications and settings. You have quick links to explore all Rancher managed clusters and a way to get back to the Rancher home page.
In this step, we will be creating a Kubernetes Lab environment within Rancher. Normally, in a production case, you would create a Kubernetes Cluster with multiple nodes; however, with this lab environment, we will only be using one virtual machine for the cluster.

1. Go back to the Rancher Home Page
<br>
<br>
2. On top of the list of available clusters, click **Create**
   - We will be using RKE2 cluster, so make sure to switch the toggle to **RKE2/K3s**
   - Note the multiple types of Kubernetes cluster Rancher supports. We will be using **Custom cluster on existing nodes** for this lab, but there are a lot of possibilities with Rancher
<br>
<br>
3. Click on the **Custom** Cluster box in the **Use existing nodes and create a cluster using RKE2** section
<br>
<br>
4. Enter a name in the **Cluster Name** box
<br>
<br>
5. Set the Kubernetes Version to a `v1.24.x` version
<br>
<br>
6. All other settings can be kept as default
<br>
<br>
7. Click **Create** at the bottom
<br>
<br>
8. Once the cluster is created, you can retrieve an installation command in the **Registration** tab that you can use to add new nodes to your Kubernetes cluster
<br>
<br>
9. Make sure the boxes **etcd**, **Control Plane**, and **Worker** are all ticked
<br>
<br>
10. Click **Show Advanced** to the bottom right of the checkboxes
<br>
<br>
11. Enter the **Node Public IP** (`${vminfo:Cluster01:public_ip}`) and **Node Private IP** (`${vminfo:Cluster01:private_ip}`)
    - **IMPORTANT:** It is VERY important that you use the correct External and Internal addresses from the **Cluster01** machine for this step, and run it on the correct machine. Failure to do this will cause the future steps to fail
<br>
<br>
12. Check the checkbox to **skip the TLS verification and accept insecure certificates** below the registration command
<br>
<br>
13. Double-click the registration command to copy it to your clipboard
<br>
<br>
14. Proceed to the next step of this scenario
**IMPORTANT NOTE:** Make sure you have selected the `Cluster01` tab in HobbyFarm in the window to the right. If you run this command on `Rancher01` you will cause problems for your scenario session.
<br>
<br>
Take the copied command and run it on `Cluster01`
<br>
<br>
You can follow the provisioning process in the **Machines**, **Conditions** and **Related Resources** tabs.
<br>
<br>
Your cluster state in the cluster list and on the cluster detail page will change to **Active**.
<br>
<br>
Once your cluster has gone to **Active** you can start exploring it by either clicking the **Explore** button in the cluster list on the home page, or by selecting the cluster in the global menu.
<br>
<br>
Proceed to the next step of this scenario.
In this step, we will be showing basic interaction with our Kubernetes cluster.
<br>
<br>
1. Select the "burger menu" at the top left and Click into your newly **active** cluster
<br>
<br>
Note the diagrams dials, which illustrate cluster capacity, and the box that show you the recent events in your cluster.
<br>
<br>
2. Click the **Kubectl Shell** button (the button with the Prompt icon) in the top right corner of the Cluster Explorer, and enter `kubectl get pods --all-namespaces` and observe the fact that you can interact with your Kubernetes cluster using `kubectl`
<br>
<br>
3. Also take note of the **Download Kubeconfig File** button next to it which will generate a Kubeconfig file that can be used from your local desktop or within your deployment pipelines
<br>
<br>
4. In the left menu, you have access to all Kubernetes resources, the Rancher Application Marketplace and additional cluster tools
<br>
<br>
5. Proceed to the next step of this scenario
Lets install longhorn for our persistent storage inside Kubernetes. This will allows applications to be able to read and write persistent data inside the cluster. 


1. Click into your newly **active** cluster **if you are not already in the cluster explorer for the newly created cluster**
<br>
<br>
2. On the left menu pane click **Apps**. This should take you to **charts**. These are all helm charts that are built into Rancher and are apart of our Certified Integrations
<br>
<br>
3. Find and select **Longhorn**
<br>
<br>
4. In the top right click **Install**
<br>
<br>
5. Select the **Install into Project** drop down and select **System** then click **Next** in the bottom right 
<br>
<br>
6. Since we are deploying a single cluster we need to tune longhorn a little. Lets select **Longhorn Storage Class Settings** and locate the **Default Storage Class Replica Count** field and change the `3` to a `1`
<br>
<br>
**NOTE:** Longhorn by default deploys with a replica count of 3. Since we are only deploying a single node it will not have enough nodes to deploy replicas of the data to. Keep in mind there are also other settings here to further customize the Longhorn installation (AirGap, etc). 
<br>
<br>
7. Click **Install**
<br>
<br>
A terminal will appear and you will be able to watch the installation process. Wait for this to state `SUCCESS: `
<br>
<br>
8. Click the **X** to close the terminal field at the bottom of Rancher UI
**Longhorn is now installed into the cluster**.
<br>
<br>
9. Lets use the Rancher Proxy to view the Longhorn UI. On the left menu pane you will not see a **Longhorn** option. Click on Longhorn and select the link. This will open a new window and take you to the Longhorn UI 
<br>
<br>
10. Since we will be deploying NeuVector in the next step and NewVector uses RWX (ReadWriteMany) we need to ensure our Longhorn hosts have NFS kernel modules installed

```ctr:Cluster01
sudo zypper install -y nfs-client
```
<br>
<br>

#### Lets install NeuVector for Container Security
Lets use helm, but inside the Rancher UI. Do you remember step 11 `Interacting with the Kubernetes Cluster`. 
<br>
<br>
We need to add the Helm repo to our shell to be able to install NeuVector. Click the `Kubectl Shell` button (the button with the Prompt icon) in the top right corner of the Cluster Explorer, and copy and paste the following: 

<br>

```bash
# helm repo add
helm repo add neuvector https://neuvector.github.io/neuvector-helm/ --force-update
```
<br>

Next we can install NeuVector using the following helm command. Copy and paste the following into the kubectl shell inside the Rancher UI: 

<br>

```bash:Rancher01
helm upgrade -i neuvector --namespace cattle-neuvector-system neuvector/core --create-namespace --set k3s.enabled=true --set controller.pvc.enabled=true --set controller.pvc.capacity=500Mi --set controller.ranchersso.enabled=true --set global.cattle.url=https://rancher.${vminfo:Rancher01:public_ip}.sslip.io
```

We should wait a few seconds for the pods to deploy. We can Follow along by clicking **Workloads** then at the top select the drop down and select `cattle-neuvector-system`. This will display the status neuvecotr deployments. 
<br>
<br>
Wait until all deployments are green and **Active**
<br>
<br>
Now we can use the Rancher proxy to get to the dashboard.
<br>
<br>
You should now see a new option on the left menu pane. Select **NeuVector** and click the Link provided. This will open a new tab. 
<br>
<br>
Accept the EULA and continue to the NeuVector Dashboard. 
<br>
<br>
**NeuVector is now installed**.

### On to GitOPs**Lets create a depployment and route traffic to our newly deployed workload.**


1. Click **Workloads**.
<br>
<br>
2. Click **Deployment**.
<br>
<br>
3. In the Namesapce field drop down select default. 
<br>
<br>
4. In the Name Field type `rodeo`.
<br>
<br>
5. In the Image field type `nginx`.
<br>
<br>
6. Under Networking Click **Add Port or Service**.
<br>
<br>
7. Click the Service Type drop down and select `ClusterIP`. Type `http` in the Name Field and `80` in the Port Field. Leave the protocol as `TCP`.
<br>
<br>
8. Click **Create**.
**We have now deployed a deployment and a service. Now lets create the ingress**.
<br>
<br>
9. On the left menu pane click **Service Discovery** then click **Ingresses**.
<br>
<br>
10. Click **Create**.
<br>
<br>
11. Name the ingress `rodeo`. 
<br>
<br>
12. Under Rules in the Request Host field put `rodeo.${vminfo:Cluster01:public_ip}.sslip.io`. In the Path field type `/`. Click the Target Service drop down and select `rodeo`. Click the Port drop down and select `80`.
<br>
<br>
13. Click **Create**.
<br>
<br>
#### Now navigate to [http://rodeo.${vminfo:Rancher01:public_ip}.sslip.io](http://rodeo.${vminfo:Rancher01:public_ip}.sslip.io).

#### We have successfully deployed an application into Kubernetes and routed the traffic through Nginx into the Kubernetes cluster. 

### Lets move to GitopsFleet is a tool built right into Rancher that allows you do perform Continuous Delivery without needing to use or maintain another tool. Store all your information into git and have Fleet deploy it. 

#### Fleet

<br>

1. Click on the "burger menu" in the top left and select `Continuous Delivery`.  
2. You should be greated with a Get Started Page Click **Get Started**.  
3. Give the Repo a `Name`.  
4. In the **Repository Field** paste `https://github.com/brooksphilip/hobbyfarm_demoapp.git`.  
5. Change the branch from master to `main`.  
6. Under Deploy To select the **Target** drop down and select your deployed cluster. **NOT THE LOCAL CLUSTER**.  
7. Click **Create**.  

<br>
<br>

#### Watch the MAGIC of Fleet!

<br>
<br>

8. When the state is `Active` and all **3** Resources have been deployed and `1/1` Clusters are showing Ready. Navigate back to your deployed cluster by using the "burger menu" in the top left. 
9. Lets examine what it deployed. Navigate to **Workloads**.
10. Select the Namespace drop down at the top of the screen and select Default. **Be sure to clear any other filters you have there by clicking the `X`**.
11. You should see a new workload called `cowsay`. You will also notice a new option at the bottom of the left pane. Click **rodeo** and a new tab should open with our Cow Demo Application. 
<br>
<br>
**Notice the color and count of the cows** This shows a round robin of traffic being load balanced over several replicas of our application. 
<br>
<br>
This was deployed by keeping the deployment information in git. Allowing you to use all the features that git offers you to control your deployments. This is called Gitops.
<br>
<br>

#### Lets make a change. 

<br>
<br>

12. Navigate back to **Continuous Delivery** by selecting the burger menu and click the **3 Dots next to our repo** and select **Edit Config**.
13. Change the branch field to `red` and click **Next** and **Save**.
14. Now Navigate back to our application. By clicking the burger menu, selecting your deployed cluster, and click **rodeo** in the bottom left menu pane. 
15. You should not either notice the cows changing in color and number. If there is no change yet, wait for fleet to poll the repo and pick up the change. Usually takes about 90 seconds at most. 

#### MAGIC!There is a nice article about it from [Businesswire](https://www.businesswire.com/news/home/20221101005546/en/DISA-Validates-Rancher-Government-Solutions%E2%80%99-Kubernetes-Distribution-RKE2-Security-Technical-Implementation-Guide).
<br>
<br>
You can download the STIG itself from [https://dl.dod.cyber.mil/wp-content/uploads/stigs/zip/U_RGS_RKE2_V1R3_STIG.zip](https://dl.dod.cyber.mil/wp-content/uploads/stigs/zip/U_RGS_RKE2_V1R3_STIG.zip).   
The SITG viewer can be found on DISA's site at [https://public.cyber.mil/stigs/srg-stig-tools/](https://public.cyber.mil/stigs/srg-stig-tools/). For this guide I have simplified the controls and provided simple steps to ensure compliance. Hope this helps a little.
<br>
<br>
Bottom Line
<br>
<br>
* Enable SElinux
* Update the config for the Control Plane and Worker nodes.

Enough STIG. Let's start deploying applications like Rancher
## Thank you for attending. 