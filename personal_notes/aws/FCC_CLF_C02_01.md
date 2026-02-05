# AWS Cloud Practitioner Study Notes
## Section: Benefits of Cloud & Global Infrastructure

*Study Date: February 3, 2026*
*Course: FreeCodeCamp AWS Cloud Practitioner*
*Section: Hours 2-4 (Benefits, Global Infrastructure, Architecture)*

---

## 1. BENEFITS OF CLOUD COMPUTING

### Six Original Advantages of Cloud (Historical)
AWS originally defined these six advantages, which are still relevant:

1. **Trade Capital Expense for Variable Expense**
   - Pay-as-you-go model (PAYG)
   - No upfront costs for data centers and servers
   - Pay by hour, minute, or second based on consumption
   - Only pay for what you use

2. **Benefit from Massive Economies of Scale**
   - Share costs with hundreds of thousands of customers
   - AWS achieves higher economies of scale → lower prices for you
   - Unbeatable savings through aggregation

3. **Stop Guessing Capacity**
   - Scale up or down to meet current needs
   - Launch and destroy services whenever needed
   - No more sitting on expensive idle resources
   - No more dealing with limited capacity

4. **Increase Speed and Agility**
   - Launch resources within minutes instead of weeks
   - Developers get access to resources in minutes vs days
   - Rapid experimentation and innovation

5. **Stop Spending Money on Running and Maintaining Data Centers**
   - Focus on customers and applications
   - No more racking, stacking, powering servers
   - AWS handles infrastructure operations

6. **Go Global in Minutes**
   - Deploy apps in multiple regions with a few clicks
   - Provide lower latency for global customers
   - Better user experience at minimal cost

### New Benefits Framework (2024+)

**⚠️ UPDATE NOTE:** AWS has expanded the original six advantages into a broader "Benefits of Cloud" framework that includes:

