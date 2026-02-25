# AWS Study Notes — FCC CLF-C02
### Source: freeCodeCamp AWS Cloud Practitioner Course (ExamPro)
### Cross-referenced against official AWS documentation, February 2026

---

## 1. AWS Well-Architected Framework & Tool

### What the Framework Is
The AWS Well-Architected Framework is a **white paper** containing best practices and design principles organized across multiple pillars. It helps you evaluate and improve cloud workloads for alignment with AWS standards.

**The Six Pillars:**
- Operational Excellence
- Security
- Reliability
- Performance Efficiency
- Cost Optimization
- Sustainability

> ✅ **Where to find it:** Search "AWS well architected framework white papers" at `amazon.com/whitepapers`. It opens as an HTML page with each pillar's design principles, definitions, and best practices. Required reading at the Solutions Architect level — surface-level knowledge sufficient for Cloud Practitioner.

### What the Well-Architected Tool Is
The **AWS Well-Architected Tool** is an auditing tool in the AWS Management Console used to assess your Cloud workloads against the framework.

- **Functions as a structured checklist** — each question maps to a pillar of the framework
- Provides inline reference information as you answer each question
- Supports multiple **lenses** (e.g., AWS Well-Architected Framework lens, Foundational Technical Review lens, SaaS lens)
- When complete, **generates a report** identifying high-risk and medium-risk findings to share with executives and stakeholders

**How to Use It:**
1. Go to the Well-Architected Tool in the console
2. Define a new **Workload** (name, environment type, region)
3. Select a lens
4. Work through the checklist (e.g., "How do you determine what your priorities are?")
5. Answer each question; click **Info** for contextual guidance
6. Save and exit — findings are scored and categorized by risk level

> 💡 **Practical tip:** The checklist questions closely mirror the white paper sections. You can use the tool itself as a study aid without reading the full document.

---

## 2. AWS Architecture Center

The **AWS Architecture Center** is a web portal at `aws.amazon.com/architecture` that contains:
- **Best practices** organized by category (security, databases, serverless, etc.)
- **Reference architectures** — real-world architectural diagrams for common workloads

### Key Features
- Browse by use case (e.g., "Build a Q&A bot with AWS")
- Each reference architecture includes:
  - An architectural diagram
  - A CloudFormation or CDK deployment template (deploy with one click)
  - Written implementation guidance
- Great for moving from theory (the Well-Architected Framework) to **concrete implementation examples**

> ✅ Many resources linked from the Well-Architected Framework white paper point back to the Architecture Center.

---

## 3. Total Cost of Ownership (TCO)

### Definition
**TCO (Total Cost of Ownership)** is a financial estimate intended to help organizations determine both the **direct and indirect costs** of a product or service. It is used primarily when planning a migration from on-premises to the cloud.

### On-Premises TCO (Common Hidden Costs)
Most organizations only think about obvious costs. TCO forces you to account for all of them:

| Obvious ("Above the Iceberg") | Hidden ("Below the Iceberg") |
|---|---|
| Software license fees | Physical security |
| Subscription fees | Hardware lifecycle management |
| — | IT personnel |
| — | Maintenance and repair |
| — | Installation & configuration |
| — | Training |
| — | Cooling and power |
| — | Taxes |

### Cloud TCO vs. On-Premises TCO
- On-premises: You are responsible for **all layers** above
- AWS: AWS absorbs the hardware and physical infrastructure costs; you focus on **implementation, configuration, and training**
- AWS's old TCO calculator advertised **75% savings** over a 3-year period — actual savings vary widely by organization

### Migration Cost Spike (Gartner Research)
A Gartner study of an organization migrating 2,500 VMs to EC2 showed:
- Costs **initially increased** during the migration period (6–12+ months)
- Once migration was complete, they achieved approximately a **55% cost reduction**
- **Key lesson:** Always account for migration costs when building a TCO comparison — they are a real, temporary spike

---

## 4. CapEx vs. OpEx

| | CapEx (Capital Expenditure) | OpEx (Operational Expenditure) |
|---|---|---|
| **What it is** | Upfront spending on physical infrastructure | Ongoing costs for services consumed |
| **Example costs** | Servers, storage, networking, data center, DR | Cloud usage fees, SaaS subscriptions, training |
| **Tax treatment** | Depreciated over time | Deducted in the year incurred |
| **Planning model** | Must guess capacity upfront | Pay for actual consumption |
| **On-prem vs Cloud** | Traditional on-premises model | Cloud / AWS model |

> 🎯 **Exam tip:** CapEx = on-premises thinking. OpEx = cloud thinking. Moving to the cloud shifts spending from CapEx to OpEx.

**Why companies resist moving:**
- CapEx spending often comes with **government tax breaks** for depreciation — finance teams are reluctant to give this up
- Cloud OpEx does not have the same depreciation advantage

**OpEx advantage:**
- You can **try a product or service without investing in equipment**
- No need to predict capacity years in advance

---

## 5. Does Cloud Migration Make IT Personnel Redundant?

A common concern when migrating. The answer is **no** — roles shift, not disappear.

**What actually happens:**

- **During migration:** IT staff are still needed to assist with the migration process itself
- **After migration:** Roles can transition to cloud equivalents (e.g., traditional network engineers transition to cloud networking roles)
- **Hybrid approach:** Some companies maintain both on-premises and cloud teams
- **Revenue reallocation (exam answer):** Companies can **shift employees from managing infrastructure to revenue-generating activities** — this is the answer most likely to appear on the exam

---

## 6. AWS Pricing Calculator

### What It Is
A **free, browser-based cost estimation tool** available at `calculator.aws`. No AWS account required.

- Contains **100+ configurable services**
- Provides both **Quick Estimate** (ballpark) and **Advanced Estimate** (detailed) modes
- Estimates can be **exported as CSV** or **shared via a public link**

### How to Use It
1. Go to `calculator.aws` → Create Estimate
2. Add a service (e.g., EC2, RDS)
3. Configure options:
   - Instance type (e.g., t2.micro, t3.micro)
   - OS (Linux, Windows)
   - Usage pattern (on-demand, reserved)
   - Storage, data transfer
4. Add more services and review the **monthly summary**

