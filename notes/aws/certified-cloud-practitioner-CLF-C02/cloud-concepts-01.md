# Domain 1: Cloud Concepts — Full Review (CLF-C02)

Domain 1 establishes the foundational knowledge of cloud computing, AWS global infrastructure, shared responsibility, cloud economics, and the general benefits of using AWS services. This domain prepares you to understand *what* the cloud is, *why* organizations move to AWS, and *how* AWS structures its global platform.

---

## 1.0 What Is Cloud Computing?

Cloud computing is the **on-demand delivery of compute, storage, networking, databases, and higher-level services** over the internet with **pay-as-you-go pricing**.

### 1.1 Five Essential Characteristics of Cloud Computing
(AWS uses these constantly in exams)

1. **On-Demand Self-Service**  
   - Provision cloud resources without human approval.  
   - Spin up compute/storage immediately.

2. **Broad Network Access**  
   - Access via the internet using standardized methods:  
     - Console  
     - CLI  
     - SDKs  
     - APIs

3. **Resource Pooling (Multi-Tenancy)**  
   - AWS resources serve multiple customers.  
   - Customers’ data and workloads remain isolated logically.

4. **Rapid Elasticity**  
   - Scale out/in automatically or manually.  
   - Scale up/down by choosing bigger or smaller instance sizes.

5. **Measured Service (Metering & Pay-As-You-Go)**  
   - Usage is tracked and billed based on:
     - GB-month  
     - vCPU-hours  
     - Requests  
     - Data transfer  

---

## 2.0 Benefits of Cloud Computing (Why Businesses Move to AWS)

AWS repeatedly emphasizes the following benefits:

### 2.1 Agility  
- Deploy infrastructure quickly.  
- Rapidly experiment and release new ideas.

### 2.2 Elasticity  
- Match capacity with traffic in real time.  
- Avoid over-provisioning servers.

### 2.3 High Availability & Fault Tolerance  
- Use **multi-AZ** architectures.  
- Build redundancy at every layer.

### 2.4 Global Reach  
- Deploy applications in **Regions worldwide**.  
- Serve users with low latency.

### 2.5 Cost Optimization  
- Move from **CapEx → OpEx**.  
- Only pay for what you consume.  
- Benefit from AWS “economies of scale.”

### 2.6 No Data Center Heavy Lifting  
AWS handles:
- Power  
- Cooling  
- Physical hardware  
- Security guards  
- Network infrastructure  
- Hardware lifecycle management  

You focus on developing your applications.

---

## 3.0 AWS Global Infrastructure

Understanding the global infrastructure is **critical** to the Cloud Practitioner exam.

### 3.1 Regions  
- A **geographic** area with multiple Availability Zones.  
- Example: `us-east-1`, `eu-west-1`.  
- Choose Regions based on:
  - Latency  
  - Compliance & regulatory requirements  
  - Service availability  
  - Pricing differences  

### 3.2 Availability Zones (AZs)  
- Each AZ consists of one or more data centers.  
- Connected by high-throughput, low-latency networking.  
- Deploy resources across AZs for:
  - High availability  
  - Fault tolerance  

### 3.3 Edge Locations  
Used by:
- **Amazon CloudFront (CDN)**  
- **Route 53 (DNS)**  
- **AWS Global Accelerator**

Purpose:
- Deliver content with low latency  
- Improve user experience across the globe  

---

## 4.0 Shared Responsibility Model

A foundational concept. Memorize this.

### 4.1 AWS Responsibility: “Security **of** the Cloud”
AWS manages:
- Physical data centers  
- Hardware  
- Networking  
- Hypervisors  
- Global infrastructure  
- Managed service maintenance  
- Managed service patching (e.g., RDS OS)

### 4.2 Customer Responsibility: “Security **in** the Cloud”
Customers manage:
- IAM  
- MFA  
- OS patching on EC2  
- Application code  
- S3 bucket permissions  
- Security groups & NACLs  
- Data classification and encryption choices  

### 4.3 Key Exam Traps  
Memorize these distinctions:

- **EC2 patching** → Customer responsibility  
- **RDS patching** → AWS responsibility  
- **S3 bucket permissions** → Customer  
- **Availability of global infrastructure** → AWS  
- **Client-side encryption** → Customer  

---

## 5.0 Compute Fundamentals (High-Level)

Domain 1 introduces compute only at a conceptual level.

### 5.1 Amazon EC2 (Virtual Servers)  
EC2 = Infrastructure as a Service (IaaS).  
You control:
- OS  
- Patching  
- Security groups  
- Applications  
- Data  
- IAM roles for the instance  

Key EC2 Concepts:
- **Instance types**: CPU, memory, storage optimized  
- **Instance families**: General purpose, compute optimized, memory optimized  
- **T-series (t2.micro / t3.micro)**:
  - Burstable CPU  
  - Common Free Tier examples  
- **AMIs**  
- **User data** (boot-time automation)

