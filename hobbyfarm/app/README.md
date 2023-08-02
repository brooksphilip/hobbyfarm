## HobbyFarm Deployment with Fleet

### Configure AWS Secret

```bash
kubectl create secret generic aws-creds -n hobbyfarm-system --from-literal=access_key=$AccessKey --from-literal=secret_key=$SecretKey
```

### Fleet Local
```bash
### Deploys hobbyfarm on the local cluster.
kubectl apply -f https://raw.githubusercontent.com/zackbradys/rgs-hobbyfarm/main/fleet/gitrepo-local.yaml
```