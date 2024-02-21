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

### 1.

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
