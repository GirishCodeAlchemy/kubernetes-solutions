---
<h1 align="center"> Kubernetes Solutions </h1>
<blockquote align="center">
  Common issues and solutions related to Kubernetes
</blockquote>

----

## Issue 1: Ingress not getting removed
Even after running the command `kubectl delete ingress <ingress_name> --force --grace-period=0`, the Ingress is not getting removed.

>#### Solution:
You can patch the Ingress using the following command:
```bash
kubectl patch ingress <name-of-the-ingress> -n <your-namespace> -p '{"metadata":{"finalizers":[]}}' --type=merge
```
<h1></h1>

## Issue 2: Debugging the Kubernetes Pod

>#### Solution:
You can create a new Pod with the curl image and open a shell in it using the following command:
```bash
kubectl run curlpod --image=curlimages/curl -i --tty -- sh
```
Once you’ve finished testing, you can press Ctrl+D to escape the terminal session in the Pod. The Pod will continue running afterwards. You can check the status of the Pod using:
``` bash
$ kubectl get pod curlpod
NAME        READY   STATUS    RESTARTS   AGE
curlpod   1/1     Running   1          72s

The Pod is still there!
```
You can re-enter the Pod again using the `kubectl exec` command:
``` bash
kubectl exec -it curlpod sh
kubectl attach curlpod -c curlpod -i -t
```
Or, you can delete the Pod with the kubectl delete pod command:
``` bash
kubectl delete po curlpod
```
<h1></h1>

## Issue 3: Drain the pods and delete the node

>#### Solution:
You can patch the Ingress using the following command:
```bash
kubectl cordon <node_name>
kubectl drain <node_name>
kubectl delete node <node_name>
```
<h1></h1>

## Issue 4: Deschedule or cordon the nodes in kuberentes

>#### Solution:

```bash
kubectl cordon <node-name>
kubectl get nodes
```
Schedule the node back so that the pods can be scheduled
```bash
kubectl uncordon <node-name>
```
<h1></h1>

## Issue 5: Execute the command inside the container

>#### Solution:

```bash
kubectl exec -i -t <pod_name> -- cat /etc/resolv.conf
kubectl exec -i -t <pod_name> -- nslookup kubernetes.default
```
<h1></h1>

## Issue 6: Track and sort by pod memory usage 

>#### Solution:

```bash
kubectl top pods -a --sort-by=memory
kubectl top pods -n <namespace> --selector=app=<app-lablename> --sort-by=memory
```

## Issue 7: Scale down/Up the replicas for deployments and statefulset

>#### Solution:

```bash
kubectl scale deployments <deployment-name> --replicas=<new-replicas>
kubectl scale statefulsets <stateful-set-name> --replicas=<new-replicas>
```

