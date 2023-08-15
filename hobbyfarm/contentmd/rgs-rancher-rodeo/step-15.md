Fleet is a tool built right into Rancher that allows you do perform Continuious Delivery without needing to use or maintain another tool. Store all your information into git and have Fleet deploy it. 

#### Fleet

Click on the "burger menu" in the top left and select `Continious Delivery`

You should be greated with a Get Started Page Click **Get Started** 

Give the Repo a `Name`

In the **Respository Field** paste `https://github.com/brooksphilip/hobbyfarm_demoapp.git`

Change the branch from master to `main`

Under Deploy To select the **Target** drop down and select your deployed cluster. **NOT THE LOCAL CLUSTER**

Click **Create**

#### Watch the MAGIC of Fleet!

When the state is `Active` and all **3** Resources have been deployed and `1/1` Clusters are showing Ready. Navigate back to your deployed cluster by using the "burger manu" in the top left. 

Lets examine what it deployed. Navigate to **Workloads**

Select the Namespace drop down at the top of the screen and select Default. **Be sure to clear any other filters you have there by clicking the `X`**

You should see a new workload called `cowsay`. You will also notice a new option at the bottom of the left pane. Click **rodeo** and a new tab should open with our Cow Demo Application. 

**Notice the color and count of the cows** This shows a round robin of traffic being loadbalanced over several replicas of our application. 

This was deployed by keeping the deployment information in git. Allowing you to use all the features that git offers you to control your deployments. This is called Gitops

#### Lets make a change. 

Navigate back to **Continuous Delivery** by selecting the burger menu and click the **3 Dots next to our repo** and select **Edit Config**

Change the branch field to `red` and click **Next** and **Save**

Now Navigate back to our application. By clicking the burger menu, selecting your deployed cluster, and click **rodeo** in the bottom left menu pane. 

You should not either notice the cows changing in color and number. If there is no change yet, wait for fleet to poll the repo and pick up the change. Usually takes about 90 seconds at most. 

#### MAGIC!