# Static Portfolio Site — Terraform IaC on AWS

## Overview

This project provisions the complete AWS infrastructure for a static portfolio website using Terraform (Infrastructure as Code). The same architecture that was previously built manually through the AWS console is now fully defined as code — reproducible, version-controlled, and deployable with a single command.

**Live site:** [https://brandontrigo.com](https://brandontrigo.com)

---

## Architecture

```
Visitor
   │
   ▼
CloudFront Distribution (CDN + HTTPS)
   │   ├── CloudFront Default Certificate (*.cloudfront.net)
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
|---------|---------|
| Amazon S3 | Private static file storage (origin) |
| S3 Public Access Block | Locks down all public access to the bucket |
| Origin Access Control (OAC) | Signs CloudFront requests to S3 with SigV4 |
| S3 Bucket Policy | Grants CloudFront-only read access via OAC |
| Amazon CloudFront | CDN, HTTPS termination, global distribution |

---

## Project Structure

```
static-portfolio-terraform/
├── main.tf                  # All AWS resources
├── variables.tf             # Input variables (region, bucket name)
├── outputs.tf               # Output values (CloudFront URL, bucket name)
├── .terraform.lock.hcl      # Provider version lock file
└── .gitignore               # Excludes .terraform/, state files
```

---

## Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) v1.15+
- [AWS CLI](https://aws.amazon.com/cli/) v2+
- AWS credentials configured via `aws configure`
- IAM user with sufficient permissions (S3, CloudFront)

---

## Usage

**1. Initialize Terraform (downloads AWS provider)**
```bash
terraform init
```

**2. Preview what will be built**
```bash
terraform plan
```

**3. Build the infrastructure**
```bash
terraform apply
```

**4. Deploy website files to S3**
```bash
aws s3 sync ./your-site-files s3://your-bucket-name
```

**5. Tear everything down**
```bash
# Empty the bucket first
aws s3 rm s3://your-bucket-name --recursive

# Destroy all infrastructure
terraform destroy
```

---

## Key Concepts

**Why IaC over the console?**
The entire stack — S3 bucket, access controls, OAC, CloudFront distribution, and bucket policy — is provisioned in under 3 minutes with a single command. No clicking, no manual configuration, no room for human error. Teardown is equally fast and complete.

**Why Block Public Access stays ON?**
The S3 bucket is completely private. CloudFront accesses it exclusively through OAC, which signs every request using AWS Signature Version 4 (SigV4). Direct S3 access returns `AccessDenied` by design.

**Why `force_destroy` matters?**
By default Terraform will not delete a non-empty S3 bucket. In a lab environment, adding `force_destroy = true` to the bucket resource allows `terraform destroy` to empty and delete the bucket in one step. In production this should be left off.

**Terraform state**
Terraform tracks all provisioned resources in a local `terraform.tfstate` file. This file is excluded from version control via `.gitignore` because it can contain sensitive values. In a team or production environment, state should be stored remotely in an S3 backend with DynamoDB locking.

---

## What's Next

- Add `force_destroy = true` to bucket resource for cleaner lab teardowns
- Add GitHub Actions pipeline to automate `aws s3 sync` on push (CI/CD)
- Migrate state to remote S3 backend
- Expand to full enterprise network environment (VPC, subnets, IGW, NAT, security groups)

---

## Tools & Versions

| Tool | Version |
|------|---------|
| Terraform | v1.15.3 |
| AWS Provider | hashicorp/aws v5.100.0 |
| AWS CLI | v2.34.50 |