# Cloud/DevOps Lab Sequence

Standalone, disposable skill labs — built before starting the official Speedy TCG portfolio project, to cement fundamentals hiring managers screen for. Each lab is built **console-first, then torn down and rebuilt in Terraform**, with full teardown after each pass (no lingering infra between sessions).

**Methodology:** no fixed timeline to move from one lab to the next. Each lab starts from the baseline/toy version (like Lab 1's first console pass) and evolves toward something production-worthy through reps — deliberately breaking something and diagnosing it, extending the build toward real-world hardening, and rebuilding in Terraform — done together, guided, not from memory. Move to "build from memory, ask questions only as needed" only once it's explicitly said to be ready — never assumed. Advance to the next lab only once the current one's progression feels done, however long that takes.

## Lab 1 — VPC & networking core
VPC with public/private subnets across 2 AZs, Internet Gateway, NAT Gateway, route tables, security groups (chained SG-to-SG pattern), S3 Gateway Endpoint, bastion host for private-subnet access via SSH agent forwarding.
**Status: Baseline console build complete — now evolving toward production, guided together.**

Progression from here (order flexible, not a checklist to rush):
- Deliberately break something (e.g. remove the NAT route, misconfigure a security group) and diagnose it from the symptom
- Extend toward production: 1-per-AZ NAT Gateways, VPC Flow Logs, SSM Session Manager instead of the bastion, tighter NACLs
- Terraform rebuild (not yet done)
- Once ready (self-declared, not assumed): rebuild solo from memory, asking questions only as needed

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