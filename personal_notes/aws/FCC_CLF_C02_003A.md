# AWS Certified Cloud Practitioner - Part 3A Study Notes
## Cost & Capacity Management + Storage Services

**Study Date:** February 10, 2026  
**Source:** freeCodeCamp CLF-C02 Course (Hours 6:00-7:00)  
**Topics:** EC2 Pricing, Cost Optimization, Storage Types, S3, EBS, EFS, Snow Family

---

## 📊 Cost & Capacity Management

### Definitions

**Cost Management** = How to save money on AWS services

**Capacity Management** = How to meet traffic demand through adding or upgrading servers

### EC2 Pricing Models

#### 1. **Spot Instances**
- **Concept:** Bid for unused EC2 capacity
- **Savings:** Up to 90% discount vs On-Demand
- **Risk:** AWS can reclaim with 2-minute warning
- **Payment:** Flexible about availability/interruption
- **Use Cases:** 
  - Batch processing
  - Data analysis
  - Fault-tolerant workloads
- **NOT for:** Databases, critical applications

#### 2. **Reserved Instances (RI)**
- **Commitment:** 1-year or 3-year contract
- **Savings:** Up to 75% vs On-Demand
- **Payment Options:**
  - All Upfront (highest discount)
  - Partial Upfront
  - No Upfront (lowest discount)
- **Use Cases:** Steady-state applications (databases, web servers)

#### 3. **Savings Plans**
- **Commitment:** Commit to $/hour for 1 or 3 years
- **Savings:** Up to 72% vs On-Demand
- **Flexibility:** More flexible than Reserved Instances
- **Types:**
  - Compute Savings Plans (most flexible)
  - EC2 Instance Savings Plans

### Cost & Capacity Services

#### AWS Batch
- **Purpose:** Plans, schedules, and executes batch computing workloads
- **Cost Benefit:** Utilizes Spot Instances to save money
- **Feature:** Provisions optimal compute resources automatically
- **Range:** Works across full range of AWS computing services

#### AWS Compute Optimizer
- **Purpose:** Suggests how to reduce costs and improve performance
- **Technology:** Uses machine learning to analyze previous usage history
- **Analyzes:** EC2 instances, Auto Scaling groups, EBS volumes, Lambda
- **Benefit:** Data-driven recommendations for optimization

#### EC2 Auto Scaling Groups (ASG)
- **Purpose:** Automatically add/remove EC2 servers based on demand
- **Cost Benefit:** Only run the amount of servers you need
- **Capacity Benefit:** Meet traffic demand automatically
- **Key Concepts:**
  - Minimum capacity
  - Desired capacity  
  - Maximum capacity
- **Result:** Saves money AND meets capacity needs

#### Elastic Load Balancer (ELB)
- **Purpose:** Distributes traffic to multiple instances
- **Routing:** 
  - Reroutes traffic from unhealthy → healthy instances
  - Routes across multiple Availability Zones
- **Benefit:** High availability and fault tolerance
- **Note:** Primarily about capacity management, not cost savings

#### AWS Elastic Beanstalk
- **Type:** Platform as a Service (PaaS)
- **Similar to:** Heroku
- **Purpose:** Deploy web applications without managing infrastructure
- **Developer Experience:** Upload code, AWS handles the rest
- **Manages:** EC2, Auto Scaling, ELB, RDS (if needed)
- **Benefit:** Easy deployment without infrastructure expertise

---

## 💾 Storage Services Overview

### Three Types of Storage

#### 1. Block Storage (EBS - Elastic Block Store)

**Characteristics:**
- Data split into evenly-sized blocks
- Directly accessed by operating system
- Supports **only single write volume** (one instance at a time)

**Protocol:** Fibre Channel (FC) or iSCSI

**Use Case:** Virtual hard drive attached to VM

**Analogy:** Like a USB drive attached to your computer

**When to Use:** 
- Boot volumes
- Database storage
- Any application needing direct block-level storage

**Example:**
```
[Application] → [Virtual Machine] → [OS] → [EBS Volume mounted as /dev/sda1]
```

---

#### 2. File Storage (EFS - Elastic File System)

**Characteristics:**
- File stored with data AND metadata
- **Multiple connections via network share**
- Supports multiple reads/writes with file locks
- Files organized in directory hierarchy

**Protocols:** 
- NFS (Network File System) - Linux
- SMB (Server Message Block) - Windows

**Use Case:** Multiple users or VMs need to access the same drive

**Analogy:** Like a network drive accessible by multiple computers

**Real-World Example:**
```
Minecraft Server Scenario:
- Game world must be on single drive
- Want multiple VMs for compute power
- EFS allows all VMs to access same world data
```

