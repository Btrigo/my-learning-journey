# AWS Study Notes — Hour 2
### Source: freeCodeCamp AWS Cloud Practitioner Course (ExamPro)
### Cross-referenced against official AWS documentation, February 2026

---

## 1. Serverless Services

### What "Serverless" Means
Serverless does not mean there are no servers — it means **you don't manage them**. The underlying infrastructure is fully handled by AWS. Serverless services generally share these characteristics:

- Highly elastic and scalable (automatically)
- Highly available and durable by default
- Secure by default
- Abstracts away underlying infrastructure
- **Scale to zero** — when idle, the service costs nothing
- **Pay for value** — you pay for actual execution/usage, not idle capacity

> 📝 **Nuance from the course (accurate):** "Serverless" is not a binary yes/no — it exists on a spectrum. Some services are more serverless than others. This is a good way to think about it.

### Core Serverless Services on AWS

| Service | Type | Description |
|---|---|---|
| **Amazon DynamoDB** | NoSQL Database | Serverless key-value and document database; scales to billions of records; no shard management |
| **Amazon S3** | Object Storage | Serverless object store; unlimited storage; pay for what you store |
| **AWS Fargate** | Container Compute | Serverless container orchestration; runs ECS/EKS containers without managing EC2 servers |
| **AWS Lambda** | Functions | Run code without provisioning servers; event-driven; pay per invocation and duration |
| **AWS Step Functions** | Workflow Orchestration | Coordinate multiple Lambda functions and services into serverless workflows (state machines) |
| **Amazon Aurora Serverless** | Relational Database | On-demand, auto-scaling version of Aurora; scales down to zero when idle |

> 📝 Other services that are also serverless but not in the core list: API Gateway, AppSync, Amplify, SQS, SNS — the list is long. The table above focuses on the most commonly tested ones.

---

## 2. AWS Lambda (Deep Dive)

### What It Is
A **serverless compute service** that runs code in response to events without provisioning or managing servers. You upload code, configure memory and timeout, and Lambda handles everything else.

### Key Characteristics
- **Event-driven:** Triggered by events from S3, API Gateway, DynamoDB Streams, SQS, SNS, EventBridge, and many more
- **Stateless:** Each invocation is independent
- **Scales automatically:** From zero to thousands of concurrent executions

### Configuration Options
- **Memory:** 128 MB to 10,240 MB (in 1 MB increments) — more memory also means more CPU
- **Timeout:** You set the maximum allowed runtime before the function is terminated
- **Supported runtimes:** Python, Node.js, Java, Go, Ruby, .NET, and custom runtimes

### Pricing (Verified against AWS docs, 2024)
Lambda billing has **two components:**

1. **Requests:** $0.20 per 1 million requests (first 1 million/month are free)
2. **Duration:** Charged per GB-second of compute time, billed in **1 millisecond increments** (rounded up to nearest 1 ms)
   - Duration free tier: 400,000 GB-seconds/month

> ⚠️ **Course correction:** The transcript states Lambda is "rounded to the nearest 100 milliseconds." This was **changed by AWS in December 2020** — Lambda now bills in **1 millisecond increments**. The more current billing is more granular and generally cheaper.

### Lambda Free Tier (per month)
- 1,000,000 free requests
- 400,000 GB-seconds of compute time

---

## 3. AWS Step Functions

A **serverless orchestration service** (state machine) used to coordinate multiple AWS services into workflows.

- Visually design and run workflows as a series of steps
- Each step is a **state** in the state machine
- Supports branching logic, parallel execution, error handling, and retries
- Integrates with Lambda, ECS/Fargate, DynamoDB, SQS, SNS, and more
- Common use cases: order processing, data pipelines, approval workflows, ETL jobs

---

## 4. Windows on AWS

AWS provides several services specifically supporting Windows workloads:

