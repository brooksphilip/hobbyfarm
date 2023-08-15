**Lets create a depployment and route traffic to our newly deployed workload.**


1. Click **Workloads**


2. Click **Deployment**


3. In the Namesapce field drop down select default. 


4. In the Name Field type `rodeo`


5. In the Image field type `nginx`


6. Under Networking Click **Add Port or Service**


7. Click the Service Type drop down and select `ClusterIP`. Type `http` in the Name Field and `80` in the Port Field. Leave the protocol as `TCP`


8. Click **Create**


### We have now deployed a deployment and a service. Now lets create the ingress


9. On the left menu pane click **Service Discovery** then click **Ingresses**


10. Click **Create**


11. Name the ingress `rodeo`. 


12. Under Rules in the Request Host field put `rodeo.${vminfo:Rancher01:public_ip}.sslip.io`. In the Path field type `/`. Click the Target Service drop down and select `rodeo`. Click the Port drop down and select `80`


13. Click **Create**


#### Now navigate to [http://rodeo.${vminfo:Rancher01:public_ip}.sslip.io](http://rodeo.${vminfo:Rancher01:public_ip}.sslip.io)


#### We have successfully deployed an application into Kubernetes and routed the traffic through Nginx into the Kubernetes cluster. 


### Lets move to Gitops