**When to Use:**
- Shared file systems
- Content management
- Web serving (shared web root)
- Development environments

---

#### 3. Object Storage (S3 - Simple Storage Service)

**Characteristics:**
- Object stored with data, metadata, AND unique ID
- **Unlimited storage** - no file limits or storage limits
- Scales automatically
- Supports multiple reads/writes (no locks)
- Not intended for high IOPS (Input/Output Operations Per Second)

**Protocol:** HTTPS and API

**Use Case:** Upload files without worrying about infrastructure

**Analogy:** Like Google Drive or Dropbox

**When to Use:**
- Static website hosting
- Backups and archives
- Data lakes
- Application assets
- When you don't need mounted filesystem

**When NOT to Use:**
- High IOPS requirements
- Need to mount as drive to VM
- Frequent small updates to same file

---

### Storage Comparison Table

| Feature | Block (EBS) | File (EFS) | Object (S3) |
|---------|-------------|------------|-------------|
| **Attachment** | Single EC2 instance | Multiple EC2 instances | Internet/API access |
| **Protocol** | FC, iSCSI | NFS, SMB | HTTPS/REST API |
| **Performance** | High IOPS | Moderate | Lower (but scalable) |
| **Use Case** | Boot volumes, databases | Shared file systems | Static content, backups |
| **Accessibility** | OS-level | Network share | HTTP/API |
| **Locking** | Single writer | File locking supported | No locks |
| **Scalability** | Manual resize | Auto-scaling | Unlimited |

---

## 🪣 Amazon S3 (Simple Storage Service)

### S3 History & Importance

- **Launched:** March 2006 (**second AWS service ever launched**)
- **Status:** AWS's flagship storage service
- **Exam Focus:** CLF-C02 asks MORE about S3 than previous versions

### What is Object Storage?

**Definition:** Data storage architecture that manages data as objects (vs files in hierarchy or blocks in sectors)

**S3 Features:**
- Unlimited storage capacity
- No need to think about underlying infrastructure
- Console interface for upload/access
- Universal namespace (bucket names globally unique)

### S3 Core Concepts

#### Objects

Objects are the fundamental entities stored in S3. Each contains:

1. **Key** - The name/path of the object (like a filename)
2. **Value** - The actual data (sequence of bytes)
3. **Version ID** - When versioning is enabled
4. **Metadata** - Additional information about the object

**Object Size Limits:**
- **Minimum:** 0 bytes (yes, empty files allowed!)
- **Maximum:** 5 TB per object
- **Important:** Individual object max is 5TB (exam question!)

#### Buckets

**Definition:** Containers that hold objects

**Characteristics:**
- Can contain folders → which contain objects
- **Universal namespace** - must be globally unique (like domain names)
- **Limit:** 100 buckets per account (soft limit - can request increase)

**Bucket Naming:**
- Must be globally unique across ALL of AWS
- Like having a domain name
- Once created, name cannot be changed

**Example Structure:**
```
my-unique-bucket-12345/
├── folder1/
│   ├── image1.jpg
│   └── document.pdf
└── folder2/
    └── video.mp4
```

---

### S3 Storage Classes

**General Principle:** The farther down the list, the cheaper the storage, but with tradeoffs in retrieval time and accessibility.

#### S3 Standard (Default)
- **Speed:** Incredibly fast access
- **Availability:** 99.99%
- **Durability:** 99.999999999% (11 nines)
- **Replication:** Across ≥3 Availability Zones
- **Cost:** Most expensive (but not actually expensive)
- **Use Case:** Frequently accessed data
- **Note:** "Expensive at scale" when you could optimize with other tiers

#### S3 Intelligent-Tiering
- **Technology:** Uses ML to analyze object usage
- **Feature:** Automatically moves data to most cost-effective tier
- **Benefit:** No performance impact or added overhead
- **Monitoring Fee:** Small monthly fee per object
- **Use Case:** Unknown or changing access patterns

#### S3 Standard-IA (Infrequent Access)
- **Speed:** Same as S3 Standard
- **Cost:** Cheaper if accessed <1/month
- **Fee:** Additional retrieval fee applied
- **Warning:** Can cost MORE than Standard if accessed too frequently
- **Use Case:** Long-term storage, backups
- **Replication:** ≥3 AZs

#### S3 One Zone-IA
- **Speed:** Same as S3 Standard
- **Replication:** **Single Availability Zone only**
- **Availability:** Lower than Standard (99.5% vs 99.99%)
- **Cost:** Cheaper than Standard-IA
- **Risk:** ⚠️ **Data could be destroyed if AZ fails**
- **Use Case:** 
  - Recreatable data
  - Secondary backups
  - When AZ failure is acceptable risk