| Service | Description |
|---|---|
| **Windows Server on EC2** | Launch Windows Server AMIs (2019, 2022, etc.) — note: free tier eligible on T2 Micro |
| **SQL Server on RDS** | Managed SQL Server; select from multiple versions |
| **AWS Directory Service** | Managed Microsoft Active Directory |
| **AWS License Manager** | Centrally manage software licenses (Microsoft, IBM, SAP, Oracle) |
| **Amazon FSx for Windows File Server** | Fully managed Windows-native shared file storage |
| **Amazon WorkSpaces** | Virtual Windows (or Linux) desktops |
| **AWS Lambda (PowerShell)** | Lambda supports PowerShell as a runtime |
| **AWS MAP for Windows** | Migration Acceleration Program — methodology for migrating large Windows enterprise workloads to AWS |

> 💡 **Interesting verified fact:** AWS offers a **free-tier eligible Windows Server** on a T2 Micro instance. This is not available on Azure, which requires a minimum paid instance size for Windows.

---

## 5. AWS License Manager

### What It Is
A service that makes it easier to **centrally manage software licenses** from vendors like Microsoft, IBM, SAP, and Oracle — across both AWS and on-premises environments.

### Bring Your Own License (BYOL)
BYOL is the process of **reusing existing software licenses** on cloud infrastructure, rather than purchasing new licenses from the cloud provider. This saves money when you've already purchased licenses in bulk.

- Example: Microsoft Volume Licensing with Software Assurance (SA) allows BYOL for Windows Server and SQL Server on AWS

### Key Details (Verified)
- Works with EC2 **Dedicated Hosts**, Dedicated Instances, and Spot Instances
- For RDS, License Manager only applies to **Oracle** databases
- **Critical exam note:** For Microsoft Windows Server or SQL Server BYOL, AWS documentation and Microsoft's licensing terms generally require a **Dedicated Host** (not just a dedicated instance) — this is a commonly tested exam detail

---

## 6. Logging Services

### Overview of the Three Key Logging Services

| Service | What It Logs | Primary Use |
|---|---|---|
| **AWS CloudTrail** | All API calls (SDK, CLI, Console) | Auditing — who did what, when, from where |
| **Amazon CloudWatch** | Metrics, logs, events, alarms, dashboards | Monitoring — how are things performing |
| **AWS X-Ray** | Distributed traces across microservices | Debugging — where is the bottleneck or failure |

---

## 7. AWS CloudTrail

### What It Is
A service that **logs every API call made in your AWS account** — whether through the console, CLI, SDK, or other services. Used for governance, compliance, auditing, and security incident detection.

### Key Information in Each CloudTrail Event
- **Who:** User identity, access key, IAM role
- **What:** Event name (API action), resource affected
- **When:** Event time
- **Where:** Source IP address, AWS region
- **How:** User agent (console, SDK, CLI, etc.)

### Event History (Default — No Setup Required)
- CloudTrail is **on by default** for all AWS accounts
- Provides **90 days** of management event history in the console — free of charge
- Viewable, searchable, downloadable, and immutable
- Region-specific: shows events only for the region you're currently viewing

> ✅ **Verified:** 90-day event history is confirmed current. No trail required to view the last 90 days.

### CloudTrail Trails (Extended Retention)
- For retention **beyond 90 days**, you must create a **Trail**
- Trails deliver log files to an **S3 bucket** you specify
- Trails created via the console are **multi-region by default** (best practice)
- First copy of management events delivered to S3 is **free**; S3 storage charges apply
- Analyzing trails requires **Amazon Athena** (or CloudTrail Lake — see below)

> ✅ **Best practice (AWS-verified):** Store trail logs in a **separate, dedicated AWS account** with restricted access — prevents tampering or deletion by developers/admins in the main account.

### CloudTrail Lake (Modern Alternative to Trails)
> 📝 **Note:** The course doesn't cover this, but it's worth knowing. CloudTrail Lake is a newer feature that lets you run **SQL-based queries** directly on CloudTrail event data — without needing to export to S3 and use Athena. Useful for multi-account, multi-region queries.

