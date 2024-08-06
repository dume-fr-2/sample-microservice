# sample-microservice

## helm commands

### dry-run
```
helm install microservices-app-a -f values.yaml --dry-run --debug ./charts/app-a/
```

### install
```
helm install microservices-app-a -f values.yaml ./charts/app-a/
helm install microservices-app-b -f values.yaml ./charts/app-b/
helm install microservices-app-c -f values.yaml ./charts/app-c/
...
helm install microservices-app-i -f values.yaml ./charts/app-i/
helm install microservices-app-j -f values.yaml ./charts/app-j/
```

### uninstall 

```
helm uninstall microservices-app-a
helm uninstall microservices-app-b
helm uninstall microservices-app-c
...
helm uninstall microservices-app-i
helm uninstall microservices-app-j
```

### upgrade/rollback

```
# upgrade
helm upgrade microservices-app-a -f values.yaml ./charts/app-a/

# rollback
helm rollback [RELEASE] [REVISION]
helm rollback microservices-app-a 1
```

## kubectl commands

### get all

```
$ kubectl get all
NAME                         READY   STATUS             RESTARTS   AGE
pod/app-a-7665fc6445-nr82p   0/1     InvalidImageName   0          14s
pod/app-b-757c97674-9sx8s    0/1     InvalidImageName   0          13s

NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/app-a        ClusterIP   10.99.22.29      <none>        8000/TCP   14s
service/app-b        ClusterIP   10.110.124.160   <none>        8000/TCP   13s
service/kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP    4h32m

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/app-a   0/1     1            0           14s
deployment.apps/app-b   0/1     1            0           13s

NAME                               DESIRED   CURRENT   READY   AGE
replicaset.apps/app-a-7665fc6445   1         1         0       14s
replicaset.apps/app-b-757c97674    1         1         0       13s
```