#### S3 Glacier
- **Purpose:** Long-term cold storage
- **Retrieval Time:** Minutes to hours
- **Cost:** Very, very cheap
- **Use Case:** 
  - Long-term archives
  - Compliance data
  - Data rarely accessed

#### S3 Glacier Deep Archive
- **Purpose:** Lowest cost storage class
- **Retrieval Time:** 12 hours
- **Cost:** Cheapest option
- **Use Case:** 
  - Data accessed once or twice per year
  - 7-10 year retention requirements
  - Regulatory archives

**Note:** S3 Glacier services "live in a weird state" - part of S3 console but almost like separate service

**S3 Outposts:** Has own storage class, doesn't fit linear "cheaper" progression (not covered in detail here)

---

### S3 Storage Class Selection Guide

```
Decision Flow:

Frequent Access (>1/month)
└─> S3 Standard

Unknown/Changing Access
└─> S3 Intelligent-Tiering

Infrequent Access (<1/month)
├─> Need Multi-AZ? → S3 Standard-IA
└─> Single AZ OK? → S3 One Zone-IA

Archive (rarely accessed)
├─> Need access in minutes? → S3 Glacier
└─> Can wait 12 hours? → S3 Glacier Deep Archive
```

---

### S3 Pricing Considerations

**Storage Costs** (approximate, verify current pricing):
- S3 Standard: ~$0.023/GB/month
- S3 Intelligent-Tiering: ~$0.023/GB/month + monitoring fee
- S3 Standard-IA: ~$0.0125/GB/month + retrieval fees
- S3 One Zone-IA: ~$0.01/GB/month + retrieval fees
- S3 Glacier: ~$0.004/GB/month
- S3 Glacier Deep Archive: ~$0.00099/GB/month

**Additional Costs:**
- Data transfer out
- Retrieval fees (IA and Glacier tiers)
- Request fees (PUT, GET, etc.)

---

## 📦 AWS Snow Family

### Overview

**Purpose:** Physical devices used to move data in/out of AWS cloud when:
- Network transfer is too slow
- Network transfer is too difficult
- Network transfer is too costly

**History:**
- Originally just "Snowball"
- Then "Snowball Edge" (added Edge Computing)
- Expanded to family of devices

**All devices now support Edge Computing capabilities**

### Snow Family Devices

#### Snowcone

**Two Sizes:**
- 8 TB usable storage
- 14 TB usable storage

**Characteristics:**
- Smallest device in family
- Portable and rugged
- Can be used for edge computing

**Use Cases:**
- Remote/edge locations
- Small data transfers
- IoT data collection

---

#### Snowball Edge

**Two Main Variants:**

**1. Storage Optimized:**
- **Storage:** 80 TB usable
- **Focus:** Maximum storage capacity

**2. Compute Optimized:**
- **Storage:** 39.5 TB usable
- **Compute:** Lots of vCPUs and increased memory
- **Benefit:** Edge computing before sending to AWS

**Note:** Technically has 4 versions, simplified to 2 main categories

**Use Cases:**
- Data center migrations
- Large data transfers
- Edge computing workloads

---

#### Snowmobile

**Capacity:** Up to 100 PB per trailer

**Physical Form:** 
- Cargo container
- Filled with racks of storage and compute
- Transported via semi-trailer tractor truck

**Marketing Note:**
- Single device: 100 PB
- AWS markets: "Move exabytes" (multiple devices)
- Snowball Edge: "Move petabytes"
- Snowmobile: "Move exabytes"

**Reality:** Most expensive option, rarely ordered

**Use Cases:**
- Entire data center migrations
- Exabyte-scale transfers
- Once-in-a-lifetime data movements

---

### Snow Family Comparison

| Device | Storage | Use Case | Mobility |
|--------|---------|----------|----------|
| **Snowcone** | 8-14 TB | Small transfers, edge | Highly portable |
| **Snowball Edge** | 39.5-80 TB | Medium-large transfers | Briefcase-sized |
| **Snowmobile** | 100 PB | Massive migrations | Semi-truck |

### Snow Family Features (Not Detailed at CCP Level)

**Security:**
- Tamper-proof
- Encryption
- Tracking

**Networking:**
- Built-in connectivity
- Edge computing capabilities

**Destination:** All data goes to Amazon S3

**Exam Focus:** Know the three device types and general storage capacities

---

## 💿 AWS Storage Services Summary

### S3 (Simple Storage Service)
- **Type:** Serverless object storage
- **Capacity:** Upload unlimited files, very large file sizes
- **Pricing:** Pay for what you store
- **Benefit:** No underlying file system management

### S3 Glacier
- **Type:** Cold storage service
- **Purpose:** Low-cost archiving and long-term backup
- **Technology:** Uses previous-generation HDD drives for low cost
- **Characteristics:** Highly secure and durable

