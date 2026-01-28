# Project 01: Secure EC2 Windows Server Instance

## Objective
Launch and configure a secure Windows Server EC2 instance with proper SSH access controls and security group configuration.

## Environment
- **Cloud Provider**: AWS
- **Region**: us-east-1
- **Instance Type**: t2.micro (Free Tier eligible)
- **Operating System**: Windows Server
- **Date**: January 27, 2026

## Prerequisites
- AWS account with appropriate IAM permissions
- Understanding of basic networking concepts
- SSH client installed locally

## Architecture Overview
This lab demonstrates fundamental AWS EC2 security concepts including instance provisioning, key-based authentication, and network security group configuration.

---

## Implementation Steps

### 1. Instance Launch
**Console Navigation**: EC2 Dashboard → Launch Instance

**Configuration**:
- Instance type: `t2.micro`
- AMI: Windows Server (latest available)
- Region: `us-east-1`
- Instance name: `winserver-lab`

### 2. Key Pair Creation
**Purpose**: Establish secure, key-based authentication for instance access

**Steps**:
1. During instance launch, select "Create new key pair"
2. Key pair type: RSA
3. File format: `.pem` (for SSH) or `.ppk` (for PuTTY)
4. Download and save securely

**Storage Best Practice**:
```bash
# Store in AWS configuration directory
~/.aws/your-file-here/

# Set restrictive permissions
chmod 400 ~/.aws/.../your-keypair.pem
```

### 3. Security Group Configuration
**Purpose**: Implement network-level access controls using AWS security groups

**Inbound Rules Configured**:
| Type | Protocol | Port | Source | Purpose |
|------|----------|------|--------|---------|
| SSH | TCP | 22 | My IP/32 | Restrict SSH access to authorized IP only |

**Security Principle**: Least privilege - only allow necessary traffic from specific source addresses

**Note**: For Windows instances, you may also need:
- RDP (TCP 3389) for graphical access
- Adjust based on your access requirements

**Best Practices Implemented**:
- ✅ Source restricted to specific IP (not 0.0.0.0/0)
- ✅ Only required ports opened
- ✅ No unnecessary services exposed

### 4. SSH Connection
**Connection Command**:
```bash
ssh -i ~/.aws/CHOOSE_YOUR_PATH!!_/your-keypair.pem Administrator@<instance-public-ip>
```

**For Windows instances, alternative methods**:
```bash
# Using RDP
mstsc /v:<instance-public-ip>

# Using SSH (if configured)
ssh -i ~/.aws/stuff-and-things/your-keypair.pem Administrator@<instance-public-ip>
```

### 5. System Updates
Once connected, update the system to ensure latest security patches:

**Windows Server**:
```powershell
# Check for updates via Windows Update
# Or use PowerShell
Install-Module PSWindowsUpdate
Get-WindowsUpdate
Install-WindowsUpdate -AcceptAll -AutoReboot
```

### 6. Instance Termination
**Important**: Properly clean up resources to avoid charges

**Steps**:
1. Navigate to EC2 → Instances
2. Select instance
3. Instance State → Terminate Instance
4. Confirm termination

**What Gets Deleted**:
- Instance compute resources
- Associated EBS root volume (by default)
- Ephemeral storage

**What Persists**:
- EBS volumes with "Delete on Termination" disabled
- Snapshots
- Elastic IPs (if allocated)
- Security groups

---

## Security Considerations

### Network Security
- **Security Groups**: Stateful firewall rules applied at instance level
- **Source IP Restriction**: Critical for preventing unauthorized access
- **Dynamic IPs**: Update security group rules if your source IP changes

### Access Management
- **Key Pairs**: Never share private keys or commit to version control
- **File Permissions**: Always set restrictive permissions (400) on private keys
- **Key Rotation**: Regularly rotate access keys and credentials

### Cost Management
- **Stop vs Terminate**: Stopping instances retains EBS volumes (ongoing storage costs)
- **Terminate**: Completely removes instance and associated resources
- **Free Tier**: t2.micro provides 750 hours/month free for first 12 months

---

## Common Issues & Troubleshooting

### Permission Denied (publickey)
**Cause**: Incorrect key permissions or wrong key file

**Solution**:
```bash
chmod 400 ~/.aws/.../your-keypair.pem
ssh -i ~/.aws/merp/your-keypair.pem -v Administrator@<ip>  # verbose mode
```

### Connection Timeout
**Cause**: Security group blocking access or incorrect source IP

**Solution**:
- Verify security group allows your current IP
- Check your public IP: `curl ifconfig.me`
- Update security group if IP changed

### Instance Not Accessible After Restart
**Cause**: Public IP changes when instance stops/starts

**Solution**:
- Use Elastic IP for static addressing (note: costs apply when not associated)
- Retrieve new public IP from EC2 console

---

## Key Takeaways

### Technical Skills Developed
- ✅ EC2 instance provisioning and configuration
- ✅ Security group rule implementation
- ✅ SSH key-based authentication
- ✅ Network security fundamentals
- ✅ AWS resource lifecycle management

### Security Best Practices
- Principle of least privilege in network access
- Proper credential management
- Regular system updates and patching
- Resource cleanup to prevent unnecessary exposure

### AWS Fundamentals
- Difference between stopping and terminating instances
- EBS volume persistence behavior
- Security groups as virtual firewalls
- Free tier resource management

---

## Lab Completion Checklist
- [x] Launch t2.micro Windows Server instance
- [x] Create and secure key pair
- [x] Configure security group with source IP restriction
- [x] Successfully connect via SSH
- [x] Perform system updates
- [x] Terminate instance and cleanup resources
- [x] Document procedures and learnings

---

## Next Steps
- Explore security groups vs Network ACLs
- Practice installing and configuring web servers
- Implement additional security hardening measures
- Experiment with different instance types and AMIs
- Set up CloudWatch monitoring and billing alerts

---

## References
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Security Groups Best Practices](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html)
- [AWS Free Tier](https://aws.amazon.com/free/)

---

**Lab Status**: ✅ Completed  
**Last Updated**: January 27, 2026
