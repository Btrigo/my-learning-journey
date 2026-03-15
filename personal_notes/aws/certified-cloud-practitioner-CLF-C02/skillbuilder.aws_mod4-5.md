# AWS CLF-C02 — Modules 4 & 5 Study Notes
**Going Global | Networking**

---

# MODULE 4: GOING GLOBAL

---

## 1. AWS Global Infrastructure Overview

AWS operates a global cloud infrastructure made up of **Regions**, **Availability Zones (AZs)**, and **edge locations**. These components work together to deliver high availability, low latency, and scalability.

### Key Benefits

| Benefit | Definition |
|---|---|
| **High Availability** | Systems stay operational even when individual components fail |
| **Elasticity** | Automatically scale resources up or down based on demand |
| **Agility** | Quickly adapt and deploy services in response to changing needs |

> 📌 These are three distinct concepts. The exam will distinguish between them.

---

## 2. Choosing an AWS Region

When selecting a Region, evaluate these four factors **in this order of priority**:

| # | Factor | What It Means | Example |
|---|---|---|---|
| 1 | **Compliance** | Legal/regulatory requirements that dictate where data must reside | GDPR requires EU customer data to stay in Europe → choose Frankfurt |
| 2 | **Proximity** | Distance to your customers affects latency and responsiveness | Most users in Singapore → deploy in ap-southeast-1 |
| 3 | **Feature Availability** | Not all AWS features roll out to all Regions simultaneously | GovCloud Regions have special controls for US government use |
| 4 | **Pricing** | Costs vary by Region due to taxes, energy costs, and local regulations | US East (N. Virginia) is often cheapest for the same services |

> 🎯 **EXAM TIP:** Compliance ALWAYS comes first. If a question mentions regulatory or data residency requirements, the answer is driven by compliance before anything else.

> 📌 Each AWS Region is completely isolated — data does NOT leave a Region without explicit permission from you.

---

## 3. Availability Zones (AZs)

An **Availability Zone** is one or more discrete data centers within a Region, each with independent power, networking, and cooling. AZs are isolated from each other to prevent single points of failure.

### Multi-AZ Architecture
- Deploy resources across multiple AZs for fault tolerance
- If one AZ goes down, traffic automatically fails over to another AZ
- Customers experience no downtime when configured correctly
- Also supports: quicker disaster recovery, improved business continuity, lower latency, compliance

### Multi-Region Architecture
- Deploy entire applications across multiple Regions
- Protects against full Region outages
- Used for global applications and strict availability requirements

> 🎯 **EXAM TIP:** Multi-AZ = protection within a Region. Multi-Region = protection across Regions. Both can be combined.

---

## 4. Edge Locations

Edge locations are **separate from AWS Regions** and are specifically designed to deliver content closer to end users with lower latency. They are part of the **Amazon Global Edge Network**.

| Component | What It Is | Key Point |
|---|---|---|
| **AWS Region** | Geographic area with 3+ AZs | Where you deploy your core infrastructure |
| **Availability Zone** | Isolated data center(s) within a Region | Independent power, networking, cooling |
| **Edge Location** | Globally distributed cache/delivery point | Separate from Regions — used by CloudFront, Route 53, Global Accelerator |

### Services That Use Edge Locations
- **Amazon CloudFront** – CDN that caches content at edge locations
- **Amazon Route 53** – DNS service hosted at edge locations
- **AWS Global Accelerator** – Routes traffic over AWS private global network
- **AWS Outposts** – Extends AWS services to on-premises locations

---

## 5. Infrastructure and Automation

Three main ways to interact with AWS resources:

| Method | Best For | Examples |
|---|---|---|
| **AWS Management Console** | Beginners, visual tasks, billing dashboards | Billing dashboards, Amazon QuickSight, Amazon Neptune |
| **Programmatic Access (CLI/SDK)** | Developers, automation, scripting | CLI: automate routine tasks (e.g., EBS backups). SDK: invoke APIs from app code |
| **Infrastructure as Code (IaC)** | Complex, repeatable, multi-environment deployments | AWS CloudFormation templates |

### AWS CloudFormation

CloudFormation is AWS's **Infrastructure as Code (IaC)** service. You define your infrastructure in a text-based template file and CloudFormation provisions everything automatically.

- Define resources **declaratively** — say WHAT you want, not HOW to build it
- CloudFormation calls the necessary AWS APIs in the background
- Deploy the same template across multiple Regions or accounts = identical environments
- Reduces human error — fully automated process
- Track infrastructure changes via source control

**CloudFormation Use Cases:**
- Managing infrastructure with DevOps CI/CD pipelines
- Scaling EC2 instances to multi-Region deployments consistently
- Replicating dev/staging/prod environments identically

> 🎯 **EXAM TIP:** CloudFormation = Infrastructure as Code. Any question about consistent, repeatable, automated deployments across environments or Regions → CloudFormation.

---

# MODULE 5: NETWORKING

---

## 6. Amazon VPC (Virtual Private Cloud)