> 💡 **TCO use case:** To calculate your organization's TCO comparison, use the AWS Pricing Calculator for the AWS side, then compare against your known on-premises costs.

---

## 7. Migration Evaluator

Formerly known as **TSO Logic** (acquired by AWS).

- An **on-premises cost analysis tool** — helps determine what your current infrastructure is actually costing you
- Uses an **agentless collector** installed on your environment to automatically extract data from your on-premises infrastructure
- Supports: VMware, Microsoft Hyper-V, SQL Server, and others
- Output: detailed report comparing your on-premises costs to projected AWS costs for migration planning

> ✅ **Difference from Pricing Calculator:** Migration Evaluator analyzes your *existing* environment; the Pricing Calculator estimates *future* AWS costs.

---

## 8. VM Import/Export

Allows you to **import virtual machines from on-premises into EC2**.

**Supported source formats:**
- VMware
- Citrix
- Microsoft Hyper-V
- Windows VHD (from Azure)
- Linux VHD (from Azure)

**How it works:**
1. Prepare your virtual image per AWS instructions
2. Upload the image to an **S3 bucket**
3. Use the **AWS CLI** to import the image (`aws ec2 import-image`)
4. AWS generates an **AMI (Amazon Machine Image)** from the uploaded file
5. Launch EC2 instances from that AMI

---

## 9. AWS Database Migration Service (DMS)

### What It Is
**DMS** enables you to quickly and securely migrate one database to another. Most commonly used to migrate on-premises databases to AWS.

### Architecture
- **Source database** → Source endpoint → **Replication instance (EC2)** → Target endpoint → **Target database**

### Supported Sources (partial list)
Oracle, Microsoft SQL Server, MySQL, MariaDB, PostgreSQL, MongoDB, SAP, IBM Db2, Azure SQL, Amazon RDS, Amazon S3, Amazon Aurora, Amazon DocumentDB

### Supported Targets (partial list)
Oracle, Microsoft SQL Server, MySQL, MariaDB, PostgreSQL, Redis, SAP, Amazon Redshift, Amazon RDS, Amazon DynamoDB, Amazon S3, Amazon Aurora, Amazon OpenSearch, Amazon ElastiCache, Amazon DocumentDB, Amazon Neptune, Apache Kafka

### Schema Conversion Tool (SCT)
When migrating between **incompatible database types** (e.g., relational → NoSQL, or Oracle → Aurora), the **AWS Schema Conversion Tool** automates or semi-automates the conversion of the source schema to the target schema.

> 💡 **Not all migration paths are possible** — research your specific source/target combination. Database version matters too.

---

## 10. AWS Cloud Adoption Framework (CAF)

A **white paper** providing guidance for planning your migration from on-premises to AWS. Organizes migration guidance into **six perspectives (focus areas):**

| Perspective | Key Stakeholders | Focus |
|---|---|---|
| **Business** | Business managers, Finance, Strategy | Optimize business value during migration |
| **People** | HR, Staffing, People managers | Update staff skills and maintain workforce competencies |
| **Governance** | CIOs, Program managers, Enterprise architects | Ensure business governance and measure cloud investments |
| **Platform** | CTOs, IT managers, Solution architects | Deliver and optimize cloud solutions and services |
| **Security** | CISO, IT security managers/analysts | Align cloud architecture to security, resilience, and compliance requirements |
| **Operations** | IT operations/support managers | Ensure system health and reliability during and after migration |

> 🎯 **Exam tip:** Know the six perspectives and their key stakeholders. Questions often ask which perspective applies to a given role (e.g., CISO → Security perspective).

---

## 11. AWS Support Plans

You **absolutely must know this inside and out for the exam.** There are four tiers:

### Overview Table

| Feature | Basic | Developer | Business | Enterprise |
|---|---|---|---|---|
| **Cost** | Free | $29/mo or 3% usage | $100/mo or tiered % | $15,000/mo or tiered % |
| **Email support** | Billing/account only | ✅ (24hr response) | ✅ (24hr response) | ✅ (24hr response) |
| **Third-party support** | ❌ | ❌ | ✅ | ✅ |
| **Phone/Chat** | ❌ | ❌ | ✅ | ✅ |
| **Trusted Advisor checks** | 7 (security only) | 7 (security only) | All checks | All checks |
| **TAM (Technical Account Manager)** | ❌ | ❌ | ❌ | ✅ |
| **Concierge Team** | ❌ | ❌ | ❌ | ✅ |

### Response Time SLAs

| Severity | Developer | Business | Enterprise |
|---|---|---|---|
| General guidance | < 24 hours | < 24 hours | < 24 hours |
| System impaired | < 12 hours | < 12 hours | < 12 hours |
| Production system impaired | — | < 4 hours | < 4 hours |
| Production system down | — | < 1 hour | < 1 hour |
| Business-critical system down | — | — | < 15 minutes |

> ⚠️ **Real-world caveat (from instructor):** These response times are targets, not always met. Higher tiers generally get faster responses.

### Cost Calculation Examples
- **Developer:** `$29/mo` OR `3% of monthly usage`, whichever is greater
  - $500 spend → 3% = $15 → pay **$29** (minimum)
  - $1,000 spend → 3% = $30 → pay **$30**
- **Business:** Tiered percentages (10% of first $10K, then lower rates above that)
  - $1,000 spend → 10% = **$100**
  - $12,000 spend → 10% of $10K ($1,000) + 7% of $2K ($140) = **$1,140**

> 🎯 **Exam note:** You won't be asked to calculate exact amounts — just know the tier of expense and which features belong to which plan.

---

## 12. Technical Account Manager (TAM)

A **TAM** is a dedicated AWS employee available only at the **Enterprise support tier** who provides both proactive guidance and reactive support.

### What a TAM Does
- Builds solutions and provides technical guidance
- Ensures your AWS environment is operationally healthy while reducing cost and complexity
- Develops a trusting relationship — understands your business needs and technical challenges
- Drives technical discussions on incidents, tradeoffs, and risk management
- Consults with stakeholders from developers to C-Suite executives
- Collaborates with Solutions Architects, Professional Services consultants, and sales
- Proactively identifies opportunities to gain additional value from AWS
- Provides detailed reviews of service disruptions and metrics
- Delivers pre-launch planning and post-launch consultative expertise
- Runs workshops and "Brown Bag Sessions" (30–60 min lunchtime learning sessions)

