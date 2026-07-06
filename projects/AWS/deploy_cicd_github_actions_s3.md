# Automating Portfolio Deployment with GitHub Actions, OIDC, and S3

**Live site:** [https://brandontrigo.com](https://brandontrigo.com)

---

## Project Overview

This project automates deployment of the portfolio site (covered in the previous S3/CloudFront project) using a GitHub Actions CI/CD pipeline. Pushing a change to the `website_portfolio/` folder on `main` now automatically syncs those files to the production S3 bucket — no manual `aws s3 sync` required.

Authentication between GitHub and AWS uses **OIDC (OpenID Connect)** rather than long-lived IAM access keys. This means no AWS credentials are stored as GitHub secrets at all — GitHub requests a short-lived, cryptographically signed token at runtime, and AWS verifies that token against a trust policy before issuing temporary credentials. If the workflow is compromised, there's no static key sitting around for an attacker to steal — the credentials expire and the role can only ever be assumed by this specific repo and branch.

CloudFront cache invalidation was deliberately kept as a **manual step** for this phase, rather than folded into the workflow. This was an intentional learning decision: automating it later (during the Terraform rebuild) is more meaningful once the manual command is fully internalized, rather than skipped from the start.

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
   ├── 2. Request OIDC token from GitHub's OIDC provider
   │      │
   │      ▼
   │   AWS STS — validates token against IAM trust policy
   │      │  (checks: aud == sts.amazonaws.com,
   │      │           sub == repo:Btrigo/my-learning-journey:ref:refs/heads/main)
   │      ▼
   │   Temporary AWS credentials issued (~1 hour, scoped to one IAM role)
   │
   └── 3. aws s3 sync ./website_portfolio s3://brandontrigo.com --delete
          │
          ▼
       S3 Bucket (private, OAC-protected — see prior project)

Manual step (intentional, not yet automated):
   aws cloudfront create-invalidation --distribution-id [ID] --paths "/*"
          │
          ▼
       CloudFront purges cached files, serves fresh content from S3
```

---

## Why OIDC Instead of Access Keys

The traditional approach to CI/CD AWS authentication is storing an IAM user's access key and secret key as GitHub repository secrets. This works, but has a real downside: those credentials are long-lived and static. If they ever leak — through a misconfigured log, a compromised dependency, or a leaked secret — they remain valid until someone manually rotates or revokes them.

OIDC removes this risk entirely. Instead of a stored secret, GitHub's OIDC provider issues a signed JSON Web Token (JWT) at the moment the workflow runs. That token is sent to AWS STS, which verifies:

1. The token is genuinely signed by GitHub (verified using GitHub's published OIDC keys)
2. The token's claims satisfy the IAM role's trust policy conditions

Only if both checks pass does AWS issue temporary credentials — and those credentials expire automatically, by default within an hour. There is no static secret to steal, rotate, or accidentally commit.

---

## AWS Services & Concepts Used

### IAM OIDC Identity Provider
A one-time registration in AWS IAM that tells AWS to trust tokens issued by GitHub's OIDC endpoint (`https://token.actions.githubusercontent.com`). This is the foundational trust relationship — without it, AWS has no way to verify a GitHub-issued token is legitimate.

### IAM Role with a Scoped Trust Policy
A dedicated role (`github-actions-portfolio-deploy`) that only GitHub Actions can assume, and only under specific conditions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::[ACCOUNT_ID]:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:Btrigo/my-learning-journey:ref:refs/heads/main"
        }
      }
    }
  ]
}
```

**Two conditions gate access:**
- **`aud` (audience):** confirms the token was intended for AWS STS specifically — uses `StringEquals` since it's always one exact value.
- **`sub` (subject):** confirms the token came from this exact repository and branch — uses `StringLike` for flexibility, scoped to `repo:Btrigo/my-learning-journey:ref:refs/heads/main`.

Without the `sub` condition (or with it set too loosely, e.g. a bare wildcard), *any* repository under the account — or any branch/PR within this repo — could assume the role. Scoping it to one repo and one branch is the least-privilege principle applied to identity, not just permissions.

### Least-Privilege IAM Policy
A custom inline policy (`github-actions-portfolio-s3-deploy`) attached to the role, granting only the four S3 actions actually needed for the sync command to function:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::brandontrigo.com",
        "arn:aws:s3:::brandontrigo.com/*"
      ]
    }
  ]
}
```

No `AmazonS3FullAccess` or other broad managed policy was used — this role can only read, write, list, and delete objects in this one specific bucket. It has no visibility into or access over any other AWS resource in the account.

### GitHub Actions Workflow
The pipeline itself, defined in `.github/workflows/deploy.yml`:

