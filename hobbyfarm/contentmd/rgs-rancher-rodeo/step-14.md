**Lets create a depployment and route traffic to our newly deployed workload.**


Click **Workloads**

Click **Deployment**

In the Namesapce field drop down select default. 

In the Name Field type `rodeo`

In the Image field type `nginx`

Under Networking Click **Add Port or Service**

Click the Service Type drop down and select `ClusterIP`. Type `http` in the Name Field and `80` in the Port Field. Leave the protocol as `TCP`

Click **Create**

### We have now deployed a deployment and a service. Now lets create the ingress

On the left menu pane click **Service Discovery** then click **Ingresses**

Click **Create**

Name the ingress `rodeo`. 

Under Rules in the Request Host field put `rodeo.${vminfo:Rancher01:public_ip}.sslip.io`. In the Path field type `/`. Click the Target Service drop down and select `rodeo`. Click the Port drop down and select `80`

Click **Create**

#### Now navigate to [http://rodeo.${vminfo:Rancher01:public_ip}.sslip.io](http://rodeo.${vminfo:Rancher01:public_ip}.sslip.io)

#### We have successfully deployed an application into Kubernetes and routed the traffic through Nginx into the Kubernetes cluster. 

### Lets move to Gitops