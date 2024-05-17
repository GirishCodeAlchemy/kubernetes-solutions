# Kubernetes Templates

## 1. Network Templates

### 1. Allow/Deny all ingress traffic

- If you want to allow all incoming connections to all pods in a namespace, you can create a policy that explicitly allows that.

- similarly selects all pods but does not allow any ingress traffic to those pods.

  <iframe src="./Network/ingress.yml" frameborder="0" width="100%" height="400"></iframe>

### 2. Allow/Deny all egress traffic

- If you want to allow all connections from all pods in a namespace, you can create a policy that explicitly allows all outgoing connections from pods in that namespace.

- Similarly selects all pods but does not allow any egress traffic from those pods.

  <iframe src="./Network/egress.yml" frameborder="0" width="100%" height="400"></iframe>

### 3. To restrict access to Kubernetes pods based on IP addresses

Network Policies allow you to define rules to control traffic to and from pods.
Define a Network Policy: Create a Network Policy manifest file specifying the desired ingress rules to restrict access based on IP addresses.

`cidr`: Specifies the allowed IP CIDR range. Only traffic from IPs within this range will be allowed.

`except`: Optionally, you can specify exceptions to the allowed CIDR range.

  <iframe src="./Network/restrict_pods_based_on_ip_address.yml" frameborder="0" width="100%" height="400"></iframe>

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

  <iframe src="./Deployment/create_dependency_deployment.yml" frameborder="0" width="100%" height="700"></iframe>

### 2. Sidecar container

Sidecar containers are auxiliary containers that run alongside the main application container within the same Kubernetes Pod. They provide additional functionalities such as logging, monitoring, or handling specific tasks without affecting the primary application

  <iframe src="./Deployment/sidecar_deployment.yml" frameborder="0" width="100%" height="550"></iframe>

### 3. Graceful Pod Shutdown with PreStop Hooks

PreStop hooks allow for the execution of specific commands or scripts inside a pod just before it gets terminated. This capability is crucial for ensuring that applications shut down gracefully, saving state where necessary, or performing clean-up tasks to avoid data corruption and ensure a smooth restart.

**When to Use:** Implement PreStop hooks in environments where service continuity is critical, and you need to ensure zero or minimal downtime during deployments, scaling, or pod recycling.

This configuration ensures that the nginx server has 30 seconds to finish serving current requests before shutting down.

```yml
spec:
  containers:
    - name: nginx-container
      image: nginx
      lifecycle:
        preStop:
          exec:
            command: ["/bin/sh", "-c", "sleep 30 && nginx -s quit"]
```

  <iframe src="./Deployment/graceful_pod_shutdown.yml" frameborder="0" width="100%" height="550"></iframe>

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

  <iframe src="./Services/gateway_api_service.yml" frameborder="0" width="100%" height="550"></iframe>

### 2. Service Internal Traffic policy

The Service Internal Traffic Policy in Kubernetes is primarily used to enhance network security and control the flow of traffic within the cluster

Isolation of Internal Services: In a microservices architecture, different services may communicate with each other within the cluster. By setting the Service Internal Traffic Policy to "Local", you can ensure that internal services are only accessible via their ClusterIP, limiting direct access via NodePort and enhancing network segmentation.

  <iframe src="./Services/service_internal_traffic_policy.yml" frameborder="0" width="100%" height="300"></iframe>

## 4. Advanced Template Details

### 1. ResourceQuota

The ResourceQuota kind is used to define these limits and enforce them within a Kubernetes cluster. By setting resource quotas, administrators can prevent resource exhaustion and ensure fair resource allocation among different users or applications within the cluster.

> For example, a resource quota can be set to limit the total amount of CPU and memory that can be consumed by all pods within a namespace. This helps prevent one application from monopolizing cluster resources and affecting the performance of other applications running in the same namespace. Similarly, resource quotas can limit the number of pods or services that can be created to avoid overloading the cluster.

  <iframe src="./AdvanceDetails/resourcequota.yaml" frameborder="0" width="100%" height="500"></iframe>

### 2. Operator Groups

An OperatorGroup in Kubernetes is a resource used to manage the deployment and scaling of operators within a cluster. It allows administrators to specify which namespaces an operator should be deployed to and which RBAC (Role-Based Access Control) rules should be applied to the operator.

> The primary use of OperatorGroup is to define a logical grouping of namespaces where a particular operator should be deployed. This helps in organizing and managing operators across different namespaces within a Kubernetes cluster. By associating an operator with an OperatorGroup, you can control which namespaces the operator has access to and which resources it can manage.

  <iframe src="./AdvanceDetails/operator_group.yml" frameborder="0" width="100%" height="500"></iframe>

### 3. Horizontal Pod Autoscaling

#### Based on Custom Metrics:

Horizontal Pod Autoscaler (HPA) can scale your deployments based on custom metrics, not just standard CPU and memory usage. This is particularly useful for applications with scaling needs tied to specific business metrics or performance indicators, such as queue length, request latency, or custom application metrics

<iframe src="./AdvanceDetails/horizontal_pod_autoscaling_custom_metrics.yml" frameborder="0" width="100%" height="400"></iframe>

