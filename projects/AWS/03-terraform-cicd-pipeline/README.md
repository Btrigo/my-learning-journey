# Rebuilding the CI/CD Pipeline in Terraform (with Automated CloudFront Invalidation)

**Live site:** [https://brandontrigo.com](https://brandontrigo.com)
**Related write-up:** [Automating Portfolio Deployment with GitHub Actions, OIDC, and S3](./deploy_cicd_github_actions_s3.md) — the original console build this project codifies.

---

## Project Overview

The GitHub Actions + OIDC + S3 deployment pipeline (built and documented separately via the AWS Console) was rebuilt entirely in Terraform, following the same "build it twice" methodology used throughout this portfolio: build it by hand first to understand every piece, then codify it as infrastructure-as-code.

This project also extends the original pipeline with one new capability: **automated CloudFront cache invalidation**. In the console build, invalidating the CDN cache after a deploy was a manual step. Here, that step was folded directly into the CI/CD workflow, so a push to `main` now results in the live site reflecting changes immediately, with no manual intervention required.

---

## Why `terraform import`, Not `terraform apply`

This project is a good illustration of an important Terraform distinction: **`terraform import` reads existing infrastructure into Terraform's state file — it never creates or modifies anything in AWS.** `terraform apply` is what actually executes changes against real infrastructure.

Because the OIDC provider, IAM role, and inline policy already existed (built manually via the console in the prior project), the goal wasn't to recreate them — it was to bring Terraform's state file into sync with what was *already* running in AWS, without ever touching the live, working pipeline.

One resource in particular made this non-negotiable rather than a stylistic choice: the IAM OIDC identity provider for `token.actions.githubusercontent.com` is a **singleton per AWS account** — AWS only allows one registration of a given OIDC provider URL per account. That meant there was no way to spin up a second "practice" copy to test the import process safely; `terraform import` against the real, live resource was the only viable path.

---

## Architecture

```
Developer (local machine)
   │
   │  git push (main, website_portfolio/** changed)
   ▼
GitHub Repository
   │
   │  triggers workflow
   ▼
GitHub Actions Runner (ubuntu-latest)
   │
   ├── 1. Checkout repository (actions/checkout@v4)
   │
   ├── 2. Request OIDC token → AWS STS validates against IAM trust policy
   │      → Temporary AWS credentials issued, scoped to one IAM role
   │
   ├── 3. aws s3 sync ./website_portfolio s3://brandontrigo.com --delete
   │
   └── 4. aws cloudfront create-invalidation
             --distribution-id ${{ vars.CLOUDFRONT_DISTRIBUTION_ID }}
             --paths "/*"
          │
          ▼
       CloudFront purges cached edge copies
          │
          ▼
       Live site reflects the change immediately, no manual step required
```

Everything above the S3 bucket (the OIDC provider, IAM role, and IAM policy) is now defined in Terraform (`main.tf`, `variables.tf`, `terraform.tfvars`, `providers.tf`) rather than existing only as manual console configuration.

---

## The Terraform Rebuild, Step by Step

### 1. Writing the resource blocks to match existing infrastructure

Three resources were written in HCL to mirror exactly what already existed in AWS:

**The OIDC provider:**
```hcl
resource "aws_iam_openid_connect_provider" "github_actions" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["22ff89586561fc2d52f77491e9f1eff1b80be33e"]
}
```

**The IAM role and its trust policy** (scoped to one repo, one branch — the same least-privilege trust condition from the original build):
```hcl
resource "aws_iam_role" "github_actions_deploy" {
  name        = var.iam_role_name
  description = "allows github actions to assume this role via OIDC and sync website portfolio files to S3. scoped to the main branch of the my-learning-journey repository."

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github_actions.arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:${var.github_org}/${var.github_repo}:ref:refs/heads/${var.github_branch}"
          }
        }
      }
    ]
  })
}
```

Notice the `Federated` value references `aws_iam_openid_connect_provider.github_actions.arn` — a resource reference rather than a hardcoded ARN string. This is deliberate: if the OIDC provider were ever recreated, this reference resolves automatically rather than silently pointing at a stale, hardcoded ARN.

**The inline S3 deployment policy:**
```hcl
resource "aws_iam_role_policy" "s3_deploy" {
  name = var.iam_policy_name
  role = aws_iam_role.github_actions_deploy.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:DeleteObject"
        ]
        Resource = [
          "arn:aws:s3:::${var.s3_bucket_name}",
          "arn:aws:s3:::${var.s3_bucket_name}/*"
        ]
      }
    ]
  })
}
```

Variables (`variables.tf`) and their values (`terraform.tfvars`) were split out from the start, keeping account-specific data (org name, repo name, bucket name) out of the reusable resource definitions.

### 2. Importing each resource into state

Each resource was imported individually against its real AWS identifier:

```bash
terraform import aws_iam_openid_connect_provider.github_actions arn:aws:iam::[ACCOUNT_ID]:oidc-provider/token.actions.githubusercontent.com
terraform import aws_iam_role.github_actions_deploy github-actions-portfolio-deploy
terraform import aws_iam_role_policy.s3_deploy github-actions-portfolio-deploy:github-actions-portfolio-s3-deploy
```

`import` only populates Terraform's state file with the resource's current real-world configuration — it does not verify that the HCL written in step 1 actually *matches* that configuration. That verification is a separate, required step.

### 3. Validating with a zero-drift `terraform plan`

After importing, `terraform plan` was run repeatedly until it reported **no changes** — confirming the hand-written HCL was a byte-for-byte accurate match of the real, already-running infrastructure. Only once `plan` showed zero drift was it safe to consider the rebuild trustworthy; a plan showing unexpected changes at this stage would mean the HCL didn't actually describe the live resource correctly, and applying it could have altered or broken the working pipeline.

### 4. Live sanity check

To confirm Terraform managing the resources hadn't broken anything, a trivial HTML comment was added to `website_portfolio/index.html`, committed, and pushed. The GitHub Actions run was watched end-to-end to confirm OIDC authentication and the S3 sync still succeeded exactly as before — proving that switching the underlying resources from console-managed to Terraform-managed was transparent to the pipeline itself. The comment was then removed and the same push/verify cycle repeated to leave the live site clean.

---

## Adding Automated CloudFront Invalidation

With the rebuild validated, the pipeline was extended with a capability the original console build deliberately left manual: invalidating the CloudFront cache automatically after every deploy.

### Granting the permission (Terraform)

A new statement was added to the existing inline policy, rather than creating a separate policy resource — keeping all of the deploy role's permissions in one place:

```hcl
data "aws_caller_identity" "current" {}

resource "aws_iam_role_policy" "s3_deploy" {
  # ...
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:DeleteObject"
        ]
        Resource = [
          "arn:aws:s3:::${var.s3_bucket_name}",
          "arn:aws:s3:::${var.s3_bucket_name}/*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = "cloudfront:CreateInvalidation"
        Resource = "arn:aws:cloudfront::${data.aws_caller_identity.current.account_id}:distribution/${var.cloudfront_distribution_id}"
      }
    ]
  })
}
```

The `aws_caller_identity` data source reads the AWS account ID of whoever Terraform is currently authenticated as, at plan/apply time — avoiding a hardcoded account ID in the resource ARN. The CloudFront ARN itself has no region segment (`arn:aws:cloudfront::ACCOUNT_ID:distribution/ID`), since CloudFront is a global service, not a regional one.

The new statement is scoped to this one specific distribution ARN — not `cloudfront:*` on `*` — keeping the permission as narrow as the task actually requires.

`terraform plan` confirmed exactly one additive change (a new statement appended to the existing policy, nothing else in the resource affected) before `terraform apply` was run. The change was independently re-verified afterward by inspecting the live policy JSON directly in the IAM console.

### Automating the invalidation step (GitHub Actions)

A fourth step was added to `.github/workflows/deploy.yml`, run immediately after the S3 sync step, using the same already-authenticated OIDC session — no additional credentials or auth steps required:

```yaml
- name: invalidate cloudfront cache
  run: |
    aws cloudfront create-invalidation --distribution-id ${{ vars.CLOUDFRONT_DISTRIBUTION_ID }} --paths "/*"
```

The distribution ID is referenced via a **GitHub Actions repository variable** (`vars.CLOUDFRONT_DISTRIBUTION_ID`), rather than hardcoded directly into the workflow file. The distribution ID itself isn't sensitive — it's publicly visible to anyone inspecting the live site — but centralizing it as a variable avoids the value being duplicated across `terraform.tfvars`, ad-hoc CLI commands, and the workflow file, all of which could drift out of sync if the distribution were ever recreated.

### End-to-end verification

The pipeline was tested by pushing a small, throwaway comment into `index.html` and watching all four steps run in the Actions tab. The live site was then inspected directly (via browser DevTools, viewing the actual served source) and confirmed to already reflect the new comment — with no manual invalidation command run at any point. This confirmed the full automated chain: push → OIDC auth → S3 sync → CloudFront invalidation → fresh content served immediately.

---

## Key Concepts Learned

**`terraform import` vs. `terraform apply`:** Import only reads real infrastructure into local state — it makes no changes to AWS. Apply is the only command that actually executes changes. Understanding this distinction was essential before touching a live, working pipeline.

**Some AWS resources are singletons:** The OIDC provider for a given URL can only exist once per AWS account, which meant `terraform import` against the real resource was the only option — there was no safe way to build and tear down a disposable practice copy first.

**Zero-drift validation is the real safety check, not `import` itself:** Running `import` successfully doesn't guarantee the HCL is correct — only a `terraform plan` showing no changes confirms the written configuration truly matches the live resource.

**Data sources read; they don't write:** `data "aws_caller_identity" "current" {}` is a lookup, not a resource — it never creates or modifies anything, it just supplies a value (the account ID) that other resources can reference dynamically instead of hardcoding.

**Granting a permission is separate from using it:** Adding `cloudfront:CreateInvalidation` to the IAM policy did nothing on its own — the workflow still needed an explicit new step actually calling that API. Terraform and the GitHub Actions workflow are two independent systems that each had to be updated for the automation to function.

**Not every non-default value belongs in Terraform variables:** The CloudFront distribution ID needed to be referenced in *two* independent systems — Terraform (for the IAM policy ARN) and the GitHub Actions workflow (for the CLI command). Rather than hardcoding it in both places, it was set once in Terraform's `terraform.tfvars` and once as a GitHub Actions repository variable, keeping each system's copy authoritative for its own context without duplicating the value inside code.

---

## Technologies & Services

| Service / Tool | Purpose |
|---|---|
| Terraform | Infrastructure-as-code for the OIDC provider, IAM role, and IAM policy |
| `terraform import` | Brought existing, console-built AWS resources into Terraform state |
| AWS IAM | OIDC identity provider, scoped role, least-privilege inline policy |
| AWS STS | Token validation and temporary credential issuance |
| GitHub Actions | CI/CD pipeline execution, including the new invalidation step |
| GitHub Actions repository variables | Non-sensitive config value (distribution ID) shared across systems |
| Amazon S3 | Deployment target for static site files |
| Amazon CloudFront | CDN cache, now invalidated automatically post-deploy |
| AWS CLI | Underlying commands run by the workflow (`s3 sync`, `cloudfront create-invalidation`) |

---

## On the Horizon

A few hardening items were identified during this project and deliberately deferred to their own future sessions, rather than bundled into this rebuild:

- Tightening the trust policy's `sub` condition from `StringLike` to `StringEquals`, since the value is an exact match with no wildcard actually needed
- Pinning third-party GitHub Actions (`actions/checkout`, `aws-actions/configure-aws-credentials`) to full commit SHAs rather than version tags, to reduce supply-chain risk
- Migrating Terraform's state from local storage to a remote S3 backend with encryption and locking