A **VPC** is your own private, isolated network within the AWS Cloud. You define the IP address range, create subnets, and control all traffic in and out using gateways and security rules.

### VPC Benefits
- **Increase security** – monitor connections, screen traffic, restrict access
- **Save time** – less overhead than managing on-premises networks
- **Control environment** – full control over resource placement, connectivity, and security

### Subnets

A subnet is a section of a VPC used to group resources based on security or operational needs.

| Subnet Type | Internet Access | Use Case | Gateway Used |
|---|---|---|---|
| **Public Subnet** | Yes | Web servers, load balancers, public-facing resources | Internet Gateway (IGW) |
| **Private Subnet** | No (by default) | Databases, app servers, internal services | None (or NAT Gateway for outbound only) |

> 🎯 **EXAM TIP:** Public subnet = has a route to an Internet Gateway. Private subnet = no route to IGW.

### Route Tables

Route tables control how traffic leaves a subnet. Every subnet must be associated with a route table.

- Each route has a **Destination** (e.g., `0.0.0.0/0` = all internet traffic) and a **Target** (IGW, NAT, VGW, etc.)
- Public subnets: route `0.0.0.0/0` → Internet Gateway
- Private subnets: no route to internet (or route `0.0.0.0/0` → NAT Gateway for outbound only)

---

## 7. Gateways and Connectivity Options

### Internet Gateway (IGW)
- Connects your VPC to the **public internet**
- Attached to the VPC (not to individual subnets)
- Subnets gain internet access via their route table pointing to the IGW
- Required for any public-facing resource

### Virtual Private Gateway (VGW)
- The AWS-side component that enables **VPN connections** into your VPC
- Creates an encrypted tunnel from an on-premises network to your VPC
- Traffic still travels over the public internet but is encrypted
- Only allows traffic from approved networks

> 📌 Virtual Private Gateway ≠ VPN. The VGW is the door on the AWS side. The VPN is the encrypted road connecting to it.

### NAT Gateway
- Placed in a **PUBLIC** subnet
- Allows instances in **PRIVATE** subnets to initiate outbound internet connections
- External services **CANNOT** initiate connections back to private instances
- Use case: Private EC2 instances downloading OS updates, pulling from external APIs

> 🎯 **EXAM TIP:** VGW connects your VPC to YOUR private corporate network. NAT Gateway lets private subnet resources reach the PUBLIC internet outbound only. These solve completely different problems.

---

## 8. More Ways to Connect to AWS Cloud

| Service | What It Does | Use Case | Key Characteristic |
|---|---|---|---|
| **AWS Client VPN** | Managed VPN for remote workers | Remote employees accessing AWS or on-prem resources from anywhere | Elastic, fully managed, OpenVPN-based |
| **AWS Site-to-Site VPN** | Encrypted tunnel between on-prem sites and AWS VPC | Branch offices, data centers connecting to AWS | Uses VGW, runs over public internet |
| **AWS Direct Connect** | Dedicated private physical fiber connection to AWS | High bandwidth, compliance requirements, large data transfers | NOT over internet — dedicated line, lower latency |
| **AWS PrivateLink** | Private connection from your VPC to AWS services or other VPCs | Access AWS services without internet exposure | No internet gateway or public IP needed |

### VPN vs Direct Connect Decision Guide

| Scenario | Use |
|---|---|
| Secure, flexible connection for remote access or small data | VPN (Site-to-Site or Client VPN) |
| High bandwidth, large data transfers, dedicated line | Direct Connect |
| Both needed (failover + high bandwidth) | Direct Connect primary + VPN as failover |
| Multiple connections for higher aggregate bandwidth | Multiple Direct Connect connections |
| Healthcare, finance, strict compliance + heavy data | Direct Connect (bandwidth + compliance) |

> 🎯 **EXAM TIP:** Direct Connect = physical dedicated fiber = not over internet. VPN = encrypted tunnel over internet. Heavy data + compliance → Direct Connect.

---

## 9. Network Security: NACLs and Security Groups

| Feature | Security Groups | Network ACLs |
|---|---|---|
| **Scope** | Instance level (attached to EC2 instances) | Subnet level (associated with subnets) |
| **State** | STATEFUL – remembers previous decisions | STATELESS – checks every packet every time |
| **Rule Types** | Allow rules only (no explicit deny) | Both Allow AND Deny rules |
| **Return Traffic** | Automatically allowed (stateful memory) | Must be explicitly allowed in both directions |
| **Default Behavior** | Deny all inbound, Allow all outbound | Default NACL: allow all. Custom NACL: deny all until rules added |
| **Explicit Deny** | No | Yes — all NACLs have a catch-all deny at the end |
| **Best Used For** | Fine-grained control per instance | Broad traffic control at the subnet boundary |

### Analogies (from the module)
- **Network ACL** = Passport control at an airport — checks everyone entering AND leaving, every single time
- **Security Group** = Building doorman — checks everyone coming IN, waves everyone going OUT without checking

### Packet Flow: Instance A → Instance B (Different Subnets)

