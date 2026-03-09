# AWS Cloud Practitioner (CLF-C02) — Module 11: Pricing and Support
> Study Notes | AWS Skill Builder | Completed: March 8, 2026

---

## Table of Contents
1. [AWS Pricing Concepts](#1-aws-pricing-concepts)
2. [Driving Factors of Cost](#2-driving-factors-of-cost)
3. [AWS Pricing and Billing Services](#3-aws-pricing-and-billing-services)
4. [AWS Support Plans](#4-aws-support-plans)
5. [Additional Support Resources](#5-additional-support-resources)
6. [AWS Marketplace and AWS Partner Network](#6-aws-marketplace-and-aws-partner-network)
7. [Cost Optimization Techniques](#7-cost-optimization-techniques)
8. [Exam Traps and Key Distinctions](#8-exam-traps-and-key-distinctions)

---

## 1. AWS Pricing Concepts

AWS uses three fundamental pricing principles:

| Principle | Description | Best For |
|---|---|---|
| **Pay as you go** | Pay only for what you use, no upfront costs or long-term commitments | Variable or unpredictable workloads |
| **Save when you commit** | Commit to 1 or 3 years of usage for significant discounts (up to 72%) | Steady-state, predictable workloads |
| **Pay less by using more** | Volume-based discounts — per-unit cost decreases as usage increases | High-volume usage (e.g., S3 storage tiers) |

> ⚠️ **Exam Trap:** "Save when you commit" = **time commitment**. "Pay less by using more" = **volume**. These are different things.

---

## 2. Driving Factors of Cost

The three primary cost drivers across all AWS services:

### Compute
- Billed by time (per hour or per second)
- Clock starts when instance **launches**, stops when **stopped or terminated**
- EC2, Lambda, ECS are primary examples

### Storage
- Billed by amount stored and duration
- **EBS**: charged on **provisioned** capacity (pay for what you allocate, not just what you use)
- **S3**: tiered pricing — charged on actual usage

#### S3 Has 6 Cost Components:
1. Storage pricing
2. Request and data retrieval pricing
3. Data transfer and transfer acceleration pricing
4. Data management and analytics pricing
5. Replication pricing
6. S3 Object Lambda processing pricing

### Outbound Data Transfer
- **Inbound to AWS** → generally **free**
- **Between services in the same region** → generally **free**
- **Outbound from AWS** → **costs money**
- **Cross-region transfer** → **costs money**
- Outbound transfer is **aggregated across services** — volume discounts apply

> ⚠️ **Key concept:** When an EC2 instance runs, you may be billed across all three drivers simultaneously: compute (instance running), storage (EBS volume), and data transfer (outbound traffic).

---

## 3. AWS Pricing and Billing Services

### Tool Decision Framework

| Tool | Purpose | When to Use |
|---|---|---|
| **AWS Pricing Calculator** | Estimate costs **before** deployment | Pre-deployment planning, comparing configurations |
| **AWS Billing Dashboard** | High-level view of **current month** spend | Quick snapshot of charges, manage payment methods |
| **AWS Budgets** | Set spending **limits and alerts** | Proactive — warns you **before** you overspend |
| **AWS Cost Explorer** | Analyze **historical** costs + forecast | Reactive — understand past trends, RI recommendations |
| **AWS Organizations** | Manage and **consolidate billing** across multiple accounts | Multi-account environments, org-wide governance |

### AWS Organizations — Consolidated Billing
- One **management (primary) account** receives the single bill
- **Member (sub) accounts** are linked and separated by team, project, or department
- Volume discounts are applied **across all accounts** in the organization — usage is aggregated
- Does NOT mean the management account controls sub-account resources (that's SCPs)

### Tags — Cost Allocation
- Tags are **key-value metadata** pairs attached to AWS resources
- Example: `Environment: Dev`, `Project: DonationApp`, `Department: Engineering`
- Both AWS Budgets and Cost Explorer can filter by tags
- Enables answering: "Which project is driving the most cost this month?"
- **Best practice:** Establish a tagging strategy early — retroactive attribution is very difficult

> ⚠️ **Exam Trap Q6:** "Monitor and consolidate billing across multiple accounts" → **AWS Organizations**, not the Billing Dashboard. The dashboard shows costs; Organizations manages and consolidates accounts.

---

## 4. AWS Support Plans

### Plan Comparison Table

| Feature | Basic | Developer | Business | Enterprise On-Ramp | Enterprise |
|---|---|---|---|---|---|
| **Cost** | Free | Paid | Paid | Paid | Paid (highest) |
| **Best for** | All customers | Experimenting/testing | Production workloads | Production + business-critical | Business/mission-critical |
| **Contact method** | Docs/forums only | Email only | Phone, email, chat | Phone, email, chat | Phone, email, chat |
| **General guidance** | — | < 24 hrs | < 24 hrs | < 24 hrs | < 24 hrs |
| **System impaired** | — | < 12 hrs | < 4 hrs | < 4 hrs | < 4 hrs |
| **Production system down** | — | — | < 1 hr | < 1 hr | < 1 hr |
| **Business/mission-critical down** | — | — | — | < 30 min | **< 15 min** |
| **Trusted Advisor** | 7 core checks | 7 core checks | Full suite | Full suite | Full suite + prioritized recommendations |
| **TAM** | ❌ | ❌ | ❌ | Pool of TAMs | **Designated TAM** |
| **Infrastructure Event Mgmt** | ❌ | ❌ | Extra fee | Included | Included |

### Key Plan Facts
- Every plan is a **superset** of the one below — you never lose features going up
- **Basic** is free and includes: 24/7 docs/forums, AWS re:Post, Trusted Advisor (7 core checks), Personal Health Dashboard
- **Developer** adds: direct email support
- **Business** adds: phone access, full Trusted Advisor suite
- **Enterprise On-Ramp** adds: pool of TAMs, < 30 min critical response
- **Enterprise** adds: designated TAM, < 15 min critical response, prioritized TA recommendations

### Technical Account Manager (TAM)
- Available at **Enterprise On-Ramp** (shared pool) and **Enterprise** (designated)
- Serves as your primary AWS contact
- Proactively monitors your environment
- Advises on architecture, cost optimization, and best integration approaches

---

## 5. Additional Support Resources

These exist alongside (not instead of) support plans:

| Resource | Purpose | Available To |
|---|---|---|
| **AWS re:Post** | Community Q&A platform; also hosts AWS Knowledge Center | Everyone |
| **AWS Knowledge Center** | Articles and videos on most common customer questions | Everyone (via re:Post) |
| **AWS Trust and Safety Center** | Report abusive or suspicious AWS activity | Everyone |
| **AWS Solutions Architects** | Architectural guidance, best practices, scalable/secure design | Business and Enterprise customers |
| **AWS Professional Services** | Deep consulting for complex migrations, security audits, performance tuning | Paid engagement |
| **Self-Support / Documentation** | User guides, SDK guides, blog posts, whitepapers | Everyone |

> **Decision hierarchy:** Self-support/re:Post first → Solutions Architects for architecture (Business+) → TAM for ongoing relationship (Enterprise) → Professional Services for project-based deep work

---

## 6. AWS Marketplace and AWS Partner Network

### AWS Marketplace
- Curated digital catalog of **third-party software** that runs on AWS
- Software from Independent Software Vendors (ISVs)
- **Key categories:** SaaS, ML/AI, Data & Analytics, Security, Networking, Storage
- **Pricing models:** Free, pay-as-you-go, annual subscriptions, BYOL
- Billing consolidates into your AWS bill (no separate vendor invoices)
- Can browse by **industry vertical** (healthcare, finance, etc.)

> ⚠️ **Exam Rule:** Marketplace = **third-party software**. Native AWS services (S3, EC2, EBS) and physical hardware are **NOT** Marketplace products.

### AWS Partner Network (APN)
- Global ecosystem of technology and consulting companies that build on AWS
- **Technology Partners:** Build software/products on AWS (ISVs, SaaS companies)
- **Consulting Partners:** Help customers design, migrate, and manage AWS environments

#### Benefits of Becoming an AWS Partner:
- **Funding benefits** — financial incentives to build, market, and sell with AWS
- **AWS Partner events** — webinars, workshops, networking with AWS experts
- **AWS Partner Training and Certification** — partner-centered learning paths

> ⚠️ **Exam Trap Q5:** APN benefit = **AWS Partner Funding**, not "early access to all AWS services." Early access is limited and program-specific, not a blanket benefit.

---

## 7. Cost Optimization Techniques

### EC2 Optimization
| Technique | How It Helps |
|---|---|
| **Rightsizing** | Analyze with AWS Compute Optimizer; match instance size to actual workload demand |
| **Spot Instances** | Up to 90% cheaper than On-Demand; use for interruptible, fault-tolerant workloads |
| **Auto Scaling** | Automatically removes excess capacity when demand drops |
| **Account cleanup** | Delete unused EBS volumes, old snapshots, idle instances — these silently accumulate charges |

### RDS Optimization
| Technique | How It Helps |
|---|---|
| **Rightsizing** | RDS storage autoscaling prevents over/underprovisioning |
| **Read Replicas** | Scale read traffic **horizontally** instead of upgrading the primary instance vertically |
| **ElastiCache** | Store frequently accessed data in-memory; reduces load on primary database instance |

### S3 Optimization
| Technique | How It Helps |
|---|---|
| **Right storage class** | Match class to access frequency (see table below) |
| **Data compression** | Use Lambda to compress objects on upload; less storage = lower bill |
| **Lifecycle policies** | Auto-delete or transition objects after set periods |
| **VPC Endpoints** | Private connection to S3 — avoids public internet, reduces data transfer costs |

#### S3 Storage Class Selection Guide
| Access Pattern | Storage Class |
|---|---|
| Frequent access | S3 Standard |
| Infrequent (monthly) | S3 Standard-IA |
| Unknown/changing patterns | **S3 Intelligent-Tiering** |
| Archive, retrieved in minutes | S3 Glacier Flexible Retrieval |
| Accessed once or twice a year | **S3 Glacier Deep Archive** (cheapest) |

### Networking / Architecture Optimization
- **Minimize inter-AZ traffic** — cross-AZ data transfer within a region costs money
- **VPC Endpoints** — keeps traffic within AWS network (no public internet charges); applies to both cost optimization AND security

---

## 8. Exam Traps and Key Distinctions

| Trap | Correct Answer |
|---|---|
| "Save when you commit" vs "Pay less by using more" | Commit = **time**; More = **volume** |
| Cost drivers vs. service categories | Drivers = compute, storage, outbound data transfer (not networking, database, etc.) |
| Billing Dashboard vs. AWS Organizations | Dashboard = **visibility**; Organizations = **account management + consolidation** |
| Pricing Calculator vs. Cost Explorer | Calculator = **pre-deployment estimate**; Explorer = **historical analysis + forecast** |
| AWS Budgets vs. Cost Explorer | Budgets = **proactive alerts**; Explorer = **reactive analysis** |
| Enterprise vs. Enterprise On-Ramp TAM | On-Ramp = **pool** of TAMs; Enterprise = **designated** TAM |
| Which plan gives full Trusted Advisor? | **Business and above** |
| Which plan gives phone access? | **Business and above** |
| APN = customer support? | ❌ APN supports **partners**, not end users. Customer support = AWS Support plans |
| Marketplace = AWS native services? | ❌ Marketplace = **third-party software only** |
| Early access as APN benefit? | ❌ Concrete APN benefit = **Partner Funding** |
| "Dedicated TAM" for mission-critical? | **Enterprise** (not Enterprise On-Ramp) |

---

*Module 11 Assessment Score: 100% (10/10)*
*Passing threshold: 80%*