### Event Types
- **Management events** (logged by default): API calls that create, modify, or delete resources
- **Data events** (not logged by default, extra charge): Object-level S3 operations, Lambda invocations
- **Insights events** (optional, extra charge): Automatically detects unusual API activity patterns

---

## 8. Amazon CloudWatch

### What It Is
An **umbrella monitoring service** that collects metrics and logs from AWS services and your applications, and lets you set alarms, visualize data, and automate responses.

### The Five Core Components

| Component | What It Does |
|---|---|
| **CloudWatch Logs** | Centralized log storage for AWS services and application logs |
| **CloudWatch Metrics** | Time-ordered data points representing a variable (e.g., CPU utilization) |
| **CloudWatch Alarms** | Trigger notifications or actions when a metric crosses a threshold |
| **Amazon EventBridge** (formerly CloudWatch Events) | Triggers actions based on scheduled or event-driven rules |
| **CloudWatch Dashboards** | Visual displays of metrics and log data |

### CloudWatch Logs — Structure

```
Log Group
  └── Log Stream (one per source, e.g. EC2 instance ID or Lambda execution env)
        └── Log Events (individual timestamped log entries)
```

- **Log Group:** Logical grouping of related log streams (e.g., one per application or service)
- **Log Stream:** A sequence of log events from a single source
- **Log Event:** A single timestamped log entry

Most AWS services (Lambda, RDS, etc.) automatically send logs to CloudWatch. For EC2 application logs, you need the **CloudWatch Agent** installed on the instance.

### CloudWatch Metrics

- Pre-built metrics for all major AWS services (namespaced by service, e.g., `AWS/EC2`)
- Example EC2 metrics: `CPUUtilization`, `NetworkIn`, `NetworkOut`, `DiskReadOps`, `DiskWriteOps`
- **Custom metrics:** You can publish your own metrics from application code
- Metrics feed into Alarms and Dashboards

### CloudWatch Alarms

Monitors a metric against a **threshold** you define and takes action when breached.

**Alarm States:**
- `OK` — metric is within the threshold
- `ALARM` — metric has exceeded the threshold (do something)
- `INSUFFICIENT_DATA` — not enough data to evaluate yet

**Actions you can trigger:**
- SNS notification (email, SMS, etc.)
- Auto Scaling policy (scale out/in)
- EC2 action (stop, terminate, reboot, recover)

**Anatomy of an alarm:**
- **Threshold/Condition:** The value the metric is compared against
- **Metric:** What is being measured
- **Period:** How often it checks (e.g., every 5 minutes)
- **Evaluation Period:** How many periods to look back
- **Datapoints to Alarm:** How many of those periods must be in breach before the alarm fires

> 💡 **Practical use you've already done:** Setting a billing alarm via CloudWatch is a common first step in any new AWS account setup.

### CloudWatch Logs Insights

An **interactive query service** for searching and analyzing CloudWatch log data using a custom query language (also supports SQL and PPL as of recent updates).

- Much more powerful than basic log stream filtering
- Can query up to **20 log groups** in a single query
- Queries time out after **15 minutes** if not completed

> ⚠️ **Course correction:** The transcript states queries time out after "50 minutes." Per current AWS documentation, the timeout is **15 minutes**. Always verify technical limits against current docs.

- Query results are available for **7 days**
- AWS provides sample queries for common services (VPC Flow Logs, Lambda, CloudTrail, etc.)
- You can **save your own queries** for repeated use
- Charged per GB of log data scanned

---

## 9. AWS X-Ray

A **distributed tracing service** for debugging and analyzing microservices and serverless applications.

- Traces requests as they travel through your application across multiple services
- Shows you **where** requests slow down or fail
- Produces a **service map** visualizing how components interact
- Measures latency between services
- Integrates with Lambda, EC2, ECS, API Gateway, and more

