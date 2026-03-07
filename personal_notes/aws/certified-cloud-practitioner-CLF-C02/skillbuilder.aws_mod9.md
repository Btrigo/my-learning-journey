# AWS Module 9 — Security

This module covers the fundamental AWS security model, the services used to protect infrastructure and applications, and the tools used to detect and respond to security threats.

Understanding these services is important because security responsibilities in AWS are shared between AWS and the customer.

---

## 1. AWS Shared Responsibility Model

AWS security follows a **shared responsibility model**.

Security responsibilities are divided between **AWS** and the **customer**.

### AWS Responsibility — Security *of* the Cloud

AWS is responsible for protecting the infrastructure that runs all AWS services.

This includes:

- Physical data centers
- Hardware infrastructure
- Global networking
- Storage infrastructure
- Virtualization layer (hypervisor)

Customers do **not** manage these components.

---

### Customer Responsibility — Security *in* the Cloud

Customers are responsible for configuring and securing the resources they deploy.

This typically includes:

- Operating systems
- Application software
- Network configurations
- IAM permissions
- Encryption settings
- Security groups and firewalls

The level of responsibility varies depending on the service.

| Service | AWS Responsibility | Customer Responsibility |
|---------|-------------------|------------------------|
| EC2 | Hardware, hypervisor | OS, patches, apps |
| S3 | Storage infrastructure | Bucket policies, access |
| RDS | Database platform | Data, access control |

---

## 2. Identity and Access Management

### AWS IAM (Identity and Access Management)

IAM controls **who can access AWS resources and what actions they can perform**.

IAM components include:

#### Users
Individual identities representing a person or application.

#### Groups
Collections of users that share the same permissions.

#### Roles
Temporary permissions that can be assumed by users, applications, or services.

#### Policies
JSON documents defining permissions.

Example permissions:

- Allow reading from an S3 bucket
- Allow launching EC2 instances

---

### IAM Security Best Practices

Recommended practices include:

- Use **least privilege access**
- Enable **multi-factor authentication (MFA)**
- Use **roles instead of long-term credentials**
- Rotate credentials regularly

---

## 3. Network and Application Protection

### Security Groups

Security groups act as **virtual firewalls for EC2 instances**.

Characteristics:

- Control inbound and outbound traffic
- Stateful firewall
- Only allow rules (no explicit deny rules)

Security groups operate at the **instance level**.

---

### AWS WAF (Web Application Firewall)

AWS WAF protects web applications from common exploits.

Examples of attacks it blocks:

- SQL injection
- Cross-site scripting (XSS)
- Malicious IP addresses

WAF is commonly deployed with:

- CloudFront
- Application Load Balancers
- API Gateway

---

### AWS Shield

AWS Shield protects applications from **Distributed Denial of Service (DDoS) attacks**.

#### Shield Standard

- Automatically enabled
- Free
- Protects against common network and transport layer attacks

#### Shield Advanced

- Paid service
- Advanced protection and monitoring
- Access to AWS DDoS Response Team

---

## 4. Encryption and Data Protection

### AWS Key Management Service (KMS)

AWS KMS manages encryption keys used to protect data.

KMS is commonly used with:

- Amazon S3
- Amazon EBS
- Amazon RDS
- Amazon DynamoDB

KMS enables **encryption at rest**.

---

### AWS Certificate Manager (ACM)

ACM manages SSL/TLS certificates.

These certificates enable **HTTPS encryption**.

ACM is used with services like:

- Elastic Load Balancing
- CloudFront
- API Gateway

ACM provides **encryption in transit**.

---

## 5. Threat Detection and Security Monitoring

### Amazon GuardDuty

GuardDuty is a **threat detection service**.

It continuously analyzes logs including:

- VPC Flow Logs
- DNS logs
- AWS CloudTrail logs

GuardDuty detects suspicious activity such as:

- Compromised EC2 instances
- Cryptocurrency mining activity
- Communication with malicious IP addresses

---

### Amazon Inspector

Amazon Inspector performs **automated vulnerability scanning**.

It evaluates AWS resources for:

- Software vulnerabilities
- Exposed network services
- Deviations from security best practices

Inspector supports:

- EC2 instances
- Container images
- Lambda functions

---

### Amazon Detective

Amazon Detective helps **investigate security incidents**.

It collects and analyzes log data to build visualizations showing:

- User activity
- Resource interactions
- Attack timelines

This helps identify the **root cause of security events**.

---

### AWS Security Hub

Security Hub provides a **centralized view of security findings**.

It aggregates alerts and findings from services including:

- GuardDuty
- Inspector
- Macie
- Other AWS security tools

Security Hub helps organizations monitor security posture across their AWS environment.

---

## 6. Sensitive Data Detection

### Amazon Macie

Amazon Macie uses machine learning to detect **sensitive data stored in Amazon S3**.

Examples of sensitive data:

- Personally identifiable information (PII)
- Financial records
- Customer data

Macie helps organizations maintain compliance and protect sensitive information.

---

## 7. AWS Security Documentation

AWS provides several resources for learning about security best practices.

Key resources include:

- **Security, Identity, and Compliance on AWS**
- **AWS Security Documentation**
- **AWS Knowledge Center**
- **AWS Security Blog**

These resources provide guidance on securing AWS workloads.

---

## 8. AWS Marketplace Security Tools

The AWS Marketplace provides a catalog of **third-party security software** that runs on AWS.

Examples include tools for:

- Threat detection and prevention
- Identity and access management
- Data protection
- Compliance and governance

Organizations can deploy security products from vendors directly within their AWS environments.

---

## Key Security Services Summary

| Service | Purpose |
|---------|---------|
| IAM | Identity and access control |
| KMS | Encryption key management |
| ACM | TLS certificate management |
| WAF | Web application protection |
| Shield | DDoS protection |
| GuardDuty | Threat detection |
| Inspector | Vulnerability scanning |
| Detective | Security investigation |
| Security Hub | Centralized security dashboard |
| Macie | Sensitive data detection |

---

## Typical AWS Security Architecture

A common architecture includes multiple layers of protection:

```
Internet
↓
AWS Shield
↓
AWS WAF
↓
Elastic Load Balancer
↓
Application (EC2 / Lambda)
↓
Data Layer (RDS / DynamoDB / S3)
```

Monitoring and detection services run alongside the architecture:

- GuardDuty
- Inspector
- CloudTrail
- Security Hub

---

## Module Takeaways

- AWS security follows a **shared responsibility model**.
- IAM controls access to AWS resources.
- Multiple services protect infrastructure from attacks.
- AWS provides tools for **prevention, detection, and investigation of security incidents**.
- Security monitoring services help organizations maintain a secure and compliant environment.