#### Based on System Metrics:

Horizontal Pod Autoscaler for an application, ensuring that it scales out when the CPU utilization goes above 50% and scales in when the usage drops, between a minimum of 3 and a maximum of 10 replicas.

<iframe src="./AdvanceDetails/horizontal_pod_autoscaler.yml" frameborder="0" width="100%" height="400"></iframe>

### 4. Node Affinity for Workload-Specific Scheduling

Node affinity allows you to specify rules that limit which nodes your pod can be scheduled on, based on labels on nodes. This is useful for directing workloads to nodes with specific hardware (like GPUs), ensuring data locality, or adhering to compliance and data sovereignty requirements.

**When to Use:** Use node affinity when your applications require specific node capabilities or when you need to control the distribution of workloads for performance optimization, legal, or regulatory reasons.

<iframe src="./AdvanceDetails/node_affinity_workload_schedule.yml" frameborder="0" width="100%" height="400"></iframe>

### 5. Pod Priority and Preemption for Critical Workloads

Kubernetes allows you to assign priorities to pods, and higher priority pods can preempt (evict) lower priority pods if necessary. This ensures that critical workloads have the resources they need, even in a highly congested cluster.

**When to Use:** Use pod priority and preemption for applications that are critical to your business operations, especially when running in clusters where resource contention is common.

<iframe src="./AdvanceDetails/pod_priority_preemption_for_critical_workload.yml" frameborder="0" width="100%" height="500"></iframe>

### 6. Custom Resource Definitions (CRDs) for Extending Kubernetes

CRDs allow you to extend Kubernetes with your own API objects, enabling the creation of custom resources that operate like native Kubernetes objects. This is powerful for adding domain-specific functionality to your clusters, facilitating custom operations, and integrating with external systems.

**When to Use:** CRDs are ideal for extending Kubernetes functionality to meet the specific needs of your applications or services, such as introducing domain-specific resource types or integrating with external services and APIs.

Then a new namespaced RESTful API endpoint is created at:

`/apis/stable.example.com/v1/namespaces/*/crontabs/...`

This endpoint URL can then be used to create and manage custom objects. The kind of these objects will be CronTab from the spec of the CustomResourceDefinition object you created above.

<iframe src="./AdvanceDetails/custom_resource_definations.yml" frameborder="0" width="100%" height="500"></iframe>

```yml
apiVersion: "stable.example.com/v1"
kind: CronTab
metadata:
  name: my-new-cron-object
spec:
  cronSpec: "* * * * */5"
  image: my-awesome-cron-image
```

`kubectl get ct -o yaml`

### 7. Pod Disruption Budgets

Pod Disruption Budgets (PDBs) help ensure that a minimum number of pods are available during voluntary disruptions, such as node maintenance. This ensures high availability without over-provisioning resources.

<iframe src="./AdvanceDetails/pod_disruption_budget.yml" frameborder="0" width="100%" height="500"></iframe>

### 8. Cluster Autoscaler

On AWS, Cluster Autoscaler utilizes Amazon EC2 Auto Scaling Groups to manage node groups. Cluster Autoscaler typically runs as a Deployment in your cluster.

<iframe src="./AdvanceDetails/cluster-autoscaler.yaml" frameborder="0" width="100%" height="1000"></iframe>

Using Mixed Instances Policies and Spot Instances

```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: beta.kubernetes.io/instance-type
                operator: In
                values:
                  - r5.2xlarge
                  - r5d.2xlarge
                  - r5a.2xlarge
                  - r5ad.2xlarge
                  - r5n.2xlarge
                  - r5dn.2xlarge
                  - r4.2xlarge
                  - i3.2xlarge
```

Cluster Auto Scaling policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "autoscaling:DescribeAutoScalingGroups",
        "autoscaling:DescribeAutoScalingInstances",
        "autoscaling:DescribeLaunchConfigurations",
        "autoscaling:DescribeScalingActivities",
        "autoscaling:DescribeTags",
        "ec2:DescribeLaunchTemplateVersions",
        "ec2:DescribeInstanceTypes",
        "ec2:DescribeLaunchTemplateVersions",
        "ec2:GetInstanceTypesFromInstanceRequirements",
        "eks:DescribeNodegroup"
      ],
      "Resource": ["*"]
    },
    {
      "Effect": "Allow",
      "Action": [
        "autoscaling:SetDesiredCapacity",
        "autoscaling:TerminateInstanceInAutoScalingGroup"
      ],
      "Resource": ["*"]
    }
  ]
}
```

IAM role

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "${providerarn}"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "${clusterid}": "system:serviceaccount:kube-system:cluster-autoscaler"
        }
      }
    }
  ]
}
```

#### **Source Ref:**

> OIDC and roles : [https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/CA_with_AWS_IAM_OIDC.md](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/CA_with_AWS_IAM_OIDC.md)

> Autoscaler Document : [https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md)

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

## 7. RBAC

RBAC enforces fine-grained access control policies to Kubernetes resources, using roles and role bindings to restrict permissions within the cluster.

<iframe src="./Security/rbac_template.yml" frameborder="0" width="100%" height="500"></iframe>