---

## 10. ML and AI Services Overview

### Definitions
- **AI (Artificial Intelligence):** Machines performing tasks that mimic human behavior
- **ML (Machine Learning):** Machines improving at tasks without explicit programming
- **Deep Learning:** ML using artificial neural networks inspired by the human brain — best for complex problems like image recognition, NLP

### Amazon SageMaker
AWS's **flagship ML platform** — a fully managed service to build, train, and deploy ML models at scale. Supports frameworks including TensorFlow, PyTorch, and Apache MXNet.

### AI/ML Services Directory

| Service | Category | What It Does |
|---|---|---|
| **Amazon SageMaker** | ML Platform | Build, train, deploy ML models |
| **Amazon CodeGuru** | Code Analysis | ML-powered code review and performance profiling |
| **Amazon Lex** | Conversational AI | Build voice and text chatbots (powers Alexa) |
| **Amazon Personalize** | Recommendations | Real-time product/content recommendations (same tech as Amazon.com) |
| **Amazon Polly** | Text-to-Speech | Convert text to lifelike audio |
| **Amazon Rekognition** | Computer Vision | Detect and label objects, faces, and celebrities in images/video |
| **Amazon Transcribe** | Speech-to-Text | Convert audio to text |
| **Amazon Textract** | OCR | Extract text and data from scanned documents and forms |
| **Amazon Translate** | Translation | Neural machine translation |
| **Amazon Comprehend** | NLP | Find relationships and insights in text (sentiment, entities, topics) |
| **Amazon Forecast** | Time Series | ML-powered business forecasting (demand, financial, resource planning) |
| **Amazon Bedrock** | Generative AI | Access large language models (LLMs) as a managed service — AWS's ChatGPT equivalent |
| **Amazon Q Developer** (formerly CodeWhisperer) | AI Code Gen | AI code completion and generation — AWS's GitHub Copilot equivalent |
| **Amazon DevOps Guru** | Operations | ML-powered anomaly detection for operational issues |
| **Amazon Kendra** | Enterprise Search | ML-powered natural language search engine for enterprise data |
| **Amazon Fraud Detector** | Fraud Detection | Identify online payment fraud and fake accounts |
| **Amazon Lookout (3 variants)** | Anomaly Detection | Quality control for equipment, metrics, and vision |
| **Amazon Monitron** | Predictive Maintenance | Uses IoT sensors to predict equipment failures |

> ⚠️ **Name change:** The transcript calls it "Amazon Code Whisperer." AWS has since rebranded this as **Amazon Q Developer** (part of the broader Amazon Q family). The functionality is the same — AI-assisted code generation.

---

## 11. Big Data and Analytics Services

**Big Data** = massive volumes of structured or unstructured data too large to process with traditional tools.

| Service | Type | Description |
|---|---|---|
| **Amazon Athena** | Serverless SQL Query | Query CSV/JSON files in S3 using SQL; no infrastructure needed |
| **Amazon OpenSearch Service** | Search & Analytics | Managed Elasticsearch cluster for full-text search and log analytics (formerly Amazon Elasticsearch Service) |
| **Amazon EMR** | Big Data Processing | Managed Hadoop/Spark clusters for processing unstructured data (ETL, reporting) |
| **Amazon Kinesis Data Streams** | Real-time Streaming | Ingest and process real-time data streams (clickstreams, IoT, logs) |
| **Amazon Kinesis Firehose** | Serverless Streaming | Simplified, serverless delivery of streaming data to destinations (S3, Redshift, etc.) |
| **Amazon Kinesis Data Analytics** | Stream Analytics | Run SQL queries against live Kinesis data streams |
| **Amazon Kinesis Video Streams** | Video Streaming | Process and analyze real-time video streams |
| **Amazon MSK** | Managed Kafka | Fully managed Apache Kafka for real-time data pipelines |
| **Amazon Redshift** | Data Warehouse | Petabyte-scale OLAP data warehouse; fast complex queries across large datasets |
| **Amazon QuickSight** | BI Dashboards | Business intelligence tool; create visual dashboards from multiple data sources |
| **AWS Data Pipeline** | Data Movement | Automate movement of data between compute and storage services |
| **AWS Glue** | ETL Service | Move and transform data between locations; similar to DMS but more robust |
| **AWS Lake Formation** | Data Lake | Centralized, curated, secure repository for raw data at scale |
| **AWS Data Exchange** | Data Marketplace | Catalog of third-party datasets (COVID, IMDb, weather, etc.) to subscribe to or purchase |

