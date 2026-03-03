# AWS Module 6 — Storage Services Comprehensive Notes

---

# 1️⃣ Storage Categories in AWS

AWS storage services fall into three core types:

| Storage Type   | Service             | Best For                                  |
|---------------|--------------------|-------------------------------------------|
| Object Storage | Amazon S3          | Static assets, backups, media, data lakes |
| Block Storage  | Amazon EBS, EC2 Instance Store | Databases, transactional workloads |
| File Storage   | Amazon EFS, Amazon FSx | Shared file systems |

Understanding this distinction is critical for architecting correctly.

---

# 2️⃣ Amazon S3 (Simple Storage Service)

## Core Definition

Scalable object storage used to store and retrieve any amount of data from anywhere on the web.

---

## Fundamental Concepts

- Data is stored as **objects**
- Objects are stored inside **buckets**
- Each object includes:
  - Key (object name)
  - Value (actual data)
  - Metadata
  - Version ID (if versioning enabled)

---

## Object Limits

- Maximum object size: **5 TB**
- Bucket size: **Unlimited**

---

## Durability & Availability

- **11 9’s durability (99.999999999%)**
- Data stored redundantly across multiple Availability Zones
- Fully managed by AWS

---

## S3 Storage Classes

| Storage Class | Use Case |
|--------------|----------|
| S3 Standard | Frequently accessed data |
| S3 Standard-IA | Infrequent access |
| S3 One Zone-IA | Infrequent access in a single AZ |
| S3 Glacier Instant Retrieval | Archive with immediate retrieval |
| S3 Glacier Flexible Retrieval | Archive with minutes–hours retrieval |
| S3 Glacier Deep Archive | Long-term archive (up to 12-hour restore) |
| S3 Intelligent-Tiering | Automatic cost optimization |

### Pricing Factors

- Storage cost per GB
- Data retrieval fees (for certain classes)
- Minimum storage duration requirements

---

## S3 Lifecycle Policies

Lifecycle policies automate:

- Moving objects between storage classes
- Deleting objects after a defined period

Used for cost optimization and data lifecycle management.

---

# 🔐 S3 Security (High Emphasis)

## Default Behavior

- All buckets and objects are **private by default**
- Block Public Access is enabled by default

---

## Identity-Based Policies

Implemented through **AWS IAM**.

IAM policies are attached to:

- Users
- Groups
- Roles

They define what actions identities can perform on S3 resources.

---

## Resource-Based Policies

### Bucket Policies

- JSON-based
- Attached directly to the bucket
- Define who can access the bucket and objects
- Can allow cross-account access

Policy structure includes:

- Effect (Allow / Deny)
- Principal
- Action
- Resource
- Condition

---

## Presigned URLs

- Provide temporary access to objects
- Time-limited
- No need to modify bucket policies
- Used for secure file sharing

---

## Object-Level Features

- Server-side encryption (SSE-S3, SSE-KMS)
- Checksums
- Object tags
- Custom metadata
- Object Lock
- Versioning

---

# 🧭 S3 Walkthrough Key Areas (Console Focus)

## Bucket Creation

- Globally unique bucket name required
- Select AWS Region
- Block Public Access enabled by default
- Default encryption can be configured

---

## Properties Tab

Configure:

- Versioning
- Default encryption
- Lifecycle rules
- Intelligent-Tiering
- Static website hosting
- Replication
- Tags

---

## Permissions Tab

Configure:

- Block Public Access
- Bucket Policy
- Object Ownership
- CORS (Cross-Origin Resource Sharing)
- ACLs (legacy access method)

---

## Management Tab

Configure:

- Lifecycle configuration
- Replication rules
- Inventory reports

---

# 🌐 Static Website Hosting (S3)

Used for:

- Hosting HTML, CSS, JavaScript
- Static assets

S3 automatically scales to handle traffic.
You pay for storage and data transfer.

---

# 3️⃣ Amazon EBS (Elastic Block Store)

## Core Definition

Persistent block storage volumes for Amazon EC2 instances.

---

## Characteristics

- Availability Zone–scoped
- Attached to EC2 instances
- Low latency
- Can be resized without downtime
- Supports point-in-time snapshots
- Commonly used for databases

---

## Volume Types

- gp3 — General Purpose SSD
- io2 — Provisioned IOPS SSD
- st1 — Throughput optimized HDD
- sc1 — Cold HDD

---

## When to Use

- Transactional databases
- Applications requiring consistent low latency
- Block-level storage needs

---

# 4️⃣ EC2 Instance Store

## Definition

Temporary block storage physically attached to the host machine.

---

## Characteristics

- Highest I/O performance
- Data lost if instance stops or terminates
- Not persistent

---

## Use Cases

- Temporary ML training data
- Scratch space
- Caching

---

# 5️⃣ Amazon EFS (Elastic File System)

## Core Definition

Fully managed, elastic NFS file system for Linux workloads.

---

## Key Characteristics

- Regional (not limited to a single AZ)
- Automatically scales
- Multiple EC2 instances can access simultaneously
- No capacity planning required
- POSIX-compliant
- High durability

---

## When to Use

- Shared file systems
- Development environments
- Media workflows
- Multi-instance Linux applications

---

# 6️⃣ Amazon FSx

Fully managed file systems designed for specific workloads.

## Variants

- FSx for Windows File Server (SMB + Active Directory)
- FSx for Lustre (High-performance computing)
- FSx for NetApp ONTAP

Used when specialized file system features are required.

---

# 7️⃣ AWS Storage Gateway

## Core Definition

Hybrid cloud storage solution connecting on-premises environments to AWS.

---

## Types

### S3 File Gateway

- Provides NFS/SMB access
- Stores data as S3 objects

### Volume Gateway

- Provides iSCSI block storage
- Data backed by EBS snapshots in AWS

### Tape Gateway

- Virtual Tape Library (VTL)
- Stores backups in S3 Glacier

---

## Use Cases

- Hybrid backup
- Disaster recovery
- Gradual cloud migration

---

# 8️⃣ iSCSI Block (Clarification)

iSCSI = Internet Small Computer Systems Interface

- Transmits SCSI commands over IP networks
- Used by Volume Gateway
- Presents block storage over the network

Applications see it as a local disk.

---

# 9️⃣ Scenario-Based Architecture Decisions

Static website hosting  
→ Amazon S3  

High-performance database  
→ Amazon EBS (Provisioned IOPS)  

Shared Linux file system  
→ Amazon EFS  

Windows file share with Active Directory  
→ Amazon FSx for Windows  

Temporary high-performance scratch storage  
→ EC2 Instance Store  

Hybrid backup from on-premises  
→ AWS Storage Gateway  

---

# 🔟 Core Mental Framework (Exam Gold)

| Requirement | Service |
|-------------|---------|
| Object storage | Amazon S3 |
| Block storage | Amazon EBS |
| Temporary block storage | EC2 Instance Store |
| Shared Linux file system | Amazon EFS |
| Windows file share | Amazon FSx |
| Hybrid on-prem integration | AWS Storage Gateway |

---

# Key Architectural Distinctions

- Amazon S3 = Object storage accessed via API
- Amazon EBS = Block storage attached to EC2
- Amazon EFS = Shared file storage (NFS)
- EC2 Instance Store = Ephemeral storage
- Amazon FSx = Specialized managed file systems
- AWS Storage Gateway = Hybrid bridge between on-prem and AWS