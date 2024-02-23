# Kubernetes Templates

## 1. Network Templates

<details>
  <summary>Click to expand/collapse</summary>

### 1. Allow/Deny all ingress traffic

- If you want to allow all incoming connections to all pods in a namespace, you can create a policy that explicitly allows that.

- similarly selects all pods but does not allow any ingress traffic to those pods.

[Sample Code](./Network/ingress.yml)

### 2. Allow/Deny all egress traffic

- If you want to allow all connections from all pods in a namespace, you can create a policy that explicitly allows all outgoing connections from pods in that namespace.

- Similarly selects all pods but does not allow any egress traffic from those pods.

[Sample Code](./Network/egress.yml)

### 3. To restrict access to Kubernetes pods based on IP addresses

Network Policies allow you to define rules to control traffic to and from pods.
Define a Network Policy: Create a Network Policy manifest file specifying the desired ingress rules to restrict access based on IP addresses.

`cidr`: Specifies the allowed IP CIDR range. Only traffic from IPs within this range will be allowed.

`except`: Optionally, you can specify exceptions to the allowed CIDR range.

[Sample Code](./Network/restrict_pods_based_on_ip_address.yml)

</details>

## 2. Deployment Templates

<details>
  <summary>Click to expand/collapse</summary>

### 1. Create the dependency deployment
using a initContainer, which is just another container in the same pod thats run first, and when it's complete, kubernetes automatically starts the [main] container.

``` yaml
initContainers:
- name: wait-for-main-app
  image: busybox
  command: ['sh', '-c', 'until wget -qO- main-application:8080/healthz; do sleep 5; done']
containers:
- name: main-app
```
using `netcat` to check for open ports
```yaml
initContainers:
- name: wait-for-services
  image: busybox
  command: ["/bin/sh","-c"]
  args: ["until echo 'Waiting for postgres...' && nc -vz -w 2 postgres 5432 && echo 'Waiting for redis...' && nc -vz -w 2 redis 9000; do echo 'Looping forever...'; sleep 2; done;"]
```
[Sample Code](./Deployment/create_dependency_deployment.yml)

### 2. Sidecar container

Sidecar containers are auxiliary containers that run alongside the main application container within the same Kubernetes Pod. They provide additional functionalities such as logging, monitoring, or handling specific tasks without affecting the primary application

[Sample Code](./Deployment/sidecar_deployment.yml)

</details>

## 3. Service Templates

<details>
  <summary>Click to expand/collapse</summary>

### 1.

</details>

## 4. Ingress Templates

<details>
  <summary>Click to expand/collapse</summary>

### 1.

</details>

## 5. Persistent Volume Templates

<details>
  <summary>Click to expand/collapse</summary>

### 1.

</details>