- **Cost Effectiveness** (combines #1 and #2 above)
- **Global Reach** (maps to #6)
- **Security** (new)
- **Reliability** (new - includes high availability)
- **Performance** (includes scalability and elasticity)
- **Agility** (includes speed from #4)

The course mentions AWS added: High Availability, Elasticity, Reliability, and Security as new categories.

### Seven Advantages (Alternative Framework)

The instructor's generalized version across cloud providers:

1. **Cost-Effective**: Pay-as-you-go, no upfront costs
2. **Global**: Launch workloads anywhere by choosing a region
3. **Secure**: Physical security + configurable access control
4. **Reliable**: Data backup, disaster recovery, replication, fault tolerance
5. **Scalable**: Increase/decrease resources based on demand
6. **Elastic**: AUTOMATIC scaling during spikes and drops
7. **Current**: Underlying hardware/software patched and upgraded automatically

**Key Distinction:** Scalable = you manually scale; Elastic = automatic scaling

---

## 2. AWS GLOBAL INFRASTRUCTURE

**✅ VERIFIED (Feb 2026):** As of early 2025, AWS has:
- **39 launched Regions** (per AWS official documentation)
- **117+ Availability Zones**
- Operating in 190+ countries

### Components of Global Infrastructure

1. **Regions** - Geographic locations with multiple AZs
2. **Availability Zones (AZs)** - Isolated data centers within regions
3. **Edge Locations** - For content delivery and caching
4. **Points of Presence (PoPs)** - Including Regional Edge Caches
5. **Direct Connect Locations** - For dedicated connections
6. **Local Zones** - Extended regions for ultra-low latency
7. **Wavelength Zones** - 5G network edge computing
8. **AWS Outposts** - On-premises AWS hardware

### What is Global Infrastructure?

Globally distributed hardware and data centers that are physically networked together to act as one large resource for end customers.

**Purpose:**
- Millions of active customers
- Tens of thousands of partners globally
- Provides redundancy, low latency, and high availability

---

## 3. AWS REGIONS

### Definition
A **Region** is a geographically distinct location consisting of one or more Availability Zones.

### Key Facts About Regions

**✅ VERIFIED:** 
- AWS has 39 launched regions as of 2025
- Most regions have 3 or more Availability Zones
- Each region is completely isolated from other regions
- Regions are independent in terms of location, power, and water supply

### Region Naming Convention
Format: `[geographic-indicator]-[direction]-[number]`

Examples:
- `us-east-1` - North Virginia (THE most important region)
- `us-west-2` - Oregon  
- `ca-central-1` - Canada (Montreal area)
- `eu-west-1` - Ireland
- `ap-southeast-1` - Singapore

### US-EAST-1 (North Virginia) - CRITICAL TO KNOW

**Why US-East-1 is Special:**
1. AWS's **FIRST** region (launched with S3 and SQS)
2. New services **almost always launch here first**
3. **All billing information** appears in us-east-1
4. Some services **only work** in us-east-1
5. Largest region with **SIX Availability Zones** (most of any region)

### Four Factors When Choosing a Region

1. **Regulatory Compliance / Data Residency**
   - Does the region meet legal requirements?
   - Where is data legally allowed to reside?

2. **Cost**
   - AWS service costs **vary by region**
   - Same service can be different prices in different regions

3. **Service Availability**
   - Not all services available in all regions
   - Check if the services you need are available

4. **Distance / Latency**
   - How close is the region to your end users?
   - Closer = lower latency = better experience

---

## 4. AVAILABILITY ZONES (AZs)

### Definition
An **Availability Zone** is a physical location made up of one or more data centers. Each AZ is designed as an independent failure zone.

**✅ VERIFIED (2025):** 
- Each region has a minimum of 3 AZs (best practice)
- Some regions have up to 6 AZs (us-east-1)
- New accounts *may* be limited to 2 AZs initially in some regions

### AZ Naming Convention
Format: `[region-code][letter]`

Examples:
- `us-east-1a`, `us-east-1b`, `us-east-1c`
- `ca-central-1a`, `ca-central-1b`, `ca-central-1d`

**⚠️ IMPORTANT:** Note that `ca-central-1` skips "c" - maybe it's haunted? (instructor joke, but shows not all regions use consecutive letters)

### AZ Characteristics

**Physical Separation:**
- AZs are within **100 km (60 miles)** of each other
- But separated by "meaningful distance" (many kilometers)
- In different flood plains
- Different power substations
- Separate physical security

**Network Connection:**
- Interconnected with high-bandwidth, low-latency networking
- Redundant, dedicated metro fiber
- All traffic between AZs is **encrypted**
- Supports synchronous replication between AZs
- Within 10 milliseconds latency

**Independence:**
- Discrete UPS (uninterruptible power supply)
- On-site backup generation
- Designed to be isolated from other AZs
- Failure in one AZ won't cascade to others

### AZ IDs vs AZ Names

**⚠️ CRITICAL UPDATE (November 2025):**

**Old System (accounts created before Nov 2025):**
- `us-east-1a` for YOUR account ≠ same physical location as `us-east-1a` for ANOTHER account
- AWS independently mapped AZ names to physical locations per account
- This distributed resources to avoid everyone choosing "1a"

**New System (accounts created Nov 2025+):**
- `us-east-1a` maps to the SAME physical location for all accounts
- Uniform mapping across accounts

**Solution: AZ IDs**
- **AZ ID** = Consistent identifier across ALL accounts
- Format: `[region-code]-az[number]`
- Example: `use2-az1`, `use2-az2`, `use2-az3`
- Use AZ IDs for cross-account coordination

**Regions still using independent mapping (for old accounts):**
- us-east-1 (N. Virginia)
- us-west-1 (N. California)

### High Availability Best Practice

**Run workloads in at least 3 AZs** to ensure:
- Services remain available if 1 or 2 data centers fail
- Protection from: power outages, lightning strikes, tornadoes, earthquakes, floods
- This is called **High Availability**
- Often driven by regulatory compliance requirements

### Subnets and AZs

**Key Concept:** You don't directly choose an AZ when launching resources like EC2 instances.

You choose a **subnet**, and each subnet is associated with ONE Availability Zone.

```
Region: us-east-1
  └─ VPC (Virtual Private Cloud)
      ├─ Subnet A → Associated with us-east-1a
      ├─ Subnet B → Associated with us-east-1b
      └─ Subnet C → Associated with us-east-1c
```

---

## 5. FAULT DOMAINS & FAULT TOLERANCE

### Fault Domain
A section of a network vulnerable to damage if a critical device or system fails.

**Purpose:** Limit blast radius - if a failure occurs, it won't cascade outside that domain.

### Fault Level
A collection of fault domains.

### AWS's Fault Domain Hierarchy

```
AWS Region (Fault Level)
  └─ Availability Zone (Fault Domain)
      └─ Data Center Building (Fault Domain)
          └─ Room in Building (could be fault domain)
              └─ Rack in Room (could be fault domain)
```

### AWS Design for Fault Tolerance

1. **Each Region is completely isolated** from other regions
   - Greatest possible fault tolerance and stability

2. **Each AZ is isolated** but connected via low-latency links
   - Each AZ is an independent failure zone

3. **Physical Separation:**
   - AZs separated by meaningful distance
   - Within 100 km but far enough apart
   - Different flood zones, power sources

4. **Network Redundancy:**
   - Connected to multiple Tier 1 transit providers
   - Redundant, dedicated metro fiber

**Result:** Adopting multi-AZ gives you **High Availability**

---

## 6. AWS GLOBAL NETWORK

### Definition
The interconnections between AWS global infrastructure - the "backbone" of AWS.

Think of it as a **private expressway** where things move fast between data centers.

### Services Using the Global Network

**On-ramps (getting data INTO AWS fast):**
1. **AWS Global Accelerator** - Fast path to AWS resources in other regions
2. **AWS S3 Transfer Acceleration** - Upload to nearest edge location, then fast transfer via network

**Off-ramps (getting data OUT to users fast):**
1. **Amazon CloudFront** - CDN providing content at the edge

**Always on the network:**
1. **VPC Endpoints** - Keep traffic within AWS network, never traverse public internet

**Example:** Resource in us-east-1 talking to resource in eu-west-1 stays on AWS backbone - much faster than going over public internet.

---

## 7. POINTS OF PRESENCE (PoP)

### Definition
An intermediate location between an AWS region and end users.

Could be:
- A data center owned by AWS
- A data center owned by a trusted partner
- Used by AWS services for content delivery or expedited upload

### Types of PoPs

1. **Edge Locations**
   - Hold cached copies of most popular files
   - Web pages, images, videos
   - Reduce delivery distance to end users

2. **Regional Edge Caches**
   - Hold much larger caches of less popular files
   - Reduce full round trip to origin
   - Reduce transfer costs

### Services Using PoPs

1. **Amazon CloudFront** (CDN)
   - Delivers content from nearest edge location
   - Caches web content globally

2. **Amazon S3 Transfer Acceleration**
   - Upload files to nearest edge location
   - Then fast transfer to S3 via AWS network

3. **AWS Global Accelerator**
   - Routes user traffic to nearest edge location
   - Then optimal path through AWS network to your application

### Tier 1 Networks

**All AWS AZs are redundantly connected to multiple Tier 1 transit providers**

**Tier 1 Network:** Can reach every other network on the internet without purchasing IP transit or paying for peering.

---

## 8. AWS DIRECT CONNECT

### Definition
Private (dedicated) connection between your data center/office and AWS.

Like having a **fiber optic cable** running directly from your location to AWS.

### Bandwidth Options

**Lower bandwidth:** 50 Mbps to 500 Mbps
**Higher bandwidth:** 1 Gbps to 10 Gbps

### Benefits

1. **Reduce network costs**
2. **Increase bandwidth throughput** - great for high-traffic networks
3. **More consistent network experience** than typical internet-based connection
4. **Reliable and secure**

### Direct Connect Locations

Trusted partner data centers where you can establish connection.

Example: Allied Data Center in downtown Toronto

**⚠️ SECURITY NOTE:** The connection is DEDICATED but not necessarily SECURE by default. You should combine Direct Connect with AWS VPN to encrypt traffic.

---

## 9. LOCAL ZONES

### Definition
Data centers located very close to densely populated areas to provide **single-digit millisecond latency**.

Example: 7 milliseconds or less

### Key Facts

- **First launched:** Los Angeles (us-west-2-lax-1a)
- **Must opt-in** - contact AWS support to enable
- Tied to parent regions
- Shows up as another AZ in the region

**✅ UPDATE:** As of 2025, AWS has expanded Local Zones beyond just Los Angeles

### Services Available

Limited subset of AWS services:
- Specific EC2 instance types
- Amazon EBS
- Amazon FSx
- Application Load Balancer
- Amazon VPC

### Use Cases

Applications requiring ultra-low latency:
- Media & entertainment production
- Electronic design automation (EDA)  
- Machine learning inference
- Real-time gaming

---

## 10. WAVELENGTH ZONES

### Definition
AWS infrastructure deployed at telecommunications providers' 5G network edges for **ultra-low latency** to mobile devices.

### Partners

- Verizon
- Vodafone
- KDDI
- SK Telecom

### How It Works

1. Create a subnet tied to a Wavelength Zone (like an AZ)
2. Launch EC2 instances into that Wavelength Zone
3. Instances deployed at the edge of 5G networks
4. Mobile users connecting to cell towers route to nearby AWS hardware

### Use Cases

Applications requiring minimal latency to 5G devices

---

## 11. DATA RESIDENCY & SOVEREIGNTY

### Key Definitions

**Data Residency:** Physical/geographical location where data or cloud resources reside

**Compliance Boundaries:** Regulatory requirements describing where data is ALLOWED to reside

**Data Sovereignty:** Jurisdictional control/legal authority over data because of its physical location

### Why This Matters

Government contracts often require:
- "All data must stay in Canada"
- "All data must stay within US borders"  
- Must provide compliance guarantees

### AWS Solutions for Compliance

1. **AWS Outposts** (Physical hardware in your data center)
   - 42U rack of servers in YOUR location
   - You KNOW exactly where data is

2. **AWS Config** (Policy as Code)
   - Continuously check resource configuration
   - Alert if resources deviate
   - Can auto-remediate (delete non-compliant resources)

3. **IAM Policies**
   - Explicitly DENY access to specific regions
   - Prevent users from launching in wrong regions

4. **Service Control Policies (SCPs)**
   - Apply IAM policies organization-wide
   - Across all AWS accounts
   - Prevent anyone from using restricted regions

---

## 12. AWS FOR GOVERNMENT

### Public Sector Definition

Includes:
- Military
- Law enforcement
- Infrastructure
- Public transit
- Public education
- Healthcare
- The government itself

### FedRAMP

**Federal Risk and Authorization Management Program**

- US government-wide program
- Standardized approach to:
  - Security assessment
  - Authorization
  - Continuous monitoring
- For cloud products and services

### AWS GovCloud

**Special isolated regions for US government workloads**

Azure also has GovCloud - not AWS-specific concept

**Characteristics:**
- Only operated by **US citizens**
- Only operated on **US soil**
- Only accessible to **US entities** and **root account holders** who pass screening
- Meets compliance for:
  - FedRAMP
  - DOJ's Criminal Justice Information Systems (CJIS)
  - US International Traffic in Arms Regulations (ITAR)
  - Export Administration Regulations (EAR)
  - Department of Defense (DoD) Cloud Computing Security Requirements

**Regions:**
- AWS GovCloud (US-West)
- AWS GovCloud (US-East)

---

## 13. AWS CHINA

### Key Facts

**AWS China is completely isolated from AWS Global** - intentionally separated for compliance.

**Domain:** amazon.cn (vs AWS Global at aws.amazon.com)

### Requirements to Operate

- Must have **Chinese business license** (ICP license)
- Not all services available in China

### Why Run in China vs Singapore?

Running in mainland China means you **don't traverse the Great Firewall** - all traffic stays within China.

### Regions

**Two regions operated by local partners:**

1. **Beijing (cn-north-1)** - Operated by Sinnet
2. **Northwest (cn-northwest-1)** - Operated by NWCD

**⚠️ BRANDING NOTE:** AWS logo is BANNED in China. Look for modified branding on amazon.cn.

---

## 14. AWS SUSTAINABILITY

**✅ VERIFIED (2024-2025):**

### Climate Pledge

Amazon co-founded the Climate Pledge to achieve **Net Zero carbon emissions by 2040** across all Amazon businesses (including AWS).

More info: sustainability.aboutamazon.com

### Three Pillars

1. **Renewable Energy**
   - **100% renewable energy** achieved in 2023 (7 years ahead of schedule)
   - **✅ VERIFIED:** 100% renewable energy matching maintained in 2024
   - Purchases renewable energy credits (RECs) and Guarantees of Origin

2. **Cloud Efficiency**
   - AWS infrastructure is **4.1x more energy efficient** than median US enterprise data centers
   - **Up to 99% carbon footprint reduction** vs on-premises
   - **✅ VERIFIED:** AWS Graviton processors use up to 60% less energy for same performance

3. **Water Stewardship**
   - Committed to being **water positive by 2030**
   - Direct evaporative cooling technology
   - Non-potable water for cooling
   - On-site water treatment and recycling
   - **✅ VERIFIED 2024:** Global data center WUE (Water Usage Effectiveness) of 0.15 L/kWh - 17% improvement from 2023

**Fun fact:** A LOT of water is involved in cooling data centers

---

## 15. AWS GROUND STATION

### Definition
Fully managed service to control satellite communications, process data, and scale operations without building ground station infrastructure.

### What's a Ground Station?

Big antenna dish pointing at sky to communicate with satellites.

### Use Cases

- Weather forecasting
- Surface imaging
- Communications
- Video broadcasts

### How It Works

1. **Schedule a contact** - Select satellite, start/end time, ground location
2. **Use Ground Station EC2 AMI** - Launch EC2 instances for uplink/downlink
3. **Receive data** - Download to S3 bucket

### Example Scenario

You have an agreement with a satellite imagery provider. They'll take photos of specific regions/times. You use Ground Station to communicate with their satellite and download image data to your S3 bucket.

---

## 16. AWS OUTPOSTS

### Definition
Fully managed service offering same AWS infrastructure/APIs/tools in virtually any data center or on-premises facility.

**Summary:** A rack of servers running AWS stuff at YOUR physical location.

### What's a Rack?

**Rack:** Frame designed to hold and organize IT equipment

**Rack Units (U):** 
- 1U = 1.75 inches
- Industry standard = 48U rack (7 feet tall)
- Full-size rack cage = 42U high

Equipment comes in 1U, 2U, 3U, 4U sizes

### Outposts Form Factors

1. **42U Rack**
   - Full rack of servers
   - AWS delivers assembled, ready to roll into position
   - Just plug into power and network

2. **1U Server**
   - Fits 19" wide x 24" deep cabinets
   - AWS Graviton2 processors
   - Up to 64 vCPUs, 128 GB memory
   - 4 TB local NVMe storage

3. **2U Server**
   - Fits 19" wide x 36" deep cabinets
   - Intel processors
   - Up to 128 vCPUs, 256 GB memory
   - 8 TB local NVMe storage

---

## 17. CLOUD ARCHITECTURE TERMINOLOGIES

### Roles

**Solutions Architect:** Architects technical solutions using multiple systems via research, documentation, experimentation

**Cloud Architect:** Solutions Architect focused solely on cloud services

**Note:** In the marketplace, "Solutions Architect" often describes both roles. Definitions vary by locality and company.

### What Cloud Architects Must Understand

Based on business requirements, factor in:

1. **Availability** - Ability to ensure service remains available
2. **Scalability** - Ability to grow rapidly or unimpeded  
3. **Elasticity** - Ability to shrink and grow to meet demand
4. **Fault Tolerance** - Ability to prevent failure
5. **Disaster Recovery** - Ability to recover from failure

**Plus:**
- **Security** - How secure is the solution?
- **Cost** - How much will this cost?

---

## 18. HIGH AVAILABILITY

### Definition
Ability for service to remain available by ensuring no single point of failure and/or ensuring a certain level of performance.

### AWS Implementation

**Multi-AZ Deployment:**
- Run workload across multiple Availability Zones
- If 1-2 AZs become unavailable, service continues
- Requires at least 2-3 servers running

**Elastic Load Balancer (ELB):**
- Evenly distributes traffic to multiple servers
- In one or more AZs
- If server becomes unavailable/unhealthy, routes only to available servers

**Key Point:** Just having additional servers ≠ high availability. Must meet performance thresholds based on demand.

---

## 19. HIGH SCALABILITY

### Definition
Ability to increase capacity based on increasing demand of traffic, memory, and computing power.

### Types of Scaling

**Vertical Scaling (Scaling Up):**
- Upgrade to bigger server
- More CPU, RAM, storage on one machine

**Horizontal Scaling (Scaling Out):**
- Add more servers of the same size
- **Bonus:** Also provides high availability
- Generally preferred for redundancy

**Decision Factors:** Very dependent on architecture and requirements

---

## 20. HIGH ELASTICITY

### Definition
Ability to AUTOMATICALLY increase or decrease capacity based on current demand.

**Key Difference from Scalability:** AUTOMATIC and BIDIRECTIONAL

### Types with Elasticity

**Horizontal Scaling:**
- **Scaling Out** - Automatically add more servers
- **Scaling In** - Automatically remove underutilized servers

**Vertical Scaling:**
- Generally hard for traditional architectures
- Elasticity usually refers to horizontal scaling

### AWS Implementation

**Auto Scaling Groups (ASG):**
- Automatically add or remove servers
- Based on scaling rules you define
- Based on metrics (CPU, memory, requests/sec, etc.)

---

## 21. FAULT TOLERANCE

### Definition
Ability to ensure no single point of failure. Preventing the chance of failure.

### Implementation

**Fail-overs:** Plan to shift traffic to redundant system if primary fails

**Common Example: Database Fail-over**
- Have a secondary database  
- All ongoing changes continuously synced
- Secondary not in use until fail-over
- Becomes primary when original fails

### AWS Implementation

**RDS Multi-AZ:**
- Run duplicate standby database in another AZ
- Automatic synchronization
- If primary database fails, automatic fail-over to standby

---

## 22. DISASTER RECOVERY & HIGH DURABILITY

### Definition
Ability to recover from disaster and prevent loss of data.

### Key Questions

- Do you have a backup?
- How fast can you restore backup?
- Does backup still work?
- How do you ensure live data isn't corrupt?

### AWS Example

**AWS CloudEndure (Disaster Recovery service):**
- Continuously replicates machines
- To low-cost staging area
- In target AWS account and region
- Fast and reliable recovery if IT data center fails

---

## 23. BUSINESS CONTINUITY PLAN (BCP)

### Definition
Document outlining how business will continue operating during unplanned disruption in services.

Basically: The disaster recovery plan you'll execute.

### Key Metrics

**RPO (Recovery Point Objective):**
- Maximum acceptable amount of DATA LOSS
- Expressed as TIME
- "How much data are you willing to lose?"
- Example: 1 hour RPO = willing to lose 1 hour of data

**RTO (Recovery Time Objective):**
- Maximum acceptable DOWNTIME
- "How much time can you be down without significant financial loss?"
- Example: 4 hour RTO = can't be down more than 4 hours

**Diagram:**
```
[Normal Operations] → [Disaster Occurs]
                          ↓
              [Data Loss Period - RPO]
              [Downtime Period - RTO]
                          ↓
              [Recovery Complete]
```

---

## 24. DISASTER RECOVERY OPTIONS

### Ranking (Cold → Hot)

From lowest cost/longest recovery to highest cost/fastest recovery:

#### 1. Backup and Restore (Coldest)

**Method:**
- Back up data
- At disaster, restore to new infrastructure

**RPO/RTO:** Hours

**Cost:** Lowest

**Use Case:** Low priority, cost-effective

**Process:**
1. Restore data after event
2. Deploy resources after event

---

#### 2. Pilot Light

**Method:**
- Data replicated to another region
- Minimal services running (just enough to keep replication going)
- Core services always on

**RPO/RTO:** ~10 minutes

**Cost:** Low-Medium

**Use Case:** Less stringent RTO/RPO

**Process:**
1. Core services already running
2. Start and scale resources after event

---

#### 3. Warm Standby

**Method:**
- Scaled-DOWN copy of infrastructure running
- All critical systems present but not at full capacity
- When disaster strikes, scale UP to needed capacity

**RPO/RTO:** Minutes

**Cost:** Medium-High

**Use Case:** Business-critical services

**Process:**
1. Scale resources after event
2. Already running, just smaller

---

#### 4. Multi-Site Active-Active (Hottest)

**Method:**
- Scaled-UP copy in another region
- Identical infrastructure running at full capacity
- Both sites actively serving traffic

**RPO/RTO:** Real-time (zero downtime, near-zero data loss)

**Cost:** Highest (double your infrastructure cost)

**Use Case:** Mission-critical services

**Note:** Most expensive but zero downtime

---

### Cost vs Interruption Trade-off

```
↑ Cost/Complexity
│
│  Multi-Site
│  Active-Active ████████████ (no downtime)
│
│  Warm Standby  ███████ (minutes)
│
│  Pilot Light   ████ (10 min)
│
│  Backup/       ██ (hours)
│  Restore
│
└──────────────────────────────→
   Length of Service Interruption

   [RTO line crosses to determine
    acceptable recovery cost]
```

**Your BCP defines:**
- Acceptable recovery cost
- Required RTO/RPO
- Which DR option to implement

---

## 25. AWS MANAGEMENT CONSOLE

### What It Is

Web-based unified console to build, manage, and monitor everything from simple web apps to complex cloud deployments.

**Access:** console.aws.amazon.com

**Also called:**
- AWS Console
- AWS Dashboard
- The Management Console

### Characteristics

- Point-and-click interface
- **Click-Ops** - perform all system operations via clicks
- Limited programming knowledge needed
- Manually launch and configure resources

**⚠️ UI Changes:** AWS constantly updates UI, so expect it to look different over time

### Interface Elements

**Top Navigation:**
- **Services** dropdown - Access all AWS services
- **Search** (Alt+S hotkey) - Search services and features
- **Region selector** - Critical! Shows current region
- **Account dropdown** - Shows account ID, billing, security credentials
- **Cloud Shell** icon - Launch terminal in browser
- **Bell icon** - Notifications/Personal Health Dashboard

**Service Consoles:**
Each service has its own console (e.g., "EC2 Console", "S3 Console", "VPC Console")

### Account ID

**12-digit number** uniquely identifying your AWS account

**Where to find it:**
- Top right account dropdown
- IAM dashboard (right side)

**Uses:**
- Logging in with non-root users
- Cross-account roles (specifying which account can access resources)
- Cross-account policies
- Support cases
- Part of ARNs (Amazon Resource Names)

**Security:** Keep it semi-private (not as sensitive as credentials, but don't broadcast it)

---

## 26. AWS TOOLS FOR POWERSHELL

### What is PowerShell?

Task automation and configuration management framework - a command-line shell and scripting language.

**Platform:** Windows (big blue window)

**Unique:** Built on .NET Common Language Runtime (CLR) - accepts/returns .NET objects (not just text)

### AWS Tools for PowerShell

Lets you interact with AWS API via PowerShell cmdlets (commandlets).

**Cmdlet Format:** Capitalized Verb-Noun
- Example: `New-S3Bucket`

### Alternative to AWS CLI

- **AWS CLI:** For Bash/Linux shells
- **PowerShell Tools:** For Windows/PowerShell users

**Available in CloudShell:** Just type `pwsh` to switch to PowerShell mode

---

## 27. AMAZON RESOURCE NAMES (ARNs)

### Definition

Uniquely identify AWS resources. Required to specify a resource unambiguously across all of AWS.

### Format Variations

```
arn:partition:service:region:account-id:resource-id
arn:partition:service:region:account-id:resource-type/resource-id
arn:partition:service:region:account-id:resource-type:resource-id
```

### Components

**partition:**
- `aws` - Standard AWS regions
- `aws-cn` - China regions  
- `aws-us-gov` - GovCloud regions

**service:** ec2, s3, iam, rds, lambda, etc.

**region:** us-east-1, eu-west-1, ca-central-1 (empty for global services)

**account-id:** Your 12-digit account ID

**resource-type:** user, instance, bucket, etc.

**resource-id:** Actual name or ID

### Examples

**S3 Bucket (Global Service):**
```
arn:aws:s3:::my-bucket-name
```
- No region (global)
- No account ID (buckets are unique globally)
- Short and simple

**IAM User:**
```
arn:aws:iam::123456789012:user/Bob
```
- No region (IAM is global)
- Has account ID
- Resource type: user

**EC2 Instance:**
```
arn:aws:ec2:us-east-1:123456789012:instance/i-0123456789abcdef
```

**Application Load Balancer:**
```
arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-server/1234567890abcdef
```

### Wildcards in ARNs

ARNs support `*` wildcards for IAM policies:

```
arn:aws:s3:::my-bucket/*  (all objects in bucket)
arn:aws:iam::*:user/*     (all users in any account)
```

### Where You See ARNs

- S3 bucket properties
- EC2 instance details
- IAM policies (specifying which resources policy applies to)
- Cross-account access
- Support tickets
- CloudFormation templates
- Anywhere you need to reference a specific resource

**Pro Tip:** Many AWS console pages have a copy button for ARNs

---

## 28. AWS COMMAND LINE INTERFACE (CLI)

### Key Definitions

**CLI:** Command Line Interface - processes commands as lines of text

**Terminal:** Text-only input/output environment

**Console:** Physical computer to input information into terminal

**Shell:** Command line program users interact with
- Popular shells: Bash, Zsh, PowerShell, MS-DOS

**Note:** People use terminal/shell/console interchangeably (technically different, but don't worry about it)

### What is AWS CLI?

Programmatically interact with AWS API by entering commands into a shell.

### Installation

**Requirement:** Python (AWS CLI is a Python executable)

**Platforms:** Windows, Mac, Linux, Unix

**Program name:** `aws`

### Getting Started - CloudShell (Easiest)

1. Click CloudShell icon in top right of AWS Console
2. Waits a moment to load environment
3. Credentials automatically loaded
4. Start using `aws` commands

**⚠️ LIMITATION:** Only available in certain regions. If you don't see it, switch to us-east-1.

### Manual Installation (Linux Example)

```bash
# Download
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# Unzip
unzip awscliv2.zip

# Install
sudo ./aws/install

# Verify
aws --version
```

### Configuration

**Configure credentials:**
```bash
aws configure
```

Prompts for:
1. AWS Access Key ID
2. AWS Secret Access Key
3. Default region (e.g., us-east-1)
4. Default output format (json, table, text)

**Where credentials are stored:**
- `~/.aws/credentials` - Access keys
- `~/.aws/config` - Default settings

### Example Commands

**List S3 buckets:**
```bash
aws s3 ls
```

**Copy file to S3:**
```bash
aws s3 cp hello.txt s3://my-bucket-name/hello.txt
```

**Copy file from S3:**
```bash
aws s3 cp s3://my-bucket-name/hello.txt hello.txt
```

**Describe EC2 instances:**
```bash
aws ec2 describe-instances
```

### Multiple Profiles

Can set up multiple AWS accounts:

**~/.aws/credentials:**
```
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

[exampro]
aws_access_key_id = AKIAI44QH8DHBEXAMPLE
aws_secret_access_key = je7MtGbClwBF/2Zp9Utk/h3yCo8nvbEXAMPLEKEY
```

**Use specific profile:**
```bash
aws s3 ls --profile exampro
```

### Finding Commands

**Documentation:** Search "AWS CLI [service] commands"

Example: aws.amazon.com/cli/latest/reference/s3/

**Structure:**
```bash
aws [service] [command] [options]
```

**Help:**
```bash
aws s3 help
aws s3 cp help
```

---

## 29. AWS SOFTWARE DEVELOPMENT KIT (SDK)

### What is an SDK?

**Software Development Kit** - Collection of software development tools in one installable package.

### What is AWS SDK?

Programmatically create, modify, delete, or interact with AWS resources.

**Available Languages:**
- Java
- Python
- Node.js
- Ruby
- Go
- .NET
- PHP
- JavaScript
- C++

### Example (Ruby)

```ruby
require 'aws-sdk-s3'

s3 = Aws::S3::Client.new(region: 'us-east-1')

response = s3.list_buckets
response.buckets.each do |bucket|
  puts bucket.name
end
```

### AWS Cloud9 IDE

**Managed cloud IDE** for writing/running/debugging code.

**Features:**
- Browser-based
- Pre-configured for AWS development
- Credentials automatically loaded
- Can run on EC2 instance

**Setup:**
1. Go to Cloud9 service
2. Create environment
3. Choose instance size (t2.micro for free tier)
4. Choose Amazon Linux 2
5. Auto-hibernates after 30 minutes

### SDK Documentation Structure

**For each language:**
1. **Getting Started Guide** - Installation, setup
2. **Developer Guide** - How to use SDK
3. **API Reference** - All available operations

**Navigation:**
1. Find your service (e.g., S3)
2. Look for Client class
3. Find operation you want (e.g., list_buckets)
4. See code example

### General Workflow

1. Create a client for the service
2. Call operations on that client
3. Handle response (usually JSON/object)

**Pro Tip:** Most cloud coding is copy-paste from documentation + minor tweaks. Not writing complex algorithms.

### Installing Dependencies

**Ruby example (Gemfile):**
```ruby
source 'https://rubygems.org'
gem 'aws-sdk-s3'
```

Then: `bundle install`

**Python example:**
```bash
pip install boto3 --break-system-packages
```

**Node.js example:**
```bash
npm install aws-sdk
```

### Environment Variables for Credentials

**Standard AWS environment variables:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN` (for temporary credentials)
- `AWS_DEFAULT_REGION`

**Setting in Linux/Mac:**
```bash
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
export AWS_DEFAULT_REGION=us-east-1
```

---

## KEY TAKEAWAYS & EXAM TIPS

### Critical Facts to Remember

1. **US-EAST-1 is the most important region**
   - First region
   - New services launch here first
   - Billing appears here
   - Some services only work here

2. **Minimum 3 AZs per region** (best practice)
   - Each AZ is independent failure zone
   - Within 100km of each other
   - Low-latency network between them

3. **High Availability = Multi-AZ deployment**
   - At least 2-3 AZs
   - Use Elastic Load Balancer

4. **Scalability vs Elasticity**
   - Scalability = you manually scale up/down
   - Elasticity = automatic scaling in both directions

5. **RPO vs RTO**
   - RPO = Data loss tolerance (time)
   - RTO = Downtime tolerance (time)

6. **DR Options** (cold to hot):
   - Backup & Restore (hours)
   - Pilot Light (~10 min)
   - Warm Standby (minutes)
   - Multi-Site Active-Active (real-time)

7. **ARN Format:**
   - `arn:partition:service:region:account-id:resource`
   - Global services (S3, IAM) omit region

8. **Account ID:**
   - 12 digits
   - Used for cross-account access
   - Keep semi-private

9. **Regional vs Global Services:**
   - Regional: EC2, RDS (choose region in console)
   - Global: S3, CloudFront, Route 53, IAM

10. **AWS China is completely separate from AWS Global**

### Common Pitfalls

❌ Assuming all regions have all services
✅ Check service availability per region

❌ Thinking "high availability" = just having 2 servers
✅ Must be in multiple AZs with load balancing

❌ Confusing scalability with elasticity  
✅ Elasticity = automatic; Scalability = manual

❌ Thinking Direct Connect is automatically secure
✅ Use VPN over Direct Connect for encryption

❌ Assuming AZ names are consistent across accounts
✅ Use AZ IDs for cross-account coordination (old accounts)

---

## STUDY QUESTIONS

Test yourself:

1. What are the six original advantages of cloud computing?
2. Why is us-east-1 the most important AWS region?
3. What's the difference between a Region and an Availability Zone?
4. How far apart are AZs within a region?
5. What is an AZ ID and why does it exist?
6. Define: High Availability, Scalability, Elasticity, Fault Tolerance
7. What's the difference between RPO and RTO?
8. List the 4 disaster recovery options from coldest to hottest
9. What are the components of an ARN?
10. What's the difference between AWS China and AWS Global?

---

*Notes compiled: February 3, 2026*
*All information verified against current AWS documentation where possible*
*Course source: FreeCodeCamp AWS Cloud Practitioner by Andrew Brown*

