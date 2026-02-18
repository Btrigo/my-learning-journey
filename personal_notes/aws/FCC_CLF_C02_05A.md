# AWS Study Notes — Hour 1
### Source: freeCodeCamp AWS Cloud Practitioner Course (ExamPro)
### Cross-referenced against official AWS documentation, February 2026

---

## 1. AWS Config

### What It Is
AWS Config is a service that enables you to **assess, audit, and evaluate the configurations of your AWS resources**. It continuously monitors and records resource configuration changes, helping you detect misconfigurations, track compliance, and understand how resources relate to and affect one another.

> ✅ **Verified against AWS docs:** The course describes this accurately. AWS Config is region-specific — you must enable it separately per region.

### Key Capabilities
- **Resource Inventory:** Discover and view resources in your account and region (takes a few minutes to populate after setup)
- **Configuration History:** Track how resource configurations change over time via a "Resource Timeline" (found under Resource Inventory in the console)
- **Compliance Evaluation:** Define rules to flag resources as compliant or non-compliant
- **Remediation:** Configure automatic or manual remediation actions when a rule is breached (backed by AWS Systems Manager Automation documents)
- **Custom Rules:** Write your own Lambda functions and provide the Lambda ARN as a custom Config rule — enabling any compliance check you can code

### Setup Requirements
- An **S3 bucket** to store configuration history/snapshots
- An **IAM service-linked role** (created automatically or manually)
- Choose to record all resources in the region, or specific resource types

### Config Rules
- **Managed rules:** Pre-built rules by AWS (e.g., `s3-bucket-public-access-prohibited`, IAM best practices)
- **Custom rules:** Your own Lambda function defines the evaluation logic
- **Trigger types:** Configuration change (evaluates when a resource changes) or Periodic (evaluates on a schedule)
- Rules return either **COMPLIANT** or **NON_COMPLIANT** per resource

### Conformance Packs
A **conformance pack** is a collection of AWS Config rules and remediation actions bundled into a single deployable entity (a YAML CloudFormation template).

- Deployed as a CloudFormation stack under the hood — you can tear one down by deleting the stack
- AWS provides a large library of **sample templates** covering frameworks like NIST, CIS, PCI, HIPAA, and IAM best practices
- Templates are open-source and hosted on GitHub
- You can deploy conformance packs at the **organization level** to enforce compliance across all accounts
- Conformance packs generate a **compliance score** (percentage of compliant resources)

> ⚠️ **Cost note (verified):** AWS Config charges per configuration item recorded and per Config rule evaluation. Conformance packs with many rules can accumulate charges — always clean up packs you no longer need.

> ✅ **Note on console UI:** The course instructor notes the console layout keeps changing. As of 2025–2026, Resource Timeline is found under **Resource Inventory** in the Config console.

---

## 2. AWS Quick Starts

> ⚠️ **Accuracy note:** AWS has rebranded "Quick Starts" as **AWS Solutions Library** (previously also called AWS Quick Start Reference Deployments). The underlying concept remains the same, but search for "AWS Solutions" if you can't find "Quick Starts" in the console.

### What They Are
Pre-built CloudFormation templates authored by AWS or AWS Partner Network (APN) partners to deploy common architectures with minimal manual effort.

- Reduce hundreds of manual steps to just a few
- Most can spin up a fully functional architecture in under an hour
- Composed of: a **reference architecture diagram**, **CloudFormation templates**, and a **deployment guide**

### Components
1. Reference architecture for the deployment
2. CloudFormation template(s) that automate provisioning
3. Deployment guide explaining architecture and implementation

> ✅ Quick Starts are essentially CloudFormation templates — understanding CloudFormation is key to understanding Quick Starts.

---

## 3. Tagging

### What Tags Are
A **tag** is a **key-value pair** you assign to an AWS resource as metadata.

- **Key:** e.g., `Department`, `Environment`, `Project`, `Team`, `CostCenter`
- **Value:** e.g., `Engineering`, `Production`, `ProjectX`

### Use Cases
| Category | Example |
|---|---|
| Resource Management | Identify dev vs. prod environments |
| Cost Management | Cost tracking, budgets, billing allocation |
| Operations | Flag mission-critical services |
| Security | Classify data sensitivity |
| Automation | Target resources in automation scripts |
| IAM Policy Conditions | Grant/deny access based on tags (ABAC) |

### Important Detail: The `Name` Tag
In services like EC2, the **Name field you see in the console IS a tag** with the key `Name`. There is no separate "name" field — it's stored as a tag under the hood.

> ✅ **Verified:** This is accurate AWS behavior across EC2 and many other services.

### Tag Best Practices (from AWS docs)
- Tag keys are **case-sensitive** — `CostCenter` and `costcenter` are different keys
- Don't store PII or sensitive information in tags
- Use consistent naming conventions: lowercase, hyphens to separate words, prefixes for organization (e.g., `mycompany:cost-center`)
- AWS generates its own system tags (e.g., `aws:cloudformation:stack-name`) — these are read-only

---

## 4. Resource Groups & Tag Editor

### Resource Groups
A **Resource Group** is a collection of AWS resources that share one or more tags (or belong to the same CloudFormation stack).

- **Tag-based groups:** Resources matching specified tag key/value pairs are automatically included
- **CloudFormation stack-based groups:** All resources in a given stack become group members
- Groups are **region-specific** — you must be in the correct region to see the right resources
- Global resources (e.g., IAM) require you to be in `us-east-1`

