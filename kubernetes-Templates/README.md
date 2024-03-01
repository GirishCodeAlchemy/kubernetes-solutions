# Kubernetes Templates

## 1. Network Templates

### 1. Allow/Deny all ingress traffic

- If you want to allow all incoming connections to all pods in a namespace, you can create a policy that explicitly allows that.

- similarly selects all pods but does not allow any ingress traffic to those pods.

[Sample Code](./Network/ingress.yml)

<details>
  <summary>Click to view Sample Code</summary>
  <iframe src="./Network/ingress.yml" frameborder="0" width="100%" height="100%"></iframe>
</details>

### 2. Allow/Deny all egress traffic

- If you want to allow all connections from all pods in a namespace, you can create a policy that explicitly allows all outgoing connections from pods in that namespace.

- Similarly selects all pods but does not allow any egress traffic from those pods.

[Sample Code](./Network/egress.yml)

<details>
  <summary>Click to view Sample Code</summary>
  <iframe src="./Network/egress.yml" frameborder="0" width="100%" height="100%"></iframe>
</details>

### 3. To restrict access to Kubernetes pods based on IP addresses

Network Policies allow you to define rules to control traffic to and from pods.
Define a Network Policy: Create a Network Policy manifest file specifying the desired ingress rules to restrict access based on IP addresses.

`cidr`: Specifies the allowed IP CIDR range. Only traffic from IPs within this range will be allowed.

`except`: Optionally, you can specify exceptions to the allowed CIDR range.

[Sample Code](./Network/restrict_pods_based_on_ip_address.yml)

<details>
  <summary>Click to view Sample Code</summary>
  <iframe src="./Network/restrict_pods_based_on_ip_address.yml" frameborder="0" width="100%" height="100%"></iframe>
</details>

## 2. Deployment Templates

### 1. Create the dependency deployment

using a initContainer, which is just another container in the same pod thats run first, and when it's complete, kubernetes automatically starts the [main] container.

```yaml
initContainers:
  - name: wait-for-main-app
    image: busybox
    command:
      [
        "sh",
        "-c",
        "until wget -qO- main-application:8080/healthz; do sleep 5; done",
      ]
containers:
  - name: main-app
```

using `netcat` to check for open ports

```yaml
initContainers:
  - name: wait-for-services
    image: busybox
    command: ["/bin/sh", "-c"]
    args:
      [
        "until echo 'Waiting for postgres...' && nc -vz -w 2 postgres 5432 && echo 'Waiting for redis...' && nc -vz -w 2 redis 9000; do echo 'Looping forever...'; sleep 2; done;",
      ]
```

[Sample Code](./Deployment/create_dependency_deployment.yml)

<details>
  <summary>Click to view Sample Code</summary>
  <iframe src="./Deployment/create_dependency_deployment.yml" frameborder="0" width="100%" height="100%"></iframe>
</details>

### 2. Sidecar container

Sidecar containers are auxiliary containers that run alongside the main application container within the same Kubernetes Pod. They provide additional functionalities such as logging, monitoring, or handling specific tasks without affecting the primary application

[Sample Code](./Deployment/sidecar_deployment.yml)

<details>
  <summary>Click to view Sample Code</summary>
  <iframe src="./Deployment/sidecar_deployment.yml" frameborder="0" width="100%" height="100%"></iframe>
</details>

## 3. Service Templates

#### 1. Gateway API Service

Gateway API is an official Kubernetes project focused on L4 and L7 routing in Kubernetes. This project represents the next generation of Kubernetes Ingress, Load Balancing, and Service Mesh APIs. From the outset, it has been designed to be generic, expressive, and role-oriented.
![gatewayservice](https://gateway-api.sigs.k8s.io/images/resource-model.png)

![sharedgw](https://gateway-api.sigs.k8s.io/images/gateway-route-binding.png)

##### How it Works¶

The following is required for a Route to be attached to a Gateway:

- The Route needs an entry in its parentRefs field referencing the Gateway.
- At least one listener on the Gateway needs to allow this attachment.

![flow](https://gateway-api.sigs.k8s.io/images/schema-uml.svg)

Gateway API offers a more advanced and flexible approach to managing ingress and egress traffic within Kubernetes clusters, while Ingress provides a simpler and more basic method for routing external traffic to services. Gateway API is intended to replace Ingress and provide a standardized way to manage networking resources in Kubernetes environments.

[Sample Code](./Services/gateway_api_service.yml)

<details>
  <summary>Click to view Sample Code</summary>
  <iframe src="./Services/gateway_api_service.yml" frameborder="0" width="100%" height="100%"></iframe>
</details>

### 2. Service Internal Traffic policy

The Service Internal Traffic Policy in Kubernetes is primarily used to enhance network security and control the flow of traffic within the cluster

Isolation of Internal Services: In a microservices architecture, different services may communicate with each other within the cluster. By setting the Service Internal Traffic Policy to "Local", you can ensure that internal services are only accessible via their ClusterIP, limiting direct access via NodePort and enhancing network segmentation.

[sample code](./Services/service_internal_traffic_policy.yml)

<details>
  <summary>Click to view Sample Code</summary>
  <iframe src="./Services/service_internal_traffic_policy.yml" frameborder="0" width="100%" height="100%"></iframe>
</details>

## 4. Resource Quota Templates

### 1. ResourceQuota

The ResourceQuota kind is used to define these limits and enforce them within a Kubernetes cluster. By setting resource quotas, administrators can prevent resource exhaustion and ensure fair resource allocation among different users or applications within the cluster.

> For example, a resource quota can be set to limit the total amount of CPU and memory that can be consumed by all pods within a namespace. This helps prevent one application from monopolizing cluster resources and affecting the performance of other applications running in the same namespace. Similarly, resource quotas can limit the number of pods or services that can be created to avoid overloading the cluster.

[sample code](./ResourceQuota/resourcequota.yaml)

<details>
  <summary>Click to view Sample Code</summary>
  <iframe src="./ResourceQuota/resourcequota.yaml" frameborder="0" width="100%" height="100%"></iframe>
</details>

## 5. Ingress Templates

<details>
  <summary>Click to expand/collapse</summary>

### 1.

</details>

## 6. Persistent Volume Templates

<details>
  <summary>Click to expand/collapse</summary>

### 1.

</details>
