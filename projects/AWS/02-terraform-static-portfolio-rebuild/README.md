# 02 — Static Portfolio Site: Terraform IaC Rebuild

## Overview

This project provisions the complete AWS infrastructure for a static portfolio website using Terraform. It is a structured rebuild of Project 01, redesigned with professional file separation, inline documentation, and production-aligned best practices.

The entire stack — S3, CloudFront, OAC, bucket policy, and CloudFront Function — is defined as code across five dedicated files and deployable with a single command.

**Live site:** [https://brandontrigo.com](https://brandontrigo.com)

---

## Architecture

```
Visitor
   │
   ▼
CloudFront Distribution (CDN + HTTPS)
   │   ├── CloudFront Default Certificate (*.cloudfront.net)
   │   ├── CloudFront Function (URI rewriting — viewer-request)
   │   └── OAC (signs every request to S3 with SigV4)
   │
   ▼
S3 Bucket (private — Block Public Access ON)
   ├── index.html
   ├── css/style.css
   ├── js/script.js
   └── images/turtle-meditation.png
```

---

## AWS Services Provisioned

| Service | Purpose |
|---|---|
| Amazon S3 | Private static file storage (origin) |
| S3 Public Access Block | Locks down all public access to the bucket |
| Origin Access Control (OAC) | Signs CloudFront requests to S3 with SigV4 |
| S3 Bucket Policy | Grants CloudFront-only read access via OAC condition |
| Amazon CloudFront | CDN, HTTPS termination, global edge distribution |
| CloudFront Function | Rewrites directory-style URIs to index.html at the edge |

---

## Project Structure

```
02-terraform-static-portfolio-rebuild/
├── providers.tf          # AWS provider declaration and version constraints
├── variables.tf          # Input variables — region and bucket name
├── main.tf               # S3 bucket, public access block, bucket policy
├── cloudfront.tf         # OAC, CloudFront distribution, CloudFront Function
├── outputs.tf            # Output values printed after apply
├── .terraform.lock.hcl   # Provider version lock — ensures reproducible builds
└── .gitignore            # Excludes .terraform/ directory and state files
```

---

## Improvements Over Project 01

| Area | Project 01 | Project 02 |
|---|---|---|
| File structure | All resources in a single `main.tf` | Separated by concern across 5 dedicated files |
| Inline documentation | Minimal | Comments on every meaningful line |
| Bucket teardown | Required manual `aws s3 rm` before destroy | `force_destroy = true` handles it automatically |
| CloudFront Function | Included | Included and documented line by line |

---

## Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) v1.5+
- [AWS CLI](https://aws.amazon.com/cli/) v2+
- AWS credentials configured via `aws configure`
- IAM user with S3 and CloudFront permissions

---

## Usage

**1. Initialize — downloads the AWS provider plugin**
```bash
terraform init
```

**2. Format — enforces HCL style standards**
```bash
terraform fmt
```

**3. Validate — checks for syntax errors and invalid references**
```bash
terraform validate
```

**4. Plan — previews every resource that will be created**
```bash
terraform plan
```

**5. Apply — provisions all infrastructure**
```bash
terraform apply
```

**6. Deploy site files to S3**
```bash
aws s3 sync ./your-site-files s3://your-bucket-name
```

**7. Tear everything down**
```bash
terraform destroy
```

---

## Key Concepts

**Why file separation?**
Splitting resources across dedicated files (`main.tf` for S3, `cloudfront.tf` for CloudFront) is standard practice on engineering teams. It improves readability, makes debugging faster, and scales cleanly as infrastructure grows. Terraform reads all `.tf` files in the directory together — the separation is for engineers, not for Terraform.

**Why Block Public Access stays ON?**
The S3 bucket is completely private. CloudFront accesses it exclusively through OAC, which signs every request using AWS Signature Version 4 (SigV4). The bucket policy enforces this with a `StringEquals` condition on `AWS:SourceArn` — only this specific CloudFront distribution can read from the bucket. Direct S3 access returns `AccessDenied` by design.

**Why a CloudFront Function?**
S3 is object storage, not a web server. It can only retrieve files by their exact key. A request to `/about` fails because no object named `about` exists — the file is `about/index.html`. The CloudFront Function intercepts every viewer request at the edge and rewrites directory-style URIs before they reach S3. Asset requests (anything containing a `.`) are passed through untouched.

**Why `force_destroy = true`?**
Terraform will not delete a non-empty S3 bucket by default. Adding `force_destroy = true` allows `terraform destroy` to empty and delete the bucket in a single operation. In a lab environment this is intentional. In production this should be omitted or gated behind a confirmation step.

**Why `.terraform.lock.hcl` is committed**
The lock file records the exact provider version used. Committing it ensures that anyone running `terraform init` on this project gets the same provider version, preventing unexpected behavior from version drift.

---

## Terraform Workflow

```
terraform init → terraform fmt → terraform validate → terraform plan → terraform apply
```

Never skip `plan` before `apply`. In production, plans are reviewed and approved before apply runs — often enforced via CI/CD pipelines.

---

## What's Next

- Project 03: CI/CD pipeline — GitHub Actions triggers `aws s3 sync` automatically on every push to main
- Project 04: VPC from scratch — subnets, IGW, NAT Gateway, route tables, security groups
- Remote state backend — migrate `terraform.tfstate` to S3 with DynamoDB locking for team use

---

## Tools & Versions

| Tool | Version |
|---|---|
| Terraform | v1.15.3 |
| AWS Provider | hashicorp/aws v5.100.0 |
| AWS CLI | v2.34.50 |