> ⚠️ **Name change (verified):** The transcript refers to "Amazon Elastic Search Service (ES)." AWS renamed this to **Amazon OpenSearch Service** in September 2021. "Elasticsearch Service" is no longer the correct name.

> ⚠️ **Name change (verified):** The transcript refers to "Amazon Elastic Map Reduce (EMR)." The correct current name is simply **Amazon EMR** (the "Elastic MapReduce" expansion is no longer used in AWS branding).

### Amazon QuickSight — Additional Detail
- Powered by **SPICE** (Super-fast Parallel In-memory Calculation Engine) for fast queries
- Supports multiple data sources: S3, Redshift, RDS, Athena, and more
- **QuickSight ML Insights:** Anomaly detection, forecasting, and natural language narratives
- **QuickSight Q:** Ask questions about your data in plain English
- Standard and Enterprise tiers available

---

## 12. Generative AI on AWS

**Generative AI** = AI capable of generating new content (text, images, music, code) from a prompt.

- **Amazon Bedrock:** AWS's managed service providing access to foundation models (LLMs) from AWS and third-party providers (Anthropic, Meta, Mistral, etc.). The AWS equivalent of OpenAI's API.
- **Amazon Q Developer (formerly CodeWhisperer):** AI pair programmer that suggests and generates code inline in your IDE. The AWS equivalent of GitHub Copilot.

---

## 13. AWS Well-Architected Framework

### What It Is
A **whitepaper and set of best practices** created by AWS to help customers build using proven architectural patterns. Available at `aws.amazon.com/architecture/well-architected`.

> 🚨 **Important correction:** The course states the framework has **5 pillars**. AWS added a **6th pillar — Sustainability — in 2021**. The exam guide for CLF-C02 currently covers **6 pillars**. Make sure you know all six.

### The Six Pillars

| Pillar | Focus |
|---|---|
| **Operational Excellence** | Run and monitor systems; improve processes and procedures |
| **Security** | Protect data and systems; mitigate risk |
| **Reliability** | Recover from disruptions; maintain availability |
| **Performance Efficiency** | Use computing resources efficiently |
| **Cost Optimization** | Achieve lowest cost while meeting requirements |
| **Sustainability** | Minimize environmental impact of cloud workloads *(added 2021)* |

> 💡 **Trade-offs:** You don't have to maximize every pillar. You can trade off pillars based on your business context (e.g., speed to market vs. cost optimization). AWS explicitly acknowledges this.

### Key Definitions

- **Component:** Code, configuration, and AWS resources for a given requirement
- **Workload:** A set of components delivering business value
- **Milestone:** Key changes in your architecture through the product lifecycle
- **Architecture:** How components work together in a workload
- **Technology Portfolio:** Collection of workloads required for the business to operate

### General Design Principles (Apply Across All Pillars)

1. **Stop guessing capacity** — use on-demand scaling instead of over-provisioning
2. **Test systems at production scale** — spin up prod-identical environments; tear them down when done
3. **Automate to make experimentation easier** — use IaC (CloudFormation) for consistent, repeatable deployments
4. **Allow for evolutionary architectures** — support CI/CD, incremental updates, and deprecation cycles
5. **Drive architectures using data** — collect metrics automatically; make data-driven decisions
6. **Improve through game days** — deliberately inject failures to test resilience (chaos engineering)

