# Lab 1: VPC & Networking Foundation — Write-up

**Date:** September 11, 2026
**Method:** Console-first build, fully verified end to end, then torn down. Terraform rebuild pending.
**Status:** Baseline complete — evolving toward a production-worthy version before advancing to Lab 2.

---

## Objective

Stand up a custom VPC with public/private subnet separation, prove that private resources are unreachable from the internet while still able to reach it outbound, and confirm controlled human access via a bastion host — all from first principles, not just clicking through a wizard.

## Architecture Built

```
VPC: lab1-vpc (10.69.0.0/16)
│
├── us-east-1a
│   ├── Public subnet   (10.69.0.0/24)   — lab1-bastion, NAT Gateway
│   └── Private subnet  (10.69.128.0/24) — lab1-private
│
├── us-east-1b
│   ├── Public subnet   (10.69.16.0/24)
│   └── Private subnet  (10.69.144.0/24)
│
├── Internet Gateway (lab1-igw) — attached to VPC
├── NAT Gateway (lab1-nat-public1-us-east-1a) — 1 AZ, zonal, with Elastic IP
├── S3 Gateway Endpoint (lab1-vpce-s3) — free, private path to S3
└── Route tables:
    ├── lab1-rtb-public              (0.0.0.0/0 → IGW)      — both public subnets
    ├── lab1-rtb-private1-us-east-1a (0.0.0.0/0 → NAT GW)   — private1
    └── lab1-rtb-private2-us-east-1b (0.0.0.0/0 → NAT GW)   — private2
```

**Security groups (SG-to-SG chaining pattern):**

| Security Group | Inbound | Outbound |
|---|---|---|
| `lab1-bastion-sg` | SSH (22) from home public IP `/32` only | All traffic, `0.0.0.0/0` |
| `lab1-private-sg` | SSH (22) from `lab1-bastion-sg` (SG reference, not an IP) | All traffic, `0.0.0.0/0` |

**Instances:**

| Name | Subnet | Public IP | Key pair |
|---|---|---|---|
| `lab1-bastion` | public1-us-east-1a | Yes (auto-assigned) | `lab1-ssh-bastion` |
| `lab1-private` | private1-us-east-1a | No | `lab1-private-ssh` |

## Key Decisions & Reasoning

- **Custom CIDR (`10.69.0.0/16`) instead of AWS's default `10.0.0.0/16`** — avoids future VPC peering conflicts, since the default is the most commonly reused block in existence.
- **2 AZs, 4 subnets** — even for a disposable lab, since "a subnet can't span AZs" and multi-AZ design is heavily tested/expected knowledge.
- **Single Zonal NAT Gateway ("In 1 AZ") instead of one per AZ** — deliberate cost tradeoff for a lab; understood and documented that this means AZ-1b's private subnet crosses AZ boundaries to reach it and loses redundancy if 1a goes down. Not a production-acceptable choice, but correct for today's scope.
- **Bastion host over SSM Session Manager** — chose the classic pattern for the first rep since it's still the dominant real-world/interview-relevant model; SSM flagged as a stronger production alternative to try in a later pass.
- **S3 Gateway Endpoint added** — free, quick rep, ties private-subnet-to-AWS-service traffic back to the NAT-avoidance conversation from earlier study.
- **Two separate key pairs (bastion vs. private instance)** rather than reusing one — more security-conscious (a compromised key doesn't expose both), at the cost of needing both loaded in the SSH agent for the two-hop connection.

## Concepts Covered / Reinforced

- Subnetting: binary/CIDR math, `2^(32-CIDR)` address counts, AWS's 5-reserved-address rule per subnet (not 2, unlike standard networks)
- Broadcast address: last address in a subnet, used for "ask everyone" discovery traffic (ARP, DHCP) — reserved but unused in AWS VPCs
- NACLs vs. security groups: stateless/subnet-level/allow+deny vs. stateful/instance-level/allow-only
- Gateway comparison: IGW, NAT Gateway (zonal vs. new regional mode), Gateway vs. Interface VPC Endpoints, VGW/Transit Gateway
- Elastic IPs: static, reattachable, free only while attached to a running resource
- NAT Gateway mechanism: source IP rewriting + stateful translation table, why it must live in a public subnet
- SSH key pairs: authentication (not authorization) via public/private key signing; private key never transmitted
- SSH agent forwarding (`-A` flag): enables a two-hop bastion connection without ever placing a private key file on the bastion itself

## Verification

- ✅ SSH'd into bastion from home IP — succeeded (whitelisted `/32` rule)
- ✅ Two-hop SSH from bastion → private instance with **no key file present on the bastion**, authenticated purely via forwarded agent — succeeded, confirming agent forwarding worked end to end
- ✅ `ping 8.8.8.8` from the private instance — 0% packet loss, confirming NAT Gateway outbound path works
- ✅ Confirmed private instance has no Public IPv4 address or Elastic IP in the console — direct inbound access from the internet is structurally impossible, not just blocked by rule

## Security Note Surfaced (Unrelated to Lab, Flagged During Session)

Discovered a long-lived, unused (66 days), `AdministratorAccess`-scoped IAM access key sitting locally in `~/.aws/`. Identified as a real least-privilege risk (static credential + full admin + dormant = pure risk, no active benefit). Deferred rotation/deactivation until confirmed safe to do so — open item, not yet resolved.

## Teardown (Full, Verified Clean)

1. Terminated both EC2 instances
2. Deleted NAT Gateway (blocked initial VPC deletion attempt — ENI dependency)
3. Deleted VPC via "Delete VPC" cascade — removed 11 dependent resources automatically (subnets, route tables, IGW, security groups, endpoint)
4. Released the orphaned Elastic IP manually — **not** cleaned up automatically by VPC deletion
5. Confirmed: 0 instances, 0 VPCs (beyond AWS default), 0 Elastic IPs remaining

