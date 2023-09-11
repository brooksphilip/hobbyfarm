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
sudo zypper install nfs-client -y
```
<br>
<br>

#### Lets install NeuVector for Container Security