**Where to find it:** Navigate to **Resource Groups & Tag Editor** under Management & Governance in the AWS console.

**Key use case:** Reference a Resource Group in IAM policies to grant/deny access to all resources in a project at once — much more scalable than listing individual resource ARNs.

> ✅ **Verified:** Resource Groups are a standalone service under Management & Governance — the instructor notes the console location changed over time, which is accurate.

### Tag Editor
A centralized tool to **find, add, edit, and remove tags across multiple AWS services and regions simultaneously**.

- Search for resources by type and/or tag across regions
- Bulk-edit tags on multiple resources at once
- Accessible from: **Management & Governance → Resource Groups & Tag Editor → Tag Editor**

### Tag Policies (Organizations)
Available when using AWS Organizations — lets you **standardize tag keys and values** across all accounts in your organization, enforcing consistent tagging at scale.

---

## 5. Business-Centric Services

> 📝 **Exam tip (from instructor):** These services are not officially in the CLF-C02 exam guide, but may appear as **distractor answer choices**. Knowing what they are helps you eliminate wrong answers.

| Service | What It Does | Similar To |
|---|---|---|
| **Amazon Connect** | Virtual cloud contact center / call center | — |
| **Amazon WorkSpaces** | Managed virtual desktops (Windows or Linux) | Azure Virtual Desktop |
| **Amazon WorkDocs** | Shared document collaboration and storage | Microsoft SharePoint |
| **Amazon Chime** | Video conferencing and online meetings | Zoom / Skype |
| **Amazon WorkMail** | Managed business email and calendar (supports IMAP) | Gmail / Exchange |
| **Amazon Pinpoint** | Marketing campaign management; targeted email, SMS, push, voice | — |
| **Amazon SES** (Simple Email Service) | Transactional email sending from applications; track open rates | SendGrid |
| **Amazon QuickSight** | Business intelligence dashboards and data visualization | Tableau / Power BI |

> 🎯 **High priority for exam:** QuickSight, SES, and Pinpoint are most likely to appear in exam questions. The rest may appear as distractors.

---

## 6. Provisioning Services

**Provisioning** = the allocation or creation of resources and services. Most AWS provisioning services use CloudFormation under the hood.

| Service | What It Does | Notes |
|---|---|---|
| **Elastic Beanstalk** | PaaS — deploy web apps without managing infrastructure | Provisions EC2, S3, SNS, CloudWatch, ASGs, Load Balancers automatically |
| **OpsWorks** | Configuration management using Chef or Puppet | Provisions servers via managed CM tooling |
| **CloudFormation** | IaC — provision any AWS service via JSON/YAML templates | The foundation most other provisioning services build on |
| **Quick Starts** | Pre-built CloudFormation templates from AWS/partners | Now called AWS Solutions Library |
| **AWS Marketplace** | Digital catalog to buy/deploy third-party software | Thousands of vendor listings |
| **AWS Amplify** | Mobile/web app framework provisioning serverless backends | Targets DynamoDB, API Gateway, AppSync, etc. |
| **AWS App Runner** | Fully managed container deployment (PaaS for containers) | No prior infrastructure experience required |
| **AWS Copilot** | CLI tool to quickly launch and manage containerized apps | Sets up CI/CD pipelines |
| **AWS CodeStar** | Unified UI for managing software development activities | Launches common stacks (LAMP, etc.) |
| **AWS CDK** (Cloud Development Kit) | IaC using your preferred programming language | Generates CloudFormation templates as output |

---

## 7. Elastic Beanstalk

### What It Is
**Platform as a Service (PaaS)** — deploy web applications without needing to manage the underlying infrastructure. You provide the code; AWS handles the rest.

> **Analogy:** The AWS equivalent of Heroku.

### How It Works
1. Choose a **platform** (runtime): Ruby, Python, Node.js, Java, .NET, PHP, Go, Docker, and more
2. **Upload your code** (or use the sample application)
3. Beanstalk provisions the infrastructure automatically

### What It Provisions (under the hood via CloudFormation)
- EC2 instances
- Elastic Load Balancer
- Auto Scaling Groups (ASG)
- RDS (optionally)
- CloudWatch monitoring
- SNS notifications
- Pre-configured platforms and deployment strategies

### Environment Tiers
- **Web Server Environment:** For standard web applications
- **Worker Environment:** For long-running background jobs (recommended to run both together)

### Deployment Strategies (configurable)
- **All at once** — fastest, causes downtime
- **Rolling** — deploys in batches
- **Rolling with additional batch** — maintains capacity during rolling deploy
- **Immutable** — spins up entirely new instances, safest
- **Blue/Green (Traffic Splitting)** — gradual traffic shift to new version

### Key Features
- Single instance (cost-effective) or High Availability (load balancer + ASG) presets
- Built-in log streaming and log rotation
- X-Ray integration for tracing
- Can rotate database passwords automatically
- Supports Docker environments

> ✅ **AWS's own note:** Beanstalk is not recommended for very large enterprises, but is perfectly viable for small-to-medium workloads.

> 💡 **Clean-up tip:** Elastic Beanstalk creates S3 buckets for deployment artifacts. These are not auto-deleted when you terminate an environment — manually empty and delete them to avoid lingering costs.

---

*Last updated: February 2026*