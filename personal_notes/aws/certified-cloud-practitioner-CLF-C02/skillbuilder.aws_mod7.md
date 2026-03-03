# AWS CLF-C02 — Module 7: Databases
**Date Studied:** March 2, 2026  
**Course:** AWS Skill Builder — AWS Cloud Practitioner Essentials  
**Module Progress:** ✅ Complete | Assessment Score: 11/12 (91.7%)

---

## Table of Contents
1. [AWS Shared Responsibility Model for Databases](#1-aws-shared-responsibility-model-for-databases)
2. [Relational Database Services](#2-relational-database-services)
   - [Amazon RDS](#amazon-relational-database-service-rds)
   - [Amazon Aurora](#amazon-aurora)
3. [NoSQL Database Services — Amazon DynamoDB](#3-nosql-database-services--amazon-dynamodb)
4. [In-Memory Caching — Amazon ElastiCache](#4-in-memory-caching--amazon-elasticache)
5. [Additional Database Services](#5-additional-database-services)
6. [Key Numbers to Memorize](#6-key-numbers-to-memorize)
7. [Service Selection Cheat Sheet](#7-service-selection-cheat-sheet)
8. [Assessment Debrief](#8-assessment-debrief)

---

## 1. AWS Shared Responsibility Model for Databases

AWS groups database services into **three management categories** based on who owns what operational tasks.

### Fully Managed Services
- **AWS handles:** Provisioning, scaling, patching, backups, performance optimization, security patches, monitoring, built-in metrics
- **Customer handles:** Designing data structures, managing access controls
- **Examples:** Amazon Aurora, Amazon DynamoDB

### Managed Services
- **AWS handles:** Backups, patching, hardware provisioning
- **Customer handles:** Database configuration, query optimization, performance tuning, server-side encryption, network traffic protection
- **Examples:** Amazon RDS

### Unmanaged Services
- **AWS handles:** Physical hardware, software for compute/storage/networking infrastructure only
- **Customer handles:** Everything — installation, configuration, patching, maintenance, DB security, backups, high availability setup, performance optimization
- **Example:** MySQL installed directly on an Amazon EC2 instance

> **Key insight:** The more managed the service, the less operational overhead for the customer — but also less control over the underlying environment.

---

## 2. Relational Database Services

### What is a Relational Database?
- Stores data in **tables** (rows and columns) with **relationships** between tables
- Tables are linked via **common attributes** (e.g., a `user_id` connecting a users table to an orders table)
- Queried using **SQL (Structured Query Language)**
- Supported engines: MySQL, PostgreSQL, Microsoft SQL Server, MariaDB, Oracle, and more

### Three Deployment Options (Progression)

| Option | Type | Who Controls OS/Config |
|--------|------|------------------------|
| **EC2 (Lift-and-Shift)** | Unmanaged | Customer |
| **Amazon RDS** | Managed | AWS |
| **Amazon Aurora** | Fully Managed | AWS |

#### Lift-and-Shift (EC2)
- Move existing on-premises database to an EC2 instance as-is
- Customer retains full control: OS, memory, CPU, storage, configuration
- Use **AWS Database Migration Service (DMS)** to help migrate
- DMS keeps the source database fully operational during migration — **minimizes downtime**

---

### Amazon Relational Database Service (RDS)

**Type:** Managed relational database service

**Supported Engines:** Amazon Aurora, MySQL, PostgreSQL, Microsoft SQL Server, MariaDB, Oracle Database

**Use Cases:** Web applications, enterprise workloads, e-commerce product inventories

#### What AWS Handles in RDS
- Infrastructure and underlying hardware
- Operating system management
- Database software patching
- Backup automation
- Redundancy and failover

#### What the Customer Handles in RDS
- Security configuration
- Encryption at rest and in transit

#### Key Features & Benefits

| Benefit | Details |
|---------|---------|
| **Cost optimization** | No upfront hardware costs; pay-as-you-go; automates admin tasks (backups, patching, monitoring) |
| **Multi-AZ deployment** | Auto-replicates data to a standby instance in a **different Availability Zone**; automatic failover during failures — no manual intervention; minimal downtime |
| **Performance optimization** | Read replicas offload read traffic from the primary instance; **RDS Performance Insights** provides real-time monitoring |
| **Security controls** | VPC isolation, encryption at rest and in transit, automated backups, Multi-AZ for resiliency |

#### DB Snapshots
- **Manual** full backups of the entire database instance
- Created by the customer (not automated)
- Useful for specific point-in-time recovery and long-term archiving

> ⚠️ **Exam trap:** Multi-AZ is for **high availability and failover** — NOT for performance scaling. Read Replicas are for performance.

---

### Amazon Aurora

**Type:** Fully managed relational database (AWS's own proprietary engine)

**Compatible with:** MySQL and PostgreSQL, and DSQL (Distributed SQL)

**Use Cases:** Gaming applications, media and content management, real-time analytics

#### Key Advantages Over Standard RDS

| Feature | Aurora | Standard RDS |
|---------|--------|--------------|
| Management level | Fully managed | Managed |
| Performance | 5x MySQL / 3x PostgreSQL throughput | Standard |
| Storage | Auto-scales 10 GB → 128 TB | Manual scaling |
| Availability | **99.99%** | High |
| Replicas | Up to **15** across AZs | Fewer |
| Copies of data | **6 copies across 3 AZs** | Varies |
| Failover | Auto-detects, redirects, **no data loss** | Auto-failover to standby |
| Backup | Continuous to S3, up to **35-day** point-in-time restore | Automated + manual snapshots |

#### Aurora Benefits
1. **High performance & availability** — Distributed storage across multiple nodes
2. **Automated storage & backup management** — Grows 10 GB → 128 TB automatically; continuous backup to Amazon S3
3. **Advanced replication & fault tolerance** — 3 AZs, 6 copies, 99.99% availability, auto-detects failures and redirects traffic to healthy replicas with no data loss

> **When to choose Aurora over RDS:** Need higher performance (5x MySQL), need 99.99% availability, need auto-scaling storage up to 128 TB, or migrating away from expensive commercial database engines like Oracle.

---

## 3. NoSQL Database Services — Amazon DynamoDB

### What is NoSQL?
- **Non-relational** database — no rigid schema required
- Data stored as **key-value pairs**
- Each item can have **different attributes** — flexible schema
- Does NOT use SQL; uses the **DynamoDB API** (accessed via AWS SDK)
- No concept of foreign keys or JOIN operations

### Relational vs. NoSQL Comparison

| Feature | Relational (RDS) | NoSQL (DynamoDB) |
|---------|-----------------|-----------------|
| Schema | Rigid — all rows same structure | Flexible — items can differ |
| Query language | SQL | DynamoDB API / AWS SDK |
| Relationships | Foreign keys, JOINs | No foreign keys, standalone tables |
| Best for | Structured, transactional data | Flexible, high-speed lookups |
| Scaling | Manual | Automatic, seamless |

### DynamoDB Data Structure

| Term | Definition |
|------|-----------|
| **Table** | The container for data |
| **Item** | A single record (like a row, but flexible) |
| **Attribute** | A field on an item (name, value pair) |
| **Partition Key** | The unique identifier every item must have; used to distribute and locate data |

> The **partition key** is the only required attribute. All other attributes are optional and can vary per item.

### Amazon DynamoDB — Key Facts

- **Type:** Fully managed, serverless NoSQL database
- **Latency:** Single-digit millisecond response times at any scale
- **No cold starts, no version upgrades, no maintenance windows, no patching, no downtime**
- **Use Cases:** Gaming platforms, financial service applications, mobile apps with global user bases
- **DynamoDB Global Tables** — multi-region replication for globally distributed applications

#### Prime Day 2024 Stat (Notable Example)
- 48 hours of operation
- Tens of trillions of API calls
- Peaked at **146 million requests per second**
- Zero manual intervention — scaled seamlessly

### DynamoDB Benefits

| Benefit | Details |
|---------|---------|
| **Scalability with provisioned capacity** | Auto-scales throughput up/down based on actual usage; no practical limits on table size; specify target utilization levels |
| **Consistent high performance** | Single-digit millisecond response at any scale; data distributed across multiple servers and SSDs |
| **High availability & durability** | **99.999%** availability; replicated across **3 facilities per Region**; multiple copies in separate Regions |
| **Data encryption** | Encrypted at rest AND in transit automatically; flexible encryption key options for customized security |

### DynamoDB Operations
- **Scan** — Reads ALL items in the table (equivalent to SELECT *)
- **Query** — Filters by partition key to return specific items

---

## 4. In-Memory Caching — Amazon ElastiCache

### The Problem ElastiCache Solves
When thousands of users repeatedly request the same data (e.g., a product page on an e-commerce site), the database must run the **same query over and over**. This causes:
- High latency
- Performance bottlenecks
- Increased database load

### What is In-Memory Caching?
- Stores frequently accessed data in **RAM** (system memory) instead of on disk
- RAM access is **hundreds or thousands of times faster** than disk-based storage
- Reduces the number of queries sent to the primary database

### Amazon ElastiCache

**Type:** Fully managed in-memory caching service

**Compatible with:** Redis OSS, Valkey, Memcached

**Latency:** **Microsecond** response times (faster than DynamoDB's millisecond)

**Use Cases:** Session data management, database query enhancement, gaming leaderboards, content delivery systems

### How ElastiCache Fits Into Architecture

```
User Request
     ↓
EC2 Application Server
     ↓
Check ElastiCache first
  ├── Cache HIT  → Return data immediately ⚡ (microseconds)
  └── Cache MISS → Query RDS → Store result in cache → Return data
                      (next request = cache hit)
```

### ElastiCache Benefits

| Benefit | Details |
|---------|---------|
| **High performance** | Handles Redis, Valkey, Memcached; auto provisions hardware, patches, monitors; add/remove nodes seamlessly |
| **High availability** | Constantly monitors primary nodes; auto-promotes replica to primary on failure; recovery typically **within minutes**; no manual intervention |
| **Multi-AZ replication** | Replicates across multiple AZs; data stays accessible even if one AZ goes down |
| **Data encryption** | At-rest encryption for disk/backups; in-transit encryption via **TLS** |

### Cost Optimization Angle
By directing read traffic to ElastiCache, you can use **smaller, cheaper RDS instances** since the primary database handles less load.

> ⚠️ **Important:** ElastiCache is a **cache layer, not a primary database**. Cached data can be lost if a node fails — but it can simply be re-fetched from RDS. It's a speed layer, not a storage layer.

### Latency Comparison

| Service | Latency |
|---------|---------|
| **ElastiCache** | Microseconds |
| **DynamoDB** | Single-digit milliseconds |
| **RDS (under load)** | Higher, variable |

---

## 5. Additional Database Services

> **Core AWS philosophy:** No one-size-fits-all database. Use **purpose-built databases** for specific workloads.

### Amazon DocumentDB (with MongoDB Compatibility)

**Type:** Fully managed document database

**Data format:** JSON-like documents with dynamic schemas (semi-structured data)

**Compatible with:** MongoDB APIs, drivers, and tools

**Use Cases:** Content management systems, catalog and inventory management, user profile and personalization systems

**Key Benefits:**
- MongoDB compatibility — migrate existing MongoDB apps with minimal code changes
- Auto-scales storage up to **64 TB** in 10 GB increments
- Handles millions of requests per second
- Up to **15 replica instances** for increased read throughput
- Automatic scaling, continuous backup, enterprise-grade security

> **DocumentDB vs DynamoDB:** DocumentDB handles complex, semi-structured JSON documents. DynamoDB handles simpler key-value pairs. Both are NoSQL but serve different use cases.

---

### AWS Backup

**Type:** Centralized backup management service

**Supports:** Amazon EBS volumes, Amazon EFS file systems, RDS databases, DynamoDB tables, and **on-premises deployments**

**Use Cases:** Centralized disaster recovery, consistent backup policies for compliance, consolidating multiple backup processes through a single interface

**Key Benefits:**

| Benefit | Details |
|---------|---------|
| **Centralized backup management** | Single dashboard for all backup jobs, restore points, compliance status across multiple AWS accounts and Regions; automated backup schedules; auto-protects new resources |
| **Cross-region backup redundancy** | Auto-replicates backups across AWS Regions for disaster recovery; restore from secondary Region if primary fails |
| **Streamlined regulatory compliance** | Detailed audit logs and reports; enforce backup policies; track backup activities for security/compliance |

---

### Amazon Neptune

**Type:** Fully managed, purpose-built **graph database**

**Use Cases:** Social network user connection mapping, **fraud detection systems**, search and recommendation systems

**Key Facts:**
- Designed for **highly connected datasets** — relationships that are difficult to identify in traditional relational databases (user connections, friend networks, interaction patterns)
- Supports **property graph** and **RDF (Resource Description Framework)** models
- Processes **billions of relationships in milliseconds**
- Auto-grows storage up to **64 TB**
- High availability with automatic failover and backups

> **Neptune keyword triggers:** Social networks, fraud detection, relationship mapping, pattern matching, interconnected data

---

### Amazon Managed Blockchain

**Type:** Managed blockchain network service

**Use Cases:** Supply chain tracking, immutable transaction records, scenarios requiring assurance that no data is altered or lost

---

### DynamoDB Accelerator (DAX)

**Type:** In-memory cache layer **built specifically for DynamoDB**

**Purpose:** Dramatically improves DynamoDB read times

> **DAX vs ElastiCache:**
> - **DAX** = caching layer specifically FOR DynamoDB
> - **ElastiCache** = general-purpose caching for RDS, applications, etc.

---

## 6. Key Numbers to Memorize

| Service | Stat | Value |
|---------|------|-------|
| **Aurora** | Throughput vs MySQL | **5x** |
| **Aurora** | Throughput vs PostgreSQL | **3x** |
| **Aurora** | Max replicas | **15** across AZs |
| **Aurora** | Data copies | **6 copies across 3 AZs** |
| **Aurora** | Availability | **99.99%** |
| **Aurora** | Storage range | **10 GB → 128 TB** |
| **Aurora** | Point-in-time restore | Up to **35 days** |
| **DynamoDB** | Availability | **99.999%** |
| **DynamoDB** | Replication | **3 facilities per Region** |
| **DynamoDB** | Latency | **Single-digit milliseconds** |
| **DynamoDB** | Prime Day 2024 peak | **146M requests/second** |
| **ElastiCache** | Latency | **Microseconds** |
| **DocumentDB** | Max storage | **64 TB** |
| **Neptune** | Max storage | **64 TB** |
| **DocumentDB** | Max read replicas | **15** |

---

## 7. Service Selection Cheat Sheet

### Scenario → Service Mapping

| Scenario Keywords | Choose |
|------------------|--------|
| Structured data, SQL, relationships between tables | **RDS** |
| High performance relational, replace Oracle/SQL Server | **Aurora** |
| Flexible schema, key-value, high speed, serverless | **DynamoDB** |
| Repeated read queries, reduce DB load, microsecond latency | **ElastiCache** |
| JSON documents, MongoDB compatibility, semi-structured | **DocumentDB** |
| Social networks, fraud detection, interconnected data | **Neptune** |
| Supply chain, immutable records, blockchain | **Managed Blockchain** |
| Accelerate DynamoDB reads | **DAX** |
| Centralized backups across multiple AWS services | **AWS Backup** |
| Migrate on-prem DB to AWS with minimal downtime | **AWS DMS** |
| Full OS/config control over database | **EC2 (Unmanaged)** |

### Exam Pattern Recognition

| Keyword in Question | Think... |
|--------------------|---------|
| "slow performance", "high throughput", "5x MySQL" | Aurora |
| "minimal downtime", "high availability", "failover" | Multi-AZ RDS |
| "offload reads", "read traffic" | Read Replicas |
| "reduce DB overhead", "managed service" | RDS |
| "unpredictable traffic", "auto-scale", "serverless" | DynamoDB |
| "millisecond latency", "gaming", "global users" | DynamoDB |
| "microsecond", "cache", "reduce DB load" | ElastiCache |
| "social network", "fraud detection", "relationships" | Neptune |
| "MongoDB", "JSON", "document", "catalog" | DocumentDB |
| "centralized backup", "cross-region backup", "compliance" | AWS Backup |
| "migrate database", "minimal downtime during migration" | AWS DMS |

---

## 8. Assessment Debrief

**Score: 11/12 (91.7%)**

### ❌ Missed Question — Q3: Aurora Use Case

**Question:** What is a possible use case for Amazon Aurora?

**Incorrect answer selected:** Processing unstructured data streams in real time without relational database constraints

**Why it's wrong:** Aurora is a **relational database** — it handles structured data only. Unstructured data and real-time streaming are not Aurora use cases.

**Correct answer:** Replacing high-cost commercial database engines with a more cost-effective solution that still provides enterprise-level performance and reliability

**Lesson learned:** Aurora is MySQL/PostgreSQL compatible, making it ideal for companies migrating away from expensive licenses (Oracle, SQL Server) while maintaining enterprise-level performance. Always remember: **Aurora = relational = structured data**.

---

## Quick Reference Summary

```
RELATIONAL (Structured, SQL)
├── EC2 + MySQL/PostgreSQL     → Full control, unmanaged
├── Amazon RDS                 → Managed, multi-engine support
└── Amazon Aurora              → Fully managed, highest performance

NON-RELATIONAL (Flexible Schema)
├── DynamoDB                   → Key-value, serverless, milliseconds
└── DocumentDB                 → JSON documents, MongoDB-compatible

CACHING (Speed Layer)
├── ElastiCache                → General caching, microseconds
└── DAX                        → DynamoDB-specific caching

SPECIALIZED
├── Neptune                    → Graph DB, social/fraud
├── Managed Blockchain         → Immutable records, supply chain
└── AWS Backup                 → Centralized backup management
```

---

*Notes compiled from AWS Skill Builder — Module 7: Databases*  
*CLF-C02 Exam Target: March 2026*