## Install NeuVector

Lets use helm, but inside the Rancher UI. Do you remember step 11 `Interacting with the Kubernetes Cluster`. 


1. We need to add the Helm repo to our shell to be able to install NeuVector. Click the `Kubectl Shell` button (the button with the Prompt icon) in the top right corner of the Cluster Explorer, and copy and paste the following: 


```bash
# helm repo add
helm repo add neuvector https://neuvector.github.io/neuvector-helm/ --force-update
```


2. Next we can install NeuVector using the following helm command. Copy and paste the following into the kubectl shell inside the Rancher UI: 

```bash
helm upgrade -i neuvector --namespace cattle-neuvector-system neuvector/core --create-namespace --set k3s.enabled=true --set controller.pvc.enabled=true --set controller.pvc.capacity=500Mi --set controller.ranchersso.enabled=true --set global.cattle.url=https://rancher.${vminfo:Cluster1:public_ip}.sslip.io
```


3. We should wait a few seconds for the pods to deploy. We can Follow along by clicking **Workloads** then at the top select the drop down and select `cattle-neuvector-system`. This will display the status neuvecotr deployments. 


4. Wait until all deployments are green and **Active**

Now we can use the Rancher proxy to get to the dashboard.


5. You should now see a new option on the left menu pane. Select **NeuVector** and click the Link provided. This will open a new tab. 


6. Accept the EULA and continue to the NeuVector Dashboard. 

**NeuVector is now installed**

### On to GitOPs