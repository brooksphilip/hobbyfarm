## Accessing Rancher

***Note:*** Rancher may not immediately be available at the link below, as it may be starting up still. Please continue to refresh until Rancher is available.

#### Access Rancher Server at [https://rancher.${vminfo:Rancher01:public_ip}.sslip.io](https://rancher.${vminfo:Rancher01:public_ip}.sslip.io).

For this Rodeo, Rancher is installed with a self-signed certificate from a CA that is not automatically trusted by your browser. Because of this, you will see a certificate warning in your browser. You can safely skip this warning. Some Chromium based browsers may not show a skip button. If this is the case, just click anywhere on the error page and type "thisisunsafe" (without quotes). This will force the browser to bypass the warning and accept the certificate.

In order to retrieve the bootstrap password run the supplied command on the initial Rancher UI scree. Then Please follow instructions on the UI to generate password for default `admin` user when prompted.

Make sure to agree to the Terms & Conditions

When prompted, the **Rancher Server URL** should be `rancher.${vminfo:Rancher01:public_ip}.sslip.io`, which is the hostname you used to access the server.

You will see the Rancher UI, with the `local` cluster in it. The `local` cluster is the cluster where Rancher itself runs, and **should not be used for deploying your demo workloads.**

In the top left corner of the UI, you can find a "burger menu" button, which opens up the global navigation menu. There you can access global applications and settings. You have quick links to explore all Rancher managed clusters and a way to get back to the Rancher home page.
