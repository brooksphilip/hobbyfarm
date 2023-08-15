# Install Longhorn

#### Lets install longhorn for our persistent storage inside Kubernetes. This will allows applications to be able to read and write persistent data inside the cluster. 

1. Click into your newly `active` cluster **if you are not already in the cluster explorer for the newly created cluster**

2. On the left menu pane click `Apps`. This should take you to `charts`

3. Find and click `Longhorn`

4. In the top right click `Install`

5. Locate the `Install into Project` drop down and select `System` then click `Next` in the bottom right. 

**NOTE:** We are going to keep all the defaults, but if you need to customize the install of Longhorn (AirGap, replica count, etc) this is the menu where you can set custom options

6. Click `Install`

7. A terminal will appear and you will be able to watch the installation process. Wait for this to state `SUCCESS: helm upgrade`

8. Click the `X` to close the terminal field at the bottom of Rancher UI. 

**Longhorn is now installed into the cluster**

9. Since we will be deploying NeuVector in the next step and NewVector uses RWX (ReadWriteMany) we need to ensure our Longhorn hosts have NFS kernel modules installed. 

```ctr:Cluster01
zypper install nfs-common -y
```

#### Lets install NeuVector for Container Security
