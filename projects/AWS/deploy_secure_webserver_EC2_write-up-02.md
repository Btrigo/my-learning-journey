# Project 01.5: Secure EC2 Apache Web Server Deployment

**Date:** January 28, 2026  
**Objective:** Deploy and harden an Apache web server on AWS EC2 with security best practices  
**Time Investment:** ~3 hours  
**Status:** ✅ Complete

---

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Deployment Steps](#deployment-steps)
- [Security Hardening](#security-hardening)
- [Verification & Testing](#verification--testing)
- [Security Controls Implemented](#security-controls-implemented)
- [Key Learnings](#key-learnings)
- [Cleanup](#cleanup)
- [References](#references)

---

## Overview

This project demonstrates the deployment of a secure Apache web server on AWS EC2, implementing security hardening measures following industry best practices. The focus is on minimizing attack surface, implementing least-privilege access controls, and documenting security configurations.

**Key Accomplishments:**
- Deployed EC2 instance with restricted network access
- Installed and configured Apache web server
- Implemented Apache security hardening (directory listing protection, version hiding)
- Configured security groups following principle of least privilege
- Documented security posture and attack surface

---

## Architecture

```
Internet
    │
    │ (HTTPS requests from anywhere)
    ├─────────────────────────────────────┐
    │                                     │
    ▼                                     │
┌─────────────────────────────────┐      │
│   Security Group                │      │
│   ┌──────────────────────────┐  │      │
│   │ Inbound Rules:           │  │      │
│   │ • SSH (22): MY_IP/32     │  │      │
│   │ • HTTP (80): 0.0.0.0/0   │  │      │
│   └──────────────────────────┘  │      │
└─────────────────┬───────────────┘      │
                  │                      │
    ┌─────────────▼──────────────┐       │
    │   EC2 Instance             │       │
    │   • Amazon Linux 2023      │       │
    │   • t3.micro (Free Tier)   │       │
    │   • Apache 2.4.x           │       │
    │   • Hardened Configuration │       │
    └────────────────────────────┘       │
                                         │
    SSH Access (port 22) ────────────────┘
    (Admin only, from specific IP)
```

**Network Details:**
- **VPC:** Default VPC
- **Subnet:** Public subnet with auto-assign public IP enabled
- **Instance Type:** t3.micro (free tier eligible)
- **OS:** Amazon Linux 2023
- **Public IP:** Dynamically assigned (changes on restart)

---

## Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| AWS EC2 | - | Virtual server hosting |
| Amazon Linux | 2023 | Operating system |
| Apache (httpd) | 2.4.x | Web server |
| AWS CLI | 2.x | Infrastructure management |
| OpenSSH | 8.x | Secure remote access |
| Nano | 8.x | Configuration editing |

---

## Prerequisites

- AWS Account with free tier remaining
- AWS CLI installed and configured
- SSH client (built-in on Linux/Mac, PuTTY on Windows)
- Basic understanding of Linux command line
- Terminal access

---

## Deployment Steps

### 1. Launch EC2 Instance

**Via AWS Console:**

```bash
# Navigate to EC2 Dashboard
# Click "Launch Instance"

# Configuration:
Name: Day-1-Secure-Apache-Lab
AMI: Amazon Linux 2023 AMI
Instance Type: t3.micro (free tier)
Key Pair: Create new RSA key pair, save as lab-01-key.pem
Network Settings:
  - VPC: Default
  - Subnet: Any (auto-assign public IP: Enable)
  - Security Group: Create new
    - Name: day-1-web-server-sg
    - Rules:
      * SSH (22) - Source: My IP
      * HTTP (80) - Source: Anywhere (0.0.0.0/0)
Storage: 8 GiB gp3 (default)
```

**Via AWS CLI:**

```bash
# Get your current public IP
MY_IP=$(curl -s ifconfig.me)

# Create security group
aws ec2 create-security-group \
    --group-name day-1-web-server-sg \
    --description "Security group for Day 1 Apache lab"

# Add SSH rule (your IP only)
aws ec2 authorize-security-group-ingress \
    --group-name day-1-web-server-sg \
    --protocol tcp \
    --port 22 \
    --cidr $MY_IP/32

# Add HTTP rule (public access)
aws ec2 authorize-security-group-ingress \
    --group-name day-1-web-server-sg \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

# Launch instance
aws ec2 run-instances \
    --image-id ami-0532be9a8e0e7e0a5 \
    --instance-type t3.micro \
    --key-name lab-01-key \
    --security-groups day-1-web-server-sg \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Day-1-Secure-Apache-Lab}]'
```

### 2. Secure Key Pair

```bash
# Create directory for AWS keys
mkdir -p ~/.ssh/aws-keys

# Move downloaded key
mv ~/Downloads/lab-01-key.pem ~/.ssh/aws-keys/

# Set restrictive permissions (required by SSH)
chmod 400 ~/.ssh/aws-keys/lab-01-key.pem
```

### 3. Connect via SSH

```bash
# Get instance public IP
aws ec2 describe-instances \
    --filters "Name=instance-state-name,Values=running" \
    --query 'Reservations[*].Instances[*].PublicIpAddress' \
    --output text

# Connect to instance
ssh -i ~/.ssh/aws-keys/lab-01-key.pem ec2-user@<PUBLIC_IP>
```

**Note:** Default username for Amazon Linux is `ec2-user`

### 4. Update System

```bash
# Update all packages (includes security patches)
sudo yum update -y
```

### 5. Install Apache

```bash
# Install Apache web server
sudo yum install httpd -y

# Start Apache
sudo systemctl start httpd

# Enable Apache to start on boot
sudo systemctl enable httpd

# Verify Apache is running
sudo systemctl status httpd
```

### 6. Deploy Custom Web Page

```bash
# Create custom index page
sudo bash -c 'cat > /var/www/html/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Day 1 - Secure Apache Lab</title>
</head>
<body>
    <h1>Welcome to My Secure Apache Server!</h1>
    <p>This is Day 1 of my 60-Day AWS Cloud Security Sprint</p>
    <p>Server deployed: $(date)</p>
</body>
</html>
EOF'

# Set proper permissions
sudo chmod 644 /var/www/html/index.html
sudo chmod 755 /var/www/html
```

### 7. Test Web Server

**From browser:**
```
http://<PUBLIC_IP>
```

**From terminal:**
```bash
curl http://localhost
```

---

## Security Hardening

### 1. Disable Directory Indexing

**Why:** Prevents attackers from browsing directory contents and discovering sensitive files.

**Risk without hardening:**
- Attacker visits `/backup/` and sees list of all backup files
- Direct download of exposed configuration files, databases, credentials

**Implementation:**

```bash
# Edit Apache configuration
sudo nano /etc/httpd/conf/httpd.conf

# Find this line:
Options Indexes FollowSymLinks

# Change to:
Options -Indexes +FollowSymLinks

# Save and exit (Ctrl+X, Y, Enter)
```

### 2. Hide Apache Version Information

**Why:** Reduces reconnaissance capabilities - attackers can't immediately identify vulnerable versions.

**Risk without hardening:**
- HTTP headers reveal exact Apache version
- Attackers search for CVEs targeting specific versions
- Targeted exploitation becomes trivial

**Implementation:**

```bash
# Edit Apache configuration
sudo nano /etc/httpd/conf/httpd.conf

# Add these lines at the end of the file:
ServerTokens Prod
ServerSignature Off

# Save and exit
```

**What this does:**
- `ServerTokens Prod`: Shows only "Apache" in HTTP headers (not version/modules)
- `ServerSignature Off`: Removes version info from error pages (404, 403, etc.)

### 3. Apply Changes

```bash
# Restart Apache to apply configuration changes
sudo systemctl restart httpd

# Verify Apache restarted successfully
sudo systemctl status httpd
```

---

## Verification & Testing

### 1. Verify Version Hiding

```bash
# Check HTTP headers
curl -I http://localhost | grep Server

# Expected output:
Server: Apache

# NOT: Server: Apache/2.4.58 (Amazon) OpenSSL/3.0.8
```

### 2. Test Directory Listing Block

```bash
# Create test directory with files
sudo mkdir /var/www/html/test
sudo touch /var/www/html/test/testfile.txt

# Visit in browser: http://<PUBLIC_IP>/test/
# Expected: "403 Forbidden" (not file list)

# Cleanup
sudo rm -r /var/www/html/test
```

### 3. Verify Security Group Configuration

```bash
# List security group rules
aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=day-1-web-server-sg" \
    --query 'SecurityGroups[*].IpPermissions'
```

### 4. Enumerate Running Services

```bash
# Check what services are exposed
sudo systemctl list-unit-files --type=service --state=enabled | grep -v disabled

# Critical services to monitor:
# - sshd.service (SSH access)
# - httpd.service (Web server)
# - auditd.service (Security logging)
```

---

## Security Controls Implemented

| Control | Type | Purpose | Risk Mitigated |
|---------|------|---------|----------------|
| SSH restricted to specific IP | Network | Prevent unauthorized access | Brute force attacks, unauthorized access |
| Key-based authentication | Access Control | Strong authentication | Password attacks, credential stuffing |
| HTTP open to 0.0.0.0/0 | Network | Public web access | N/A (required for web server) |
| Directory listing disabled | Application | Prevent information disclosure | File enumeration, sensitive data exposure |
| Version hiding (ServerTokens) | Application | Reduce reconnaissance surface | Targeted vulnerability exploitation |
| Server signature disabled | Application | Minimize info leakage | Version disclosure in error pages |
| System updates applied | Patch Management | Fix known vulnerabilities | CVE exploitation |
| File permissions (644/755) | Access Control | Principle of least privilege | Unauthorized file modification |

**Attack Surface Analysis:**
- **Exposed Ports:** 22 (SSH, restricted), 80 (HTTP, public)
- **Running Services:** sshd, httpd, system services only
- **Information Leakage:** Minimized (version info hidden)
- **Authentication:** Key-based SSH (no passwords)

---

## Key Learnings

### Technical Skills Gained
1. **AWS EC2 Management:**
   - Instance launch and configuration
   - Security group design and implementation
   - Understanding VPC networking basics

2. **Linux System Administration:**
   - Package management with `yum`
   - Service management with `systemctl`
   - File permissions and ownership

3. **Apache Configuration:**
   - Installation and basic setup
   - Security hardening best practices
   - Configuration file editing

4. **Security Concepts Applied:**
   - Principle of least privilege
   - Defense in depth
   - Attack surface reduction
   - Information disclosure prevention

### Security Engineering Insights

**Why these controls matter:**

1. **SSH Restriction (My IP only):**
   - Blocks automated bot scans
   - Prevents brute force attempts from unknown sources
   - Reduces attack surface by 99.9%

2. **HTTP Public Access (0.0.0.0/0):**
   - Necessary for web server functionality
   - Risk accepted and mitigated through application hardening
   - Not a vulnerability when properly configured

3. **Directory Indexing Disabled:**
   - Professional sites never show directory listings
   - Prevents reconnaissance of file structure
   - Blocks direct access to unintended files

4. **Version Hiding:**
   - Makes targeted attacks harder
   - Forces attackers to probe blindly
   - Increases time required for reconnaissance
   - Not security through obscurity alone (layered with actual hardening)

### Shared Responsibility Model

**AWS Responsibilities:**
- Physical data center security
- Hypervisor and network infrastructure
- Hardware maintenance
- Availability and redundancy

**My Responsibilities:**
- Operating system patches and updates
- Application security (Apache configuration)
- Security group configuration
- Access control (SSH keys, IAM)
- Data encryption
- Firewall rules

**Key Insight:** AWS secures the infrastructure, but I'm responsible for everything I configure and deploy. Misconfigurations are not AWS's fault.

---

## Cleanup

**Important:** Always clean up resources to avoid unexpected charges.

```bash
# Terminate EC2 instance
aws ec2 terminate-instances --instance-ids <INSTANCE_ID>

# Wait 2-3 minutes for termination to complete

# Check for orphaned EBS volumes
aws ec2 describe-volumes --filters "Name=status,Values=available"

# Delete orphaned volumes (if any)
aws ec2 delete-volume --volume-id <VOLUME_ID>

# Delete security group
aws ec2 delete-security-group --group-name day-1-web-server-sg

# Delete key pair from AWS (optional)
aws ec2 delete-key-pair --key-name lab-01-key

# Delete local key file (optional)
rm ~/.ssh/aws-keys/lab-01-key.pem
```

**Cost Verification:**
- Check AWS Billing Dashboard
- Verify no running instances
- Confirm no orphaned EBS volumes
- Review free tier usage

---

## References

### AWS Documentation
- [EC2 User Guide](https://docs.aws.amazon.com/ec2/)
- [EC2 Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html)
- [AWS Free Tier](https://aws.amazon.com/free/)

### Apache Documentation
- [Apache HTTP Server Documentation](https://httpd.apache.org/docs/2.4/)
- [Apache Security Tips](https://httpd.apache.org/docs/2.4/misc/security_tips.html)

### Security Best Practices
- [OWASP Web Application Security](https://owasp.org/)
- [CIS Apache HTTP Server Benchmark](https://www.cisecurity.org/benchmark/apache_http_server)
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)

### Tools Used
- [AWS CLI Reference](https://docs.aws.amazon.com/cli/)
- [curl Documentation](https://curl.se/docs/)

---

## Next Steps

**Recommended follow-on projects:**
1. Implement CloudWatch monitoring and alerting
2. Enable CloudTrail for audit logging
3. Deploy multi-tier VPC architecture
4. Automate deployment with Terraform
5. Add SSL/TLS certificate (HTTPS)
6. Implement Web Application Firewall (WAF)

**Skills to develop:**
- Infrastructure as Code (Terraform/CloudFormation)
- Container security (Docker/ECS)
- CI/CD pipeline security
- Incident response automation

---

## Project Metadata

**Part of:** 60-Day AWS Cloud Security Sprint  
**Project Number:** 01  
**Difficulty:** Beginner  
**Estimated Time:** 2-3 hours  
**Cost:** $0 (free tier)  

**Author:** Brandon Trigo  
**Date:** January 28, 2026  
**GitHub:** [Link to repository]  
**LinkedIn:** [Link to profile]

---

## License

This documentation is provided for educational purposes. Feel free to use and modify for your own learning.

---

**End of Document**