### 5.2 AWS Lambda (Serverless Compute)
- No servers to manage  
- Pay only per invocation and compute time  
- Automatically scales  
- Event-driven (API Gateway, S3 events, etc.)

### 5.3 Containers (High Level Only)
- **ECS** – Amazon’s container orchestration  
- **EKS** – Managed Kubernetes  
- **Fargate** – Serverless compute for containers  

---

## 6.0 Storage Fundamentals

Domain 1 focuses on **categories**, not deep technical configuration.

### 6.1 Amazon S3 (Object Storage)
- 11 “nines” durability (99.999999999%)  
- Global namespace (bucket names must be unique)  
- Virtually infinite scaling  
- Storage Classes:
  - S3 Standard  
  - S3 Standard-IA  
  - S3 Intelligent-Tiering  
  - Glacier Instant Retrieval  
  - Glacier Flexible Retrieval  
  - Glacier Deep Archive

### 6.2 EBS (Block Storage)
- Attach to EC2 instances  
- Persistent block volumes  
- Good for databases and file systems  

### 6.3 EFS (Network File System)
- Scales automatically  
- Multi-AZ  
- Shared file storage across multiple EC2 instances  

---

## 7.0 Networking Fundamentals

Domain 1 doesn’t expect network engineering depth — just high-level understanding.

### 7.1 Amazon VPC (Virtual Private Cloud)
- Your logically isolated section of AWS  
- You define:
  - IP ranges (CIDR blocks)  
  - Subnets  
  - Routing  
  - Security rules  

### 7.2 Subnets
- Public subnets → internet-facing  
- Private subnets → internal-only  

### 7.3 Security Groups (SGs)
- Virtual firewalls **for EC2 instances**  
- **Stateful**  
- Default deny  

### 7.4 Network ACLs (NACLs)
- Firewall rules applied at the subnet level  
- **Stateless**  
- Rule evaluation in order  

### 7.5 Routing
- Route tables determine traffic flow  
- Internet Gateway → outbound internet access  
- NAT Gateway → private subnet internet access  

---

## 8.0 Migration Concepts

Domain 1 reviews AWS migration fundamentals.

### 8.1 Why Organizations Migrate
- Reduce operational overhead  
- Improve agility  
- Enhance security posture  
- Scale globally  
- Save costs  
- Increase performance  

### 8.2 Migration Tools
- **AWS Application Migration Service (MGN)** – Lift-and-shift  
- **AWS Database Migration Service (DMS)** – Move databases  
- **AWS Snow Family** – Physical devices for large data migrations  
- **AWS Migration Hub** – Central tracking  

### 8.3 Cloud Adoption Framework (CAF)
6 perspectives:
- Business  
- People  
- Governance  
- Platform  
- Security  
- Operations  

---

## 9.0 Cloud Economics Fundamentals

Critical for exam questions and real-world interviews.

### 9.1 CapEx vs OpEx  
**CapEx (on-prem):**
- Buying servers  
- Data center costs  
- Long-term depreciation  

**OpEx (cloud):**
- Pay only for consumption  
- Scales with usage  

### 9.2 Variable vs Fixed Costs  
- Cloud ≈ Variable  
- On-prem ≈ Fixed  

### 9.3 AWS Pricing Advantages  
- Pay-as-you-go  
- Volume discounts  
- No upfront commitments (optional)  
- Free Tier for many services  
- Reduced operational burden  

### 9.4 Cost Optimization Concepts
- **Rightsizing**
- **Auto Scaling**
- **Use the correct storage class**
- **Turn off unused resources**
- **Choose appropriate pricing models:**
  - On-Demand  
  - Reserved Instances (EC2, RDS)  
  - Savings Plans  
  - Spot Instances  

---

## 10.0 Core AWS Service Categories (Mapped to Domain 1)

| Category        | Common Services |
|-----------------|----------------|
| Compute         | EC2, Lambda, ECS, EKS, Fargate |
| Storage         | S3, EBS, EFS |
| Networking      | VPC, Route 53, NACLs, SGs, IGW |
| Databases       | RDS, Aurora, DynamoDB |
| Security        | IAM, KMS, WAF, Shield |
| Management      | CloudWatch, CloudTrail, Config |
| Edge / Global   | CloudFront, Global Accelerator |

---

## 11.0 Domain 1 Exam Tips You MUST Know

1. **EC2 patching is your responsibility — RDS patching is AWS’s.**  
2. **t2.micro / t3.micro** = Free Tier compute example.  
3. **S3 durability is 11 nines.**  
4. **Security groups are stateful; NACLs are stateless.**  
5. **Regions are separate; AZs are isolated within a region.**  
6. **CloudFront = CDN / edge caching.**  
7. **Lambda = serverless compute, pay per invocation.**  
8. **CapEx vs OpEx** questions appear often.  
9. **Migration tools** — know MGN, DMS, Snowball.  
10. **Cloud benefits** — agility, elasticity, HA, pay-as-you-go.

---

# ✔ End of Domain 1 Review  