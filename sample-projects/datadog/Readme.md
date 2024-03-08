// Useful commands


kubectl get secret/datadog-api -o json | jq .data.token | base64 -d -i

kubectl get pods --no-headers -o custom-columns=":metadata.name" | grep datadog
kubectl exec $(kubectl get pods --no-headers -o custom-columns=":metadata.name" | grep datadog | head -n 1) -- agent status


// Show labels
kubectl get deployments -n ns1 -l service=advertisements --show-labels
kubectl get pods -n ns1 -l service=advertisements --show-labels


//Get IP
k get pod -o json | jq -r '.items[] | .metadata.name + " - IP: " + .status.podIPs[].ip '


<!-- Helm -->

1) helm install datadogagent --set datadog.apiKey=$DD_API_KEY --set datadog.appKey=$DD_APP_KEY -f values.yaml datadog/datadog


k exec -ti $(k get pods -l app=datadogagent -o jsonpath='{.items[0].metadata.name}') -- agent status

2) helm upgrade datadogagent --set datadog.apiKey=$DD_API_KEY --set datadog.appKey=$DD_APP_KEY -f values.yaml datadog/datadog

#### check the configcheck of agent
3) kubectl exec -ti $(k get pods -l app=datadogagent --field-selector=spec.nodeName=kubernetes -o jsonpath='{.items[0].metadata.name}') -- agent configcheck

### to list the containers
4) kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{range .spec.containers[*]}{.name}{"\n"}{end}{end}'
