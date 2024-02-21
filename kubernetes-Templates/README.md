# Kubernetes Templates

## Network Templates

1. ### Allow all Ingress

If you want to allow all incoming connections to all pods in a namespace, you can create a policy that explicitly allows that.

[Sample Code](./Network/allow_all_ingress.yml)

2. ### To restrict access to Kubernetes pods based on IP addresses

Network Policies allow you to define rules to control traffic to and from pods.
Define a Network Policy: Create a Network Policy manifest file specifying the desired ingress rules to restrict access based on IP addresses.

`cidr`: Specifies the allowed IP CIDR range. Only traffic from IPs within this range will be allowed.
`except`: Optionally, you can specify exceptions to the allowed CIDR range.

[Sample Code](./Network/restrict_pods_based_on_ip_address.yml)