| Step | Checkpoint | Behavior |
|---|---|---|
| 1 | Security Group of Instance A (outbound) | Stateful — all outbound allowed by default |
| 2 | NACL of Subnet A (outbound) | Stateless — checks outbound rules list |
| 3 | NACL of Subnet B (inbound) | Stateless — checks inbound rules list |
| 4 | Security Group of Instance B (inbound) | Stateful — checks inbound allow rules |
| Return 4 | Security Group of B (outbound) | Stateful — automatically allows return traffic |
| Return 3 | NACL of Subnet B (outbound) | Stateless — checks outbound rules again |
| Return 2 | NACL of Subnet A (inbound) | Stateless — checks inbound rules again |
| Return 1 | Security Group of A (inbound) | Stateful — automatically allows return traffic |

> 🎯 **EXAM TIP:** NACLs are stateless = they check the list EVERY TIME including return traffic. Security groups are stateful = return traffic is automatically allowed.

> 📌 **Shared Responsibility:** Configuring NACLs and security groups is YOUR responsibility as the customer, not AWS's.

---

## 10. Global Networking: DNS, CDN, and Edge Services

### Amazon Route 53

Route 53 is AWS's **DNS (Domain Name System)** service. DNS translates human-readable domain names (like amazon.com) into machine-readable IP addresses (like 192.0.2.0).

- Globally distributed DNS with automatic scaling
- Routes users to EC2 instances, load balancers, S3, and infrastructure outside AWS
- Register and manage domain names directly in Route 53

**Routing Policies:**
- **Latency-based** – Routes to the Region with lowest latency for the user
- **Geolocation** – Routes based on where the user is physically located
- **Geoproximity** – Routes based on geographic proximity to resources
- **Weighted round robin** – Distributes traffic across multiple endpoints by weight
- **Failover** – Routes to a healthy endpoint when primary is unhealthy

### Amazon CloudFront

CloudFront is AWS's **Content Delivery Network (CDN)**. It caches copies of your content at edge locations around the world so users receive content from the nearest location rather than your origin server.

- Reduces latency — content served from geographically nearby edge locations
- Reduces load on origin servers — cached content served directly from edge
- Works with Route 53, Application Load Balancers, EC2, and S3

**Use Cases:**
- Streaming video – Smooth playback without buffering for global users
- E-commerce websites – Fast product images/pages during peak shopping
- Mobile apps – Quick delivery of map data and media globally

### AWS Global Accelerator

Uses the **AWS private global network** (not the public internet) to route traffic to your application, improving performance, availability, and security.

- Uses static Anycast IPs as entry points
- Directs traffic through AWS backbone — bypasses congested internet routes
- Fast failover if an application endpoint becomes unhealthy

### Edge Services Comparison

| Service | Layer | How It Works | Best For |
|---|---|---|---|
| **Route 53** | DNS layer | Translates domain names to IPs using routing policies | Directing users to the right Region or endpoint |
| **CloudFront** | Application/HTTP layer | Caches content at edge locations globally | Static content, media, websites |
| **Global Accelerator** | Network layer | Routes traffic via AWS private backbone using Anycast IPs | Dynamic content, latency-sensitive apps, gaming, finance |

> 🎯 **EXAM TIP:** CloudFront = CDN = caches CONTENT at edge locations. Global Accelerator = routes TRAFFIC over AWS private network. Route 53 = DNS. These serve different purposes and are commonly confused on the exam.

---

## 11. How Route 53 and CloudFront Work Together

Standard request flow for a globally distributed web application:

| Step | What Happens |
|---|---|
| 1 – Customer request | User types anycompany.com in browser |
| 2 – Route 53 DNS resolution | Route 53 resolves the domain and applies its routing policy to find the best Region |
| 3 – CloudFront edge location | Request is routed to the nearest CloudFront edge location |
| 4 – Origin fetch | CloudFront retrieves content from the origin (ALB → EC2 in the chosen Region) |
| Return | Content delivered to the user with low latency |

---

## 12. Quick Reference: Service One-Liners

| Service | One-Liner |
|---|---|
| **CloudFormation** | Infrastructure as Code — deploy infrastructure from a template |
| **VPC** | Your private isolated network in AWS |
| **Internet Gateway** | The front door connecting your VPC to the internet |
| **Virtual Private Gateway** | The VPN door connecting your VPC to your corporate network |
| **NAT Gateway** | Lets private instances call out to internet but blocks inbound calls |
| **AWS Client VPN** | VPN for remote workers connecting to AWS |
| **Site-to-Site VPN** | Encrypted tunnel for offices/data centers connecting to AWS |
| **Direct Connect** | Dedicated private fiber — no internet, high bandwidth |
| **PrivateLink** | Private VPC-to-service connection with no internet exposure |
| **Network ACL** | Stateless passport control at the subnet border |
| **Security Group** | Stateful doorman at the EC2 instance door |
| **Route 53** | DNS — translates domain names to IP addresses |
| **CloudFront** | CDN — caches content at edge locations near users |
| **Global Accelerator** | Routes traffic via AWS private backbone for performance |