```yaml
name: Deploy Website Portfolio Site

on:
  push:
    branches:
      - main
    paths:
      - 'website_portfolio/**'

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::[ACCOUNT_ID]:role/github-actions-portfolio-deploy
          aws-region: us-east-1

      - name: Sync files to S3
        run: |
          aws s3 sync ./website_portfolio s3://brandontrigo.com --delete
```

**Key design decisions:**
- **Path-filtered trigger:** Since the GitHub repository is a monorepo containing daily study logs, personal notes, and other unrelated projects alongside the portfolio site, the `paths:` filter ensures this workflow only runs when files inside `website_portfolio/` actually change. A commit to a daily log file does not trigger a deploy attempt.
- **`id-token: write` permission:** Required at the workflow level for the job to be able to request an OIDC token at all. Without this single line, the OIDC handshake cannot occur.
- **`--delete` flag on sync:** Makes S3 a true mirror of the local `website_portfolio/` folder — files removed locally are also removed from the live bucket, rather than accumulating as orphaned objects in S3 over time.

---

## Debugging a Real Authentication Failure

The first pipeline run failed with:

```
Could not assume role with OIDC: Not authorized to perform sts:AssumeRoleWithWebIdentity
```

**Root cause:** a single-character case mismatch. The IAM trust policy's `sub` condition had been entered as `repo:btrigo/my-learning-journey:...` (lowercase `b`), while the actual GitHub account is `Btrigo` (capital `B`). GitHub's OIDC token reports the `sub` claim using the account's actual casing, and IAM's `StringLike`/`StringEquals` condition operators are case-sensitive by default — so the token's claim and the policy's expected value didn't match, and AWS rejected the assume-role request.

This is a useful failure mode to understand: AWS's error message gives no indication of *which* condition failed or *why* — it's a generic authorization denial. Diagnosing it required re-reading the trust policy line by line against the actual GitHub account name, rather than assuming the policy was correct because it had been generated through the console form.

**Fix:** corrected the casing in the trust policy's `sub` condition to match GitHub's exact account casing (`Btrigo`), removed a redundant duplicate condition value left over from the console's role-creation form, and re-ran the workflow — which succeeded on the next attempt.

---

## Verifying the Full Pipeline

To confirm the entire chain worked end-to-end (not just that the workflow reported success), a trivial change was made to `website_portfolio/index.html` (an HTML comment with no visual effect), pushed, and the live site's page source was inspected directly to confirm the change appeared after a manual CloudFront invalidation — proving the path: local edit → push → OIDC auth → S3 sync → cache invalidation → live site.

---

## Key Concepts Learned

**OIDC vs. static credentials:** Federated, short-lived tokens eliminate the risk of a leaked long-lived access key, and scope trust to a specific repo/branch rather than an entire AWS account.

**Trust policy condition operators are case-sensitive:** `StringEquals` and `StringLike` perform exact (or pattern) matching with no case normalization. A policy that "looks correct" can still fail authorization over a single-character casing difference.

**Path-filtered triggers are essential in a monorepo:** Without scoping a workflow's trigger to the specific folder it deploys, unrelated commits elsewhere in the repository would unnecessarily trigger deploy attempts.

**Granting a permission is not the same as using it:** Attaching `s3:DeleteObject` to the IAM role does not, by itself, cause any deletions — the `aws s3 sync` command still needs the `--delete` flag explicitly set for that behavior to occur. Permissions define what's *allowed*; the command defines what's *requested*.

**Generic authorization errors require systematic debugging:** `Not authorized to perform sts:AssumeRoleWithWebIdentity` does not specify which condition failed. Resolving it required methodically checking each piece of the trust policy against the actual values being presented, rather than guessing.

---

## Technologies & Services

| Service / Tool | Purpose |
|---|---|
| GitHub Actions | CI/CD pipeline execution |
| OIDC (OpenID Connect) | Federated, short-lived authentication between GitHub and AWS |
| AWS IAM | Identity provider registration, scoped role, least-privilege policy |
| AWS STS | Token validation and temporary credential issuance |
| Amazon S3 | Deployment target for static site files |
| Amazon CloudFront | CDN cache, manually invalidated post-deploy |
| AWS CLI | Manual CloudFront invalidation command |

---

## On the Horizon

This project's console/CLI phase is complete. Per the established "build it twice" methodology, the next phase is rebuilding this same pipeline's AWS-side configuration (OIDC provider, IAM role, trust policy, permissions policy) in Terraform — at which point CloudFront invalidation automation will also be revisited and folded into the pipeline, once the manual command has been run enough times to be fully internalized rather than just understood conceptually.
