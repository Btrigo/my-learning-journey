# Module 12: Migrating to the AWS Cloud
**AWS Certified Cloud Practitioner (CLF-C02) Study Notes**

---

## Table of Contents
1. [Introduction to Migration](#1-introduction-to-migration)
2. [AWS Cloud Adoption Framework (AWS CAF)](#2-aws-cloud-adoption-framework-aws-caf)
3. [Seven Migration Strategies (7 Rs)](#3-seven-migration-strategies-7-rs)
4. [Migration Services and Tools](#4-migration-services-and-tools)
5. [Database Migrations (DMS & SCT)](#5-database-migrations-dms--sct)
6. [Transferring Data Online](#6-transferring-data-online)
7. [Transferring Data Offline](#7-transferring-data-offline)
8. [Assessment Results](#8-assessment-results)
9. [Key Exam Traps](#9-key-exam-traps)

---

## 1. Introduction to Migration

**Cloud migration** = moving digital assets, IT resources, applications, and databases from on-premises (or another cloud) to AWS.

Migration is **NOT a one-and-done process** — large migrations happen in phases.

### 3-Phase Migration Process

| Phase | Goal | Key Tools |
|---|---|---|
| **Assess** | Evaluate cloud readiness, identify business outcomes, build business case | Migration Evaluator |
| **Mobilize** | Create migration plan, address readiness gaps, map app dependencies | Application Discovery Service, Migration Hub |
| **Migrate & Modernize** | Architect, migrate, validate each application | Application Migration Service, DMS, DataSync, Transfer Family, Snow Family |

> **Note:** AWS Migration Hub spans **both** Mobilize AND Migrate & Modernize phases.

---

## 2. AWS Cloud Adoption Framework (AWS CAF)

Created by **AWS Professional Services**. Organizes migration guidance into **6 perspectives** to ensure all roles are aligned.

### Business Capabilities (People Side)

| Perspective | Focus | Key Roles |
|---|---|---|
| **Business** | Aligns IT with business goals; ensures IT investments link to key business results | CEO, CFO, COO, CIO, CMO, CPO, CTO |
| **People** | Organization-wide change management, skill gap identification | HR, Staffing, People managers |
| **Governance** | Aligns IT strategy with business strategy; maximizes value, minimizes risk | CIO, CTO, CFO, CDO (Chief Data Officer), CRO (Chief Risk Officer), Program managers, Enterprise architects, Business analysts, Portfolio managers |

### Technical Capabilities (Tech Side)

| Perspective | Focus | Key Roles |
|---|---|---|
| **Platform** | Implements new solutions, migrates on-prem workloads using architectural models | CTO, IT managers, Solutions architects, Engineers |
| **Security** | Meets security objectives: confidentiality, integrity, availability of data and cloud workloads | CISO, CCO (Chief Compliance Officer), Internal audit leaders, IT security architects and engineers |
| **Operations** | Enables, runs, operates, and recovers IT workloads to agreed-upon levels | IT operations managers, IT support managers, Site reliability engineers |

### CAF Process
Each perspective uncovers **gaps** → gaps become **inputs** → inputs create the **AWS CAF Action Plan** → plan guides change management.

### CAF Benefits
- Reduces business risk
- Improves ESG (environmental, social, governance) performance
- Grows revenue
- Reduces operational costs
- Increases productivity
- Improves customer experience

> **Exam tip:** "Company-wide change management strategy" = **People** perspective (NOT Business). Business = IT/business alignment and ROI.

---

## 3. Seven Migration Strategies (7 Rs)

| # | Strategy | Nickname | Key Detail |
|---|---|---|---|
| 1 | **Relocate** | Hypervisor-level lift and shift | Transfers servers from an on-prem platform to a **cloud version of that same platform** (e.g., VMware SDDC on-prem → VMware Cloud on AWS). Requires no new hardware, no code changes, no architecture changes. |
| 2 | **Rehost** | Lift and Shift | Move as-is, no changes to the application. Source can be **physical, virtual, or another cloud**. Up to 30% cost savings; used in large legacy migrations for speed/scale. |
| 3 | **Replatform** | Lift, Tinker & Shift | Minor cloud optimizations; NO core architecture changes (e.g., MySQL → RDS/Aurora) |
| 4 | **Refactor** | Rearchitect | Write new code; reimagine using cloud-native features; highest upfront cost; driven by need for features/performance not achievable on-prem |
| 5 | **Repurchase** | Drop and Shop | Move from traditional license to SaaS model (e.g., CRM → Salesforce); OR replace app with cloud-based version from AWS Marketplace |
| 6 | **Retain** | Stays Where It Lays | Keep on-prem; app needs major refactoring before migration OR work can be postponed |
| 7 | **Retire** | — | Remove apps no longer needed; 10%+ of enterprise workloads are typically unused |

### Key Distinctions
- **Rehost vs. Relocate:** Rehost moves **anything** (physical, virtual, or cloud) as-is to AWS. Relocate is specifically for moving a platform to its **cloud equivalent** (e.g., VMware SDDC → VMware Cloud on AWS).
- **Replatform vs. Refactor:** Replatform = same code, minor optimizations. Refactor = new code written.
- **Retain vs. Retire:** Retain = not yet. Retire = shut it down now.
- **"Moving to a different product"** = **Repurchasing**

---

## 4. Migration Services and Tools

| Service | Phase | Purpose |
|---|---|---|
| **Migration Evaluator** | Assess | Data-driven migration assessment; analyzes current state and target state; produces migration readiness plan with projected cloud costs; helps reuse existing software licensing |
| **AWS Application Discovery Service** | Mobilize | Discovers on-prem server inventory and connections; gathers configuration, performance, and connection details for servers AND databases; integrates with Migration Hub |
| **AWS Migration Hub** | Mobilize + Migrate & Modernize | Centralized hub: discovery → assessment → planning → execution; prescriptive journey templates; automated recommendations; supports modernization; **FREE to use** |
| **AWS Application Migration Service** | Migrate & Modernize | Moves and improves on-prem AND cloud-based apps; supports any source infrastructure with supported OS; can modernize during migration; works for moving between AWS Regions |

> **Exam tip:** Migration Hub is **unique** because it's free AND it spans the full migration journey from discovery through execution.

---

## 5. Database Migrations (DMS & SCT)

### AWS DMS (Database Migration Service)
- Migrates relational DBs, data warehouses, NoSQL DBs, and analytics workloads
- Virtual machine running replication software; define source + target, schedule task
- **Source database stays LIVE during migration** — minimal disruption
- Supports ongoing data replication (not just one-time migrations)
- Can migrate terabyte-sized databases at low cost
- Can replicate to other AWS Regions or Availability Zones
- Use cases: move to managed DBs, remove licensing costs, replicate ongoing changes, improve data lake integration

### AWS SCT (Schema Conversion Tool)
- Used for **heterogeneous migrations** (changing DB engines, e.g., Oracle → Aurora)
- Converts source schema AND code objects (stored procedures, views, functions)
- Provides effort estimates for conversion planning
- Code that can't be auto-converted is flagged for manual review
- Saves weeks or months of manual conversion time

### Homogeneous vs. Heterogeneous

| Migration Type | Definition | Tools Needed |
|---|---|---|
| **Homogeneous** | Same database engine (e.g., MySQL → MySQL) | DMS only |
| **Heterogeneous** | Different database engines (e.g., Oracle → Aurora) | SCT first, then DMS |

### DMS vs. SCT Summary
- **DMS** = moves the **DATA**
- **SCT** = converts the **SCHEMA/CODE**

> **Schema definition:** Blueprint of a database — table structures, field types, relationships between items.

---

## 6. Transferring Data Online

### Four Considerations When Migrating Data Online
1. Security (will it get there safely?)
2. Data validation (will it arrive intact?)
3. Scheduling (when is the best time?)
4. Bandwidth (enough capacity?)

### Online Transfer Services

| Service | Best For | Key Features |
|---|---|---|
| **AWS DataSync** | Default choice for most data migration workloads | Automates and accelerates moving large amounts of data between on-prem storage and AWS (S3, EFS, FSx); handles encryption, network optimization, bandwidth throttling, scheduling, task filtering, and reporting |
| **AWS Transfer Family** | Managed file transfers using standard protocols | Supports FTP, SFTP, FTPS; transfers files directly into/out of S3 and EFS; use for sharing data with partners or integrating business data into a data lake |
| **AWS Direct Connect** | Dedicated private network connection | Private connection between your network and VPC; fast, reliable, secure; reduces network costs; increases bandwidth |

### Decision Guide
- Need **automation, scheduling, and task reporting** → **DataSync**
- Need **SFTP/FTP/FTPS protocol support** → **Transfer Family**
- Need a **dedicated private network connection** → **Direct Connect**

---

## 7. Transferring Data Offline

### When Offline Transfer Is Needed
- Limited or no bandwidth
- Remote locations without internet or Direct Connect
- Massive data volumes (petabytes) — physically shipping a device is faster than internet transfer

### AWS Snowball Edge Storage Optimized
- Physical device shipped to customer
- Customer loads data onto the device
- Device shipped back to AWS
- AWS loads data into the cloud
- Used for large-scale offline data migrations

---

## 8. Assessment Results

**Score: 89% (8/9 correct) — Passing score: 80%**

| Q | Topic | Result |
|---|---|---|
| 01 | SFTP/FTPS file transfers → Transfer Family | ✅ |
| 02 | Migrate AND modernize apps → Application Migration Service | ✅ |
| 03 | Centralized migration tracking → Migration Hub | ✅ |
| 04 | Primary function of AWS CAF | ✅ |
| 05 | Seven Rs (Relocate, Rehost, Replatform, Refactor, Repurchase, Retain, Retire) | ✅ |
| 06 | Automate + schedule + track data transfer (no Direct Connect) → DataSync | ✅ |
| 07 | Plan, assess, convert, migrate DB in one tool → DMS | ✅ |
| 08 | Company-wide change management strategy → **People** *(answered Business)* | ❌ |
| 09 | Build business case for CFO/stakeholders → Migration Evaluator | ✅ |

---

## 9. Key Exam Traps

- **People vs. Business (CAF):** "Change management strategy" or "organizational readiness" = **People**. "IT aligns with business goals/ROI" = **Business**.
- **Rehost vs. Relocate:** Rehost = move anything (physical, virtual, or cloud) as-is. Relocate = move a platform to its cloud equivalent (e.g., VMware → VMware Cloud on AWS).
- **Replatform vs. Refactor:** Replatform = same code, minor optimizations. Refactor = new code written.
- **DMS vs. SCT:** DMS moves data. SCT converts schema. Heterogeneous migrations need **both** (SCT first).
- **DataSync vs. Transfer Family:** DataSync = automation and acceleration. Transfer Family = protocol support (SFTP/FTP/FTPS).
- **Migration Hub is free** — this is a notable distinction worth remembering.
- **Application Discovery Service vs. Application Migration Service:** Discovery = find/map what you have. Migration Service = actually move the apps.