### Structure of Each Pillar
Every pillar follows the same structure:
- **Design Principles** — high-level guidelines
- **Definition** — overview of best practice categories
- **Best Practices** — detailed guidance with specific AWS service recommendations
- **Resources** — whitepapers, videos, and additional documentation

> 📝 **For CLF-C02:** Focus on understanding the **design principles** for each pillar. The associate/professional-level exams go deeper into the specific best practices and service implementations.

---

### Design Principles by Pillar

#### Operational Excellence
- Perform operations as code (IaC — CloudFormation, CDK)
- Make frequent, small, reversible changes
- Refine operations procedures frequently (game days, post-mortems)
- Anticipate failure — pre-test recovery procedures
- Learn from all operational failures — share lessons learned

#### Security
- Implement a strong identity foundation — least privilege, centralized IAM, no long-lived credentials
- Enable traceability — monitor and audit all actions in real time (CloudTrail, CloudWatch)
- Apply security at all layers — defense in depth (edge, VPC, load balancer, instance, OS, code)
- Automate security best practices
- Protect data in transit and at rest
- Keep people away from data (automate access where possible)
- Prepare for security events — have incident response plans and runbooks

#### Reliability
- Automatically recover from failure — monitor KPIs and trigger automated responses
- Test recovery procedures — simulate failures; validate recovery
- Scale horizontally — replace one large resource with many small ones to eliminate single points of failure (multi-AZ)
- Stop guessing capacity — use auto scaling
- Manage change in automation — use IaC to make tracked, reviewable infrastructure changes

#### Performance Efficiency
- Democratize advanced technology — use managed AWS services instead of DIY (SageMaker, Aurora, etc.)
- Go global in minutes — deploy to multiple regions to reduce latency
- Use serverless architectures — eliminate server management overhead
- Experiment more often — try different instance types, storage, and configs; right-size resources
- Consider mechanical sympathy — understand how cloud services work internally and align your usage pattern

#### Cost Optimization
- Implement Cloud Financial Management — dedicate time and tooling to cost monitoring (Cost Explorer, Budgets)
- Adopt a consumption model — pay only for what you use (on-demand, serverless)
- Measure overall efficiency — track cost per unit of business output
- Stop spending money on undifferentiated heavy lifting — let AWS manage servers, patching, and infrastructure
- Analyze and attribute expenditure — tag resources to track cost per workload/team

#### Sustainability *(Not covered in the course — added here for completeness)*
- Understand your impact — measure the environmental footprint of your workloads
- Establish sustainability goals — set long-term targets for energy and emissions reduction
- Maximize utilization — right-size resources to avoid idle compute
- Anticipate and adopt new, more efficient technologies — move to newer instance types and services
- Use managed services — AWS optimizes shared infrastructure for energy efficiency
- Reduce the downstream impact of your cloud workloads — optimize code and data to require less compute

---

### Amazon Leadership Principles (Referenced in the Framework)
The Well-Architected Framework references Amazon's leadership principles as the mechanism by which Amazon's distributed teams stay aligned. Key principles relevant to cloud architecture:

- **Customer Obsession** — start with the customer; work backwards
- **Invent and Simplify** — favor simple solutions over complex ones
- **Ownership** — act like an owner; take responsibility for your architecture
- **Frugality** — accomplish more with less; constraints drive innovation
- **Dive Deep** — stay connected to details; validate assumptions with data
- **Earn Trust** — maintain high standards; follow through

Full list available at: `amazon.jobs/en/principles`

---

*Key corrections made: Lambda billing (1ms increments, not 100ms), Well-Architected Framework (6 pillars, not 5 — Sustainability added 2021), CloudWatch Logs Insights timeout (15 min, not 50 min), Amazon ES renamed to OpenSearch Service, CodeWhisperer renamed to Amazon Q Developer.*
*Last updated: February 2026*