> ✅ **Key fact:** TAMs follow Amazon's Leadership Principles, especially **Customer Obsession**. TAMs are exclusively available at the **Enterprise support tier**.

---

## 13. AWS Marketplace

A **curated digital catalog** with thousands of software listings from Independent Software Vendors (ISVs).

- Browse, buy, test, and deploy software that already runs on AWS
- Products can be **free** or **paid** — charges are added directly to your AWS bill
- AWS Marketplace then pays the vendor/provider
- Acts as a **sales channel** for ISVs and Consulting Partners selling solutions to other AWS customers

**Types of products available:**
- AMIs (pre-configured EC2 images)
- CloudFormation templates
- SaaS offerings
- Web ACLs / WAF rules
- Containers

> 💡 **Where you encounter it:** The Marketplace is embedded in many AWS services — for example, when launching an EC2 instance, the "AWS Marketplace" tab in the AMI selection screen is the same catalog.

---

## 14. Consolidated Billing (AWS Organizations)

A feature of **AWS Organizations** that allows you to pay for multiple AWS accounts via a **single bill**.

### How It Works
- Designate one **management (root) account** that pays charges for all member accounts
- Member accounts within the organization are billed through the management account
- Accounts outside the organization have their own separate bills
- Cost: **Free** (no additional charge for consolidated billing)

### Benefits
- **Single bill** for all accounts
- **Volume discounts** — AWS treats all accounts in the org as one for pricing tiers
  - Example: Two accounts each using 4 TB of data transfer pay individually at a higher rate; consolidated, their combined 8 TB may push into a lower-rate tier — saving ~$80
- Visualize usage across accounts with **Cost Explorer**
- Accounts can leave the organization but must attach a new payment method first

> ✅ **Exam tip:** Volume discounts are a key reason to use consolidated billing. You won't get them unless accounts are within an AWS Organization.

---

## 15. AWS Trusted Advisor

An **automated recommendation tool** that continuously monitors your AWS account and provides best-practice recommendations across five categories:

| Category | Examples |
|---|---|
| **Cost Optimization** | Idle load balancers, unassociated Elastic IPs |
| **Performance** | High-utilization EC2 instances that could be resized |
| **Security** | MFA on root account, key rotation, open security groups |
| **Fault Tolerance** | RDS backups disabled, no multi-AZ |
| **Service Limits** | VPC count approaching limit, EC2 instance limits |

### Checks Available by Support Tier

| Tier | Trusted Advisor Checks |
|---|---|
| Basic / Developer | 7 checks (security-focused only) |
| Business / Enterprise | **All checks** |

**Free security checks (available on all tiers):**
1. MFA on root account
2. Security groups — unrestricted ports
3. S3 bucket permissions
4. EBS public snapshots
5. RDS public snapshots
6. IAM use (discourages root account usage)
7. Service limits (all service limit checks are free)

> 💡 **Think of Trusted Advisor as:** An automated checklist of AWS best practices that loosely maps to the Well-Architected Framework pillars.

---

## 16. Service Level Agreements (SLAs)

### Key Terms

| Term | Definition |
|---|---|
| **SLA** (Service Level Agreement) | Formal commitment between customer and provider on expected service levels; customer eligible for compensation if missed |
| **SLI** (Service Level Indicator) | A metric measuring actual performance (e.g., uptime, latency, error rate, durability) |
| **SLO** (Service Level Objective) | The specific target percentage the provider has agreed to meet (e.g., 99.99% availability over 3 months) |

### Target Percentage Notation

| Notation | Meaning |
|---|---|
| 99.95% | "Three nines five" |
| 99.99% | "Four nines" |
| 99.999% | "Five nines" |
| 99.9999999% | "Nine nines" |

### Example AWS SLAs

**DynamoDB:**
- Global Tables: 99.999%
- Standard Tables: 99.99%
- If uptime drops below 99% but ≥ 95%: 25% service credit
- If uptime drops below 95%: 100% service credit

**Compute (EC2, EBS, ECS, EKS):**
- Region level and instance level SLAs tracked separately

**RDS (Multi-AZ):**
- 99.95% monthly uptime commitment

> 🎯 **Exam note:** You won't be asked for specific SLA percentages per service. Know the concepts (SLA, SLI, SLO) and that compensation comes in the form of **service credits**.

---

## 17. AWS Health Dashboards

There are **two different health dashboards** — don't confuse them.

### Service Health Dashboard
- Shows the **general status of all AWS services** globally
- Browse by geographic area (North America, Europe, etc.)
- Simple status icons: Operating Normally, Degraded, Outage
- Includes **RSS feed** for updates
- URL: `status.aws.amazon.com`

### Personal Health Dashboard (AWS Health)
- **Personalized alerts** for events that may affect *your specific* AWS environment
- All AWS customers have access
- Shows:
  - Recent events active in your environment
  - Proactive notifications for scheduled maintenance
  - Guidance to diagnose and resolve issues affecting your resources
- Use this to create **alerts triggered when changes affect your resources**

> 🎯 **Key distinction for the exam:** Service Health Dashboard = global status for everyone. Personal Health Dashboard = tailored to *your* account and resources.

---

## 18. AWS Trust & Safety Team

A dedicated AWS team that handles **abuse reports** involving AWS infrastructure. Contact them (not regular support) for:

| Abuse Type | Description |
|---|---|
| **Spam** | Receiving unwanted emails from AWS-owned IPs, or AWS resources used to spam |
| **Port Scanning** | AWS IPs sending packets to multiple ports (attempting to find unsecured ports) |
| **DoS Attack** | AWS IPs used to flood your ports with traffic |
| **Intrusion Attempts** | AWS IPs used to attempt unauthorized login to your resources |
| **Prohibited Content Hosting** | AWS resources hosting illegal or unauthorized copyrighted content |
| **Malware Distribution** | AWS resources distributing malicious software |

**How to report:**
- Email: `abuse@amazonaws.com`
- Or fill out the **Report Amazon AWS Abuse** form

> ✅ This applies whether the abuse is coming from an external AWS account or from a compromised account you own.

---

## 19. AWS Free Tier

Three categories of free offerings:

