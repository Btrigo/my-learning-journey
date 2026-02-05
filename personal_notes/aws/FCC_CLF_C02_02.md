# AWS Certified Cloud Practitioner (CLF-C02) - Study Notes Part 2

**Course:** freeCodeCamp CLF-C02 Certification Course  
**Study Date:** February 4, 2026  
**Video Timestamps:** ~3:30:00 - ~6:00:00  
**Topics Covered:** AWS CLI, CloudShell, ARNs, SDKs, IaC (CloudFormation/CDK), Access Keys, Documentation, Shared Responsibility Model, Computing Services, Edge/Hybrid Computing, HPC

---

## Table of Contents
1. [AWS CLI (Command Line Interface)](#aws-cli)
2. [AWS CloudShell](#aws-cloudshell)
3. [Amazon Resource Names (ARNs)](#arns)
4. [AWS SDKs](#aws-sdks)
5. [Infrastructure as Code (IaC)](#infrastructure-as-code)
6. [AWS Access Keys](#aws-access-keys)
7. [AWS Documentation](#aws-documentation)
8. [Shared Responsibility Model](#shared-responsibility-model)
9. [Computing Services](#computing-services)
10. [Edge and Hybrid Computing](#edge-and-hybrid-computing)
11. [High Performance Computing (HPC)](#high-performance-computing)

---

## AWS CLI (Command Line Interface)

### What is the AWS CLI?

The **AWS Command Line Interface (CLI)** allows you to programmatically interact with AWS services by entering commands into a shell/terminal.

**Key Facts (As of February 2026):**
- **AWS CLI v2** is the current major version (v1 enters maintenance mode July 15, 2026; end-of-support July 15, 2027)
- CLI is a **Python executable** but v2 includes embedded Python (no separate Python installation required)
- The program name is `aws`
- Pre-installed in **AWS CloudShell** with credentials already configured

### CLI Terminology

| Term | Definition |
|------|------------|
| **CLI** | Command Line Interface - processes commands as lines of text |
| **Terminal** | Text-only input/output environment |
| **Console** | Physical computer to input information into terminal |
| **Shell** | Command line program users interact with (bash, zsh, PowerShell, etc.) |

*Note: People commonly use terminal/shell/console interchangeably, though technically different.*

### AWS CLI Version 2 vs Version 1

**AWS CLI v2 Features (Current as of 2026):**
- Embedded Python (no separate install needed)
- Server-side command completion
- Auto-prompt mode (`--cli-auto-prompt`)
- Wizards for guided setup
- AWS SSO integration
- High-level DynamoDB commands (`ddb put`, `ddb select`)
- CloudWatch Logs `tail` command
- Enhanced EC2 Instance Connect
- YAML output support
- `aws configure import` for CSV credentials

**Installation:**
```bash
# Linux example
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**Check Version:**
```bash
aws --version
# Example output: aws-cli/2.27.41 Python/3.11.6 Linux/... botocore/...
```

### Basic CLI Commands

**S3 Examples:**
```bash
# List S3 buckets
aws s3 ls

# Create bucket
aws s3 mb s3://my-bucket-name

# Copy file to S3
aws s3 cp local-file.txt s3://my-bucket/

# Copy file from S3
aws s3 cp s3://my-bucket/file.txt ./

# List objects in bucket
aws s3 ls s3://my-bucket/
```

**EC2 Examples:**
```bash
# Describe EC2 instances
aws ec2 describe-instances

# Describe instances with table output
aws ec2 describe-instances --output table
```

### Configuration

**AWS CLI Credentials Location:**
```bash
~/.aws/credentials  # Access keys stored here
~/.aws/config       # Default configuration (region, output format)
```

**Configure CLI:**
```bash
aws configure
# Prompts for:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region (e.g., us-east-1)
# - Default output format (json, table, yaml, text)
```

**Multiple Profiles:**
```
# In ~/.aws/credentials
[default]
aws_access_key_id = YOUR_KEY
aws_secret_access_key = YOUR_SECRET

[profile-name]
aws_access_key_id = ANOTHER_KEY
aws_secret_access_key = ANOTHER_SECRET
```

**Use specific profile:**
```bash
aws s3 ls --profile profile-name
```

**Environment Variables:**
```bash
# Set credentials via environment variables (most secure for code)
export AWS_ACCESS_KEY_ID=YOUR_KEY
export AWS_SECRET_ACCESS_KEY=YOUR_SECRET
export AWS_DEFAULT_REGION=us-east-1

# Or use AWS_REGION (v2) which overrides AWS_DEFAULT_REGION
export AWS_REGION=us-west-2
```

### CLI Command Structure

```bash
aws <service> <command> [options]
```

Example:
```bash
aws s3 cp file.txt s3://bucket-name/ --region us-west-2
```

### Finding CLI Commands

**AWS CLI Command Reference:** https://docs.aws.amazon.com/cli/

Navigate to specific service, then view available commands and examples.

---

## AWS CloudShell

### What is AWS CloudShell?

**AWS CloudShell** is a browser-based shell environment with AWS CLI pre-installed and pre-authenticated.

**Key Features (Current as of February 2026):**
- **Location:** Top-right corner of AWS Console (shell icon)
- **Compute Environment:** Amazon Linux 2023
- **Pre-installed tools:** AWS CLI v2, Python, Node.js, Git, Make, pip, sudo, tar, tmux, vim, wget, zip
- **Shells available:** Bash (default), PowerShell (`pwsh`), Zsh (`zsh`)
- **No cost:** Free service (you pay for resources you create)
- **Pre-authenticated:** Uses your AWS Management Console credentials automatically

### Storage in CloudShell

**Persistent Storage:**
- **Location:** `$HOME` directory (`/home/cloudshell-user`)
- **Size:** 1 GB per AWS Region
- **Scope:** Private to you, per-region (isolated)
- **Retention:** Up to 120 days of inactivity (resets when you launch CloudShell in that region)
- **Cost:** Free

**Temporary Storage:**
- **Location:** Any directory outside `$HOME`
- **Lifespan:** Deleted when session ends
- **Use:** For temporary files only

**Important Notes:**
- Storage is **NOT** EFS, S3, or EBS - it's AWS-managed CloudShell-specific storage
- **Cannot be expanded beyond 1 GB** - use S3 for larger storage needs
- **Not synchronized across regions** - us-east-1 storage ≠ us-west-2 storage
- **CloudShell VPC environments do NOT have persistent storage** - $HOME deleted after timeout/restart

**Check Storage Usage:**
```bash
df -h $HOME
```

**Example output:**
```
Filesystem      Size  Used Avail Use% Mounted on
overlay         974M  164K  907M   1% /home/cloudshell-user
```

### Session Limits

**Inactive Session Timeout:**
- **20-30 minutes** of no keyboard/pointer interaction = session ends
- Running processes don't count as interaction

**Long-Running Session Timeout:**
- **~12 hours** even with continuous interaction = session ends

### Switching Shells in CloudShell

```bash
# Switch to PowerShell
pwsh

# Switch to Zsh
zsh

# Return to Bash
bash
```

### CloudShell Availability

**Not available in all regions.** Check supported regions in AWS Console.

Example supported regions: us-east-1, us-west-2, eu-west-1, ap-southeast-1, etc.

### Using CloudShell

**Upload File:**
- Actions menu → Upload file
- Max size: 1 GB
- Files uploaded to `$HOME` persist

**Download File:**
- Actions menu → Download file
- Enter file path

**Create Script Example:**
```bash
# Using vim
vi script.sh

# Enter INSERT mode: press 'i'
# Type your script
#!/bin/bash
sleep 30
echo "Hello World from $(hostname)"

# Exit INSERT mode: press 'Esc'
# Save and quit: type ':wq' and press Enter

# Make executable
chmod +x script.sh

# Run
./script.sh
```

### Persisting Custom Tools

Install tools to `~/bin/` for persistence:

```bash
# Create bin directory
mkdir -p ~/bin

# Add to PATH (add to ~/.bashrc for permanence)
export PATH="$HOME/bin:$PATH"

# Install Python packages locally
pip3 install --user boto3

# Custom scripts in ~/bin/ persist across sessions
```

---

## Amazon Resource Names (ARNs)

### What is an ARN?

An **Amazon Resource Name (ARN)** uniquely identifies AWS resources across all of AWS.

**When ARNs are used:**
- IAM policies (specifying which resources to grant access to)
- API calls (referencing specific resources)
- Cross-service references (Lambda accessing S3)

### ARN Format

**General structure:**
```
arn:partition:service:region:account-id:resource-id
arn:partition:service:region:account-id:resource-type/resource-id
arn:partition:service:region:account-id:resource-type:resource-id
```

**Components:**
- **partition:** `aws` (standard), `aws-cn` (China), `aws-us-gov` (GovCloud)
- **service:** ec2, s3, iam, lambda, etc.
- **region:** us-east-1, eu-west-1, etc. (empty for global services)
- **account-id:** 12-digit AWS account number
- **resource-type/resource-id:** Varies by service

### ARN Examples

**S3 Bucket (Global Service - no region/account in ARN):**
```
arn:aws:s3:::my-bucket-name
arn:aws:s3:::my-bucket-name/object-key.txt
```

**EC2 Instance:**
```
arn:aws:ec2:us-east-1:123456789012:instance/i-0abc123def456789
```

**IAM User:**
```
arn:aws:iam::123456789012:user/Bob
```

**Load Balancer:**
```
arn:aws:elasticloadbalancing:us-west-2:123456789012:loadbalancer/app/my-lb/50dc6c495c0c9188
```

**Lambda Function:**
```
arn:aws:lambda:us-east-1:123456789012:function:my-function
```

### Wildcards in ARNs

ARNs support wildcards (`*`) in IAM policies:

```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::my-bucket/*"
}
```

This allows access to all objects in `my-bucket`.

### Finding ARNs

**In AWS Console:**
- Most resources display ARN in properties/details
- Often copyable via copy button

**Example locations:**
- S3: Bucket properties
- EC2: Instance details
- Lambda: Function configuration
- IAM: User/role summary

### Using ARNs in IAM Policies

**Example Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

This policy allows putting objects into the specified S3 bucket.

---

## AWS SDKs (Software Development Kits)

### What is an AWS SDK?

An **SDK** is a collection of software development tools in one installable package, allowing you to programmatically create, modify, delete, or interact with AWS resources using code.

### Available SDKs (As of 2026)

- **Java**
- **Python** (Boto3)
- **.NET**
- **Node.js** (JavaScript)
- **Ruby**
- **Go**
- **PHP**
- **C++**
- **JavaScript** (browser)

### SDK vs CLI

| SDK | CLI |
|-----|-----|
| Programmatic access via code | Command-line access |
| Embed in applications | Run commands interactively or in scripts |
| Does NOT manage state (idempotency) | Does NOT manage state |
| Create resources each time code runs | Each command execution is independent |

**Example:** Running SDK code that creates an EC2 instance 3 times = 3 instances created

### Python SDK (Boto3) Example

**Installation:**
```bash
pip3 install boto3
```

**Example - List S3 Buckets:**
```python
import boto3

# Create S3 client
s3 = boto3.client('s3', region_name='us-east-1')

# List buckets
response = s3.list_buckets()

# Print bucket names
for bucket in response['Buckets']:
    print(bucket['Name'])
```

**Example - Upload to S3:**
```python
import boto3

s3 = boto3.client('s3')
s3.upload_file('local-file.txt', 'my-bucket', 'remote-file.txt')
```

### Ruby SDK Example

**Gemfile:**
```ruby
source 'https://rubygems.org'
gem 'aws-sdk-s3'
```

**Install:**
```bash
bundle install
```

**Code:**
```ruby
require 'aws-sdk-s3'

# Configure credentials (if not using environment variables or IAM role)
Aws.config.update({
  region: 'us-east-1',
  credentials: Aws::Credentials.new(
    ENV['AWS_ACCESS_KEY_ID'],
    ENV['AWS_SECRET_ACCESS_KEY']
  )
})

# Create S3 client
s3 = Aws::S3::Client.new

# List buckets
response = s3.list_buckets

response.buckets.each do |bucket|
  puts bucket.name
end
```

### Credentials in SDK

**Best practices for credentials:**

1. **IAM Roles (Best):** If running on EC2/Lambda/ECS, use IAM roles (automatic)
2. **Environment Variables (Good):** Export credentials as env vars
3. **Credentials File (Okay):** `~/.aws/credentials`
4. **Hard-coded (NEVER):** Don't hard-code credentials in code!

**Environment Variable Method:**
```python
import boto3

# SDK automatically loads from environment variables:
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# AWS_DEFAULT_REGION (or AWS_REGION in CLI v2)

s3 = boto3.client('s3')
```

### Finding SDK Documentation

**AWS SDK Documentation:** https://aws.amazon.com/developer/tools/

Navigate to your language, then find:
- **Developer Guide:** Getting started, concepts
- **API Reference:** All available methods/functions

**Example:** Python Boto3 - https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

---

## Infrastructure as Code (IaC)

### What is IaC?

**Infrastructure as Code** allows you to write configuration scripts to automate creating, updating, or destroying cloud infrastructure.

**Benefits:**
- Version control infrastructure
- Reproducible environments
- Automate deployments
- Share infrastructure definitions
- Reduce manual errors

### AWS IaC Tools

| Tool | Type | Language |
|------|------|----------|
| **CloudFormation (CFN)** | Declarative | JSON, YAML |
| **AWS CDK** | Imperative | TypeScript, Python, Java, C#, Go |

### Declarative vs Imperative

**Declarative (CloudFormation):**
- "What you see is what you get"
- You define the **desired end state**
- AWS figures out how to achieve it
- Written in JSON/YAML
- More verbose, but explicit

**Imperative (CDK):**
- "Say what you want, rest is filled in"
- You write **code to define** infrastructure
- Uses programming language
- More concise, more abstraction
- Generates CloudFormation under the hood

---

## AWS CloudFormation

### What is CloudFormation?

**CloudFormation** allows you to write infrastructure as code using JSON or YAML templates.

**Key Concepts:**
- **Template:** The blueprint (JSON/YAML file defining resources)
- **Stack:** The actual infrastructure created from template
- **Resource:** AWS service/component in template (EC2, S3, VPC, etc.)

### CloudFormation Template Structure

**Minimum template (YAML):**
```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: "My CloudFormation stack"

Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-unique-bucket-name
```

**Template Sections:**
- **AWSTemplateFormatVersion:** (Required in practice) Template version
- **Description:** (Optional) What the template does
- **Resources:** (Required) AWS resources to create
- **Parameters:** (Optional) Input values
- **Outputs:** (Optional) Values to export/display
- **Mappings:** (Optional) Key-value lookups
- **Conditions:** (Optional) Conditional resource creation

### Creating a Stack

**Via AWS Console:**
1. Go to CloudFormation service
2. Create stack
3. Upload template file or provide S3 URL
4. Specify stack name
5. Configure parameters (if any)
6. Review and create

**Via AWS CLI:**
```bash
aws cloudformation create-stack \
  --stack-name my-stack \
  --template-body file://template.yaml
```

### Stack Operations

**View stack:**
```bash
aws cloudformation describe-stacks --stack-name my-stack
```

**Update stack:**
```bash
aws cloudformation update-stack \
  --stack-name my-stack \
  --template-body file://updated-template.yaml
```

**Delete stack:**
```bash
aws cloudformation delete-stack --stack-name my-stack
```

### CloudFormation in Console

**Monitoring Stack Creation:**
- **Events tab:** Shows resource creation progress
- **Resources tab:** Lists all resources being created/created
- **Outputs tab:** Shows output values
- **Parameters tab:** Shows input parameters used

**Stack States:**
- **CREATE_IN_PROGRESS:** Creating resources
- **CREATE_COMPLETE:** Successfully created
- **CREATE_FAILED:** Creation failed
- **DELETE_IN_PROGRESS:** Deleting resources
- **DELETE_COMPLETE:** Successfully deleted

### CloudFormation Example - S3 Bucket with Output

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: "S3 bucket with domain name output"

Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket

Outputs:
  BucketDomainName:
    Description: "Domain name of the S3 bucket"
    Value: !GetAtt MyS3Bucket.DomainName
```

**Intrinsic Functions:**
- `!Ref` - Reference resource (returns resource name/ID)
- `!GetAtt` - Get attribute of resource
- `!Sub` - Substitute variables
- `!Join` - Join strings

---

## AWS CDK (Cloud Development Kit)

### What is CDK?

**AWS CDK** allows you to define infrastructure using programming languages (TypeScript, Python, Java, C#, Go).

**How it works:**
1. Write code in your language
2. CDK synthesizes code into CloudFormation template
3. CloudFormation deploys the infrastructure

**As of February 2026:** CDK is actively maintained and supports all major programming languages.

### CDK vs CloudFormation

| Feature | CloudFormation | CDK |
|---------|----------------|-----|
| **Language** | JSON/YAML | TypeScript, Python, Java, C#, Go |
| **Abstraction** | Low-level (explicit) | High-level (constructs) |
| **Reusability** | Limited | High (constructs, libraries) |
| **Learning Curve** | Moderate | Steeper (requires programming knowledge) |
| **Underlying** | Native | Generates CloudFormation |

### CDK Components

**Constructs:**
- Reusable cloud components
- Available at https://constructs.dev
- Pre-built patterns for common architectures
- Similar to Terraform modules

**CDK CLI:**
- `cdk init` - Initialize new project
- `cdk synth` - Synthesize CloudFormation template
- `cdk deploy` - Deploy stack
- `cdk destroy` - Delete stack
- `cdk diff` - Show differences

**CDK Pipelines:**
- Quickly set up CI/CD for CDK projects
- Automated deployment pipelines

### CDK Example (TypeScript)

**Initialize project:**
```bash
npm install -g aws-cdk
mkdir my-cdk-project
cd my-cdk-project
cdk init app --language typescript
```

**Example Stack (lib/my-stack.ts):**
```typescript
import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class MyStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create S3 bucket
    new s3.Bucket(this, 'MyBucket', {
      bucketName: 'my-unique-bucket-name',
      versioned: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });
  }
}
```

**Deploy:**
```bash
cdk deploy
```

**Destroy:**
```bash
cdk destroy
```

### CDK Python Example

**Initialize:**
```bash
cdk init app --language python
source .venv/bin/activate
pip install -r requirements.txt
```

**Stack (app.py):**
```python
from aws_cdk import Stack, aws_s3 as s3
from constructs import Construct

class MyStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Create S3 bucket
        s3.Bucket(self, "MyBucket",
            versioned=True
        )
```

### CDK Testing Framework

CDK includes testing support (primarily TypeScript):
- Unit testing
- Integration testing
- Snapshot testing

---

## AWS Access Keys

### What are Access Keys?

**Access Keys** are credentials required for programmatic access to AWS (CLI, SDK, API calls outside Console).

**Components:**
- **Access Key ID:** Public identifier (like a username)
- **Secret Access Key:** Private key (like a password)

**Format:**
- Access Key ID: `AKIAIOSFODNN7EXAMPLE`
- Secret Access Key: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

### Access Key Security

**Critical Security Rules:**
1. **NEVER share access keys** - They're equivalent to your account credentials
2. **NEVER commit to code/repos** - Use environment variables or IAM roles
3. **NEVER hard-code in applications**
4. **Rotate regularly** - Generate new keys periodically
5. **Delete unused keys** - If not needed, delete immediately

### Access Key Limits

**Per User:**
- **Maximum 2 active access keys** at any given time
- Can deactivate and reactivate keys
- Can delete keys permanently

**Best Practice:** Keep both slots filled (even if one is deactivated) to prevent attackers from creating keys if they compromise your account.

### Creating Access Keys

**Via AWS Console:**
1. Go to IAM service
2. Select Users
3. Click your username
4. Security credentials tab
5. Create access key
6. **Download and save immediately** - Secret shown only once!

**Key states:**
- **Active:** Key works for API calls
- **Inactive:** Key temporarily disabled (can reactivate)

### Storing Access Keys

**Location:**
```
~/.aws/credentials
```

**Format:**
```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY

[profile-name]
aws_access_key_id = ANOTHER_KEY_ID
aws_secret_access_key = ANOTHER_SECRET_KEY
```

**Config file (`~/.aws/config`):**
```ini
[default]
region = us-east-1
output = json

[profile profile-name]
region = us-west-2
output = table
```

### Access Key Best Practices

**For Development:**
1. Use AWS CLI profiles for different accounts/environments
2. Use environment variables when running code
3. Never hard-code credentials

**For Production:**
4. Use **IAM roles** (EC2, Lambda, ECS) - no keys needed!
5. Use **AWS Secrets Manager** or **Parameter Store** if keys required
6. Enable **MFA for key operations** if possible

**Security:**
7. Use AWS CloudTrail to monitor access key usage
8. Use IAM Access Analyzer to identify exposed keys
9. Delete keys when users leave organization
10. Rotate keys every 90 days (AWS recommendation)

---

## AWS Documentation

### What is AWS Documentation?

**AWS Documentation** is the comprehensive technical resource for all AWS services.

**Location:** https://docs.aws.amazon.com

**As of February 2026:** Documentation remains the most authoritative and up-to-date source for AWS service information.

### Documentation Structure

**For Each Service:**
- **User Guide:** How to use the service, concepts, best practices
- **API Reference:** Detailed API calls, parameters, responses
- **Developer Guide:** For SDK integration
- **CLI Reference:** CLI commands for the service

**Additional Resources:**
- **Whitepapers:** Architecture patterns, best practices
- **FAQs:** Common questions per service
- **Tutorials:** Step-by-step guides
- **AWS Samples (GitHub):** Example code and projects

### Finding Documentation

**Method 1 - Direct URL:**
```
https://docs.aws.amazon.com/[service]/
```

**Method 2 - Search:**
- Google: "[service] AWS documentation"
- AWS Console: Search for service, click "Documentation" link

**Method 3 - AWS Docs Homepage:**
- Visit https://docs.aws.amazon.com
- Browse or search for service

### Using Documentation

**Example - S3 Documentation:**
1. Go to https://docs.aws.amazon.com/s3/
2. Click "User Guide"
3. Navigate topics in left sidebar
4. Search using search bar

**Documentation Features:**
- **PDF download:** Entire guide as PDF
- **Kindle format:** Available for some guides
- **Code examples:** Embedded in documentation
- **GitHub:** All docs are open-source, can submit issues/PRs

**AWS Documentation GitHub:**
- https://github.com/awsdocs/
- Can submit corrections, improvements
- Community contributions accepted

### Documentation Quality

**AWS Documentation Strengths:**
- **Comprehensive:** Covers all services in detail
- **Up-to-date:** Reflects current service features
- **Examples:** Includes code snippets and use cases
- **Organized:** Well-structured (usually)

**Challenges:**
- **Density:** Very detailed, can be overwhelming
- **Inconsistency:** Some services better documented than others
- **Organization:** Not always easy to find what you need (e.g., Amazon Cognito)

### Complementary Resources

**AWS Labs (Tutorials):**
- Hands-on tutorials and workshops
- Not in main documentation
- https://github.com/aws-samples/

**AWS Blogs:**
- Announcements, deep dives, best practices
- https://aws.amazon.com/blogs/

**AWS re:Post (Community):**
- Community Q&A forum (replaces AWS Forums)
- https://repost.aws/

---

## Shared Responsibility Model

### What is the Shared Responsibility Model?

The **Shared Responsibility Model** is a cloud security framework defining security obligations:
- **AWS (Cloud Provider):** Security OF the cloud
- **Customer:** Security IN the cloud

**Core Principle:**
- **AWS:** Responsible for infrastructure (hardware, facilities, network, hypervisor)
- **Customer:** Responsible for data, configurations, access controls

### Simple Mnemonics

**"Security IN the cloud" vs "Security OF the cloud"**
- **IN:** If you can configure it or store data on it → You're responsible
- **OF:** If you cannot configure it (physical/infrastructure) → AWS is responsible

**Another way:**
- **Customer:** Data and configuration
- **AWS:** Physical infrastructure and managed services operation

### AWS Responsibilities (Security OF the Cloud)

AWS is responsible for protecting the infrastructure:

**Physical Security:**
- Data center security (guards, cameras, access controls)
- Physical servers, storage devices, networking equipment
- Climate control, power, redundancy

**Global Infrastructure:**
- Regions
- Availability Zones
- Edge locations
- Network backbone

**Infrastructure Software:**
- Compute (hypervisor layer)
- Storage infrastructure
- Database infrastructure
- Networking infrastructure

**Managed Service Operations:**
- Patching managed services (RDS, Lambda, etc.)
- Operating managed services
- Infrastructure maintenance

### Customer Responsibilities (Security IN the Cloud)

Customer is responsible for everything they control:

**Data:**
- **Customer data:** Content you upload/create
- **Classification:** Determining sensitivity levels
- **Encryption:** Encrypting data at rest and in transit

**Platform, Applications:**
- **Identity & Access Management:** IAM users, roles, policies, MFA
- **Applications:** Security of apps you run
- **Configuration:** How services are configured

**Operating System, Network:**
- **OS:** Patching guest OS (EC2), security updates
- **Network configuration:** Security groups, NACLs, routing tables
- **Firewall configuration:** Virtual firewalls

**Encryption:**
- **Client-side encryption:** Before uploading to AWS
- **Server-side encryption:** Enabling encryption on services (S3, EBS, RDS)
- **Key management:** Managing encryption keys (KMS)

**Network Traffic:**
- **Protection:** VPC Flow Logs, AWS Shield, WAF
- **Monitoring:** CloudWatch, CloudTrail, GuardDuty

### Shared Responsibility by Service Type

The responsibility shifts based on service model:

**IaaS (Infrastructure as a Service) - EC2:**
- **AWS:** Hardware, hypervisor, physical network/storage
- **Customer:** Guest OS, applications, data, network config, firewalls
- **Example:** Launch EC2 instance → You patch OS, manage apps, configure security groups

**PaaS (Platform as a Service) - RDS, Elastic Beanstalk:**
- **AWS:** OS patches, database engine updates, infrastructure
- **Customer:** Database config, access controls, data, network config (security groups)
- **Example:** RDS database → AWS patches MySQL, you manage DB users and backups

**SaaS (Software as a Service) - WorkDocs:**
- **AWS:** Everything about the application infrastructure
- **Customer:** Data, user access, sharing permissions
- **Example:** WorkDocs → AWS runs the app, you manage who sees what documents

**FaaS (Function as a Service) - Lambda:**
- **AWS:** Everything except your code
- **Customer:** Just the function code and IAM permissions
- **Example:** Lambda function → AWS handles runtime, scaling, patching; you write code

### Shared Responsibility Across Compute

| Service | Customer Manages | AWS Manages |
|---------|------------------|-------------|
| **Bare Metal** (EC2 Bare Metal) | Host OS, hypervisor, guest OS, apps, data | Physical machine |
| **Virtual Machine** (EC2) | Guest OS, runtime, apps, data | Hypervisor, host OS, physical machine |
| **Containers** (ECS) | Container config, deployment, apps | OS, runtime, hypervisor, physical |
| **PaaS** (Elastic Beanstalk) | Code, some config | Servers, OS, networking, storage, security |
| **SaaS** (WorkDocs) | Data, access controls | Everything else |
| **Functions** (Lambda) | Code only | Everything else |

### Common Exam Questions

**Who is responsible for:**
- **Patching EC2 guest OS?** → Customer
- **Physical data center security?** → AWS
- **S3 bucket permissions?** → Customer
- **RDS database engine patches?** → AWS
- **Encrypting data before upload?** → Customer
- **EC2 hypervisor maintenance?** → AWS
- **IAM user creation and permissions?** → Customer
- **Network infrastructure redundancy?** → AWS

### Key Takeaways

✅ **Customer controls = Customer responsible**
✅ **Infrastructure/hardware = AWS responsible**
✅ **Responsibility increases with control** (IaaS > PaaS > SaaS)
✅ **"Can you configure it?" = Your responsibility**
✅ **Both share responsibility for security success**

---

## Computing Services

### Overview of AWS Compute

AWS offers compute services across multiple categories:
1. **Virtual Machines (VMs)** - EC2, LightSail
2. **Containers** - ECS, EKS, Fargate
3. **Serverless Functions** - Lambda

### Virtual Machines

**Amazon EC2 (Elastic Compute Cloud):**
- Launch virtual machines (instances)
- Full control over OS, networking, storage
- Most flexible compute option
- **Backbone of AWS:** Most services use EC2 under the hood

**What is a Virtual Machine?**
- Emulation of physical computer using software
- Multiple VMs run on same physical server (cost sharing)
- Can create, copy, resize, migrate easily
- Think: "Your server as an executable file"

**EC2 Instance:**
- Virtual machine launched from an **AMI (Amazon Machine Image)**
- Choose: CPU, RAM, storage, network bandwidth, OS
- Configure: Security groups, key pairs, IAM roles
- Attach: EBS volumes (storage), Elastic IPs

**Amazon LightSail:**
- Simplified, managed virtual server service
- "Beginner-friendly" EC2
- **Use when:** Quick WordPress site, simple web server, limited AWS knowledge needed
- Pre-configured options (WordPress, LAMP stack, etc.)

### Containers

**What are Containers?**
- Virtualize an OS to run multiple workloads on single OS instance
- Lighter than VMs (share host OS kernel)
- Used for **microservices architecture** (app divided into smaller services)

**Amazon ECS (Elastic Container Service):**
- **Container orchestration** for Docker
- Launches cluster of EC2 instances with Docker installed
- You manage: Container images, task definitions, services
- AWS manages: Orchestration, scheduling
- **Use when:** Need Docker as a service, run containers with EC2 control

**Amazon ECR (Elastic Container Registry):**
- **Repository for container images**
- Like DockerHub but AWS-managed
- Stores Docker images with version control
- Required to run containers on ECS/EKS

**AWS Fargate:**
- **Serverless container orchestration**
- Same as ECS but no EC2 servers to manage
- Pay per running container (per-second billing)
- AWS handles: Scaling, patching, infrastructure
- **Use when:** Don't want to manage servers, variable workloads, serverless containers

**Amazon EKS (Elastic Kubernetes Service):**
- **Fully managed Kubernetes service**
- Kubernetes (K8s): Open-source orchestration by Google
- Industry standard for microservices management
- **Use when:** Need Kubernetes as a service, already using K8s, multi-cloud portability

### Serverless

**AWS Lambda:**
- **Serverless functions service**
- Upload code, AWS runs it on-demand
- No servers to provision or manage
- Pay only for execution time (rounded to nearest 100ms)
- **Languages:** Python, Node.js, Java, C#, Go, Ruby, custom runtimes

**How Lambda Works:**
1. Upload code (function)
2. Configure: Memory, timeout, triggers
3. AWS provisions compute automatically
4. Function runs when triggered (API call, S3 upload, schedule, etc.)
5. Pay only for runtime

**Lambda Characteristics:**
- **Max runtime:** 15 minutes
- **Stateless:** Each invocation is independent
- **Event-driven:** Triggered by events (not always running)
- **Auto-scaling:** AWS scales automatically

---

## Edge and Hybrid Computing

### Edge Computing

**Definition:** Push computing workloads **outside your network** to run **close to destination location**.

**Why Edge Computing?**
- **Lower latency:** Process data closer to user
- **Reduced bandwidth:** Less data sent to central cloud
- **Faster response:** Critical for real-time applications
- **Offline capability:** Can work without cloud connection

**Use Cases:**
- IoT devices processing data locally
- Mobile apps needing instant response (gaming, AR/VR)
- Smart factories with sensors
- External servers not in your cloud network

### Hybrid Computing

**Definition:** Run workloads on **both on-premise datacenter AND AWS Cloud (VPC)**.

**Why Hybrid?**
- **Legacy systems:** Can't move to cloud yet
- **Regulatory compliance:** Some data must stay on-premise
- **Gradual migration:** Move to cloud incrementally
- **Cost optimization:** Use existing infrastructure + cloud scalability
- **Data sovereignty:** Keep sensitive data on-premise

**Architecture:**
```
Your Company:
├── On-Premise Datacenter (legacy apps, sensitive data)
└── AWS Cloud (VPC) (new apps, scalable workloads)
         ↕
    Secure connection (VPN, Direct Connect)
```

### AWS Outposts

**What it is:** Physical rack of AWS servers installed **in your datacenter**.

**Key Features:**
- **Physical hardware:** 42U rack shipped by AWS
- **AWS-managed:** AWS handles maintenance, patches, updates remotely
- **AWS services locally:** Run EC2, EBS, S3, RDS, EKS in your facility
- **Same APIs:** Use AWS APIs/console as if in AWS region

**Use Cases:**
- **Low latency requirements:** Process data locally with AWS tools
- **Data residency:** Data cannot leave your facility (compliance)
- **Local processing:** Real-time manufacturing, healthcare
- **Consistent hybrid:** Same AWS experience on-prem and in cloud

**How it works:**
- AWS delivers and installs rack in your datacenter
- Connect to parent AWS region
- Managed remotely by AWS
- You use services as normal

**Benefits:**
- AWS experience on-premise
- No learning curve (same APIs)
- Hardware maintenance by AWS
- Local compute/storage with cloud integration

### AWS Wavelength

**What it is:** Build applications **inside telecom carrier datacenters** (Verizon, Vodafone) for **5G networks**.

**Key Features:**
- **Location:** Inside telecom provider datacenters (near cell towers)
- **Ultra-low latency:** Traffic stays in carrier network
- **5G integration:** Optimized for 5G mobile networks
- **EC2/EBS:** Run compute and storage at edge of 5G network

**How it differs from regular AWS:**
```
Traditional:
Mobile Device → Cell Tower → Internet → AWS Region (far away) → Response
                             High latency

Wavelength:
Mobile Device → Cell Tower → Wavelength Zone (in carrier datacenter) → Response
                             Ultra-low latency (<10ms)
```

**Use Cases:**
- **Mobile gaming:** Multiplayer games needing <10ms latency
- **AR/VR applications:** Real-time augmented/virtual reality
- **Live video streaming:** Low-latency broadcasts
- **Autonomous vehicles:** Connected cars needing instant decisions
- **Industrial IoT:** Real-time factory automation

**Setup Components:**
- **Wavelength Zones:** Edge datacenters in carrier network
- **Carrier Gateway:** Special gateway for telecom carrier network
- **Carrier IP addresses:** IP addresses routable through carrier

**Partners:**
- Verizon (US)
- Vodafone (Europe)
- KDDI (Japan)
- SK Telecom (South Korea)

### VMware Cloud on AWS

**What it is:** Run **on-premise VMware VMs** as **EC2 instances** on AWS.

**The Problem:**
- Many companies use VMware (vSphere, ESXi) for virtualization
- Moving to AWS traditionally requires re-architecting
- AWS uses different hypervisor (Nitro, not VMware)

**The Solution:**
- Run VMware natively on AWS
- Use same VMware tools (vCenter, vSphere)
- **Lift and shift:** Move VMs without changes
- No re-training needed

**Requirements:**
- On-premise datacenter **must use VMware**
- Not for other hypervisors (Hyper-V, KVM, etc.)

**Use Cases:**
- **Datacenter migration:** Move VMware workloads to cloud
- **Disaster recovery:** Replicate VMs to AWS for backup
- **Capacity extension:** Burst to AWS when needed
- **Hybrid cloud:** Keep some workloads on-prem, others in AWS

**Benefits:**
- Same VMware experience
- Integrate with AWS services
- No application changes
- Familiar management tools

### AWS Local Zones

**What they are:** Small AWS datacenters **outside AWS Regions** in populated areas for low latency.

**Why Local Zones?**
- **Problem:** Users far from AWS Regions have high latency
- **Solution:** Place compute closer to users in major cities

**Architecture:**
```
AWS Region: us-east-1 (Virginia)
    ↓ Extends to:
Local Zones:
├── Boston Local Zone
├── Miami Local Zone  
├── Houston Local Zone
└── Los Angeles Local Zone
```

**Available Services (Limited):**
- EC2 instances
- EBS volumes
- VPC networking
- Some other core services

**Use Cases:**
- **Media streaming:** Low-latency video in specific markets
- **Gaming:** Game servers in major cities
- **Real-time applications:** Financial trading, live betting
- **ML inference:** Fast ML predictions near users

**Difference from Regions:**
- **Smaller:** Limited services compared to full AWS Region
- **Closer:** More locations, closer to end users
- **Low latency:** Single-digit millisecond latency to nearby users

---

## High Performance Computing (HPC)

### What is HPC?

**High Performance Computing** uses clusters of servers for computationally intensive workloads.

**When HPC is Needed:**
- Supercomputer-level computational power
- Large-scale simulations
- Complex scientific calculations
- Deep learning model training
- Problems too large/slow for standard computers

### AWS Nitro System

**What is Nitro?**
- AWS-designed hardware and lightweight hypervisor
- Powers all new EC2 instance types (as of 2026)
- Enables faster performance, enhanced security, innovation

**Components:**
- **Nitro Cards:** Specialized cards for VPC, EBS, instance storage
- **Nitro Security Chip:** Integrated in motherboard for hardware-level security
- **Nitro Hypervisor:** Lightweight hypervisor (near bare-metal performance)
- **Nitro Enclaves:** Isolated compute for sensitive workloads

**Benefits:**
- Better performance
- Enhanced security
- Bare-metal instances available
- Innovation velocity

### EC2 Bare Metal Instances

**What they are:** EC2 instances with **no hypervisor** (direct hardware access).

**Use Cases:**
- Maximum performance
- Full control over hardware
- Workloads requiring direct hardware access
- Specific licensing requirements (Oracle, etc.)
- Custom hypervisor (run your own)

**Instance Families:**
- M5, R5, C5 (and newer) support bare metal
- Example: `m5.metal`, `r5.metal`

**Customer Responsibility:**
- Install and manage hypervisor (if needed)
- Install host OS
- Everything above

### Bottlerocket OS

**What it is:** Linux-based OS purpose-built by AWS for running containers.

**Features:**
- Designed for VMs or bare metal
- Optimized for containers (ECS, EKS)
- Minimal attack surface
- Fast boot times
- Transactional updates

### AWS ParallelCluster

**What it is:** Open-source cluster management tool for deploying and managing **HPC clusters** on AWS.

**How it works:**
1. Install `pcluster` CLI
2. Configure cluster (instance types, scheduler, size)
3. Deploy cluster (creates CloudFormation stack)
4. Submit jobs to cluster
5. Cluster auto-scales based on queue

**Job Schedulers Supported:**
- **Slurm** (most popular)
- **AWS Batch**
- **SGE (Sun Grid Engine)**
- **Torque**

**Architecture:**
```
HPC Cluster:
├── Head/Master Node (job submission, scheduling)
└── Compute Nodes (auto-scaling fleet)
    ├── EC2 instances (spin up when jobs queued)
    └── Terminate when idle
```

**Use Cases:**
- Scientific simulations (climate, physics, chemistry)
- Genomics/bioinformatics
- Financial modeling
- Engineering simulations (crash tests, aerodynamics)
- Machine learning training

**Key Features:**
- Auto-scaling compute
- Shared file systems (EFS, FSx for Lustre)
- Spot instances supported
- Multiple queues/instance types
- Cost-effective (pay only for compute time)

**Installation:**
```bash
pip3 install aws-parallelcluster
pcluster configure
pcluster create-cluster --cluster-name my-hpc-cluster
```

**Benefits:**
- Pay-as-you-go HPC
- No upfront hardware investment
- Scales to thousands of cores
- AWS-maintained infrastructure

---

## Key Concepts for CLF-C02 Exam

### Must-Know CLI/Tools
✅ AWS CLI is for programmatic interaction via command line
✅ CLI v2 is current (v1 end-of-support July 2027)
✅ CloudShell = browser-based CLI (free, pre-authenticated)
✅ SDKs = programmatic access via code (Boto3 for Python)

### Must-Know IaC
✅ CloudFormation = declarative IaC (JSON/YAML templates)
✅ CDK = imperative IaC (code in TypeScript/Python/etc., generates CloudFormation)
✅ Stack = infrastructure created from template
✅ Template = blueprint defining resources

### Must-Know Security
✅ ARNs = unique identifiers for AWS resources
✅ Access Keys = credentials for programmatic access (NEVER share/commit)
✅ IAM Roles = preferred over access keys (for EC2/Lambda/etc.)

### Must-Know Shared Responsibility
✅ **IN the cloud** = Customer (data, configuration, access control)
✅ **OF the cloud** = AWS (infrastructure, hardware, managed service operations)
✅ Responsibility shifts by service type (IaaS > PaaS > SaaS)
✅ "Can you configure it?" → Your responsibility

### Must-Know Compute
✅ EC2 = Virtual machines (most control)
✅ Lambda = Serverless functions (least management)
✅ ECS = Container orchestration (Docker with EC2)
✅ Fargate = Serverless containers (no EC2 to manage)
✅ EKS = Managed Kubernetes
✅ LightSail = Simplified VMs

### Must-Know Edge/Hybrid
✅ **Edge Computing** = Workloads outside your network, close to users
✅ **Hybrid Computing** = Workloads on-prem AND in cloud
✅ **Outposts** = AWS rack in your datacenter
✅ **Wavelength** = Compute in carrier datacenters (5G, ultra-low latency)
✅ **Local Zones** = Mini-datacenters in cities (closer to users)
✅ **VMware Cloud** = Run VMware VMs on AWS

---

## Python Connection Points

As you learn AWS and Python in parallel, note these integration opportunities:

**Boto3 (AWS SDK for Python):**
- Automate AWS tasks with Python
- Interact with any AWS service programmatically
- Examples: Create EC2 instances, upload to S3, query DynamoDB

**Lambda Functions:**
- Write serverless functions in Python
- Event-driven automation
- Most popular Lambda language

**CloudFormation Custom Resources:**
- Use Python Lambda to extend CloudFormation

**AWS CLI Scripting:**
- Wrap CLI commands in Python scripts
- Parse JSON output with Python

**Data Processing:**
- Use AWS services (S3, Athena, Glue) with Python
- Pandas + S3 for data analysis

---

## Continue Working On

**Next Steps:**
1. **Practice AWS CLI locally** - Install CLI, configure credentials, practice S3/EC2 commands
2. **Explore CloudShell** - Familiarize with browser-based environment
3. **Review Shared Responsibility** - Understand "IN vs OF" deeply
4. **Understand compute options** - Know when to use EC2 vs Lambda vs containers
5. **Study for CLF-C02** - Focus on core services, shared responsibility, basic security

**For Your AWS Journey:**
- Set up AWS CLI with proper profiles
- Create simple CloudFormation templates
- Experiment with Lambda functions (Python!)
- Practice ARN identification
- Understand IAM and access keys deeply

---

## Additional Resources

**Official AWS Documentation:**
- AWS CLI: https://docs.aws.amazon.com/cli/
- CloudShell: https://docs.aws.amazon.com/cloudshell/
- CloudFormation: https://docs.aws.amazon.com/cloudformation/
- CDK: https://docs.aws.amazon.com/cdk/
- IAM Best Practices: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- Shared Responsibility: https://aws.amazon.com/compliance/shared-responsibility-model/

**Learn More:**
- AWS Free Tier: Practice without cost
- AWS Workshops: https://workshops.aws/
- AWS Skill Builder: Free AWS training

---

*Notes compiled: February 4, 2026*
*All information verified against current AWS documentation where possible*
*Course source: FreeCodeCamp AWS Cloud Practitioner by Andrew Brown*


---