### EBS (Elastic Block Store)
- **Type:** Persistent block storage
- **Function:** Virtual hard drive in the cloud
- **Attachment:** Attached to EC2 instances
- **Options:**
  - SSD (General Purpose, Provisioned IOPS)
  - HDD (Throughput Optimized, Cold HDD)

### EFS (Elastic File System)
- **Type:** Cloud-native NFS file system service
- **Attachment:** Mount to **multiple EC2 instances simultaneously**
- **Use Case:** Share files between multiple servers
- **Protocol:** NFS

### Storage Gateway
- **Type:** Hybrid cloud storage service
- **Purpose:** Extends on-premise storage to cloud

**Three Offerings:**

1. **File Gateway**
   - Extends local storage to S3

2. **Volume Gateway**
   - Caches local drives to S3
   - Continuous backup of local files in cloud

3. **Tape Gateway**
   - Stores files onto virtual tapes
   - Cost-effective long-term storage

### Snow Family (Covered Above)
- **Snowcone:** 8 TB
- **Snowball/Snowball Edge:** 50-80 TB
- **Snowmobile:** 100 PB per trailer

### AWS Backup
- **Type:** Fully managed backup service
- **Purpose:** Centralize and automate backups
- **Supports:** EC2, EBS, RDS, DynamoDB, EFS, Storage Gateway
- **Feature:** Create backup plans with schedules and retention

### CloudEndure Disaster Recovery
- **Purpose:** Disaster recovery solution
- **Function:** Continuously replicates machines to low-cost staging area
- **Location:** Target AWS account and region
- **Benefit:** Fast and reliable recovery from IT/data center failures

### Amazon FSx

**Two Types:**

**FSx for Windows File Server:**
- **Protocol:** SMB
- **Function:** Mount FSx to Windows servers
- **Use Case:** Windows-based applications

**FSx for Lustre:**
- **Protocol:** Lustre (Linux)
- **Function:** Mount FSx to Linux servers
- **Use Case:** High-performance computing, ML workloads

**Characteristics:** Feature-rich and highly performant

---

## 🎯 Key Exam Tips - First Hour

### Cost Management
1. **Remember the 4 main pricing models:** On-Demand, Reserved, Savings Plans, Spot
2. **Spot = up to 90% savings** but can be interrupted
3. **Reserved/Savings Plans = commit to save** (1 or 3 years)
4. **Auto Scaling = cost + capacity** optimization

### Storage Types
1. **Block (EBS):** Virtual hard drive, single instance
2. **File (EFS):** Network share, multiple instances
3. **Object (S3):** Unlimited storage, API access

### S3 Essentials
1. **Object size:** 0 bytes to 5 TB
2. **Bucket names:** Globally unique
3. **11 nines durability** (99.999999999%)
4. **Storage classes** trade cost for retrieval time

### S3 Storage Classes (Most Tested)
- **Standard:** Frequent access, 3+ AZs
- **Standard-IA:** <1/month access, retrieval fee
- **One Zone-IA:** Single AZ, cheaper, data loss risk
- **Glacier:** Minutes-hours retrieval
- **Glacier Deep Archive:** 12-hour retrieval, cheapest

### Snow Family
- **Snowcone:** 8-14 TB
- **Snowball Edge:** 40-80 TB
- **Snowmobile:** 100 PB
- **Use when:** Network too slow/expensive

---

## 📝 Practice Questions

**Q1:** What EC2 pricing model offers up to 90% savings but instances can be interrupted?
<details>
<summary>Answer</summary>
Spot Instances - AWS can reclaim with 2-minute warning
</details>

**Q2:** Which storage type allows multiple EC2 instances to access the same data simultaneously?
<details>
<summary>Answer</summary>
EFS (Elastic File System) - uses NFS protocol for shared access
</details>

**Q3:** What is the maximum size of a single S3 object?
<details>
<summary>Answer</summary>
5 TB (5 terabytes) - minimum is 0 bytes
</details>

**Q4:** Which S3 storage class has data in only one Availability Zone?
<details>
<summary>Answer</summary>
S3 One Zone-IA - cheaper but data could be lost if AZ fails
</details>

**Q5:** What AWS service automatically optimizes costs by analyzing usage with ML?
<details>
<summary>Answer</summary>
AWS Compute Optimizer
</details>

---

## 🔄 Next Steps

Continue to **Part 3B** for:
- S3 Hands-on (bucket creation, lifecycle policies, encryption)
- EBS Deep Dive
- EFS Configuration
- Database Services

---

**Study Tip:** S3 storage classes are heavily tested. Create a mental flowchart for choosing the right storage class based on access frequency and durability requirements.
