# AWS Cloud Practitioner (CLF-C02) — Modules 1–3 Study Notes

---

## Module 1 – Introduction to the Cloud

### What Is Cloud Computing?

On-demand delivery of IT resources over the internet with pay-as-you-go pricing.

### NIST Five Key Characteristics

> Note: These are NIST's cloud characteristics. On the exam, AWS focuses on its **Six Benefits** below.

- On-demand self-service
- Broad network access
- Resource pooling
- Rapid elasticity
- Measured service (pay only for what you use)

### AWS Six Benefits of Cloud Computing

1. Trade CapEx for OpEx
2. Benefit from massive economies of scale
3. Stop guessing capacity
4. Increase speed and agility
5. Stop spending money running and maintaining data centers
6. Go global in minutes

### Cloud Deployment Models

| Model | Description |
|-------|-------------|
| **Public Cloud** | Infrastructure owned and operated by AWS |
| **Private Cloud** | Infrastructure used exclusively by one organization |
| **Hybrid Cloud** | Combination of on-premises + cloud (e.g., AWS Outposts) |

### Cloud Service Models

| Model | Example | You Manage | AWS Manages |
|-------|---------|------------|-------------|
| **IaaS** | Amazon EC2 | OS, apps, data, networking | Physical hardware, hypervisor |
| **PaaS** | AWS Elastic Beanstalk | Application, data | Infrastructure, runtime, scaling |
| **SaaS** | Amazon WorkDocs | Nothing — just use it | Everything |

> **Rule of thumb:** Higher abstraction = less customer responsibility.

### AWS Shared Responsibility Model

**AWS is responsible for security *of* the cloud:**
- Physical data centers
- Hardware
- Global infrastructure
- Managed service runtimes

**Customer is responsible for security *in* the cloud:**
- Data
- IAM configuration
- Application code
- OS (if using EC2)
- Security groups & NACLs

---

## Module 2 – Compute in the Cloud

### Amazon EC2

Virtual machines running in AWS. You choose the instance type, AMI, storage, networking, and security groups.

#### EC2 Instance Categories

| Type | Best For |
|------|----------|
| General Purpose | Balanced CPU/memory (web servers, dev environments) |
| Compute Optimized | High CPU workloads (gaming, HPC, scientific modeling) |
| Memory Optimized | High RAM workloads (in-memory databases, real-time analytics) |
| Storage Optimized | High disk throughput (data warehouses, distributed file systems) |
| Accelerated Computing | GPU / ML workloads (machine learning inference, graphics rendering) |

#### EC2 Pricing Models

| Model | Description |
|-------|-------------|
| **On-Demand** | No commitment, pay by the hour/second |
| **Reserved Instances** | 1–3 year commitment, up to 72% savings |
| **Savings Plans** | Flexible usage commitment — *Compute* (EC2, Lambda, Fargate) or *EC2 Instance* (more restrictive, deeper discount) |
| **Spot Instances** | Discounted spare capacity — can be interrupted with 2-min notice |
| **Dedicated Hosts** | Physical server dedicated to you (compliance/licensing needs) |
| **Capacity Reservations** | Reserve capacity in a specific AZ with no term commitment |

> **Exam tip:** Spot = interruptible workloads. Reserved/Savings Plans = predictable, long-term workloads.

### Auto Scaling

Automatically adjusts EC2 capacity based on demand.

- Maintains desired capacity
- Improves availability
- Reduces cost by scaling down when demand drops

### Elastic Load Balancing (ELB)

Distributes incoming traffic across multiple instances.

- Improves high availability and fault tolerance
- Integrates with Auto Scaling
- Works across multiple Availability Zones

### AWS Lambda

Fully serverless, event-driven compute.

| Characteristic | Detail |
|---------------|--------|
| Trigger | Event-driven (S3 upload, API call, schedule, etc.) |
| Max runtime | 15 minutes per invocation |
| Scaling | Automatic |
| State | Stateless |
| Billing | Per invocation + per 100ms of compute time |

**Best for:** Event-based processing, backend APIs, automation, data transformations.

---

## Module 3 – Exploring Compute Services

### Containers vs. Virtual Machines

| | Virtual Machines | Containers |
|--|-----------------|------------|
| OS | Full OS per instance | Shares host OS |
| Size | Heavier | Lightweight |
| Portability | Lower | Higher |
| Startup | Slower | Faster |

### Container Services

#### Amazon ECR (Elastic Container Registry)

Stores and manages container images. Used as the source for ECS and EKS deployments.

#### Amazon ECS (Elastic Container Service)

AWS-native container orchestration.

- Schedules containers, manages scaling, monitors health
- Integrates with load balancers

| Launch Type | Description |
|-------------|-------------|
| **EC2 mode** | You manage the underlying EC2 instances |
| **Fargate mode** | Serverless — no instance management |

#### Amazon EKS (Elastic Kubernetes Service)

Managed Kubernetes service. Choose EKS when your team already uses Kubernetes and wants AWS to manage the control plane without running it themselves.

> **ECS vs EKS:** ECS is AWS-native and simpler. EKS is for teams with existing Kubernetes expertise or tooling.

#### AWS Fargate

Serverless compute engine for containers. Works with both ECS and EKS.

- No EC2 management
- Pay per CPU and memory used
- Use cases: microservices, APIs, containerized applications

### Other Compute Services

#### AWS Elastic Beanstalk

Managed application deployment platform — give it your code, it handles the rest.

AWS provisions: EC2, Auto Scaling, Load Balancer, and Monitoring.

Best for: web applications, REST APIs, developers who want to avoid infrastructure management.

#### AWS Batch

Managed batch job scheduling for large-scale parallel workloads.

- ML training, simulations, big data processing
- Not for real-time workloads

#### Amazon Lightsail

Simplified VPS hosting at a fixed monthly price.

- Includes compute, storage, and networking
- Best for: small websites, blogs, low-traffic apps

#### AWS Outposts

Hybrid cloud solution — AWS hardware installed in your on-premises environment.

- Uses the same AWS APIs and services
- Use cases: low latency, data residency requirements, regulatory compliance

---

## Compute Abstraction Ladder

```
EC2                   →  Full control, full responsibility
ECS (EC2 mode)        →  Orchestration + you manage servers
ECS + Fargate         →  Serverless containers
Lambda                →  Fully serverless functions
```

> Higher on the ladder = less operational overhead = less control.

---

## Exam Pattern Recognition Cheat Sheet

| Scenario | Answer |
|----------|--------|
| Event-driven / trigger-based compute | **Lambda** |
| Container image stored in registry | **ECR → ECS or EKS** |
| Containers without managing servers | **Fargate** |
| Simple web app deployment | **Elastic Beanstalk** |
| Large-scale parallel compute workloads | **Batch** |
| Basic VPS / simple hosted app | **Lightsail** |
| Hybrid / on-premises AWS extension | **Outposts** |
| Kubernetes orchestration, managed control plane | **EKS** |
| AWS-native container orchestration | **ECS** |
| Flexible compute commitment across services | **Compute Savings Plan** |
| Reserve capacity, no term commitment | **Capacity Reservation** |

---

*Last updated: February 2026 | CLF-C02 prep*