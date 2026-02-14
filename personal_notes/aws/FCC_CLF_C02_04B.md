# AWS Certified Cloud Practitioner (CLF-C02) - Study Notes
## Part 3 - Hour 2: IAM Deep Dive, Organizations, and Container Services

---

## Table of Contents
- [AWS IAM (Identity and Access Management)](#aws-iam-identity-and-access-management)
- [IAM Policies Deep Dive](#iam-policies-deep-dive)
- [IAM Policies Follow-Along](#iam-policies-follow-along)
- [Principle of Least Privilege](#principle-of-least-privilege)
- [AWS Root User](#aws-root-user)
- [AWS Single Sign-On (SSO)](#aws-single-sign-on-sso)
- [Application Integration](#application-integration)
- [Virtual Machines vs Containers](#virtual-machines-vs-containers)
- [Microservices Architecture](#microservices-architecture)
- [Kubernetes (K8s)](#kubernetes-k8s)
- [Docker](#docker)
- [Podman](#podman)
- [AWS Container Services](#aws-container-services)
- [AWS Organizations](#aws-organizations)
- [AWS Control Tower](#aws-control-tower)
- [AWS Config](#aws-config)

---

## AWS IAM (Identity and Access Management)

### What is IAM?
- Service to **create and manage AWS users and groups**
- Control **permissions** to allow/deny access to AWS resources
- **Free service** - no additional cost
- **Global service** - not region-specific

### Core IAM Components

#### 1. IAM Policies
- **JSON documents** that grant permissions
- Define which API actions are allowed/denied
- Attached to identities (users, groups, roles)

#### 2. IAM Permissions
- Individual **API actions** that can be performed
- Represented in policy documents
- Example: `s3:GetObject`, `ec2:StartInstances`

#### 3. IAM Users
- **End users** who interact with AWS
- Can log into AWS Console
- Can use programmatic access (CLI, SDK)
- Each user has own credentials

#### 4. IAM Groups
- **Collection of users** with same permission levels
- Example groups:
  - Administrators
  - Developers
  - Auditors
  - Data Scientists
- Users inherit group permissions

#### 5. IAM Roles
- **Grant AWS resources** permissions to AWS services
- NOT for people - for services/resources
- Example: EC2 instance needs to access S3
- Attach role (not policy) to EC2
- Role contains policies

### Key Distinction: Policies vs Roles
- **Policies** → Attach to **users and groups**
- **Roles** → Attach to **AWS resources** (EC2, Lambda, etc.)
- Roles contain policies, but you don't attach policies directly to resources

---

## IAM Policies Deep Dive

### Policy Document Structure
IAM policies written in **JSON format**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "StatementLabel",
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:user/Barkley"
      },
      "Condition": {
        "StringLike": {
          "iam:AWSServiceName": ["rds.amazonaws.com"]
        }
      }
    }
  ]
}
```

### Policy Elements Explained

#### Version
- **Policy language version**
- Current version: `"2012-10-17"`
- Hasn't changed in years
- Unlikely to change

#### Statement
- **Array of policy rules**
- Can have **multiple statements**
- Each statement is a separate permission rule

#### Sid (Statement ID)
- **Optional label** for statement
- Useful for:
  - Documentation
  - Referencing specific statements
  - Visualization in console
- Not required for policy to work

#### Effect
- Either **"Allow"** or **"Deny"**
- Determines if action is permitted
- Explicit deny always wins

#### Action
- **AWS service API action(s)**
- Format: `service:Action`
- Examples:
  - `s3:*` - All S3 actions
  - `s3:GetObject` - Only read objects
  - `iam:CreateServiceLinkedRole` - Specific IAM action
- Can use wildcards (`*`)

#### Resource
- **Which AWS resources** the action applies to
- Specified by **ARN** (Amazon Resource Name)
- Examples:
  - `arn:aws:s3:::my-bucket/*` - All objects in bucket
  - `*` - All resources

#### Principal
- **Who** the policy applies to
- Account, user, role, or federated user
- Format: ARN
- Example: `"AWS": "arn:aws:iam::123456789012:user/Barkley"`
- Only used in resource-based policies

#### Condition
- **Optional constraints** for when policy applies
- Many condition types available
- Examples:
  - `StringLike` - Pattern matching
  - `IpAddress` - Source IP restriction
  - `DateGreaterThan` - Time-based
  - `Bool` - True/false conditions

### Common Condition Examples

#### Time-Based Access
```json
"Condition": {
  "DateGreaterThan": {"aws:CurrentTime": "2025-01-01T00:00:00Z"},
  "DateLessThan": {"aws:CurrentTime": "2025-12-31T23:59:59Z"}
}
```

#### IP-Based Access
```json
"Condition": {
  "IpAddress": {
    "aws:SourceIp": ["192.0.2.0/24", "203.0.113.0/24"]
  }
}
```

#### MFA Requirement
```json
"Condition": {
  "Bool": {"aws:MultiFactorAuthPresent": "true"}
}
```

#### Service Name Restriction
```json
"Condition": {
  "StringLike": {
    "iam:AWSServiceName": ["rds.amazonaws.com", "elasticache.amazonaws.com"]
  }
}
```

### Important Policy Notes
- **Rarely write policies by hand** - Use AWS Policy Generator
- **Always test policies** before applying to production
- **Explicit Deny always wins** over Allow
- If not confident about statement, **don't include it**
- **Never invent attributions** - use actual ARNs

---

## IAM Policies Follow-Along

### Lab Overview
**Goal:** Create policy that gives EC2 instance access to specific S3 bucket only

### Step 1: Create S3 Bucket
1. Navigate to **S3**
2. Click **Create bucket**
3. Name: `policy-tutorial-34141` (use random numbers)
4. Accept defaults
5. Create bucket

### Step 2: Create Folder Structure
1. Click into bucket
2. Create folder: `enterprise-d`
3. Click into folder
4. Upload sample images

### Step 3: Create IAM Policy

#### Using Visual Editor
1. Navigate to **IAM → Policies**
2. Click **Create policy**
3. Select service: **S3**
4. Select actions: **List → List buckets**
5. Resources: **Specific**
6. Add ARN: `arn:aws:s3:::policy-tutorial-34141`
7. Click **Next**
8. Name: `my-bucket-policy`
9. Create policy

#### Important Discovery
The visual editor might not create exact policy needed. May need to refine.

### Step 4: Create IAM Role

1. Navigate to **IAM → Roles**
2. Click **Create role**
3. Trusted entity: **AWS service**
4. Use case: **EC2**
5. Click Next
6. Attach policies:
   - `my-bucket-policy` (custom)
   - `AmazonSSMManagedInstanceCore` (for Session Manager)
7. Role name: `my-ec2-role-for-s3`
8. Create role

### Step 5: Launch EC2 Instance

1. Navigate to **EC2**
2. Launch instance
3. Name: (optional)
4. AMI: **Amazon Linux 2**
5. Instance type: **t2.micro**
6. Key pair: **None** (using Session Manager)
7. **Network settings:**
   - NO SSH port needed
   - No security group rules (Session Manager doesn't need them)
8. **Advanced details:**
   - IAM instance profile: `my-ec2-role-for-s3`
9. Launch instance

### Step 6: Connect to Instance

1. Wait for instance to reach "Running" state
2. Select instance
3. Click **Connect**
4. Choose **Session Manager** tab
5. Click **Connect**

#### If Session Manager Not Available
**Error:** "We weren't able to connect to your instance"

**Common reasons:**
- SSM agent not installed (should be on Amazon Linux 2)
- **IAM instance profile not attached**

**Fix if profile missing:**
1. Stop instance (if needed)
2. Actions → Security → **Modify IAM role**
3. Select `my-ec2-role-for-s3`
4. Save
5. **Reboot instance** (required when attaching first profile)

**Note:** Only need to reboot when attaching profile for first time. Subsequent policy changes don't require reboot.

### Step 7: Switch User and Test

#### Switch to ec2-user
```bash
whoami                    # Shows: ssm-user
sudo su - ec2-user       # Switch to ec2-user
whoami                    # Shows: ec2-user
```

#### Test S3 Access
```bash
aws s3 ls
```

**Expected:** Access denied (need more permissions than just ListBucket)

### Step 8: Debug and Fix Policy

#### Problem Discovery
Need additional permissions beyond `ListBucket`:
- `GetObject` - To read/download files
- Possibly others

#### Fix: Update Policy
1. Go to **IAM → Policies**
2. Find `my-bucket-policy`
3. Edit policy
4. Change to:
   - Actions: **All S3 actions** (`s3:*`)
   - Resources: **All resources** (`*`)
5. Save changes

#### Test Again
```bash
aws s3 ls
```

**Expected:** Success! Bucket list appears

**Important:** Policy changes propagate **immediately** (usually)
- No reboot needed
- May take 1-2 minutes in rare cases

### Step 9: Download from S3

```bash
aws s3 cp s3://policy-tutorial-34141/enterprise-d/data.jpg data.jpg
```

**Result:** File downloaded successfully

### Step 10: Refine Policy (Advanced)

#### Goal: Restrict to specific folder only

Update policy to:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": "arn:aws:s3:::policy-tutorial-34141/enterprise-d/*"
    },
    {
      "Effect": "Deny",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::policy-tutorial-34141/data.jpg"
    }
  ]
}
```

**This policy:**
- ✅ Allows all S3 actions in `enterprise-d/` folder
- ❌ Denies access to `data.jpg` in root

#### Test Deny Rule
```bash
# Should fail
aws s3 cp s3://policy-tutorial-34141/data.jpg data.jpg

# Should work
aws s3 cp s3://policy-tutorial-34141/enterprise-d/data.jpg data.jpg
```

### Step 11: Cleanup

1. **Empty S3 bucket:**
   - Select all objects
   - Delete
   - Type "permanently delete"

2. **Delete S3 bucket:**
   - Actions → Delete bucket
   - Type bucket name to confirm

3. **Terminate EC2 instance:**
   - Select instance
   - Instance state → Terminate

4. **Delete IAM resources:**
   - Delete role: `my-ec2-role-for-s3`
   - Delete policy: `my-bucket-policy`

### Key Lessons Learned

1. **Visual editor limitations** - Sometimes need to edit JSON directly
2. **Testing is critical** - Policies may not work as expected first time
3. **Multiple permissions needed** - `ListBucket` alone isn't enough
4. **No reboot for policy changes** - Only when first attaching profile
5. **Explicit Deny wins** - Deny always overrides Allow
6. **ARNs are specific** - Wildcards (`*`) for flexibility

---

## Principle of Least Privilege (PoLP)

### Definition
**Provide minimum permissions necessary** to perform a task

### Two Dimensions

#### 1. Just Enough Access (JEA)
- Permit only **exact actions** needed
- Example: If user only needs to read S3, don't give write permissions
- **Scope:** What actions are allowed

#### 2. Just-in-Time (JIT)
- Permit access for **smallest time duration** needed
- **Short-lived credentials** vs long-lived
- **Scope:** How long access is granted

### Traditional Focus: JEA
Most organizations focus on "what" permissions:
- Define role-based access
- Grant minimum necessary actions
- Standard practice

### Modern Focus: JIT
Growing emphasis on time-based access:
- **Long-lived access keys** = security risk
- **Short-lived tokens** = better security
- Temporary credentials expire automatically

### Risk-Based Adaptive Policies (Most Advanced)

#### What Are They?
**Dynamically adjust permissions based on risk score**

#### Risk Factors
Each access attempt generates risk score based on:
- 📱 **Device type** - Managed vs personal device
- 👤 **User behavior** - Normal vs anomalous
- 📍 **Location** - Expected vs unusual
- 🌐 **IP address** - Known vs unknown
- 🔐 **MFA used** - Yes/no, type used
- ⏰ **Time of day** - Business hours vs night
- 🎯 **Resource accessed** - Sensitivity level
- 📊 **Historical patterns** - Matches typical behavior?

#### Example Policy Logic
```
IF risk_score > 0.8:
    DENY access
ELIF risk_score > 0.5:
    ALLOW read-only, non-sensitive data only
ELIF risk_score < 0.3:
    ALLOW full access
```

### Risk-Based Policies on AWS

#### AWS Native Limitations
**AWS IAM does NOT have built-in risk-based adaptive policies**

**What AWS has:**
- IAM Conditions (manual rules)
- Can restrict by IP, time, MFA presence
- **Not intelligent** - doesn't calculate risk
- **Not adaptive** - doesn't learn from behavior

**AWS Cognito has it:**
- **Adaptive Authentication** in User Pools
- But only for end-user authentication
- Not for AWS resource access (that's Identity Pools)

#### Third-Party Solutions Required
For true risk-based adaptive policies, use:
- Azure Active Directory
- Okta
- Auth0
- Google BeyondCorp

### Just-in-Time Access Tools

#### Console.me (Netflix Open Source)
**Features:**
- Self-service temporary permissions
- Request access through wizard
- Automated approval/denial
- Time-limited credentials
- Enforces both JEA and JIT

**Benefits:**
- ✅ Users don't need to ask admins
- ✅ Automatic expiration
- ✅ Audit trail
- ✅ No permanent over-privileging

#### How It Works
1. User requests specific permissions
2. System evaluates based on rules
3. Grants temporary access (e.g., 2 hours)
4. Credentials automatically expire
5. Must request again if needed

---

## AWS Root User

### Understanding AWS Account Types

#### 1. AWS Account
- The **billing container**
- Holds all AWS resources
- Created when you sign up for AWS
- Not the same as a user

#### 2. Root User
- **Special user** created with AWS Account
- Has **complete, unrestricted access**
- Cannot be deleted
- Cannot have permissions limited (within account)

#### 3. IAM User
- **Regular user** for daily tasks
- Created within AWS Account
- Can be assigned permissions
- Can be deleted

### Root User Confusion
People often say "account" but mean different things:
- "Log into your account" → Usually means root user or IAM user
- "Create an AWS account" → Means AWS Account (billing entity)

**Context matters!**

### Root User Characteristics

#### Login Credentials
- **Email address** (not username)
- **Password**
- Different from IAM users who use:
  - Account ID or alias
  - Username
  - Password

#### Permissions
- ✅ **Full access** to everything
- ❌ **Cannot be limited** by IAM policies
- ❌ **Cannot be deleted**
- ⚠️ Can be limited by **Service Control Policies (SCPs)** in AWS Organizations

#### Important Facts
- **One root user per AWS account** (only one)
- Intended for **specialized tasks only**
- **Not for daily use**
- **Should not use access keys** (create them, but don't use them)
- **Must enable MFA** - AWS will constantly remind you

### Tasks That Require Root User

#### ⚠️ EXAM CRITICAL - Memorize These

**Account Management:**
1. ✅ **Change account settings**
   - Account name
   - Email address
   - Root user password
   - Root user access keys

**Billing & Tax:**
2. ✅ **View certain tax invoices**
3. ✅ **Activate IAM access to Billing console**
4. ✅ **Change/cancel AWS Support plan**

**IAM Recovery:**
5. ✅ **Restore IAM user permissions**
   - If admin accidentally revokes own permissions
   - Only root can restore

**Organizations:**
6. ✅ **Create AWS Organization** (not in official docs, but true)

**Account Management:**
7. ✅ **Close AWS account**

**Specialized Services:**
8. ✅ **Sign up for AWS GovCloud**
9. ✅ **Register as seller in Reserved Instance Marketplace**

**S3 Security:**
10. ✅ **Enable MFA Delete on S3 buckets**
11. ✅ **Edit/delete S3 bucket policy with invalid VPC ID/endpoint**

### Tasks That DON'T Require Root

**These do NOT need root user:**
- ❌ Change contact information
- ❌ Change payment currency preferences
- ❌ Manage AWS regions
- ❌ Regular resource creation/management
- ❌ Daily administrative tasks

### Root User Best Practices

#### Essential Security Measures
1. ✅ **Enable MFA immediately**
   - Use hardware key (YubiKey) if possible
   - At minimum use virtual MFA

2. ✅ **Never use for daily tasks**
   - Create IAM admin user instead
   - Use that for regular work

3. ✅ **Never create/use access keys**
   - If they exist, delete them
   - Too risky if compromised

4. ✅ **Use strong, unique password**
   - Different from all other accounts
   - Store in password manager

5. ✅ **Limit access**
   - Only for required tasks from list above
   - Log out immediately after

#### Emergency Access
**Keep root credentials secure but accessible:**
- Store in secure password manager
- Document location for emergencies
- Don't lose access completely

---

## AWS Single Sign-On (SSO)

### Official Name Change
- Previously: **AWS Single Sign-On (SSO)**
- Now: **AWS IAM Identity Center**
- Same service, just renamed
- Exam may still use "AWS SSO"

### What is AWS SSO?

**Centrally manage access to:**
- Multiple AWS accounts
- Business applications (SaaS)
- SAML-enabled applications
- Custom applications

**Through single sign-on experience**

### How It Works

#### 1. Choose Identity Source

**Option A: AWS SSO Identity Store**
- Built-in user directory
- Create users directly in SSO
- Simple but limited

**Option B: Active Directory**
- On-premise AD via AD Connector
- Or AWS Managed Microsoft AD
- Sync existing corporate users

**Option C: External IdP**
- SAML 2.0 compatible
- Azure AD, Okta, OneLogin, etc.
- Most flexible

#### 2. Manage Permissions Centrally
- Define who can access what
- Create permission sets
- Assign to users/groups
- Apply across AWS accounts

#### 3. Access Resources
- **Single sign-on portal**
- Click to access AWS accounts
- Click to access applications
- No repeated logins

### Architecture Example

```
[On-Premise AD] 
       ↓ (AD Trust)
[AWS SSO/IAM Identity Center]
       ↓
    ┌──────────────┬──────────────┬──────────────┐
    ↓              ↓              ↓              ↓
[AWS Accounts] [Office 365] [Salesforce] [Custom Apps]
```

### Benefits

**For Organizations:**
- ✅ Single identity source
- ✅ Centralized access management
- ✅ Works with AWS Organizations
- ✅ MFA enforcement
- ✅ Audit trails

**For Users:**
- ✅ One login for everything
- ✅ No password juggling
- ✅ Quick access to resources
- ✅ Better user experience

### Use Cases

**Perfect for:**
- Multi-account AWS environments
- Organizations using AWS Organizations
- Companies with existing Active Directory
- Need to access mix of AWS and SaaS apps

**Example:**
- Employee logs into corporate AD
- Automatically gets access to:
  - Production AWS account (read-only)
  - Development AWS account (admin)
  - Salesforce
  - Office 365
  - Custom internal apps

---

## Application Integration

### What is Application Integration?

**Process of enabling independent applications to:**
- Communicate with each other
- Share data
- Work together

**Usually facilitated by intermediate system**

### Why Application Integration?

**Cloud workloads best practice:**
- ✅ **Loosely coupled** systems
- ✅ **Independent services**
- ✅ **Scalable components**
- ✅ **Fault isolation**

**Avoid:**
- ❌ Tightly coupled monoliths
- ❌ Direct dependencies
- ❌ Single points of failure

### Common Integration Patterns

AWS has services for each pattern:

1. **Queuing** - Simple Queue Service (SQS)
2. **Streaming** - Kinesis
3. **Pub/Sub** - Simple Notification Service (SNS)
4. **API Gateway** - Amazon API Gateway
5. **State Machines** - AWS Step Functions
6. **Event Bus** - Amazon EventBridge
7. **Message Broker** - Amazon MQ

---

### Queuing (SQS)

#### What is Queuing?

**Messaging system characteristics:**
- Messages **deleted after consumption**
- Simple communication
- **Not real-time** - must poll for messages
- **Not reactive** - consumers pull messages
- Asynchronous processing

**Analogy:** People queuing in line at a bank

#### Amazon SQS (Simple Queue Service)

**Fully managed queue service:**
- Decouple microservices
- Scale distributed systems
- Enable serverless applications

**How it works:**
```
[Producer] → [SQS Queue] → [Consumer]
```

**Common use case:**
```
[Web App] → [SQS] → [Email Worker]
   ↓
User signs up
   ↓
Queue welcome email
   ↓
Background worker sends email
```

#### Why Use Queues?

**Without queue:**
- Sending email blocks web request
- Slow user experience
- Can overwhelm application

**With queue:**
- Web app responds immediately
- Email sent in background
- Better user experience
- Scalable processing

#### SQS Key Features
- **Durability**: Messages stored redundantly
- **Scalability**: Handles unlimited messages
- **Retention**: Messages kept 1-14 days
- **Visibility timeout**: Prevents duplicate processing
- **Dead-letter queue**: Handle failed messages

---

### Streaming (Kinesis)

#### What is Streaming?

**Different from queuing:**
- Multiple **consumers can react** to same events
- Events **persist for long periods**
- **Real-time** processing
- **Complex operations** possible
- Used for analytics and monitoring

**Analogy:** Live video stream - multiple viewers can watch simultaneously

#### Amazon Kinesis

**Fully managed streaming service:**
- Collect data
- Process data
- Analyze data
- Real-time insights

#### Kinesis Architecture

```
[Producers]         [Data Stream]      [Consumers]
   ↓                    ↓                  ↓
EC2 instances  →   [Shard 1]      →   Redshift
Mobile devices →   [Shard 2]      →   DynamoDB
Servers        →   [Shard 3]      →   S3
IoT devices    →   [Shard 4]      →   EMR
```

#### Key Differences from SQS

| Feature | SQS (Queue) | Kinesis (Stream) |
|---------|-------------|------------------|
| **Speed** | Not real-time | Real-time |
| **Consumers** | One consumer | Multiple consumers |
| **Message life** | Deleted after read | Persists 24h-365 days |
| **Use case** | Decoupling tasks | Real-time analytics |
| **Cost** | Lower | Higher |
| **Complexity** | Simple | More complex |

#### When to Use Kinesis
- ✅ Real-time data analytics
- ✅ Log and event data collection
- ✅ IoT device data
- ✅ Clickstream analysis
- ✅ Multiple consumers need same data

---

### Pub/Sub (SNS)

#### What is Pub/Sub?

**Publish-Subscribe pattern:**
- **Publishers** send messages
- Don't send directly to receivers
- Send to **event bus/topic**
- **Subscribers** subscribe to topics
- Messages immediately **pushed** to subscribers

**Key principle:**
- Publishers don't know subscribers
- Subscribers don't pull messages
- Messages automatically pushed

**Analogy:** Magazine subscription - publisher sends to all subscribers automatically

#### Amazon SNS (Simple Notification Service)

**Fully managed pub/sub service:**
- Highly available
- Durable
- Secure
- Decouple microservices
- Distributed systems
- Serverless apps

#### SNS Architecture

```
     [Publishers]
         ↓
[EC2] [Lambda] [CloudWatch] [S3]
         ↓
    [SNS Topic]
         ↓
  ┌──────┼──────┐
  ↓      ↓      ↓
[Lambda] [SQS] [Email] [HTTP] [SMS]
```

#### SNS Features

**Message delivery to:**
- Lambda functions
- SQS queues
- HTTP/HTTPS endpoints
- Email addresses
- SMS text messages
- Mobile push notifications

**Benefits:**
- Message filtering
- Fan-out pattern
- Topic policies
- Encryption at rest

#### Common Use Cases

**Real-time notifications:**
- Order confirmations
- Account alerts
- System monitoring
- Breaking news alerts

**Fan-out pattern:**
```
[Order Placed]
     ↓
 [SNS Topic]
     ↓
  ┌──┴──┐──┐
  ↓     ↓  ↓
[Email] [SMS] [SQS→Inventory System]
```

#### SNS vs SQS vs Kinesis

| Feature | SNS | SQS | Kinesis |
|---------|-----|-----|---------|
| **Pattern** | Pub/Sub | Queue | Stream |
| **Delivery** | Push | Pull | Pull |
| **Consumers** | Multiple | One | Multiple |
| **Persistence** | No | Yes | Yes |
| **Real-time** | Yes | No | Yes |

---

### API Gateway

#### What is an API Gateway?

**Program that sits between:**
- Single entry point (frontend)
- Multiple backends (services)

**Provides:**
- Throttling (rate limiting)
- Logging
- Request/response routing
- Request/response transformation
- Authentication
- Authorization

#### Amazon API Gateway

**Create secure APIs at any scale:**
- RESTful APIs
- WebSocket APIs
- Acts as front door for applications
- Access data, business logic, backend services

#### Architecture Example

```
[Clients]
   ↓
Mobile apps, Web apps, IoT devices
   ↓
[API Gateway]
   ↓
Define routes:
  /users → Lambda function
  /products → RDS database
  /analytics → Kinesis stream
  /legacy → EC2 application
```

#### Key Features

**Request handling:**
- Authentication (API keys, IAM, Cognito)
- Throttling (protect backends)
- Request validation
- Request transformation

**Response handling:**
- Response transformation
- CORS configuration
- Caching

**Monitoring:**
- CloudWatch metrics
- Access logs
- Execution logs

#### Benefits

**Flexibility:**
- Change backend without changing API
- A/B testing
- Blue/green deployments

**Security:**
- Centralized auth
- DDoS protection
- WAF integration

**Scalability:**
- Automatic scaling
- No infrastructure management

#### Common Pattern

**Serverless API:**
```
[Mobile App]
     ↓
[API Gateway]
     ↓
  ┌──┴──┬──┬──┐
  ↓     ↓  ↓  ↓
[Lambda Functions]
     ↓
[DynamoDB]
```

---

### State Machines (Step Functions)

#### What is a State Machine?

**Abstract model that:**
- Decides how states transition
- Based on conditions
- Like a flowchart with logic

**Think:** Visual workflow with decision points

#### AWS Step Functions

**Coordinate multiple AWS services:**
- Into serverless workflows
- Visual interface
- Error handling
- Retries
- Logging

#### Step Functions Architecture

```
[Start]
   ↓
[Lambda: Validate Order]
   ↓
  If valid?
   ├─Yes→[Lambda: Process Payment]
   │         ↓
   │     If success?
   │      ├─Yes→[Lambda: Send Confirmation]
   │      └─No──→[Lambda: Refund]
   │
   └─No─→[Lambda: Send Error Email]
   ↓
[End]
```

#### Key Features

**Built-in capabilities:**
- Sequential steps
- Parallel execution
- Branching logic
- Error handling
- Automatic retries
- Wait states
- Human approvals

**Integrations:**
- Lambda functions
- ECS/Fargate tasks
- DynamoDB
- SNS/SQS
- API Gateway
- Many AWS services

#### Use Cases

**Perfect for:**
- Order processing workflows
- Data processing pipelines
- DevOps automation
- ETL jobs
- Microservice orchestration

**Example: E-commerce order:**
1. Validate order
2. Check inventory
3. Process payment
4. Update database
5. Send confirmation
6. Trigger shipping

Each step is a separate Lambda or service

#### Benefits

**Visual development:**
- See workflow visually
- Easier to understand
- Easier to debug

**Serverless:**
- No servers to manage
- Pay per execution
- Automatic scaling

**Reliable:**
- Built-in error handling
- Automatic retries
- State persistence

---

### Event Bus (EventBridge)

#### What is an Event Bus?

**System that:**
- Receives events from sources
- Routes events to targets
- Based on rules

```
[Event] → [Event Bus] → [Rules] → [Target]
```

#### Amazon EventBridge

**Serverless event bus service:**
- Stream real-time data
- Connect applications
- React to state changes
- Build event-driven architectures

**Formerly:** CloudWatch Events (rebranded and enhanced)

#### EventBridge Architecture

```
[Event Sources]
     ↓
AWS Services → [Event Bus] → [Rules] → [Targets]
SaaS Apps   →               ↓
Custom Apps →            Filter & Route
```

#### Event Bus Types

**1. Default Event Bus**
- Every AWS account has one
- Receives events from AWS services
- CloudWatch Events compatibility

**2. Custom Event Bus**
- Create for your applications
- Scope to your account
- Organize by application/team

**3. Partner Event Bus (SaaS)**
- Receive events from SaaS providers
- Pre-built integrations
- Example: Zendesk, DataDog, PagerDuty

#### EventBridge Components

**Event Sources (Producers):**
- AWS services (automatic)
- Your applications (custom events)
- SaaS partners

**Events:**
- JSON objects
- Contain event data
- Travel through event bus

**Rules:**
- Define event patterns to match
- Filter which events to capture
- Route to targets

**Targets:**
- Lambda functions
- Step Functions
- SQS queues
- SNS topics
- Kinesis streams
- EC2 instances (trigger automation)
- Many more...

#### Example Use Case

**EC2 state change monitoring:**
```
[EC2 Instance State Changes]
     ↓
[EventBridge Rule: "Instance Stopped"]
     ↓
  ┌──┴──┐
  ↓     ↓
[Lambda: [SNS:
 Log to  Alert
 Database] Team]
```

**Scheduled events:**
```
[EventBridge Schedule: Daily at 2 AM]
     ↓
[Lambda: Generate Daily Report]
     ↓
[S3: Store Report]
```

#### Benefits

**Already collecting events:**
- AWS services auto-emit events
- Don't need custom logging
- Just define rules and targets

**Real-time:**
- Events processed immediately
- Fast response times

**Serverless:**
- No infrastructure
- Pay per event
- Auto-scales

---

## Application Integration Services Summary

### Service Comparison

| Service | Pattern | Use Case | Real-time | Complexity |
|---------|---------|----------|-----------|------------|
| **SQS** | Queue | Decouple tasks, background jobs | No | Low |
| **SNS** | Pub/Sub | Notifications, fan-out | Yes | Low |
| **Kinesis** | Streaming | Real-time analytics, IoT | Yes | High |
| **EventBridge** | Event bus | React to state changes | Yes | Medium |
| **Step Functions** | State machine | Workflows, orchestration | No | Medium |
| **API Gateway** | API | Frontend for services | Yes | Medium |
| **Amazon MQ** | Message broker | Apache ActiveMQ workloads | Yes | High |
| **Managed Kafka** | Streaming | Apache Kafka workloads | Yes | High |
| **AppSync** | GraphQL | Query multiple data sources | Yes | Medium |

### When to Use Each

**SQS:** Need simple task queue, background processing
**SNS:** Need to notify multiple subscribers
**Kinesis:** Real-time data analytics, multiple consumers
**EventBridge:** React to AWS service events
**Step Functions:** Complex workflows with branching
**API Gateway:** RESTful or WebSocket APIs
**Amazon MQ:** Migrating ActiveMQ applications
**Managed Kafka:** Migrating Kafka applications
**AppSync:** GraphQL APIs for mobile/web apps

---

## Virtual Machines vs Containers

### Virtual Machines (Traditional)

#### Architecture
```
[Hardware]
    ↓
[Host OS]
    ↓
[Hypervisor]
    ↓
┌────────┬────────┬────────┐
[VM 1]   [VM 2]   [VM 3]
Ubuntu   CentOS   Windows
  ↓        ↓        ↓
Django MongoDB  RabbitMQ
```

#### Characteristics
- Full operating system per VM
- Includes all OS packages
- Guest OS + Libraries + App
- Hypervisor provides virtualization
- Heavy resource usage

#### Challenges
- **Wasted space** - Always some unused capacity
- Need headroom for growth
- Pay for unused resources
- Not efficient resource usage
- Slower to start

### Containers (Modern)

#### Architecture
```
[Hardware]
    ↓
[Host OS]
    ↓
[Container Runtime] (Docker Daemon)
    ↓
┌──────────┬──────────┬──────────┐
[Container1] [Container2] [Container3]
Alpine       Ubuntu       FreeBSD
  ↓            ↓            ↓
Django    MongoDB      RabbitMQ
```

#### Characteristics
- Share host OS kernel
- Lightweight OS (if needed)
- Only necessary libraries
- Isolated from each other
- Efficient resource usage

#### Benefits
- ✅ **Better space usage** - No wasted capacity
- ✅ **Flexible sizing** - Grow/shrink as needed
- ✅ **Isolation** - Apps don't conflict
- ✅ **Fast startup** - Seconds, not minutes
- ✅ **Cost effective** - Pay for what you use (especially with Fargate)

### Key Differences

| Aspect | VMs | Containers |
|--------|-----|------------|
| **Size** | GB | MB |
| **Startup** | Minutes | Seconds |
| **OS** | Full OS | Shared kernel |
| **Isolation** | Hardware | Software |
| **Efficiency** | Lower | Higher |
| **Portability** | Limited | High |

### Container Advantages

**Resource optimization:**
- No unused headroom
- Dynamic allocation
- Better density

**Configuration:**
- Different OS per container
- Different dependencies per app
- No conflicts

**Deployment:**
- Launch many containers fast
- Easy updates
- Rollback capability

---

## Microservices Architecture

### Monolithic Architecture (Traditional)

#### What is a Monolith?
- **One application** responsible for everything
- All functionality **tightly coupled**
- Everything runs on **single server** (or small cluster)

#### Monolith Components
```
[Single Server]
     ↓
Load Balancing
Cache Layer
Database
Marketing Website
Frontend (React/Angular)
Backend API
ORM (Database layer)
Background Jobs
```

**Everything in one place!**

#### Monolith Characteristics
- Single deployment unit
- Shared codebase
- Tightly coupled components
- Scale entire app together
- One programming language/framework usually

#### Monolith Challenges
- ❌ Hard to scale specific components
- ❌ One bug can crash everything
- ❌ Difficult to update
- ❌ Long deployment times
- ❌ Technology lock-in
- ❌ Hard to test in isolation

### Microservices Architecture (Modern)

#### What are Microservices?
- **Multiple apps** each responsible for **one thing**
- Functionality is **isolated and stateless**
- Each service runs **independently**

#### Microservices Breakdown
```
[Load Balancer Service]     [Elastic Load Balancer]
[Cache Service]             [ElastiCache]
[Database Service]          [RDS]
[Marketing Website]         [S3 Static Hosting]
[Frontend]                  [S3 + CloudFront]
[Backend APIs]              [Containers: ECS/EKS]
[ORM Services]              [Containers]
[Background Jobs]           [Lambda Functions]
[Queue Service]             [SQS]
```

**Each component is separate service!**

#### Microservices Characteristics
- Independent deployment
- Separate codebases
- Loosely coupled
- Scale services individually
- Different technologies per service
- Distributed system

#### Microservices Benefits
- ✅ **Scale independently** - Only scale what's needed
- ✅ **Fault isolation** - One service failing doesn't crash all
- ✅ **Technology freedom** - Best tool for each job
- ✅ **Faster deployments** - Deploy one service at a time
- ✅ **Easier testing** - Test services in isolation
- ✅ **Team autonomy** - Teams own services

### Monolith vs Microservices

| Aspect | Monolith | Microservices |
|--------|----------|---------------|
| **Deployment** | All at once | Independent |
| **Scaling** | Scale everything | Scale parts |
| **Failure** | Total failure | Isolated failure |
| **Technology** | One stack | Multiple stacks |
| **Complexity** | Lower initially | Higher overall |
| **Development** | Simpler | More coordination |
| **Best for** | Small teams/apps | Large teams/apps |

### When to Use Microservices

**Good fit:**
- Large applications
- Multiple teams
- Need independent scaling
- Different parts have different requirements
- Long-term flexibility needed

**Not necessary:**
- Small applications
- Small teams
- Simple requirements
- Rapid prototyping
- Tight budget/timeline

### AWS and Microservices

**AWS makes microservices easier:**
- Managed services replace monolith components
- S3 for static sites
- Lambda for functions
- ECS/EKS for containers
- RDS for databases
- ElastiCache for caching
- Application Load Balancer for routing
- API Gateway for APIs

---

## Kubernetes (K8s)

### What is Kubernetes?

**Open-source container orchestration system:**
- Automate deployment
- Automate scaling
- Automate management
- Of containerized applications

**Created by:** Google
**Maintained by:** Cloud Native Computing Foundation (CNCF)

### Why "K8s"?
- **Kubernetes** = K + 8 letters + s
- Abbreviation: **K8s**
- Pronounced: "kates"

**Oddity:** Most people still say "Kubernetes" with the 's' instead of "Kubernete"

### Kubernetes vs Docker

#### Docker
- Run containers on **single host**
- Great for development
- Limited for production scale

#### Kubernetes
- Run containers **distributed across multiple VMs**
- Production-ready
- High availability
- Auto-scaling
- Self-healing

**Key difference:** Scale and distribution

### Kubernetes Architecture

```
[Kubernetes Cluster]
        ↓
[Master Node]
    ↓
┌──────┬──────────┬────────┬───────────┐
Scheduler │ Controller │ etcd │ API Server
          │           │      │
          └───────────┴──────┘
                ↓
        [Worker Nodes]
              ↓
      ┌───────┼───────┐
   [Node 1] [Node 2] [Node 3]
      ↓        ↓        ↓
   [Pods]   [Pods]   [Pods]
      ↓        ↓        ↓
[Containers][Containers][Containers]
```

### Kubernetes Components

#### Master Node
- **Scheduler** - Decides which node runs pods
- **Controller** - Maintains desired state
- **etcd** - Distributed key-value store (configuration)
- **API Server** - Frontend for Kubernetes control plane

#### Worker Nodes
- Run actual containerized applications
- Host pods
- Managed by master

#### Pods
**Unique Kubernetes concept:**
- Group of **one or more containers**
- Share storage and network
- Smallest deployable unit
- Scheduled together

**Example pod:**
```
[Pod]
  ├─ Web server container
  └─ Logging sidecar container
```

### When to Use Kubernetes

#### Ideal for:
✅ **Tens to hundreds of services**
✅ Large microservice architectures
✅ Need multi-cloud portability
✅ Complex orchestration needs
✅ Large engineering teams
✅ Need fine-grained control

#### NOT ideal for:
❌ Simple applications
❌ Small number of services (< 10)
❌ Small teams
❌ Just getting started with containers

**Important:** Don't use K8s just because it's popular. It's complex and has overhead.

### Kubernetes Benefits

**Orchestration:**
- Automatic scheduling
- Load balancing
- Resource optimization

**Self-healing:**
- Restart failed containers
- Replace containers
- Kill unresponsive containers

**Scaling:**
- Horizontal auto-scaling
- Manual scaling
- Based on metrics

**Deployment:**
- Rolling updates
- Rollback capability
- Canary deployments
- Blue/green deployments

**Service discovery:**
- DNS for services
- Environment variables
- Load balancing

### Kubernetes Challenges

**Complexity:**
- Steep learning curve
- Many concepts to learn
- Complex networking
- Security configuration

**Operational overhead:**
- Cluster management
- Upgrades
- Monitoring
- Troubleshooting

**Overkill for small apps:**
- More complexity than needed
- Higher costs
- Longer time to production

---

## Docker

### What is Docker?

**Platform as a service (PaaS):**
- Uses **OS-level virtualization**
- Delivers software in **containers**
- Not just one tool - suite of tools

### Docker History

**Impact:**
- **First popularized** open-source container platform
- Made containers mainstream
- Huge community
- Extensive tutorials
- Broad service integration

**When people think containers → they think Docker**

### Docker Tools Suite

#### 1. Docker CLI
**Command-line interface:**
- Download containers
- Upload containers
- Build containers
- Run containers
- Debug containers

**Common commands:**
```bash
docker pull nginx           # Download image
docker run nginx           # Run container
docker build -t myapp .    # Build image
docker ps                  # List containers
docker logs <container>    # View logs
```

#### 2. Dockerfile
**Configuration file:**
- Defines how to build container
- Step-by-step instructions
- Like a recipe

**Example:**
```dockerfile
FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3
COPY app.py /app/
CMD ["python3", "/app/app.py"]
```

#### 3. Docker Compose
**Tool for multi-container apps:**
- Define multiple containers
- Configure relationships
- Single command to start all

**Example use case:**
- Web app container
- Database container
- Cache container
- All defined in one file

#### 4. Docker Swarm
**Orchestration tool:**
- Manage multi-container deployments
- Clustering
- Load balancing
- Less popular than Kubernetes

#### 5. Docker Hub
**Public container registry:**
- Download community containers
- Publish your containers
- Official images
- Free and paid options

**Like GitHub for containers**

### Open Container Initiative (OCI)

**Docker's legacy:**
- Created **OCI** standards
- Open governance structure
- Industry standards for:
  - Container formats
  - Container runtimes
- Now maintained by **Linux Foundation**

**Impact:**
- Write Dockerfile → Works with other OCI tools
- Not locked into Docker
- Interoperability

### Docker Challenges (Recent)

**Licensing changes:**
- Introduced paid model
- Caused community concern
- Some saw as "bait and switch"
- Open source but commercial licensing

**Result:**
- Alternatives gaining popularity
- Podman growing
- Community fragmentation
- But Docker still dominant

### Docker on AWS

**Not directly offered:**
- AWS doesn't have "Docker as a service"
- But containers are Docker-compatible
- ECS uses Docker images
- EKS uses Docker images
- Fargate uses Docker images

**Docker is the container standard on AWS**

---

## Podman

### What is Podman?

**Container engine:**
- **OCI-compliant** (works with Docker images)
- **Drop-in replacement** for Docker
- Gaining popularity as Docker alternative

### Why Podman Exists

**Response to Docker licensing:**
- Open source
- Community-driven
- No licensing concerns
- Red Hat backed

### Podman vs Docker

#### Key Differences

**1. Daemonless**
- **Docker:** Uses `containerd` daemon (background service)
- **Podman:** No daemon required
- Direct fork model
- More secure (no root daemon)

**2. Pods (Like Kubernetes)**
- **Docker:** No pod concept
- **Podman:** Has pods like Kubernetes
- Group containers together
- Share namespace

**3. Modular Architecture**
- **Docker:** All-in-one tool
- **Podman:** Part of suite
  - **Podman** - Run containers
  - **Buildah** - Build images
  - **Skopeo** - Move images

### Podman Tools

#### Podman
**Run containers:**
```bash
podman run nginx
podman ps
podman stop <container>
```

Commands identical to Docker!

#### Buildah
**Build OCI images:**
- More control than Docker build
- Scriptable
- Doesn't require Dockerfile (but supports it)

#### Skopeo
**Move container images:**
- Copy between registries
- Inspect images
- Delete images from registries
- Sign images

### Podman Advantages

**Security:**
- ✅ Rootless containers
- ✅ No daemon
- ✅ Better isolation

**Compatibility:**
- ✅ Docker command compatible
- ✅ Works with Docker images
- ✅ Kubernetes YAML compatible

**Licensing:**
- ✅ Fully open source
- ✅ No commercial licensing

### Podman and AWS

**Not tested on exam:**
- Won't see Podman questions
- Focus on concepts
- Practical knowledge for real world

**Why mentioned:**
- Docker alternatives exist
- Industry is evolving
- Good to know options

### Should You Use Podman?

**Consider Podman if:**
- ✅ Security conscious
- ✅ Want no daemon
- ✅ Avoid Docker licensing
- ✅ Red Hat ecosystem

**Stick with Docker if:**
- ✅ Team already using Docker
- ✅ Extensive Docker tooling
- ✅ No licensing concerns
- ✅ Want broadest compatibility

**Either works with AWS!**

---

## AWS Container Services

### Overview

AWS offers multiple ways to run containers:

**Primary services (run containers):**
1. ECS - Elastic Container Service
2. Fargate - Serverless containers
3. EKS - Elastic Kubernetes Service
4. Lambda - Serverless functions (supports containers)

**Deployment tools:**
5. Elastic Beanstalk - Platform as a Service
6. App Runner - Fully managed container apps

**Supporting services:**
7. ECR - Elastic Container Registry
8. X-Ray - Distributed tracing
9. Step Functions - Container orchestration

### 1. Amazon ECS (Elastic Container Service)

#### What is ECS?
- **AWS-proprietary** container orchestration
- Run Docker containers on AWS
- Integrated with AWS services

#### ECS Launch Types

**EC2 Launch Type:**
- Containers run on **EC2 instances you manage**
- You provision and manage instances
- You install ECS agent
- **No cold starts** - always running
- **Always paying** for EC2 instances

**Fargate Launch Type:**
- Containers run on **AWS-managed infrastructure**
- Serverless - no EC2 to manage
- Pay only for containers running
- **Has cold starts**
- More expensive per container (but no idle costs)

#### When to Use ECS
- ✅ Want AWS-native solution
- ✅ Don't need Kubernetes
- ✅ Tight AWS integration needed
- ✅ Want simplicity over portability

### 2. AWS Fargate

#### What is Fargate?
- **Serverless compute** for containers
- No EC2 instances to manage
- Pay per second of container runtime
- Works with ECS and EKS

#### Fargate Characteristics

**Serverless:**
- No server management
- No patching
- No cluster optimization

**Scaling:**
- Can scale to zero
- Pay nothing when not running
- Automatic scaling

**Cold starts:**
- Containers take time to start
- Not instant like ECS on EC2
- Similar to Lambda but longer-running

#### When to Use Fargate
- ✅ Want serverless containers
- ✅ Variable workloads
- ✅ Don't want to manage EC2
- ✅ Willing to accept cold starts
- ✅ Want to minimize idle costs

### 3. Amazon EKS (Elastic Kubernetes Service)

#### What is EKS?
- **Managed Kubernetes** service
- Run Kubernetes on AWS
- Certified Kubernetes conformant
- Compatible with standard K8s tools

#### EKS Benefits

**Portability:**
- ✅ Standard Kubernetes
- ✅ Avoid vendor lock-in
- ✅ Multi-cloud capable
- ✅ Hybrid cloud support

**Ecosystem:**
- ✅ Kubernetes tools work
- ✅ Large community
- ✅ Extensive documentation

#### EKS vs ECS

| Feature | EKS | ECS |
|---------|-----|-----|
| **Orchestrator** | Kubernetes | AWS proprietary |
| **Portability** | High | AWS only |
| **Complexity** | Higher | Lower |
| **Cost** | Control plane fees | No extra fees |
| **Learning curve** | Steep | Moderate |
| **Community** | Huge | AWS only |

#### When to Use EKS
- ✅ Need Kubernetes specifically
- ✅ Want portability
- ✅ Large microservice architecture
- ✅ Team knows Kubernetes
- ✅ Multi-cloud strategy

### 4. AWS Lambda

#### Lambda and Containers

**Previously:**
- Only pre-built runtimes (Python, Node.js, Java, etc.)
- Limited customization

**Now:**
- ✅ **Deploy custom container images**
- Up to 10 GB image size
- Use any runtime/dependencies

#### Lambda Characteristics

**Focus:**
- Only think about **code**
- No server management
- Event-driven
- Short-running tasks (15 min max)

**Container support:**
- Build custom container
- Must implement Lambda runtime API
- Deploy to Lambda
- Still scales automatically

#### Lambda vs Fargate

| Feature | Lambda | Fargate |
|---------|--------|---------|
| **Max duration** | 15 minutes | Unlimited |
| **Use case** | Short tasks | Long-running apps |
| **Container size** | 10 GB | 20 GB |
| **Scaling** | Automatic | Automatic |
| **Cold starts** | Faster | Slower |

#### When to Use Lambda
- ✅ Event-driven workloads
- ✅ Short-running functions
- ✅ Need fastest cold starts
- ✅ Simple deployment model

### 5. Elastic Beanstalk

#### What is Elastic Beanstalk?
- **Platform as a Service (PaaS)**
- Deploy apps without thinking about infrastructure
- Supports multiple platforms including containers

#### Beanstalk and Containers

**Can deploy:**
- Single Docker container
- Multi-container Docker (uses ECS)
- Preconfigured Docker platforms

**What it manages:**
- EC2 instances
- Load balancers
- Auto Scaling groups
- ECS clusters (for multi-container)
- Monitoring

#### When to Use Elastic Beanstalk
- ✅ Want simplicity
- ✅ Deploy entire application
- ✅ Don't want to configure infrastructure
- ✅ Quick deployment needed

### 6. AWS App Runner

#### What is App Runner?
- **Fully managed** container app service
- Newest AWS container service
- Simplest way to run containers
- Competes with services like Heroku, Google Cloud Run

#### App Runner Features

**Automatic:**
- Build from source code OR container image
- Deploy automatically
- Scale automatically
- Load balance automatically
- HTTPS automatically

**Managed:**
- Can't see underlying infrastructure
- AWS manages everything
- Just configure your app

#### App Runner vs Elastic Beanstalk

| Feature | App Runner | Elastic Beanstalk |
|---------|------------|-------------------|
| **Transparency** | Black box | See infrastructure |
| **Control** | Minimal | More control |
| **Simplicity** | Highest | High |
| **Flexibility** | Limited | Higher |

#### When to Use App Runner
- ✅ Want simplest deployment
- ✅ Web apps and APIs
- ✅ Don't need infrastructure access
- ✅ Want fast time to market

### 7. AWS Copilot CLI

#### What is Copilot?
- **CLI tool** for containerized apps
- Simplifies deployment to:
  - App Runner
  - ECS
  - Fargate

#### Copilot Features

**Build, release, operate:**
- One command deployments
- Infrastructure as code
- Best practices built-in
- Production-ready setups

**Example:**
```bash
copilot init            # Initialize app
copilot deploy          # Deploy to production
copilot svc status      # Check status
```

#### When to Use Copilot
- ✅ Want CLI-based workflow
- ✅ Don't want to click through console
- ✅ Infrastructure as code
- ✅ Repeatable deployments

### Supporting Services

#### Amazon ECR (Elastic Container Registry)

**What is it:**
- Docker registry for storing container images
- Private by default
- Integrated with IAM

**Features:**
- Image scanning
- Encryption at rest
- Replication
- Lifecycle policies

**Not just for Docker:**
- OCI-compliant
- Any container format

#### AWS X-Ray

**Distributed tracing:**
- Analyze microservices
- Debug distributed apps
- Find performance bottlenecks
- Trace requests across services

**How it works:**
```
[API Gateway] → [Lambda 1] → [Lambda 2] → [DynamoDB]
      ↓            ↓            ↓            ↓
   X-Ray traces entire request path
```

#### AWS Step Functions (with containers)

**Orchestrate containers:**
- ECS tasks
- Lambda functions
- Together in workflows

**Example:**
```
[Start]
  ↓
[Lambda: Validate]
  ↓
[ECS Task: Process]
  ↓
[Lambda: Notify]
  ↓
[End]
```

---

## AWS Organizations

### What is AWS Organizations?

**Centrally manage multiple AWS accounts:**
- Create new accounts
- Manage billing
- Control access
- Enforce compliance
- Share resources

### Core Concepts

#### Root Account (Master Account)
- First account in organization
- Has complete control
- Pays for all accounts
- Cannot be removed
- **Not same as root user!**

#### Organizational Units (OUs)
- **Groups of AWS accounts**
- Create hierarchy
- Can contain:
  - AWS accounts
  - Other OUs (nested)

**Example structure:**
```
[Root Account]
    ↓
[Organization]
    ↓
  ┌─┴─┬──┐
  ↓   ↓  ↓
[OU: Production] [OU: Development] [OU: Testing]
  ↓                ↓                  ↓
[Accounts]      [Accounts]        [Accounts]
```

#### Service Control Policies (SCPs)

**Organization-wide IAM policies:**
- Apply to accounts/OUs
- Set maximum permissions
- Override local permissions
- Centrally enforced

**Example SCP:**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Deny",
    "Action": "*",
    "Resource": "*",
    "Condition": {
      "StringEquals": {
        "aws:RequestedRegion": "ca-central-1"
      }
    }
  }]
}
```
**Result:** No one can use Canada region, even root users

### Organizations Architecture

```
[Organization Root]
        ↓
    [Root Account]
        ↓
   ┌────┴────┬─────────┐
   ↓         ↓         ↓
[OU: IT]  [OU: HR]  [OU: Finance]
   ↓         ↓         ↓
[Dev Acct] [HR Acct] [Finance Acct]
[Prod Acct]
```

### Key Features

#### 1. Consolidated Billing
- One bill for all accounts
- Volume discounts
- Reserved Instance sharing
- Savings Plans sharing

#### 2. Account Creation
- Programmatically create accounts
- Standardized setup
- Pre-configured

#### 3. Access Control
- SCPs for guardrails
- Prevent unauthorized actions
- Enforce compliance

#### 4. Resource Sharing
- Share resources across accounts
- AWS Resource Access Manager
- Example: VPC subnets, Transit Gateway

### Important Notes

**Must be enabled:**
- Organizations not on by default
- Once enabled, cannot be disabled
- Recommended for production workloads

**Account isolation:**
- Best practice: separate accounts for workloads
- Production account
- Development account
- Testing account
- Security account

**Root account vs root user:**
- **Root account** = Master/management account in organization
- **Root user** = Special user in each AWS account
- Different concepts!

---

## AWS Control Tower

### What is Control Tower?

**Automated multi-account setup:**
- Quick setup for AWS Organizations
- Best practices built-in
- Baseline security environment
- Governance at scale

**Purpose:** Enterprise-ready AWS environment in hours, not weeks

### Core Components

#### 1. Landing Zone

**Pre-configured baseline environment:**
- Well-Architected best practices
- Security configurations
- Logging enabled
- Network setup
- Ready for production workloads

**Includes:**
- ✅ **SSO enabled** by default
- ✅ **Centralized logging** (CloudTrail)
- ✅ **Cross-account security auditing**
- ✅ **Network configurations**
- ✅ **Pre-approved regions**

**Analogy:** Like a construction site ready for building - foundation laid, utilities connected

#### 2. Account Factory

**Automated account provisioning:**
- Standardize new account creation
- Pre-approved configurations
- Self-service for teams
- Via AWS Service Catalog

**Formerly called:** Account Vending Machine

**How it works:**
1. Define account template
2. Set network configuration
3. Set region selections
4. Users request accounts via Service Catalog
5. Accounts created automatically
6. Pre-configured and compliant

**Benefits:**
- ✅ Consistent account setup
- ✅ Reduce manual work
- ✅ Enforce standards
- ✅ Empower teams

#### 3. Guardrails

**Pre-packaged governance rules:**
- Security policies
- Operational policies
- Compliance rules
- Apply enterprise-wide or per OU

**Types of guardrails:**

**Preventive:**
- Enforce controls
- Block actions
- Implemented via SCPs
- Example: "Cannot delete CloudTrail logs"

**Detective:**
- Monitor compliance
- Alert on violations
- Implemented via AWS Config
- Example: "Alert if MFA not enabled"

**Levels:**

| Level | Description | Can disable? |
|-------|-------------|--------------|
| **Mandatory** | Required for all | ❌ No |
| **Strongly recommended** | Best practice | ✅ Yes |
| **Elective** | Optional | ✅ Yes |

### Control Tower vs Landing Zone

**AWS Landing Zone (Retired):**
- Previous solution
- Required AWS Professional Services
- Expensive
- Complex setup
- Not self-service

**AWS Control Tower:**
- Replacement for Landing Zone
- Self-service
- Free to use (pay for resources only)
- Automated setup
- Continuous governance

### When to Use Control Tower

**Perfect for:**
- ✅ New AWS deployments
- ✅ Multi-account strategy
- ✅ Need quick setup
- ✅ Want best practices
- ✅ Governance requirements

**Not necessary for:**
- ❌ Single account setups
- ❌ Existing complex Organizations
- ❌ Non-standard requirements

### Control Tower Benefits

**Speed:**
- Days/weeks → Hours
- Automated setup
- No manual configuration

**Best practices:**
- Well-Architected Framework
- Security standards
- Operational excellence

**Governance:**
- Ongoing compliance
- Continuous monitoring
- Automated remediation

**Scalability:**
- Start small, grow
- Add accounts easily
- Maintain standards

---

## AWS Config

### What is AWS Config?

**Compliance as Code framework:**
- Monitor AWS resource configurations
- Enforce desired configurations
- Remediate non-compliant resources
- Track configuration changes

**Purpose:** Automate compliance and change management

### Understanding Prerequisites

#### Change Management
**Formal process to:**
- Monitor changes
- Enforce changes
- Remediate changes

**In cloud context:**
- Configuration drift detection
- Automated compliance checking
- Automatic remediation

#### Compliance as Code (CaC)
**Use programming to:**
- Automate monitoring
- Automate enforcement
- Automate remediation
- Stay compliant with standards

### How AWS Config Works

#### Config Rules

**Define expected state:**
```
Rule: "EC2 instances must be t2.micro"
Current State: Instance is t2.large
Result: Non-compliant
Action: Remediate (stop instance? notify?)
```

**Rules are powered by Lambda functions**

#### Example Scenarios

**Scenario 1: EC2 Instance Type**
```
[Config Rule: "EC2 must be t2.micro"]
     ↓
[EC2 Instance created as t2.large]
     ↓
[Config detects non-compliance]
     ↓
[Lambda remediates: change to t2.micro]
```

**Scenario 2: RDS Encryption**
```
[Config Rule: "RDS must be encrypted"]
     ↓
[RDS instance created unencrypted]
     ↓
[Config detects non-compliance]
     ↓
[Lambda remediates: flag for deletion? notify?]
```

### AWS Config Features

#### 1. Configuration Recording
- Track all resource configurations
- Historical configurations
- Who changed what, when

#### 2. Configuration Snapshots
- Point-in-time view
- Store in S3
- Audit trail

#### 3. Configuration History
- Timeline of changes
- Configuration drift
- Compliance over time

#### 4. Resource Relationships
- Understand dependencies
- Impact analysis
- Security group → EC2 → EBS

#### 5. Compliance Dashboard
- Visual compliance status
- Compliant vs non-compliant
- Trends over time

### Per-Region Service

**Important:** Config is **region-specific**
- Must enable per region
- Rules per region
- Not global like IAM

**Example:**
- Enable in us-east-1
- Enable in eu-west-1
- Separate dashboards
- Separate rules

### When to Use AWS Config

**Use Config when:**
- ✅ "This resource must stay configured this way for compliance"
- ✅ "I want to track all configuration changes"
- ✅ "I need a list of all resources in this region"
- ✅ "I need to analyze security weaknesses"
- ✅ "I need detailed historical configuration data"

**Don't use Config when:**
- ❌ Real-time blocking needed (use SCPs instead)
- ❌ Cross-region enforcement (use SCPs)
- ❌ Simple alerting only (use CloudWatch)

### Config vs Other Services

| Service | Purpose | Scope | Action |
|---------|---------|-------|--------|
| **Config** | Monitor & remediate | Per region | After resource created |
| **SCPs** | Prevent actions | Organization-wide | Before resource created |
| **CloudWatch** | Metrics & logs | Per region | Alert only |
| **CloudTrail** | API audit | Per region/org | Record only |

### Config Rules Examples

**Security:**
- S3 buckets must have encryption
- IAM users must have MFA
- Security groups cannot allow 0.0.0.0/0 on port 22

**Compliance:**
- EC2 instances must have approved AMIs
- Resources must have required tags
- EBS volumes must be encrypted

**Cost optimization:**
- EC2 instances must be specific types
- Unattached EBS volumes deleted
- Unused Elastic IPs released

### Remediation

**Automatic remediation:**
- Config detects non-compliance
- Triggers Lambda function
- Lambda fixes the issue
- Or Lambda notifies team

**Manual remediation:**
- Config detects non-compliance
- Alerts sent
- Team manually fixes
- Config confirms compliance

---

## Key Takeaways - Hour 2

### IAM Deep Dive
- ✅ Policies are JSON documents with Version, Statement, Effect, Action, Resource
- ✅ Conditions enable fine-grained control (IP, time, MFA, etc.)
- ✅ Roles for resources, policies for users/groups
- ✅ Test policies thoroughly before production use
- ✅ Explicit Deny always wins over Allow

### Principle of Least Privilege
- ✅ JEA = Just Enough Access (what permissions)
- ✅ JIT = Just-in-Time (how long)
- ✅ Risk-based adaptive policies most advanced (requires 3rd party)
- ✅ AWS doesn't have intelligent adaptive policies natively

### Root User
- ✅ One per AWS account, cannot be deleted
- ✅ Enable MFA immediately
- ✅ Only use for specific tasks (memorize the list!)
- ✅ Never use for daily work
- ✅ Can be limited by SCPs (not IAM policies)

### Application Integration
- ✅ SQS for queuing (simple, async, pull-based)
- ✅ SNS for pub/sub (push-based, fan-out)
- ✅ Kinesis for streaming (real-time, multiple consumers)
- ✅ EventBridge for event-driven (AWS service events)
- ✅ Step Functions for workflows (state machines)
- ✅ API Gateway for APIs (REST, WebSocket)

### Containers
- ✅ Containers more efficient than VMs
- ✅ Share OS kernel, faster startup
- ✅ Docker industry standard, Podman alternative
- ✅ Kubernetes for large-scale orchestration (10s-100s of services)

### AWS Container Services
- ✅ ECS = AWS-native, simple
- ✅ Fargate = serverless containers
- ✅ EKS = managed Kubernetes
- ✅ Lambda = serverless functions (now supports containers)
- ✅ App Runner = simplest deployment

### Organizations & Governance
- ✅ Organizations manage multiple accounts
- ✅ SCPs enforce organization-wide policies
- ✅ Control Tower for automated setup
- ✅ Config for compliance monitoring

---

## Exam Tips - Hour 2

### Must Remember for Exam

**IAM:**
1. Roles attach to resources, policies attach to users/groups
2. Policy elements: Version, Statement, Effect, Action, Resource, Condition
3. Explicit Deny always overrides Allow

**Root User Tasks (memorize):**
4. Change account settings
5. Restore IAM permissions
6. Close AWS account
7. Enable MFA Delete on S3
8. Create organization
9. View certain tax invoices

**Application Integration:**
10. SQS = queue (delete after read)
11. SNS = pub/sub (push to subscribers)
12. Kinesis = streaming (multiple consumers, real-time)
13. EventBridge = event bus (AWS service events)
14. Step Functions = state machine (workflows)

**Containers:**
15. Kubernetes = for large microservice architectures
16. Pods = unique Kubernetes concept (group of containers)
17. ECS = AWS-native orchestration
18. Fargate = serverless containers
19. EKS = managed Kubernetes

**Organizations:**
20. SCPs can limit root user (only organization-level)
21. Organizations cannot be turned off once enabled
22. Control Tower = automated multi-account setup
23. Config = per-region service for compliance

### Common Exam Scenarios

**"Need to prevent all accounts from using specific region"**
→ Service Control Policy (SCP) in AWS Organizations

**"Track all configuration changes to resources"**
→ AWS Config

**"Set up multi-account AWS environment with best practices"**
→ AWS Control Tower

**"Need immediate notification to multiple subscribers"**
→ Amazon SNS (pub/sub)

**"Queue background jobs for processing"**
→ Amazon SQS

**"Real-time analytics on streaming data"**
→ Amazon Kinesis

**"Orchestrate multi-step workflow with error handling"**
→ AWS Step Functions

**"Run containers without managing servers"**
→ AWS Fargate

**"Need Kubernetes for portability"**
→ Amazon EKS

**"Simplest way to deploy containerized web app"**
→ AWS App Runner

**"Restore accidentally removed admin permissions"**
→ Root user

**"Prevent users from disabling CloudTrail logs"**
→ SCP (organization-level) or Config rule (per-region)

---