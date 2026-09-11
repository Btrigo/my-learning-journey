# Cloud/DevOps Lab Sequence

Standalone, disposable skill labs — built before starting the official Speedy TCG portfolio project, to cement fundamentals hiring managers screen for. Each lab is built **console-first, then torn down and rebuilt in Terraform**, with full teardown after each pass (no lingering infra between sessions).

## Lab 1 — VPC & networking core
VPC with public/private subnets across 2 AZs, Internet Gateway, NAT Gateway, route tables, security groups (chained SG-to-SG pattern), S3 Gateway Endpoint, bastion host for private-subnet access via SSH agent forwarding.
**Status: Complete (console pass)**

## Lab 2 — EC2 behind an ALB
Classic multi-tier pattern: EC2 instances in private subnets, Application Load Balancer in public subnets, target groups, health checks, listener rules.

## Lab 3 — RDS + Secrets Manager
Private-subnet-only RDS instance, security group locked to EC2 SG only, DB credentials pulled from Secrets Manager instead of hardcoded.

## Lab 4 — IAM least privilege deep dive
Writing scoped IAM policies (EC2-to-RDS access, Lambda execution roles, CI/CD roles) instead of relying on managed AdministratorAccess.

## Lab 5 — CloudWatch monitoring & alarms
Dashboards and alarms for the Lab 2/3 stack — CPU, target group health, RDS connections — detecting problems before a user would.

## Lab 6 — Containers: Docker, then ECS or a single-node EKS
Containerize a simple app, deploy via ECS (lighter) or a minimal EKS cluster.

## Lab 7 — WAF + Route 53 + CloudFront edge stack
DNS, CDN caching, and WAF actively filtering traffic in front of a real stack, independent of any specific application.

---

Once all seven are complete, the official Speedy TCG project (AWS_Network_Architect portfolio, Projects 04–12) begins with these fundamentals already internalized.