# AWS Module 10 — Monitoring, Compliance, and Governance

This module covers the AWS services used to monitor infrastructure, track activity, enforce compliance, and govern large AWS environments.

These services are critical for:

- Operational visibility
- Security monitoring
- Compliance auditing
- Cost optimization
- Multi-account governance

---

# 1. Monitoring in AWS

Monitoring allows organizations to observe system behavior, detect issues, and automate responses.

AWS provides several services to monitor resources, logs, and infrastructure health.

Primary monitoring tools:

| Service | Purpose |
|------|------|
| CloudWatch | Metrics, logs, alarms, monitoring |
| CloudTrail | API activity logging |
| AWS Health | AWS service health notifications |
| AWS Config | Resource configuration tracking |

---

# 2. Amazon CloudWatch

Amazon CloudWatch is the **primary monitoring service in AWS**.

It collects operational data such as:

- Metrics
- Logs
- Events

from AWS resources and applications.

### Key Capabilities

CloudWatch can:

- Monitor EC2 performance
- Track CPU utilization
- Store logs from applications
- Trigger alarms when thresholds are exceeded
- Automatically trigger actions

### Example Use Case

If CPU utilization exceeds 80%:

CloudWatch can:

1. Trigger an alarm
2. Send notification via SNS
3. Automatically scale EC2 instances

---

### Core Components

| Component | Description |
|------|------|
| Metrics | Performance data (CPU, memory, disk) |
| Logs | Application and system logs |
| Alarms | Trigger actions when thresholds are reached |
| Events | Trigger automated workflows |

---

# 3. AWS CloudTrail

AWS CloudTrail records **API activity in an AWS account**.

It answers:

- **Who performed an action**
- **What action was taken**
- **When the action occurred**
- **Which resource was affected**

This is critical for:

- Security monitoring
- Auditing
- Compliance investigations

### Example

If someone deletes an S3 bucket:

CloudTrail logs:

- the IAM user
- the time of deletion
- the API call used

---

### CloudTrail Tracks

- Console activity
- SDK activity
- CLI commands
- API calls

---

# 4. AWS Config

AWS Config monitors and evaluates **configuration changes of AWS resources**.

It records:

- the configuration of resources
- configuration changes over time
- compliance with rules

---

### Key Capabilities

AWS Config can:

- Track configuration history
- Detect unauthorized changes
- Evaluate compliance rules
- Audit resource configurations

---

### Example

Rule:


All S3 buckets must have encryption enabled


If a bucket is created without encryption:

AWS Config flags it as **noncompliant**.

---

# 5. AWS Trusted Advisor

AWS Trusted Advisor evaluates your AWS environment and provides **recommendations based on best practices**.

Trusted Advisor analyzes resources and suggests improvements across several categories.

---

### Categories of Checks

| Category | Purpose |
|------|------|
| Cost Optimization | Reduce unnecessary spending |
| Performance | Improve system performance |
| Security | Identify security risks |
| Fault Tolerance | Increase resilience |
| Service Limits | Monitor service quotas |

---

### Example Recommendations

Trusted Advisor might recommend:

- deleting unused EBS volumes
- closing unused security group ports
- enabling MFA on root accounts

---

# 6. AWS Health Dashboard

AWS Health provides information about **AWS service outages or issues**.

It shows:

- AWS service disruptions
- scheduled maintenance
- account-specific service events

---

### Types of Health Dashboards

| Dashboard | Description |
|------|------|
| Service Health Dashboard | Global AWS service status |
| Personal Health Dashboard | Issues affecting your resources |

---

# 7. Compliance in AWS

Organizations often must follow regulatory frameworks such as:

- HIPAA
- PCI DSS
- SOC
- ISO

AWS provides services that support compliance and auditing.

---

# 8. AWS Artifact

AWS Artifact provides **on-demand access to AWS security and compliance reports**.

These reports include:

- SOC reports
- ISO certifications
- PCI compliance reports

Artifact also allows customers to review and accept agreements.

---

### Examples of Agreements

- Business Associate Agreement (BAA)
- Non-disclosure agreements
- AWS service terms

---

# 9. AWS License Manager

AWS License Manager helps organizations manage **software licenses** across AWS resources.

This is important when migrating software to the cloud using **Bring Your Own License (BYOL)**.

---

### License Manager Features

- Track license usage
- Prevent license overuse
- Enforce license limits
- Manage licenses across accounts

---

# 10. AWS Organizations

AWS Organizations helps manage **multiple AWS accounts from a central location**.

Organizations allow companies to:

- consolidate billing
- group accounts
- apply governance policies

---

### Organizational Structure

AWS Organizations uses:

| Level | Description |
|------|------|
| Root | Top-level container |
| Organizational Units (OUs) | Groups of accounts |
| Accounts | Individual AWS accounts |

---

# 11. Service Control Policies (SCPs)

Service Control Policies define **permission guardrails** across accounts in AWS Organizations.

They restrict which AWS services and API actions can be used.

Important:

SCPs **do not grant permissions**.

They only **limit permissions**.

---

### Example

An SCP may block:


ec2:TerminateInstances


Even if an IAM user has permission, the SCP can still block it.

---

# 12. AWS Service Catalog

AWS Service Catalog allows organizations to provide **approved AWS resource templates** for employees.

This enables **self-service deployments while maintaining governance**.

---

### Example

Developers can launch:

- approved EC2 environments
- approved VPC templates
- approved application stacks

without building infrastructure from scratch.

---

# 13. AWS Control Tower

AWS Control Tower helps organizations **set up and manage a secure multi-account AWS environment**.

It automates best practices for:

- account setup
- governance
- compliance

---

### Landing Zone

A **landing zone** is a preconfigured environment that includes:

- organizational units
- accounts
- security guardrails
- compliance policies

This ensures new accounts follow security standards automatically.

---

# Key Service Comparison

| Service | Purpose |
|------|------|
| CloudWatch | Monitoring metrics, logs, alarms |
| CloudTrail | Logging API activity |
| AWS Config | Tracking resource configuration changes |
| Trusted Advisor | Optimization recommendations |
| AWS Health | AWS service health notifications |
| AWS Artifact | Compliance reports and agreements |
| License Manager | Software license management |
| AWS Organizations | Multi-account governance |
| SCPs | Permission guardrails across accounts |
| Service Catalog | Approved resource templates |
| Control Tower | Multi-account environment setup |

---

# Key Takeaways

- **CloudWatch** monitors performance and triggers alarms.
- **CloudTrail** records API activity and user actions.
- **AWS Config** tracks configuration changes and compliance.
- **Trusted Advisor** provides recommendations for optimization and security.
- **AWS Artifact** provides access to compliance reports.
- **AWS Organizations** allows centralized management of multiple accounts.
- **Service Control Policies** enforce organization-wide permission guardrails.
- **AWS Service Catalog** enables controlled self-service infrastructure deployment.
- **AWS Control Tower** automates governance of multi-account AWS environments.

---