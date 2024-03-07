// Useful commands


kubectl get secret/datadog-api -o json | jq .data.token | base64 -d -i

kubectl get pods --no-headers -o custom-columns=":metadata.name" | grep datadog
kubectl exec $(kubectl get pods --no-headers -o custom-columns=":metadata.name" | grep datadog | head -n 1) -- agent status


// Show labels
kubectl get deployments -n ns1 -l service=advertisements --show-labels
kubectl get pods -n ns1 -l service=advertisements --show-labels