| Type | Description | Example |
|---|---|---|
| **12 Months Free** | Free up to a usage limit for the first year after sign-up | EC2 t2.micro (750 hrs/mo), RDS t2.db.micro (750 hrs/mo) |
| **Always Free** | Free usage up to a monthly limit forever | Lambda (1M requests/mo), S3 (5 GB), DynamoDB (25 GB) |
| **Free Trials** | Short-term free access to specific services | Varies by service |

### Notable Free Tier Highlights (12 Months)

| Service | Free Allowance |
|---|---|
| EC2 | 750 hours/month (t2.micro) |
| RDS | 750 hours/month (t2.db.micro, MySQL or PostgreSQL) |
| Classic Load Balancer | 750 hours/month |
| CloudFront | 50 GB data transfer out (total for year) |
| ElastiCache | 750 hours (cache.t3.micro) |
| Amazon Connect | 90 minutes of call time/month |
| Pinpoint | 5,000 targeted users/month |
| CodeBuild | 100 build minutes/month |

### Notable Always Free

| Service | Free Allowance |
|---|---|
| Lambda | 1 million requests/month; 3.2M seconds compute/month |
| SES | 62,000 emails/month (when sent from EC2) |
| CodePipeline | 1 active pipeline free |

### AWS Services That Are Always Free (No Usage Limit)

Some AWS services are **free to use entirely** — they don't have a usage cap, they just cost nothing. This is separate from the free tier above. The services themselves are free, but be aware: **some of these services can provision other resources that do cost money.**

| Service | Caveat |
|---|---|
| Amazon VPC | Free — but resources inside it (EC2, NAT Gateways, etc.) cost money |
| Auto Scaling | Free — but the EC2 instances it launches cost money |
| CloudFormation | Free — but the resources it provisions (EC2, RDS, etc.) cost money |
| Elastic Beanstalk | Free — but the underlying EC2/RDS it spins up cost money |
| OpsWorks | Free — but servers it launches cost money |
| Amplify | Free — but Lambdas and other services it uses cost money |
| AppSync | Free tier, then paid beyond it |
| CodeStar | Free |
| AWS Organizations | Free |
| Consolidated Billing | Free |
| Cost Explorer | Free |
| Systems Manager (SSM) | Free for most features |
| SageMaker Studio | Free (compute used within it costs money) |

> ⚠️ **Key exam concept:** "The service is free but may launch resources that cost money." This is the distinction AWS draws — CloudFormation itself doesn't cost you anything, but if it creates 10 EC2 instances, those EC2 instances will be billed normally.

---

## 20. AWS Promotional Credits

- Equivalent to **USD dollars** on the AWS platform
- How to earn them:
  - AWS Activate (startup program)
  - Winning a hackathon
  - Participating in AWS surveys
  - Other AWS-granted promotions
