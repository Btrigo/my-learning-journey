# AWS Certified Cloud Practitioner (CLF-C02) - Study Notes
## Part 3 - Hour 1: EC2 Operations, Pricing Models & Identity

---

## Table of Contents
- [EC2 Instance Management](#ec2-instance-management)
- [Elastic IP (EIP)](#elastic-ip-eip)
- [AMI (Amazon Machine Images)](#ami-amazon-machine-images)
- [Launch Templates](#launch-templates)
- [Auto Scaling Groups](#auto-scaling-groups)
- [Load Balancers](#load-balancers)
- [EC2 Pricing Models](#ec2-pricing-models)
- [Reserved Instances](#reserved-instances)
- [Spot Instances](#spot-instances)
- [Dedicated Instances](#dedicated-instances)
- [AWS Savings Plans](#aws-savings-plans)
- [Zero Trust Model](#zero-trust-model)
- [Identity Concepts](#identity-concepts)

---

## EC2 Instance Management

### Connecting to EC2 Instances

#### SSH Client Method
- Uses SSH key pair (.pem file)
- Command: `ssh -i "keyname.pem" ec2-user@<public-ip>`
- **Security concern**: SSH keys can be shared/stolen
- Less secure than Session Manager

#### Session Manager (Preferred Method)
- **No SSH key required** - more secure
- Requires **SSM agent** installed on instance
- Requires **IAM instance profile** with SSM permissions
- Logs in as `ssm-user` by default
- Switch to ec2-user: `sudo su - ec2-user`

**Key Advantages:**
- ✅ More secure (no key management)
- ✅ All connections tracked
- ✅ Auditable access
- ✅ No need to manage SSH keys

### Working with EC2 Instances

#### Important User Context
- Default Linux user for Amazon Linux: **ec2-user**
- SSM logs you in as: **ssm-user**
- Always switch: `sudo su - ec2-user`
- Check current user: `whoami`

#### File Editing
- Use `vi` or `vim` for file editing
- Must use `sudo` for system files
- Example: `sudo vi /var/www/html/index.html`
- **Vi commands:**
  - Press `i` to enter INSERT mode
  - Press `ESC` then `:wq` to write and quit
  - Press `ESC` then `:q!` to quit without saving

#### Web Server Management
- Restart Apache: `sudo systemctl restart httpd`
- No restart needed for static HTML changes (just refresh browser)

### Instance States and IP Addresses

**Critical Concept: IP Address Changes**
- Public IP addresses **change** when instance is stopped and restarted
- Public IP remains the same during reboot
- **Solution**: Use Elastic IP for static addressing

---

## Elastic IP (EIP)

### What is Elastic IP?
- **Static IPv4 address** that doesn't change
- Allocated from Amazon's pool of IP addresses
- Remains assigned even when instance is stopped

### Why Use Elastic IP?
**Problem:** When you stop and start an instance, the public IP changes
- Example: 54.163.4.104 → 54.235.211.10
- Breaks DNS records, application configurations, etc.

**Solution:** Elastic IP provides a consistent address
- Allocate once, use indefinitely
- Associate with different instances as needed

### Elastic IP Operations

#### Allocate an Elastic IP
1. Navigate to EC2 → Elastic IPs
2. Click "Allocate Elastic IP address"
3. Select region (e.g., us-east-1)
4. Choose "Amazon's pool of IPv4 addresses"
5. Allocate

#### Associate Elastic IP
1. Select the Elastic IP
2. Actions → Associate Elastic IP address
3. Choose the EC2 instance
4. Optionally select private IP
5. Click Associate

#### Disassociate and Release
1. Select Elastic IP
2. Actions → Disassociate Elastic IP address
3. Actions → Release Elastic IP address

### ⚠️ Important Cost Warning
- **Elastic IPs cost $1/month if not associated** with a running instance
- Always release unused Elastic IPs
- Hidden cost that accumulates over time

---

## AMI (Amazon Machine Images)

### What is an AMI?
- A **saved snapshot** of an EC2 instance configuration
- Includes:
  - Operating system
  - Installed software and packages
  - Configuration settings
  - Attached volumes
  - Tags (if specified)

### Why Create AMIs?
- **Save configurations** - Don't lose work when terminating instances
- **Quick deployment** - Launch identical instances rapidly
- **Version control** - Number AMIs (e.g., my-ec2-001, my-ec2-002)
- **Backup** - Preserve known-good configurations

### Creating an AMI

#### Steps to Create
1. Select running EC2 instance
2. Actions → Image and templates → Create image
3. Provide:
   - **Image name**: e.g., "my-ec2-001"
   - **Description**: e.g., "My Apache Server"
   - **Tags**: Add name tag for organization
4. Click "Create image"

#### Important Notes
- Creation takes several minutes
- AMI will show "pending" status initially
- Refresh the AMIs page to see updated status
- Don't rely on auto-refresh - **manually refresh**

### Using AMIs
- Select AMI from AMIs page
- Actions → Launch instance from AMI
- Must still configure instance settings (but OS/software pre-configured)

---

## Launch Templates

### What is a Launch Template?
- **Reusable configuration** for launching EC2 instances
- Stores all settings in one place
- **More flexible than AMIs alone**

### Why Use Launch Templates?
- ✅ Don't repeat configuration every time
- ✅ Version control for configurations
- ✅ Used with Auto Scaling Groups
- ✅ Override settings when needed

### Launch Template Components

#### Required Settings
1. **Template name**: e.g., "my-apache-server"
2. **AMI**: Select your custom AMI or AWS-provided
3. **Instance type**: e.g., t2.micro (can be overridden)
4. **Key pair**: For SSH access (optional)
5. **Security group**: Define network access rules
6. **IAM instance profile**: For AWS resource permissions
7. **Storage**: Volume configuration
8. **User data**: Bootstrap scripts (optional if baked into AMI)

#### Advanced Settings
- **IAM instance profile**: Critical for Sessions Manager
- **Network interfaces**: VPC, subnet configuration
- **Tags**: Metadata for resource organization

### Creating Launch Templates

#### Step-by-Step Process
1. EC2 → Launch Templates → Create launch template
2. Name the template
3. **Search for your AMI** (type AMI name, wait for search to complete)
4. Select instance type (or exclude to choose at launch)
5. Select key pair (or exclude)
6. **Select security group**
7. **Set IAM instance profile** (e.g., SSM role)
8. Review and create

#### Versioning
- Create **new versions** when making changes
- Set **default version** or choose version at launch
- Example: Version 1 → Version 2 (with tags added)

### Using Launch Templates
1. Select launch template
2. Actions → Launch instance from template
3. Review vertical layout of settings
4. Override any settings as needed
5. Launch instance

---

## Auto Scaling Groups

### What is an Auto Scaling Group (ASG)?
- Automatically **maintains desired number of instances**
- **Scales out** (add instances) when demand increases
- **Scales in** (remove instances) when demand decreases
- Ensures high availability

### ASG Requirements
- Must use a **Launch Template**
- Define min, max, and desired capacity
- Select VPC and subnets (typically 3 AZs for high availability)
- Optional: Load balancer integration

### Creating an Auto Scaling Group

#### Configuration Steps
1. Navigate to EC2 → Auto Scaling Groups
2. Click "Create Auto Scaling group"
3. **Name**: e.g., "my-asg"
4. **Select launch template** and version
5. Click Next

#### Network Configuration
- Select **VPC** (usually default)
- Select **3 subnets** across different AZs
  - High availability requires ≥3 availability zones
- Click Next

#### Load Balancer (Optional for now)
- Can attach load balancer later
- Usually ASGs are paired with load balancers
- Skip for basic setup

#### Capacity Settings
| Setting | Example | Description |
|---------|---------|-------------|
| **Desired capacity** | 1 | Target number of instances |
| **Minimum capacity** | 1 | Never go below this |
| **Maximum capacity** | 2 | Never exceed this |

#### Scaling Policies
**Target Tracking Scaling Policy:**
- Metric: CPU utilization
- Target: 50% (example)
- Action: Launch instance if CPU > 50%

**Scale-in Protection:**
- Prevents ASG from terminating instances
- Use when you want manual control over scale-in

#### Notifications (Optional)
- Alert when scaling events occur
- Requires SNS topic setup

#### Tags
- Tags can propagate to instances
- **Better to define in Launch Template**
- ASG tags typically for the ASG resource itself

### ASG Operations

#### Instance Management
- ASG monitors instance health
- **Automatically replaces unhealthy instances**
- Uses **EC2 status checks** by default
- Can use **ELB health checks** (more sophisticated)

#### Testing ASG
1. Wait for instance to launch
2. Verify instance shows in Auto Scaling Group
3. Access instance via public IP
4. **Terminate instance** manually
5. ASG detects and launches replacement

#### Connection Draining
- When terminating, ASG waits for connections to drain
- Ensures no interruption to active requests
- May take time if load balancer is attached

---

## Load Balancers

### Why Use a Load Balancer?
Even with a **single instance**, load balancers provide:
- ✅ Easy scaling when ready
- ✅ Intermediate layer for security (WAF integration)
- ✅ **Free SSL certificates** (via ACM)
- ✅ Static DNS endpoint
- ✅ Health checks for instances

### Types of Load Balancers
1. **Application Load Balancer (ALB)** - HTTP/HTTPS (Layer 7)
2. **Network Load Balancer (NLB)** - TCP/UDP (Layer 4)
3. **Gateway Load Balancer (GLB)** - Layer 3 traffic
4. **Classic Load Balancer** - Legacy (deprecated)

### Creating an Application Load Balancer

#### Basic Configuration
1. Navigate to EC2 → Load Balancers
2. Click "Create load balancer"
3. Select **Application Load Balancer**
4. **Name**: e.g., "my-alb"
5. **Scheme**: Internet-facing
6. **IP address type**: IPv4

#### Network Mapping
- Select **VPC**
- Select **3 availability zones** (same as ASG)
- Critical: **Must match ASG subnets**

#### Security Groups
- Create or select security group
- Must allow **Port 80** (HTTP) inbound
- ALB forwards to instances

#### Listeners and Routing
- **Listener**: Port 80 (HTTP)
- **Default action**: Forward to target group
- Need to create target group first

### Target Groups

#### What is a Target Group?
- Collection of instances that receive traffic
- ALB routes requests to targets
- Performs health checks on targets

#### Creating Target Group
1. Navigate to EC2 → Target Groups
2. Click "Create target group"
3. **Target type**: Instances
4. **Name**: e.g., "my-target-group"
5. **Protocol**: HTTP
6. **Port**: 80
7. **VPC**: Select your VPC

#### Health Check Configuration
- **Health check path**: `/` (index page)
- **Healthy threshold**: 2 successful checks
- **Unhealthy threshold**: 3 failed checks
- **Timeout**: 10 seconds
- **Interval**: 30 seconds
- **Success codes**: 200

#### Register Targets
- Select instances to add
- Instances auto-discovered if from ASG
- Click "Create target group"

### Integrating ALB with ASG

#### Attach Load Balancer to ASG
1. Go to Auto Scaling Group
2. Edit settings
3. **Load balancing**: Enable
4. **Select target group**
5. **Health check type**: Change to "ELB"
  - Uses load balancer health checks instead of EC2 checks
  - More sophisticated health monitoring

### Accessing Applications via ALB
- Load balancer provides **DNS name**
- Format: `my-alb-123456789.us-east-1.elb.amazonaws.com`
- Point Route 53 domain to this DNS (if you have one)
- Never use instance IPs directly

### Load Balancer DNS
- Copy DNS name from load balancer details
- Paste in browser to access application
- May take time for health checks to pass
- Once healthy, traffic flows through ALB

---

## EC2 Pricing Models

### Overview of Pricing Models
AWS offers **5 ways** to pay for EC2:

| Model | Savings | Use Case | Flexibility |
|-------|---------|----------|-------------|
| **On-Demand** | 0% (baseline) | Short-term, unpredictable | Highest |
| **Spot** | Up to 90% | Non-critical, interruptible | High |
| **Reserved** | Up to 75% | Steady-state, predictable | Medium |
| **Dedicated** | Varies | Compliance, licensing | Low |
| **Savings Plans** | Up to 66-72% | Flexible commitment | High |

### Marketed Feature
- The "create files" feature includes document creation (docx, pptx, xlsx)
- These pricing models apply to virtual machine usage

---

## On-Demand Pricing

### What is On-Demand?
- **Pay-as-you-go** model
- No upfront payment
- No long-term commitment
- Default pricing when launching EC2

### Billing Methods

#### Per-Second Billing
**Applies to:**
- Linux instances
- Windows instances
- Windows with SQL Enterprise
- Windows with SQL Standard
- Windows with SQL Web
- Instances **without separate hourly charge**

**Minimum:** 60 seconds (1 minute)

#### Per-Hour Billing
**Applies to:**
- All other instance types
- Instances with separate hourly charges
- Pricing always shown as hourly rate

### When to Use On-Demand
✅ **Short-term workloads** - Days or weeks, not months/years
✅ **Spiky workloads** - Unpredictable traffic patterns
✅ **Unpredictable workloads** - Cannot forecast usage
✅ **Cannot be interrupted** - Critical workloads
✅ **First-time applications** - Testing and experimentation

### Pricing Display
- AWS console shows **hourly rates**
- Even for per-second billing
- Bill shows actual per-second usage

---

## Reserved Instances

### What are Reserved Instances (RI)?
- **Commitment to AWS** for 1-year or 3-year term
- Discounted pricing for predictable usage
- Best for **steady-state applications**
- **Does not auto-renew** - must repurchase

### RI Pricing Formula
**Savings based on:**
1. **Term** - Longer = more savings
2. **Class** - Less flexible = more savings
3. **Payment option** - More upfront = more savings
4. **RI attributes** - Instance type, region, tenancy, platform

### Terms
| Term | Commitment | Savings | Auto-Renewal |
|------|------------|---------|--------------|
| **1-year** | 12 months | Lower | ❌ No |
| **3-year** | 36 months | Higher | ❌ No |

**Important:** At expiration, instances convert to On-Demand (no interruption)

### Class Offerings

#### Standard RI
- **Savings**: Up to 75% vs On-Demand
- **Flexibility**: Can modify RI attributes
- **Cannot**: Exchange for different instance family
- Best for: Known, unchanging workloads

#### Convertible RI
- **Savings**: Up to 54% vs On-Demand
- **Flexibility**: Can exchange RIs
- **Requirement**: New RI must be ≥ value of old RI
- Best for: Workloads that may change instance types

#### ~~Scheduled RI~~ (Discontinued)
- AWS no longer offers this class
- Historical reference only

### Payment Options

| Option | Upfront | Ongoing | Savings |
|--------|---------|---------|---------|
| **All Upfront** | 100% | None | Highest |
| **Partial Upfront** | 50% | Discounted hourly | Medium |
| **No Upfront** | 0% | Discounted hourly | Lowest |

**No Upfront Benefits:**
- Pay monthly as usual
- Automatically get discount
- Just commit to usage duration
- Great for cash flow management

### RI Sharing and Marketplace
- ✅ **Shared across organization** accounts
- ✅ **Can sell unused RIs** on RI Marketplace
- Limitations apply (covered next)

### RI Attributes
These affect final pricing and flexibility:

#### 1. Instance Type
- **Format**: Family + Size (e.g., m4.large)
- **Family**: m4, t2, c5, etc.
- **Size**: small, medium, large, xlarge, etc.

#### 2. Region
- Where RI is purchased
- Cannot move between regions (for Standard RI)

#### 3. Tenancy
- **Shared** (default): Multi-tenant hardware
- **Dedicated**: Single-tenant hardware (more expensive)

#### 4. Platform
- **Linux/UNIX**
- **Windows**
- **RHEL, SUSE** (if applicable)
- Affects pricing even with On-Demand

### Regional vs Zonal RI

#### Regional RI
- **Scope**: Any AZ within the region
- **Capacity reservation**: ❌ No guarantee
- **AZ flexibility**: ✅ Use in any AZ
- **Instance flexibility**: ✅ Any size in family (Linux only)
- **Queueing**: ✅ Can queue purchases

**Use case:** Maximum flexibility, don't need guaranteed capacity

#### Zonal RI
- **Scope**: Specific availability zone only
- **Capacity reservation**: ✅ Guaranteed capacity
- **AZ flexibility**: ❌ Locked to one AZ
- **Instance flexibility**: ❌ Exact instance only
- **Queueing**: ❌ Cannot queue purchases

**Use case:** Critical workloads that must have capacity

### RI Limits

#### Regional Limits
- **Max per region**: 20 Regional RIs
- **Important**: Cannot exceed On-Demand limit
- **Default On-Demand limit**: 20 instances
- **Action required**: Request limit increase before purchasing RIs

#### Zonal Limits
- **Max per AZ**: 20 Zonal RIs
- **Special ability**: Can exceed On-Demand limit
- **Example**: 20 On-Demand + 20 Zonal = 40 instances possible

### Capacity Reservations

#### The Problem
- AWS has **finite hardware** in each AZ
- Popular instance types can **run out**
- "InsufficientInstanceCapacity" error

#### The Solution: Capacity Reservation
- **Reserve capacity** for specific instance type
- **Guarantee availability** when you need it
- Charged at **On-Demand rate** whether used or not
- Can **combine with Regional RI** for billing discount

#### Capacity Reservation Options
1. **Manual**: Specify exact configuration
2. **Flexible**: Specify time window
3. **Open-ended**: Reserve indefinitely
4. **Targeted**: Specific instance requirements

---

## Standard vs Convertible RI

### Standard RI Modifications
**Can modify:**
- ✅ Availability Zone (within same region)
- ✅ Scope (Zonal ↔ Regional)
- ✅ Instance size (Linux, default tenancy only)
- ✅ Network (EC2-Classic ↔ VPC)

**Cannot modify:**
- ❌ Instance family
- ❌ Operating system
- ❌ Tenancy type

### Convertible RI Exchanges
**Can exchange:**
- ✅ Instance family (e.g., m4 → c5)
- ✅ Instance type (e.g., m4.large → m4.xlarge)
- ✅ Platform (e.g., Linux → Windows)
- ✅ Scope (Regional ↔ Zonal)
- ✅ Tenancy (Shared ↔ Dedicated)

**Requirement:** New RI value ≥ old RI value

### Marketplace Differences

| Feature | Standard RI | Convertible RI |
|---------|-------------|----------------|
| **Buy from marketplace** | ✅ Yes | ❌ No |
| **Sell in marketplace** | ✅ Yes | ❌ No |
| **Direct AWS only** | No | ✅ Yes |

---

## Reserved Instance Marketplace

### What is the RI Marketplace?
- Platform to **sell unused Standard RIs**
- Recoup costs for unused commitments
- **Standard RIs only** (not Convertible)

### Selling Requirements
- ✅ RI must be active for **≥30 days**
- ✅ AWS must have received upfront payment
- ✅ Must have **US bank account**
- ✅ Must have **≥1 month remaining** on term
- ✅ Annual selling limit: **$20,000**

### What Happens When Selling
**You retain:**
- Pricing and capacity benefits until sold
- Your RI remains active during listing

**What's shared:**
- Company name and address (for tax purposes)
- Shared with buyer upon request

**What you set:**
- Upfront price only

**What's fixed:**
- Usage price (remains original)
- Instance type, AZ, platform (cannot change)
- Term length (rounded down to nearest month)

### Limitations
- ❌ Cannot sell GovCloud RIs
- ❌ Cannot sell >$20,000/year without approval
- ❌ Cannot change instance attributes

---

## Spot Instances

### What are Spot Instances?
- **Spare AWS capacity** being resold
- **Up to 90% discount** vs On-Demand
- Can be **terminated by AWS** at any time
- 2-minute warning before termination

### When to Use Spot Instances
✅ **Flexible start/end times** - Jobs can be interrupted
✅ **Feasible only at low cost** - Economically viable with discount
✅ **Fault-tolerant workloads** - Can handle interruptions
✅ **Batch processing** - Non-time-sensitive jobs
✅ **Big Data workloads** - Distributed processing

**Common use cases:**
- Scientific computing
- Rendering farms
- Data analysis
- CI/CD testing
- Stateless web servers

### Spot Instance Lifecycle

#### Termination Scenarios

**If AWS terminates:**
- ✅ **No charge** for partial hour
- Capacity needed elsewhere

**If you terminate:**
- ❌ **You pay** for full hour used

### AWS Batch Integration
- Purpose-built for batch processing with Spot
- Simpler than managing Spot directly
- Automatically handles spot management
- Recommended for batch workloads

### Reality Check
Instructor's experience: **Spot instances rarely terminate**
- AWS has substantial spare capacity
- Terminations happen but are uncommon
- Great for cost savings with minimal risk

---

## Dedicated Instances

### Multi-Tenancy vs Single-Tenancy

#### Multi-Tenancy (Default)
- **Multiple customers** on same physical hardware
- Separated by **virtualization** (hypervisor)
- Like living in an **apartment building**
- Most cost-effective

#### Single-Tenancy (Dedicated)
- **One customer** per physical hardware
- Separated by **physical isolation**
- Like having your own **house**
- More expensive

### What are Dedicated Instances?
- EC2 instances on **dedicated hardware**
- No other AWS customers on same server
- For **regulatory/compliance** requirements

### Dedicated Instances vs Dedicated Hosts
**Dedicated Instances:**
- Focus: Security and compliance
- Hardware shared only within your account

**Dedicated Hosts** (covered later):
- Focus: Licensing requirements
- Server-bound software licensing
- Need exact physical server control

### Pricing Options for Dedicated
Can still use:
- ✅ On-Demand pricing
- ✅ Reserved Instance pricing
- ✅ Spot Instance pricing

**Surprising fact:** Can save money with Dedicated + Reserved or Spot

### Launching Dedicated Instances
1. Launch EC2 instance
2. **Tenancy** dropdown:
   - Shared (default)
   - Dedicated instance
   - Dedicated host
3. Select "Dedicated instance"
4. Continue with launch

### When to Use Dedicated
- ✅ Security concerns about multi-tenancy
- ✅ Regulatory compliance requirements
- ✅ Industry obligations
- ✅ Corporate policies

---

## AWS Savings Plans

### What are Savings Plans?
- **Simplified alternative** to Reserved Instances
- Commit to **hourly spend** for 1 or 3 years
- More flexible than RIs
- Easier to purchase and manage

### Types of Savings Plans

#### 1. Compute Savings Plans
- **Savings**: Up to 66%
- **Most flexible option**
- Applies to:
  - EC2 (any family, size, AZ, region, OS, tenancy)
  - AWS Fargate
  - AWS Lambda
- Best for: Maximum flexibility

#### 2. EC2 Instance Savings Plans
- **Savings**: Up to 72%
- **Lowest prices**
- Applies to:
  - Specific instance family in specific region
  - Any size, OS, tenancy within family
- Best for: Predictable EC2 usage

#### 3. SageMaker Savings Plans
- **Savings**: Up to 64%
- Applies to: Amazon SageMaker usage
- Any instance family, size, component, region
- Best for: ML workloads

### Terms Available
- **1-year commitment**
- **3-year commitment**

### Payment Options
- **All Upfront** - Pay 100% now, highest savings
- **Partial Upfront** - Pay ~50% now, rest monthly
- **No Upfront** - Pay monthly, lowest savings

### Savings Plans vs Reserved Instances

**Savings Plans advantages:**
- ✅ Simpler to understand
- ✅ Commit to dollar amount, not specific instances
- ✅ More flexible across services
- ✅ No attribute management
- ✅ Automatic optimization

**Don't need to worry about:**
- ❌ Standard vs Convertible classes
- ❌ Regional vs Zonal scope
- ❌ RI attributes (family, size, AZ, region, OS, tenancy)

### How to Purchase
1. AWS Console → Savings Plans
2. Select plan type (Compute/EC2/SageMaker)
3. Choose term (1-year or 3-year)
4. Choose payment option
5. Set hourly commitment (e.g., $10/hour)
6. Purchase

---

## Zero Trust Model

### What is Zero Trust?
**Principle**: "Trust no one, verify everything"

**Traditional security** assumed:
- Inside network = trusted
- Outside network = untrusted

**Zero Trust** assumes:
- ❌ No implicit trust
- ✅ Verify every access attempt
- ✅ Least privilege access
- ✅ Continuous authentication

### Why Zero Trust?

**Old problems:**
- Malicious actors bypass perimeters
- Insider threats
- Compromised credentials
- Lateral movement within network

**New security perimeter:**
- Not network-based
- **Identity-based** security

### Traditional Network-Centric Security
- Focused on **firewalls and VPNs**
- Assumption: Office = safe, outside = dangerous
- Few remote workers
- Controlled physical locations

### Modern Identity-Centric Security
**Driving factors:**
- ☁️ BYOD (Bring Your Own Device)
- 🏠 Remote work
- 🌐 Untrusted locations
- 📱 Multiple devices per user

**Security controls:**
- Multi-Factor Authentication (MFA)
- Provisional access based on risk
- Continuous verification
- Context-aware policies

**Important:** Identity-centric **augments** (adds to) network security, doesn't replace it

---

## Zero Trust on AWS

### AWS Identity Security Services

AWS doesn't have built-in "intelligent" zero trust, but provides tools:

#### IAM (Identity and Access Management)
- Create users, groups, policies
- Define permissions for AWS services

#### Permission Boundaries
- Set maximum permissions a user can have
- Even if granted more, boundaries limit them
- Example: "Never allow ML services access"

#### Service Control Policies (SCPs)
- Organization-wide policies
- Applied across all AWS accounts
- Example: "No one can use Canada region"
- Enforced universally

#### IAM Conditions
Fine-grained control based on:
- 📍 **Source IP**: Restrict by location
- 🌎 **Requested region**: Block certain regions
- 🔐 **MFA presence**: Require MFA
- 🕐 **Time of day**: Restrict access hours
- 🔗 And many more

### AWS Zero Trust Limitations

**AWS provides manual controls, not intelligent detection:**
- ❌ No automatic risk scoring
- ❌ No behavioral analysis
- ❌ No adaptive policies based on context
- ❌ Requires expert configuration
- ❌ Labor-intensive setup

**Example limitation:**
- Can restrict "nighttime access"
- Cannot detect "suspicious nighttime access"
- Cannot auto-restrict if behavior seems malicious

### Supporting AWS Services

Can build zero trust with:

#### CloudTrail
- Logs all API calls
- Feeds into other services for analysis

#### GuardDuty
- Intrusion detection/prevention
- Analyzes CloudTrail logs
- Detects suspicious activity

#### Detective
- Investigates security issues
- Analyzes data from GuardDuty
- Helps identify root causes

**Challenge:** Requires significant expertise to implement effectively

---

## Zero Trust with Third-Party Solutions

### Why Third-Party?
AWS native tools lack **intelligent identity controls**:
- No real-time risk detection
- No contextual decision-making
- Manual policy creation

### Third-Party Advantages

#### Azure Active Directory
**More data points for risk:**
- Device type and health
- Application being accessed
- Time of day patterns
- Location analysis
- MFA status
- What resources accessed
- Historical behavior

**Capabilities:**
- Real-time risk calculation
- Adaptive access controls
- "If risky, restrict to non-sensitive data"
- "If trusted device + MFA, allow full access"

### Popular Third-Party Solutions
1. **Azure Active Directory** (Microsoft)
2. **Google BeyondCorp** (Google zero trust framework)
3. **JumpCloud** (Cloud directory)
4. **Okta** (Identity platform)

### Integration with AWS
- Use **Single Sign-On (SSO)**
- Third-party directory as primary identity source
- SSO federates to AWS
- Get intelligent controls + AWS access

**Result:** Better zero trust than AWS native tools alone

---

## Identity Concepts

### Directory Services

#### What is a Directory Service?
- Maps **network resource names** to **network addresses**
- Shared infrastructure for managing:
  - Users and groups
  - Devices and computers
  - Files and folders
  - Printers
  - Telephone numbers
  - Other network objects

#### Directory Server (Name Server)
- Server that provides directory service
- Critical component of network OS
- Stores resource information as **objects**
- Each object has **attributes**

#### Well-Known Directory Services
1. **DNS (Domain Name Service)** - Internet's directory
2. **Microsoft Active Directory** - On-premise Windows
3. **Azure Active Directory** - Microsoft cloud directory
4. **Apache Directory Service**
5. **Oracle Internet Directory (OID)**
6. **OpenLDAP** - Open-source LDAP
7. **Cloud Identity** (Google)
8. **JumpCloud** - Cloud directory platform

---

## Active Directory (AD)

### History and Purpose
- Introduced in **Windows 2000**
- Manage multiple on-premise infrastructure with **single identity per user**
- Still widely used in enterprises today

### Evolution
- Started with on-premise only
- Now includes **Azure AD** (cloud-hosted)
- Runs on Microsoft Azure cloud

### Active Directory Architecture

#### Domain Controllers
- Servers running AD Domain Services
- Store directory information
- Authenticate and authorize users
- Can have **multiple DCs** for redundancy

#### Forest
- Collection of one or more domains
- Top-level AD structure
- Trust relationships between domains

#### Domain
- Logical group of objects
- Security boundary
- Can have **child domains**

#### Organizational Units (OUs)
- Containers within domains
- Organize objects logically
- Can nest OUs within OUs

#### Objects
Objects stored in OUs:
- 👤 Users
- 🖥️ Computers
- 🖨️ Printers
- 🗄️ Servers
- 📁 File shares
- 👥 Groups

### Why It Matters for AWS
- Many enterprises use AD
- Need to integrate AD with AWS
- Understanding AD helps with:
  - AWS Directory Service
  - SSO implementations
  - Hybrid cloud architectures

---

## Identity Providers (IdPs)

### What is an Identity Provider?
**System that:**
- Creates and maintains identity information
- Provides authentication services
- Enables federation across networks
- Acts as **trusted provider** of user identity

**Analogy:** Like using Google or Facebook to log into other apps

### Popular Identity Providers
- 🔵 Facebook
- 🟠 Amazon
- 🔴 Google
- 🔵 Twitter
- ⚫ GitHub
- 💼 LinkedIn
- 🟦 Microsoft Account

### Federated Identity
**Definition:** Method of linking user identity across multiple separate identity systems

**Example:**
- Your company's AD = Identity Provider
- AWS Account = Service Provider
- Federation = Connect them together

### Authentication Standards

#### OpenID
- **Open standard** for authentication
- Decentralized protocol
- **Purpose**: Prove **who you are**
- Used for social login
- Example: "Login with Google"

#### OAuth 2.0
- **Industry standard** for authorization
- **Purpose**: Grant **access to functionality**
- Doesn't share passwords
- Uses **authorization tokens**
- Example: "Allow app to post on your behalf"

**Key difference:**
- OpenID = Who you are (authentication)
- OAuth = What you can do (authorization)

#### SAML (Security Assertion Markup Language)
- **Open standard** for exchanging auth data
- Between **Identity Provider** and **Service Provider**
- XML-based protocol
- **Primary use**: Single Sign-On (SSO)
- Commonly used via browser

**SAML workflow:**
1. User tries to access service
2. Service redirects to IdP
3. User authenticates with IdP
4. IdP sends SAML assertion to service
5. Service grants access

---

## Single Sign-On (SSO)

### What is SSO?
**Authentication scheme:**
- Log in **once** with single ID and password
- Access **multiple systems** without re-entering credentials
- Seamless experience

### Benefits of SSO

**For IT Departments:**
- ✅ Single identity to manage
- ✅ Access many systems and cloud services
- ✅ Centralized user management
- ✅ Easier to provision/deprovision
- ✅ Better security control

**For End Users:**
- ✅ One password to remember
- ✅ No repeated logins
- ✅ Faster access to resources

### SSO Example Architecture

**Primary Directory:**
- Azure Active Directory (example)

**Connected Services via SAML:**
- Google Workspace
- Salesforce
- Your laptop/computer
- AWS accounts
- Internal applications

**User experience:**
1. Log into Azure AD once
2. Click on AWS - automatically logged in
3. Click on Salesforce - automatically logged in
4. No password entry after initial login

### SSO vs Other Methods
**Not the same as:**
- Same Sign-On (requires password each time)
- Password managers (store passwords, still need to enter)

**True SSO:**
- May show intermediate screen
- But never asks for credentials again

---

## LDAP (Lightweight Directory Access Protocol)

### What is LDAP?
- **Open standard** protocol
- Access and maintain **directory information** over IP
- **Vendor-neutral** (works with any vendor)

### Common LDAP Use Case
**Central storage** for:
- 👤 Usernames
- 🔐 Passwords
- 👥 User groups
- 🎯 Attributes

### Same Sign-On (Not SSO)
LDAP enables **same sign-on:**
- ✅ Same credentials across systems
- ❌ Must **enter credentials each time**
- Different from true SSO

**Example:**
- On-premise Active Directory stores credentials
- Multiple services check LDAP
- Google, Kubernetes, Jenkins all use same credentials
- But you type password at each service

### LDAP vs SSO

| Feature | LDAP (Same Sign-On) | SSO (Single Sign-On) |
|---------|---------------------|---------------------|
| **Password entry** | Each time | Once only |
| **User experience** | Type password repeatedly | Seamless after first login |
| **Protocol** | LDAP | Usually SAML |
| **Convenience** | Lower | Higher |

### When to Use LDAP
**LDAP is necessary when:**
- ❌ System doesn't support SSO
- ✅ System only supports LDAP integration
- Older enterprise applications
- Some CLI tools and services

**Background:**
- Most SSO systems use LDAP underneath
- LDAP wasn't originally designed for web apps
- SAML/SSO built on top for web convenience

---

## Multi-Factor Authentication (MFA)

### What is MFA?
**Security control:**
- Username/email + password (first factor)
- **Second device** confirms identity (second factor)
- Protects against stolen passwords

### Why MFA?
**Protection against:**
- 🚫 Stolen passwords
- 🚫 Phishing attacks
- 🚫 Credential stuffing
- 🚫 Brute force attacks

### Common MFA Methods

#### 1. SMS/Text Message
- Code sent to phone
- Enter code to proceed
- ⚠️ Vulnerable to SIM swapping

#### 2. Authenticator Apps
- Time-based codes (TOTP)
- Apps: Google Authenticator, Authy, Microsoft Authenticator
- More secure than SMS

#### 3. Push Notifications
- Approve login on secondary device
- Tap "Yes" or "Approve"
- Very user-friendly

#### 4. Security Keys (Hardware)
- Physical device (covered next)
- Most secure option

### MFA Availability
- ✅ Most cloud providers (AWS, Azure, GCP)
- ✅ Social media (Facebook, Twitter, Instagram)
- ✅ Email services (Gmail, Outlook)
- ✅ Banking and finance apps

### AWS MFA Recommendation
**Strongly recommended:**
- Enable on **all AWS accounts**
- **Especially AWS root account** (critical)
- Covered in follow-along exercises

### Types of MFA

**Something you know:**
- Password/PIN

**Something you have:**
- Phone, security key, smart card

**Something you are:**
- Fingerprint, face, retina scan

**Strongest security:** Combine multiple factors

---

## Security Keys

### What is a Security Key?
- **Physical device** for second-factor authentication
- Resembles USB memory stick
- Touch metal contact to generate security token
- Auto-fills token into login form

### Popular Brand: YubiKey
**Features:**
- Looks like USB stick
- Works out-of-box with Gmail, Facebook, hundreds more
- Supports **FIDO2, WebAuthn, U2F**
- **Waterproof and crush-resistant**
- Multiple connector types:
  - USB-A
  - USB-C  
  - NFC (Near Field Communication)
  - Lightning (Apple devices)

### Why Security Keys?

**Advantages over phone-based MFA:**
- ✅ Always at your desk (if you want)
- ✅ No battery to charge
- ✅ Very fast (just tap)
- ✅ No phone dependency
- ✅ Most phishing-resistant

**Example use:**
- Plug into computer
- Touch button when prompted
- Instantly authenticated

### AWS MFA Options

When enabling MFA on AWS account:

#### 1. Virtual MFA Device
- Phone apps (Google Authenticator, Authy, etc.)
- Most common method

#### 2. U2F Security Key
- **YubiKey and similar**
- Physical hardware device
- Most secure option

#### 3. Other Hardware MFA Devices
- Dedicated hardware tokens
- Less common
- Not covered in detail

### Recommendation
**For AWS production accounts:**
- Use **U2F security key** (YubiKey)
- Better than virtual MFA for security
- Keep at secure location

---

## Key Takeaways - Hour 1

### EC2 Management
- ✅ Session Manager preferred over SSH for security
- ✅ Elastic IPs provide static addresses (release when unused!)
- ✅ AMIs save instance configurations
- ✅ Launch Templates simplify repeated deployments
- ✅ Auto Scaling Groups ensure availability
- ✅ Load Balancers essential even for single instance

### Pricing Models
- ✅ On-Demand = flexibility, no commitment
- ✅ Reserved = up to 75% savings, 1-3 year commitment
- ✅ Spot = up to 90% savings, interruptible
- ✅ Savings Plans = simplified alternative to RIs

### Security & Identity
- ✅ Zero Trust = verify everything, trust nothing
- ✅ AWS provides tools but requires manual configuration
- ✅ Third-party IdPs offer better intelligent controls
- ✅ MFA critical for all accounts, especially root
- ✅ SSO improves user experience and security
- ✅ LDAP for systems that don't support SSO

---

## Exam Tips - Hour 1

### Must Remember for Exam
1. **Elastic IP costs $1/month if not attached**
2. **Regional RI** = no capacity guarantee, AZ flexible
3. **Zonal RI** = capacity guaranteed, AZ locked
4. **Spot instances** can be terminated by AWS anytime
5. **Convertible RI** savings lower but more flexible
6. **All Upfront** payment = highest savings
7. **Zero Trust** = identity-based security perimeter
8. **SAML** used for browser-based SSO
9. **OAuth** = authorization (what you can do)
10. **OpenID** = authentication (who you are)
11. **MFA strongly recommended** for AWS root account
12. **Session Manager** more secure than SSH keys

### Common Exam Scenarios
- "Instance IP changed after stopping" → Use Elastic IP
- "Guarantee instance availability" → Zonal RI + Capacity Reservation
- "Flexible cost savings across services" → Compute Savings Plan
- "Maximum RI savings" → 3-year All Upfront Standard RI
- "Need to change instance family" → Convertible RI
- "Cheapest option for batch processing" → Spot Instances
- "Connect to instance without SSH key" → Session Manager
- "Browser-based SSO" → SAML
- "Central credential storage" → LDAP directory

---