- To redeem: Use the **Redeem Credit** button in the Billing console, enter your code
- Monitor via: **AWS Budgets** or **Cost Explorer**
- Credits have an **expiration date** (typically a few months to a year)
- **Cannot be used for:** Purchasing domains via Route 53 (domain registrations involve real-world costs outside AWS's infrastructure)

---

## 21. AWS Partner Network (APN)

A **global partner program** for organizations building on or selling AWS.

### Partner Types

| Type | Description |
|---|---|
| **Consulting Partner** | Organizations that help companies utilize AWS (e.g., migration consultancies) |
| **Technology Partner** | Organizations that build technology products/services on top of AWS |

### Partner Tiers
- **Select → Advanced → Premier**
- Tiers require:
  - An **annual fee** (starts in the thousands of dollars, increases per tier)
  - **Certification requirements** (AWS certifications at foundational/associate level, or APN-exclusive training certifications)

### Benefits of APN Membership
- **Promotional AWS credits** (typically offset the annual fee commitment)
- Access to **exclusive training and marketing events**
- **Speaking opportunities** via official AWS marketing channels (blogs, webinars)
- **Vendor booth sponsorship** at AWS events (re:Invent, etc.) — requires APN membership

---

## 22. AWS Budgets

A service to **set spending alerts** so you're notified before or when you exceed a defined budget.

### Budget Types
- **Cost budget** — alert when spend reaches a dollar threshold
- **Usage budget** — alert based on service usage units (e.g., EC2 running hours)
- **Reservation budget** — monitor reserved instance/savings plan utilization

### Key Features
- Track at **monthly, quarterly, or yearly** intervals with customizable date ranges
- Supports reservations for EC2, RDS, Redshift, ElastiCache
- Alerts via **email** or **chatbot** at configurable thresholds (actual or forecasted)
- First **2 budgets are free**; each additional budget costs ~$0.02/day (~$0.60/month)
- Up to **20,000 budgets** supported

> 💡 **Best practice:** Set at least one budget immediately after creating an AWS account — the first two are free.

---

## 23. AWS Budget Reports

Used alongside AWS Budgets to automatically send **daily, weekly, or monthly budget performance reports** via email to specified recipients.

- More convenient than logging into the console to check budget status
- Configure: report name → select budgets to include → choose frequency → add email recipients

---

## 24. AWS Cost and Usage Report (CUR)

Generates a **detailed spreadsheet** of all AWS costs and usage data.

### Features
- Stored in an **S3 bucket** (configured when you enable the report)
- Granularity options: **hourly, daily, or monthly**
- Contains **cost allocation tags** (once activated)
- Data format: **CSV (compressed/zipped)** or **Parquet**

### Integration Options

| Tool | Use Case |
|---|---|
| **Amazon Athena** | Query the CUR data directly from S3 as SQL |
| **Amazon QuickSight** | Visualize billing data as dashboards/graphs |
| **Amazon Redshift** | Ingest CUR for large-scale analytics |

> 🎯 **Exam tip:** CUR is the most detailed billing data source available. Use it when you need granular analysis beyond what Cost Explorer provides.

---

## 25. Cost Allocation Tags

Optional **key-value metadata** attached to AWS resources that appear in billing reports.

### Tag Types
- **User-defined tags** — tags you created on your resources (e.g., `Project: Apollo`, `Department: Engineering`)
- **AWS-generated tags** — system tags AWS creates (e.g., `aws:cloudformation:stack-name`)

### How to Activate
Go to **Cost Allocation Tags** in the Billing console → activate the specific tag keys you want to appear in Cost and Usage Reports.

> ⚠️ Tags must be **activated** before they show up in billing reports — simply tagging a resource is not enough.

---

## 26. Billing Alarms (CloudWatch)

You can create **CloudWatch Alarms** that monitor billing metrics and trigger notifications when spend exceeds a threshold.

- Billing alerts must be **enabled first** in the Billing preferences console before CloudWatch billing metrics become available
- Go to CloudWatch → Alarms → choose **Billing** as the metric
- More **flexible** than AWS Budgets for complex monitoring scenarios

> 💡 **vs. AWS Budgets:** Budgets is simpler to configure and sufficient for most use cases. CloudWatch billing alarms offer more customization for complex alerting logic.

---

## 27. AWS Cost Explorer

A tool to **visualize, understand, and manage your AWS costs and usage over time**.

### Features
- Choose time range and aggregation (daily or monthly)
- Filter by service, region, linked account, tag, and more
- **Default reports** included:
  - Monthly cost by service
  - Monthly cost by linked account
  - Daily costs
  - Marketplace costs
  - Reservation utilization
- **Save custom reports** for repeated use
- **Forecasting** — project future costs based on historical trends
- Lives in the **us-east-1** region in the console

> 💡 **Practical tip:** The **Bills** page (in Billing & Cost Management) is often more useful than Cost Explorer for itemized, per-service breakdowns. Use both together.

---

## 28. AWS Pricing API

Allows programmatic access to current AWS pricing data.

| API Type | Also Known As | Access Method |
|---|---|---|
| **Query API** | Pricing Service API | Application JSON requests (via Postman or code) |
| **Batch API** | Price List API | HTML URLs (paste directly in browser) |

- Subscribe to **SNS notifications** to receive alerts when AWS prices change
- Prices change when AWS reduces prices, launches new instance types, or introduces new services

---

## 29. Savings Plans

A flexible pricing model offering **lower prices in exchange for a usage commitment** (measured in $/hour) over 1 or 3 years.

### Types of Savings Plans

| Plan | Applies To | Flexibility |
|---|---|---|
| **Compute Savings Plans** | EC2, Fargate, Lambda | Most flexible — any instance family, region, OS, tenancy |
| **EC2 Instance Savings Plans** | Specific instance family in a region | Less flexible, deeper discount |
| **SageMaker Savings Plans** | SageMaker ML compute | SageMaker-specific |

### Commitment Options
- **All Upfront** — deepest discount, pay full commitment now
- **Partial Upfront** — moderate discount, split payment
- **No Upfront** — smallest discount, pay monthly

**Term:** 1 year or 3 years (3-year = deeper discount)

### How to Purchase
1. Go to **Cost Explorer → Savings Plans**
2. Review **recommendations** based on your last 30 days of usage
3. Select a plan from recommendations → Add to Cart → Submit Order

> 💡 **Recommendations are auto-generated.** AWS will show you which plan would have saved you money based on your recent usage — the easiest way to get started.

---

## 30. Defense in Depth

A layered security model. Each layer protects assets from the outside in. Breaching one layer doesn't automatically compromise inner layers.

**Layers (outside → inside):**

1. **Physical** — Data center access controls, security guards, biometric locks
2. **Identity & Access** — IAM, MFA, access policies *(highlighted as the new primary perimeter from a customer perspective)*
3. **Perimeter** — DDoS protection (AWS Shield)
4. **Network** — VPCs, security groups, NACLs, segmentation
5. **Compute** — EC2 instance security, port management
6. **Application** — Secure code, patching, vulnerability management
7. **Data** — Encryption at rest and in transit, access controls

> 🎯 **Identity & Access is the most important layer for AWS customers** — especially in the context of Zero Trust architecture.

---

## 31. CIA Triad

The foundational model for information security, first documented in NIST Publication 1977.

| Principle | Definition | AWS Example |
|---|---|---|
| **Confidentiality** | Protect data from unauthorized viewers | Encryption with KMS, envelope encryption |
| **Integrity** | Ensure data accuracy and completeness over its lifecycle | Tamper-evident HSMs, ACID-compliant databases |
| **Availability** | Ensure data/systems are accessible when needed | Multi-AZ architectures, DDoS protection |

> 💡 The CIA Triad involves tradeoffs — you don't always get all three simultaneously. Security decisions often require choosing which properties to prioritize.

---

## 32. Encryption Fundamentals

### Cryptography
The practice and study of techniques for secure communication in the presence of adversaries.

### Encryption
The process of encoding information using a **key** and a **cipher** so that only authorized parties can read it.

- **Plain text** → (encrypt) → **Cipher text**
- **Cipher text** → (decrypt with key) → **Plain text**

### Cipher
An algorithm that performs encryption or decryption (synonymous with "code").

### Symmetric Encryption
- **Same key** used for both encryption and decryption
- Faster and simpler
- Primary AWS standard: **AES (Advanced Encryption Standard)**

### Asymmetric Encryption
- **Two different keys:** one to encrypt, one to decrypt
- Public key encrypts; private key decrypts (or vice versa for signing)
- Primary standard: **RSA** (named after Rivest, Shamir, and Adleman)

---

## 33. Hashing and Salting

### Hashing
A **one-way function** that maps any input to a fixed-size output. The same input always produces the same output (deterministic). You cannot reverse a hash to get the original input.

**Primary use case:** Storing passwords securely in databases.

**How it works at login:**
1. User enters password → system hashes it
2. Hash compared to stored hash in the database
3. If they match → user is authenticated
4. The original password is never stored

**Popular hash functions:** MD5, SHA-256, bcrypt

### Salting
A **random string** added to input before hashing to make the output unique even for identical inputs.

- **Problem it solves:** Without salting, an attacker who steals your database can enumerate a dictionary of common passwords and compare hashes (dictionary attack)
- With salting, even "password123" produces a different hash for every user because a unique random salt is prepended

---

## 34. Digital Signatures and Code Signing

### Digital Signature
A mathematical scheme for verifying the **authenticity and integrity** of a digital message or document.

**Three algorithms involved:**
1. **Key Generation** — generates a public/private key pair
2. **Signing** — uses the **private key** to sign the message
3. **Verification** — uses the **public key** to verify the signature

**Key principle:** Private key signs; public key verifies.

### SSH
- Uses public/private key pairs to authorize remote access to virtual machines
- Common algorithm: RSA
- Generate keys with: `ssh-keygen`

### Code Signing
Using a digital signature to ensure that **code has not been tampered with** since it was signed. Used to verify the integrity of software before execution or before committing to a repository.

---

## 35. Encryption In Transit vs. At Rest

| | Encryption In Transit | Encryption At Rest |
|---|---|---|
| **What it protects** | Data moving between systems over a network | Data stored on disk or in a database |
| **Common algorithms** | TLS, SSL | AES, RSA |
| **AWS example** | HTTPS connections to S3, API calls | S3 server-side encryption, RDS encryption |

### TLS and SSL
- **TLS (Transport Layer Security):** Current standard for data integrity in transit
  - TLS 1.2 and 1.3 are current best practice
  - TLS 1.0 and 1.1 are deprecated
- **SSL (Secure Sockets Layer):** Predecessor to TLS
  - SSL 1.0, 2.0, and 3.0 are all deprecated
  - The term "SSL" is still colloquially used even when TLS is being used

---

## 36. Common Compliance Programs

A **compliance program** is a set of internal policies and procedures for a company to comply with laws, regulations, or maintain business reputation.

| Program | Description |
|---|---|
| **ISO 27001** | Control implementation guidance (most widely adopted) |
| **ISO 27017** | Enhanced focus on cloud security |
| **ISO 27018** | Protection of personal data in the cloud |
| **ISO 27701** | Privacy Information Management System (PII framework) |
| **SOC 1** | Internal controls over financial reporting |
| **SOC 2** | Security, availability, processing integrity, confidentiality, privacy (most important for cloud) |
| **SOC 3** | Publicly distributable report based on Trust Services Criteria |
| **PCI DSS** | Security standards for organizations handling credit card data |
| **FIPS 140-2** | US/Canadian government standard for cryptographic module security |
| **PHIPA** | Ontario, Canada — patient health information protection |
| **HIPAA** | US federal law — patient health information protection |
| **CSA STAR** | Independent third-party cloud security assessment |
| **FedRAMP** | US Government — risk/authorization management for cloud services |
| **CJIS** | FBI database access requirement for US state/local agencies |
| **GDPR** | EU privacy law — governs data collection and processing of EU residents |

> 🎯 **For the exam:** Know the most common ones: SOC 2, PCI DSS, HIPAA, GDPR, FedRAMP. The others are good general knowledge for your career.

---

## 37. AWS Artifact

A **self-serve portal** for on-demand access to AWS compliance reports and agreements.

- Available within the **AWS Management Console** (search "Artifact")
- Download compliance reports such as:
  - SOC reports
  - PCI compliance reports
  - ISO certifications
  - Government-specific packages (e.g., Government of Canada Partner Package)
- Reports are typically **PDF files** with embedded links to detailed Excel spreadsheets
- **Requires Adobe Acrobat** to properly open and access links within the PDF

> 🎯 **Exam tip — Artifact vs. Inspector:** Both generate PDF reports, but they're completely different:
> - **Artifact:** Proves that AWS itself is compliant with global compliance frameworks
> - **Inspector:** Proves that *your EC2 instance* is secure

---

## 38. Penetration Testing on AWS

You are **allowed** to perform pen testing on AWS, with restrictions.

### Permitted Services (No Prior Approval Needed)
EC2 instances, NAT Gateways, ELBs, RDS, CloudFront, Aurora, API Gateways, Lambda (and Lambda@Edge), Lightsail resources, Elastic Beanstalk environments

### Prohibited Activities
- DNS Zone Walking via Route 53 hosted zones
- DoS or DDoS simulation
- Port flooding
- Protocol flooding
- Request flooding

### Simulated Events (Requires Approval)
For anything not explicitly permitted, **submit a request** to AWS via the Simulate Event form. AWS may take up to **7 days** to respond.

---

## 39. Amazon Inspector

A security tool for **hardening EC2 instances**.

### What Hardening Is
Eliminating as many security risks as possible from a virtual machine by running a collection of security checks against it (a **security benchmark**).

### How Amazon Inspector Works
1. Install the **AWS Inspector Agent** on your EC2 instance
2. Define an **Assessment Target** (which instances to scan)
3. Select **Assessment Type:**
   - **Network Assessment** — identifies network exposure
   - **Host Assessment** — examines the instance OS and software
4. Run the assessment
5. Review **findings** — a list of vulnerabilities and misconfigurations with severity ratings
6. Remediate security issues

### CIS Benchmark
A popular benchmark Inspector can run: **699 checks** from the **Center for Internet Security (CIS)** — a standards body that publishes security controls.

> 🎯 **Exam tip:** Inspector audits *your* EC2 instance. Artifact provides compliance reports for *AWS itself*.

---

## 40. Denial of Service (DoS) and DDoS

### DoS (Denial of Service)
An attack that disrupts normal traffic by **flooding a target with fake traffic**, overwhelming it and making it unavailable to legitimate users.

### DDoS (Distributed DoS)
Same as DoS, but the attack traffic originates from **many compromised machines (a botnet)**, making it far harder to block by IP.

**AWS Protection:** AWS's global network provides built-in DDoS protection via **AWS Shield**, available to all customers at no cost (standard tier).

---

## 41. AWS Shield

A managed **DDoS protection service** for applications running on AWS.

### How It Works
Traffic routed through Route 53, CloudFront, Elastic IP, or Global Accelerator automatically passes through Shield protection before reaching your resources.

**OSI Layers Protected:**
- Layer 3 (Network)
- Layer 4 (Transport)
- Layer 7 (Application) — only with WAF attached

### Shield Standard
- **Free** — automatically enabled for all AWS customers
- Protects against the most common DDoS attacks
- Access to tools and best practices for DDoS-resilient architecture

### Shield Advanced
- **$3,000 USD/month** per organization (1-year subscription commitment) + additional usage-based costs

> ✅ **Correction from transcript:** The course states "$3,000/year" — this is incorrect. Per the [official AWS Shield pricing page](https://aws.amazon.com/shield/pricing/), the fee is **$3,000/month**, billed once per payer account regardless of how many linked accounts are subscribed. The 1-year commitment is required, but the charge is monthly.
- Available for: Route 53, CloudFront, ELB, Global Accelerator, Elastic IP
- Additional features:
  - Visibility and reporting on Layer 3, 4, and 7 attacks
  - Access to **DDoS Response Team (DRT)** — requires Business or Enterprise support plan
  - **DDoS cost protection** — prevents bill spikes caused by DDoS traffic
  - SLA guarantee
  - Integrates with WAF for Layer 7 protection

> ⚠️ **Layer 7 protection only works if you also have WAF configured.** Shield Advanced alone does not provide application-layer protection.

---

## 42. Amazon GuardDuty

An **IDS/IPS (Intrusion Detection/Prevention System)** that uses machine learning to continuously monitor for malicious and suspicious activity.

### What It Monitors
- **CloudTrail logs** — API calls and account activity
- **VPC Flow Logs** — network traffic
- **DNS logs** — domain resolution requests

### How It Works
- Must be **enabled** in the console (not on by default)
- Uses ML to identify anomalous patterns (unusual API calls, unexpected geographic access, root account usage, etc.)
- Generates **findings** with severity ratings and details
- Can **automate incident response** via EventBridge (formerly CloudWatch Events) → Lambda or third-party services

### Example Findings
- Root credential usage (API calls made using root credentials)
- Anomalous access patterns (user accessing from unexpected location)
- Unusual IAM activity

### Additional Features
- Add **Trusted IPs** (whitelist known-good addresses) or **Threat Lists** (block known-bad addresses)
- Can be **centralized across accounts** — aggregate findings from all organization accounts into one place
- Cost: Based on data volume analyzed (very cost-effective to enable)

---

## 43. Amazon Macie

A fully managed service that **monitors S3 data access for anomalies** and generates detailed alerts for data risks.

### What It Does
- Uses ML to analyze **CloudTrail logs** for unusual S3 access patterns
- Identifies **sensitive data** (PII, credentials) stored in S3 buckets
- Generates **alerts** across categories including:
  - Anomalous access, open permissions, privilege escalation
  - Data compliance issues, credential loss
  - Ransomware indicators, suspicious access

### Key Use
Protecting against unauthorized access to S3 data and detecting accidental data leaks — particularly useful for compliance-sensitive data stores.

---

## 44. AWS VPN

Establishes a **secure, encrypted tunnel** from your network or device to the AWS global network.

### Two Options

| Service | Use Case |
|---|---|
| **Site-to-Site VPN** | Connect an on-premises network or branch office to a VPC |
| **Client VPN** | Connect individual users (remote workers) to AWS or on-premises resources |

### IPSec
**Internet Protocol Security (IPSec)** — the network protocol suite used by AWS VPN to authenticate and encrypt data packets. Provides encrypted communication between two endpoints over the internet.

> ✅ **Key distinction from Direct Connect:** Direct Connect is a **private** connection but is NOT encrypted. If you need both private AND secure, apply a VPN connection on top of Direct Connect.

---

## 45. AWS WAF (Web Application Firewall)

Protects web applications from common web exploits by **filtering HTTP/HTTPS requests** based on rules you define.

### How It Works
- You write rules (or use managed rule sets) to **allow or deny traffic** based on HTTP request contents
- Rules can inspect: IP addresses, geographic origin, HTTP headers, body content, URI strings
- Can purchase pre-built rule sets from security vendors via the **WAF Rule Marketplace**

### Attachment Points
WAF can be attached to:
- **CloudFront** (global, edge-level protection)
- **Application Load Balancer (ALB)**

### OWASP Top 10
WAF is designed to protect against the **OWASP (Open Web Application Security Project) Top 10** — the most common and dangerous web vulnerabilities:

1. Injection (SQL, OS, LDAP)
2. Broken Authentication
3. Sensitive Data Exposure
4. XML External Entities (XXE)
5. Broken Access Control
6. Security Misconfiguration
7. Cross-Site Scripting (XSS)
8. Insecure Deserialization
9. Using Components with Known Vulnerabilities
10. Insufficient Logging and Monitoring

### WAF Features
- **Managed Rule Groups** (free from AWS, or paid from security vendors)
- **Bot Control** — detect and manage bot traffic
- IP whitelist/blacklist capabilities
- Capacity system limits total rules per WebACL

> ⚠️ **Exam reminder:** WAF only attaches to CloudFront or ALB — not NLB or other services.

---

## 46. Hardware Security Modules (HSM)

A **physical hardware device** designed to store encryption keys securely.

### Key Properties
- Holds keys **in memory only** — never written to disk
- If the device is powered off, the key is gone (a security guarantee)
- Extremely expensive to purchase outright
- Follows **FIPS (Federal Information Processing Standard)** compliance requirements

### FIPS Levels

| Level | Description | HSM Type |
|---|---|---|
| **FIPS 140-2 Level 2** | Tamper-evident (can detect tampering) | Multi-tenant HSM |
| **FIPS 140-2 Level 3** | Tamper-proof (physically prevents tampering) | Single-tenant HSM |

> ✅ **FIPS 140-3** also exists as a newer standard, but not all AWS services have achieved it yet.

### AWS HSM Services

| Service | HSM Type | FIPS Level | Use Case |
|---|---|---|---|
| **AWS KMS** | Multi-tenant | FIPS 140-2 Level 2 | General encryption, most workloads |
| **AWS CloudHSM** | Single-tenant (dedicated hardware) | FIPS 140-2 Level 3 | Enterprise regulatory compliance requirements |

---

## 47. AWS Key Management Service (KMS)

A **managed, multi-tenant HSM service** that makes it easy to create and control encryption keys used to encrypt your data.

### Key Facts
- Deeply integrated with most AWS services — enable encryption via a simple checkbox
- Key types: **Symmetric (AES)** and **Asymmetric (RSA)**
- **AWS Managed Keys:** Created and managed by AWS for you, free to use, available per service
- **Customer Managed Keys:** You create and control them — $1/key/month

### Envelope Encryption
KMS uses envelope encryption as an additional layer of protection:
1. Your **data** is encrypted with a **data key**
2. The **data key** itself is encrypted with a **master key** (stored in KMS)
3. Only the encrypted data key is stored alongside your data
4. To decrypt, KMS decrypts the data key first, then you decrypt your data

> 🎯 **Exam tip:** KMS is the most common encryption answer for most AWS services. CloudHSM is only for enterprises needing FIPS 140-2 Level 3 compliance.

---

## 48. AWS CloudHSM

A **single-tenant, dedicated HSM** as a service.

- Automates hardware provisioning, software patching, high availability, and backups
- Generates and uses encryption keys on **FIPS 140-2 Level 3 validated hardware**
- Built on open HSM industry standards: PKCS#1, Java Cryptography Extension (JCE), Microsoft CryptoAPI
- Can transfer keys to other commercial HSM solutions (portable)
- Can configure **KMS to use CloudHSM as a custom key store** instead of the default KMS key store
- **Significantly more expensive** than KMS — fixed monthly cost for dedicated hardware

> ✅ **Only use CloudHSM** when you are an enterprise with a hard regulatory requirement for FIPS 140-2 Level 3 compliance.

---

## 49. Common AWS Initialism Reference

| Initialism | Full Name |
|---|---|
| IAM | Identity and Access Management |
| S3 | Simple Storage Service |
| SWF | Simple Workflow Service |
| SNS | Simple Notification Service |
| SQS | Simple Queue Service |
| SES | Simple Email Service |
| SSM | Systems Manager |
| RDS | Relational Database Service |
| VPC | Virtual Private Cloud |
| VPN | Virtual Private Network |
| CFN | CloudFormation |
| WAF | Web Application Firewall |
| ASG | Auto Scaling Group |
| TAM | Technical Account Manager |
| ELB | Elastic Load Balancer |
| ALB | Application Load Balancer |
| NLB | Network Load Balancer |
| GWLB | Gateway Load Balancer |
| CLB | Classic Load Balancer |
| EC2 | Elastic Compute Cloud |
| ECS | Elastic Container Service |
| ECR | Elastic Container Registry |
| EBS | Elastic Block Store |
| EFS | Elastic File System |
| EB | Elastic Beanstalk |
| EKS | Elastic Kubernetes Service |
| MSK | Managed Streaming for Kafka |
| RAM | AWS Resource Access Manager |
| ACM | AWS Certificate Manager |
| PoLP | Principle of Least Privilege |
| IoT | Internet of Things |
| RI | Reserved Instances |

---

## 50. Service & Concept Comparison Quick Reference

### SNS vs. SQS vs. SES vs. Pinpoint vs. WorkMail

All involve messaging, but serve completely different purposes:

| Service | Type | Use For | HTML Email? | Similar To |
|---|---|---|---|---|
| **SNS** | Pub/Sub notifications | Internal alerts, billing alarms, event triggers | ❌ Plain text only | Pusher, PubNub |
| **SQS** | Message queue | Background jobs, delayed tasks, decoupling | ❌ | RabbitMQ, Sidekiq |
| **SES** | Transactional email | Sign-up emails, password resets, invoices | ✅ | SendGrid |
| **Pinpoint** | Marketing campaigns | Promotional emails, A/B testing, customer journeys | ✅ | Mailchimp |
| **WorkMail** | Email web client | Employee email and calendar (like Gmail) | ✅ | Gmail, Outlook |

### Amazon Inspector vs. AWS Trusted Advisor

| | Amazon Inspector | AWS Trusted Advisor |
|---|---|---|
| **Scope** | Single EC2 instance (or multiple) | Entire AWS account, multiple services |
| **Output** | Detailed PDF security report | Dashboard with recommendations |
| **Focus** | Is this EC2 instance hardened/secure? | Holistic best practices (cost, security, performance, etc.) |
| **Categories** | Security only | Cost, Performance, Security, Fault Tolerance, Service Limits |

### AWS Artifact vs. Amazon Inspector

| | AWS Artifact | Amazon Inspector |
|---|---|---|
| **Question answered** | "Why should an enterprise trust AWS?" | "Is this EC2 instance secure?" |
| **Report type** | Global compliance framework reports (SOC, PCI) | EC2 security benchmark scan results |

### Direct Connect vs. Amazon Connect vs. Media Connect

| | Direct Connect | Amazon Connect | Media Connect |
|---|---|---|---|
| **Type** | Network connection | Call center service | Video transcoding |
| **Use case** | Private fiber link from data center to AWS | Toll-free numbers, IVR, call routing | Transcode videos at scale |

> 🎯 **Exam trap:** These three services share "Connect" in the name but have nothing to do with each other. Direct Connect = networking. Amazon Connect = phone/call center. Media Connect = video.

### Elastic Transcoder vs. AWS Elemental MediaConvert

Both transcode videos, but one is old and one is new:

| | Elastic Transcoder | AWS Elemental MediaConvert |
|---|---|---|
| **Status** | Legacy — original transcoding service | Current — the recommended replacement |
| **Use case** | Transcode videos to streaming formats | Transcode videos to streaming formats + more |
| **Extra features** | Basic transcoding only | Overlay images, insert video clips, extract captions, watermarks, robust UI |
| **Cost** | Essentially the same | Essentially the same |
| **Should you use it?** | Only if migrating from it is too costly | ✅ Yes — use this for new projects |

> 💡 **Why Elastic Transcoder still exists:** Legacy customers with existing workflows or APIs that depend on it haven't migrated yet. If you see it on the exam as an option, know that MediaConvert is the modern equivalent.

### ELB Load Balancer Types

| Type | Layer | Best For |
|---|---|---|
| **ALB** (Application) | Layer 7 | HTTP/HTTPS, rule-based routing, WAF support |
| **NLB** (Network) | Layer 3/4 | Extreme performance, TCP/UDP, gaming, millions of req/sec |
| **GWLB** (Gateway) | — | Third-party virtual network appliances |
| **CLB** (Classic) | 3/4/7 | Legacy EC2-Classic (being retired; don't use) |

### AWS Config vs. AWS AppConfig

| | AWS Config | AWS AppConfig |
|---|---|---|
| **Purpose** | Governance / compliance as code | Application configuration variable deployment |
| **What it checks** | Whether resources are configured as expected | Whether app config changes will break your app |
| **Example** | Flag S3 buckets that aren't encrypted | Deploy a feature flag change to your web app |

---

*Last updated: February 2026*
