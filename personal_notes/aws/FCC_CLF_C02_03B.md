# AWS Certified Cloud Practitioner - Part 3B Study Notes
## Database Services Deep Dive

**Study Date:** February 10, 2026  
**Source:** freeCodeCamp CLF-C02 Course (Hours 7:00-8:00)  
**Topics:** Databases, RDS, Aurora, DynamoDB, Redshift, NoSQL Services

---

## 🗄️ Database Fundamentals

### What is a Database?

**Definition:** A data store that stores semi-structured and structured data

**Key Characteristic:** Requires formal design and modeling techniques (more complex than simple data stores)

### Database Categories

#### 1. Relational Databases

**Structure:** 
- Strongly represents tabular data
- Tables, rows, and columns
- Structured data

**Orientations:**
- **Row-oriented:** Traditional (most common)
- **Column-oriented:** Data warehouses

**Languages:** SQL (Structured Query Language)

**Example:**
```sql
SELECT * FROM customers WHERE country = 'USA';
```

**Returns:** Tables with rows and columns

---

#### 2. Non-Relational Databases (NoSQL)

**Structure:**
- Semi-structured
- May or may not resemble tabular data
- Flexible schema

**Types:**
- Key-value stores
- Document databases
- Graph databases
- Time-series databases

---

### Database Functionality

Relational databases provide:

1. **Specialized Query Language (SQL)**
   - Retrieve data efficiently
   - Complex joins and aggregations

2. **Specialized Modeling Strategies**
   - Optimize retrieval for different use cases
   - Indexing, normalization

3. **Fine-tuned Control**
   - Transform data into useful structures
   - Generate reports

4. **Default Assumption**
   - When someone says "database" → usually means relational, row-oriented
   - Examples: PostgreSQL, MySQL

---

## 📊 Data Warehouses

### Definition

**Data Warehouse:** Relational data store designed for analytical workloads (column-oriented)

### Why Column-Oriented?

**Companies' Needs:**
- Terabytes of data
- Millions of rows
- Need fast analytics reports

**Optimization:**
- Column-oriented for fast aggregation
- Quickly aggregate column data

### Key Concept: Aggregation

**Aggregation** = Grouping data to find totals or averages

**Examples:**
- SUM(sales) by region
- AVG(temperature) by month
- COUNT(users) by country

---

### Data Warehouse Characteristics

#### "Hot" Data
- **Definition:** Can return queries very fast
- **Despite:** Vast amounts of data stored

#### Infrequent Access
- **Not for:** Real-time reporting
- **Typical Use:** 
  - Once or twice a day
  - Once a week
  - Generate business/user reports

**Note:** Frequency varies by service and use case

#### Data Sources

**Primary Source:** Relational databases

**Process:**
```
Relational DB → ETL/ELT → Data Warehouse → Analytics/Reports
```

**ETL Tools:**
- Extract, Transform, Load
- Can consume from other sources (requires transformation)

---

### Data Warehouse vs Database

| Feature | Database (OLTP) | Data Warehouse (OLAP) |
|---------|----------------|----------------------|
| **Purpose** | Transactions | Analytics |
| **Queries** | Simple, fast | Complex, aggregated |
| **Data** | Current | Historical + Current |
| **Users** | Many (concurrent) | Few (analysts) |
| **Size** | GB to TB | TB to PB |
| **Orientation** | Row-oriented | Column-oriented |

**OLTP** = Online Transaction Processing  
**OLAP** = Online Analytical Processing

---

## 🔑 Key-Value Stores

### Definition

**Key-Value Store:** Type of non-relational database (NoSQL) using simple key-value method

### Characteristics

**Structure:**
```
Key (unique) → Value (binary data)
```

**Features:**
- "Dumb and fast"
- Lack features like:
  - Relationships
  - Indexes
  - Aggregation

**Note:** Managed solutions may "polyfill" some features

---

### How Key-Value Stores Work

**Under the Hood:**
```
Key: "user123" → Value: [01010110...] (binary data)
```

**Interpretation:**
- How the store interprets the value determines functionality
- Document databases are key-value stores that interpret values as documents

**Common Storage Pattern:**
```
Key: "user123" → Value: {
  "name": "Alice",
  "email": "alice@example.com",
  "age": 30
}
```

**Associative Array:** Even stores that look like tables (rows/columns) are actually key-value underneath

---

### Schema-less Nature

**Why Schema-less?**
- Underneath it's just key → binary value
- No enforced structure

**Benefit:**
```
Row 1: { name, email, age }
Row 2: { name, email }           // Different columns OK!
Row 3: { name, email, age, city }
```

Each "row" can have different attributes

---

### Advantages

1. **Scalability**
   - Scale well beyond relational databases
   - Horizontal scaling (add more servers)

2. **Performance**
   - Very fast reads/writes
   - Simple design = speed

3. **Flexibility**
   - No rigid schema
   - Easy to adapt to changing data

**Trade-off:** Fewer features than relational databases

---

## 📄 Document Stores

### Definition

**Document Store:** NoSQL database that stores documents as primary data structure

**Documents can be:**
- XML
- JSON
- BSON (Binary JSON)
- JSON-like formats

---

### Relationship to Key-Value Stores

**Document stores are subclasses of key-value stores**

Key difference: Values are interpreted as structured documents

---

### Document Store vs Relational Database

**Translation Table:**

| Relational | Document Store |
|------------|----------------|
| Tables | Collections |
| Rows | Documents |
| Columns | Fields |
| Indexes | Indexes (yes, they have them!) |
| Joins | Embedding & Linking |

---

### Characteristics

**Similarities to Relational:**
- Can have indexes
- Can represent relationships (embedding/linking)
- Query capabilities

**Differences:**
- Better scalability
- Flexible schema
- Fewer guarantees (ACID compliance varies)

**Reality:** Document stores = key-value stores with additional features built on top

---

## 🗃️ AWS NoSQL Database Services

### Amazon DynamoDB

#### Overview
- **Type:** Serverless NoSQL key-value AND document database
- **Performance:** Consistent data returned in ≤1 second (single-digit millisecond)
- **Scale:** Billions of records
- **Management:** No shard management required
- **Status:** ⭐ **AWS's flagship database service**

#### Key Phrase
**"Massively scalable database"** = Think DynamoDB

#### Amazon's Migration Story (2019)

**Before:**
- 7,500 Oracle databases
- 75 petabytes of data

**After (DynamoDB):**
- **60% cost reduction**
- **40% latency reduction**

**Lesson:** Testimonial showing relational → NoSQL benefits at scale

---

### Amazon DocumentDB

#### Overview
- **Type:** NoSQL document database
- **Compatibility:** MongoDB-compatible
- **Why it exists:** Open-source licensing issues with MongoDB

#### Background
- MongoDB very popular with developers
- Licensing conflicts with managed services
- AWS built their own MongoDB-compatible database

#### When to Use
**Need MongoDB?** → Use DocumentDB (on AWS)

---

### Amazon Keyspaces

#### Overview
- **Type:** Fully managed Apache Cassandra database
- **Compatibility:** Cassandra-compatible

#### About Cassandra
- Open-source NoSQL database
- Key-value database
- Column-store database (similar to DynamoDB)
- Additional functionality beyond basic key-value

#### When to Use
**Need Apache Cassandra?** → Use Amazon Keyspaces

---

## 🐘 Relational Database Services (RDS)

### Amazon RDS Overview

**RDS = Relational Database Service**

**Key Concepts:**
- Relational = SQL
- SQL = Online Transaction Processing (OLTP)
- Most commonly used database type by tech companies/startups

**Why popular?** Easy to use, well-understood, ACID compliant

---

### RDS Supported Engines

#### 1. MySQL
- **Status:** Most popular open-source SQL database
- **Owner:** Oracle (acquired via Sun Microsystems purchase)
- **History:** Originally not supposed to go to Oracle
- **Fork:** MariaDB created by original MySQL creators to avoid Oracle control

#### 2. PostgreSQL
- **Abbreviation:** psql
- **Status:** Most popular open-source SQL database among developers
- **Features:** Rich feature set (more than MySQL)
- **Trade-off:** Added complexity
- **Personal note from instructor:** Preferred choice

#### 3. MariaDB
- **Origin:** Fork of MySQL
- **Created by:** Original MySQL creators
- **Why:** Keep popular DB from Oracle control
- **Compatibility:** Drop-in replacement for MySQL

#### 4. Oracle Database
- **Type:** Proprietary SQL database
- **Used by:** Enterprise companies
- **License:** Required purchase

#### 5. Microsoft SQL Server
- **Type:** Microsoft's proprietary SQL database
- **License:** Required purchase
- **Versions:** Multiple editions available

#### 6. Amazon Aurora
- **Type:** Fully managed database
- **Compatibility:** MySQL (5x faster) OR PostgreSQL (3x faster)
- **Special status:** Almost separate service, powered by RDS

---

### Amazon Aurora

#### Performance Claims
- **MySQL-compatible:** 5x faster than standard MySQL
- **PostgreSQL-compatible:** 3x faster than standard PostgreSQL

#### When to Use
**Need:** Highly available, durable, scalable, and secure relational database for PostgreSQL or MySQL → **Aurora**

---

### Aurora Serverless

#### Overview
- **Type:** On-demand version of Aurora
- **Scaling:** Automatic scaling to zero

#### When to Use
- Want Aurora benefits
- Can accept cold starts
- Don't have lots of traffic/demand
- Variable/unpredictable workloads

#### Trade-offs
- Cold starts (delay when scaling from zero)
- Slightly different pricing model

---

### RDS on VMware

#### Overview
- Deploy RDS-supported engines to on-premise data centers
- **Requirement:** Data center must use VMware for server virtualization

#### When to Use
**Need:** Databases managed by RDS in your own data center

**Note:** Instructor notices spelling mistake in slide ("on" vs full word)

---

## 🔧 Other AWS Database Services

### Amazon Redshift

#### Overview
- **Type:** Petabyte-size data warehouse
- **Purpose:** Online Analytical Processing (OLAP)
- **Cost:** Expensive (keeps data "hot")

#### "Hot" Data Explained
- Run complex queries on large data
- Get results back very fast
- Trade cost for speed

#### When to Use
**Need:** Quickly generate analytics/reports from large amounts of data → **Redshift**

---

### Amazon ElastiCache

#### Overview
- **Type:** Managed in-memory caching database
- **Engines:** Redis OR Memcached

#### When to Use
**Need:** Improve application performance by adding caching layer in front of:
- Web servers
- Databases

#### Benefit
- Microsecond latency
- Reduce database load
- Scale read-intensive applications

---

### Amazon Neptune

#### Overview
- **Type:** Managed graph database
- **Data Model:** Interconnected nodes
- **Query Language:** Gremlin (most cloud providers use this)

#### Use Cases
- **Fraud detection:** Map fraud rings
- **Social networks:** User relationships
- **Recommendation engines:** Connection-based recommendations
- **Knowledge graphs:** Highly relational data

#### When to Use
**Need:** Understand connections between data → **Neptune**

---

### Amazon Timestream

#### Overview
- **Type:** Fully managed time-series database
- **Performance:** 1000x faster than relational databases (for time-series)

#### Use Cases
- **IoT devices:** Send time-sensitive data
- **DevOps monitoring:** Metrics over time
- **Application metrics:** Track changes over time

#### When to Use
**Need:** Measure how things change over time → **Timestream**

---

### Amazon QLDB (Quantum Ledger Database)

#### Overview
- **Type:** Fully managed ledger database
- **Features:**
  - Transparent
  - Immutable
  - Cryptographically verifiable transaction logs

#### Use Cases
- **Financial transactions:** History that can be trusted
- **Supply chain:** Track ownership changes
- **Compliance:** Audit trails

#### When to Use
**Need:** Record history of financial activities that can be trusted → **QLDB**

---

### AWS Database Migration Service (DMS)

#### Overview
- **Type:** Migration service (not a database)
- **Purpose:** Migrate databases to AWS

#### Features
- **Minimal downtime:** Continuous replication
- **Flexibility:** Multiple migration scenarios

#### Migration Types

**1. Homogeneous Migration**
- Same database engine
- Example: MySQL → MySQL
- Simpler process

**2. Heterogeneous Migration**
- Different database engines
- Example: Oracle → PostgreSQL
- **Requires:** Schema Conversion Tool (SCT)

**3. Continuous Replication**
- **CDC:** Change Data Capture
- Keep databases in sync

#### Migration Scenarios
- On-premise → AWS
- AWS → AWS (different accounts)
- Different SQL engines
- SQL → NoSQL

**Note:** Covered in greater detail elsewhere in course

---

## 🧪 Hands-On: DynamoDB

### Creating a Table

**Table Name:** `my-dynamodb-table`

**Partition Key:** `email` (String)

**Sort Key:** `created_at` (String)

**Key Types Available:**
- String
- Binary
- Number

---

### Settings

#### Default Settings
- Provisioned capacity mode
- 5 read/write units
- No secondary indexes
- KMS encryption

#### Custom Settings Explored

**Capacity Modes:**

1. **On-Demand**
   - Pay for actual reads/writes used
   - Simplifies billing
   - Good for unpredictable workloads

2. **Provisioned**
   - Guarantee performance level
   - Example: 1,000 read/write per second
   - Pay for provisioned capacity (even if unused)
   - Cheaper if usage is predictable

---

### Secondary Indexes

**Not created in demo, but available:**
- **Purpose:** Alternate ways to query data
- Can be added later

---

### Encryption

**Options:**

1. **Owned by Amazon DynamoDB**
   - Similar to SSE-S3
   - AWS manages keys

2. **AWS managed CMK**
   - KMS-managed
   - More control

**Cost:** $0.21/month (in demo)

**Best Practice:** Always turn on encryption

---

### Adding Data

**Created Item:**
```json
{
  "email": "andrew@exampro.co",
  "created_at": "2025-05-05",
  "today": true,
  "food": ["banana", "pizza"]
}
```

**Field Types Used:**
- String (email, created_at)
- Boolean (today)
- List (food)

**Schema Flexibility:** Each item can have different attributes

---

### Querying Data

#### Scan
- Returns ALL items
- Inefficient for large tables

#### Query
- Filter by key
- More efficient

#### PartiQL Editor
- **PartiQL:** SQL-compatible query language for DynamoDB
- Query example:
```sql
SELECT email FROM "my-dynamodb-table"
```

**Result:** Returns email field from items

**Additional fields:**
```sql
SELECT email, food FROM "my-dynamodb-table"
```

---

### DynamoDB Streams

**Purpose:** Stream data changes to trigger actions

**Retention:** Can stream to other services

**Use Cases:**
- Trigger Lambda functions
- Real-time processing
- Replication

---

### Cleanup

**Delete Table:**
- Option to delete CloudWatch alarms
- Option to create backup (declined in demo)
- Confirm deletion

---

## 🐘 Hands-On: Amazon RDS

### Creating RDS Instance

#### Engine Selection

**Available Engines:**
- Amazon Aurora (MySQL/PostgreSQL compatible)
- MySQL
- MariaDB
- PostgreSQL ✓ (selected)
- Oracle
- Microsoft SQL Server

**License Notes:**
- **SQL Server:** Comes with license (all editions)
- **Oracle:** Bring Your Own License (BYOL) via License Manager

---

#### Templates

**Options:**
1. **Production:** High availability, expensive
2. **Dev/Test:** ✓ Selected for cost
3. **Free Tier:** T2 instances

**Note:** Template affects default settings, can customize

---

#### Settings

**DB Identifier:** `my-database`

**Master Username:** `postgres` (default)

**Master Password:** `Testing123!`
- Capital T
- Exclamation mark
- Meets complexity requirements

---

#### Instance Configuration

**Instance Class:**

**Searched for:** T2 Micro (free tier)
- Not available in dropdown
- T3 Micro appears to be new free tier

**Selected:** T3 Micro (burstable class)

**Instance Classes:**
- **Burstable:** T3, T4g (cheap, for variable loads)
- **Standard:** M classes (consistent performance)
- **Memory Optimized:** R, X classes

---

#### Storage

**Size:** Default (20 GB)

**Auto Scaling:** Disabled (keep costs down)

---

#### Availability & Durability

**Multi-AZ:** ✗ Disabled
- Would create standby instance
- Significantly increases cost
- Production feature

**Single AZ:** Development/testing

---

#### Connectivity

**Public Access:** No
- Not accessible from internet
- Requires VPC configuration to access

**VPC:** Default VPC created automatically

---

#### Database Authentication

**Options:**
1. Password authentication ✓
2. Password and IAM authentication
3. Password and Kerberos

**Selected:** Password authentication (simplest)

---

#### Additional Configuration

**Database Name:** `mydatabase`
- Must specify to create initial database

**PostgreSQL Version:** Selected from dropdown

**Backups:** ✗ Disabled
- Would slow instance launch
- Production should enable

**Encryption:** ✓ Enabled
- Always recommended
- Same cost

**Performance Insights:** Enabled
- Retention: 7 days (minimum)

**Enhanced Monitoring:** ✗ Disabled
- Additional cost
- More detailed metrics

**Delete Protection:** ✗ Disabled
- Prevents accidental deletion
- Good for production

---

### Instance Launch

**Estimated Cost:** ~$0.02/hour (shown, then preview disappeared)

**Actual Cost:** Shown as $118/month initially
- Changed with settings
- Dev/Test template much cheaper

**Launch Time:** Several minutes

---

### RDS Capabilities (Not Demonstrated)

**Connection Methods:**
- Endpoint (hostname)
- Port (5432 for PostgreSQL)
- Tools: TablePlus, pgAdmin, etc.

**Out of Scope:** 
- Actual connection
- Query execution
- Solutions Architect/Developer level

**Demo Purpose:** Show how easy it is to create RDS instance

---

### Cleanup

**Delete Database:**
1. Select database
2. Actions → Delete
3. Confirm: type "delete me"

**Note:** If backups enabled, takes longer to delete

---

## 🔴 Hands-On: Amazon Redshift

### Overview

**Warning:** Redshift is expensive
- Not for day-to-day use
- Demo: Watch only (don't have to create)

---

### Creating Cluster

#### Free Trial Option

**Requirements:**
- Organization has never created a cluster
- Limited time

**Features:**
- Configure for learning
- When trial ends: delete cluster to avoid charges

---

#### Configuration

**Node Type:** dc2.large
- 2 vCPUs
- 160 GB storage

**Pricing:** (Instructor couldn't find specific price)
- "Not cheap"
- Significant cost even for smallest option

---

#### Sample Data

**Option:** Load sample data into cluster
- **Dataset:** "Ticket" sample data

**Benefit:** Can query immediately without setup

---

#### Credentials

**Admin User:** `awsuser`

**Password:** `Testing123456!`
- Capital T
- Exclamation mark at end

---

### Cluster Launch

**Launch Time:** Unknown (instructor paused recording)

**Result:** "A lot faster than expecting"

---

### Query Interface

#### Redshift Query Editor v2

**Access:** Click "Query data" → Redshift Query Editor v2

**Features:**
- Nice UI
- In-console querying (no external tools needed)

**Historical Note:** Previously required JDBC/ODBC driver (Java .jar file)

---

#### Sample Data Loading

**Expected:** Data auto-loaded

**Reality:** Had to manually load

**Instructions:** "Load the sample data from Amazon S3"

**Steps:**
1. Found tutorial
2. CREATE TABLE statements
3. COPY commands to load from S3

---

#### Loading Process

**7 Tables to Create:**
- Date
- Event
- Sales
- (others)

**Process:**
- Run CREATE TABLE for each
- Some showed "already exists" (auto-created during wait)

**Confusion:** Whether data was pre-loaded or not

---

#### Querying

**First Query Attempted:**
```sql
SELECT * FROM sales LIMIT 100;
```

**Error:** "relation sales does not exist"

**Solution:** Wait for data to load

**Successful Query:**
```sql
SELECT * FROM sales LIMIT 100;
```

**Result:** Returns 100 rows of sample data

---

### Query Features

#### Charting

**Feature:** Can chart query results

**Example:** Created visualization

**Export Options:**
- Save chart
- Cannot export to QuickSight directly
- Would need to rebuild in QuickSight

---

### Data Marketplace

**Feature:** Pull data from AWS Data Marketplace

**Note:** Looks nice, not explored in demo

---

### Integration

**QuickSight:** 
- Business intelligence tool
- Would integrate with Redshift
- Not demonstrated

---

### Cleanup

**Delete Cluster:**
1. Go to Clusters
2. Select cluster
3. Delete
4. **Snapshot:** No (don't create final snapshot)
5. Confirm deletion

**Important:** Redshift is expensive - verify deletion!

---

## 🎯 Key Exam Tips - Second Hour

### Database Fundamentals
1. **Relational = SQL = OLTP** (row-oriented usually)
2. **Data Warehouse = OLAP** (column-oriented)
3. **NoSQL** includes key-value, document, graph, time-series

### Key-Value vs Document
1. **Key-value:** Simple, fast, "dumb"
2. **Document:** Key-value + structure interpretation
3. **Both:** Schema-less, horizontally scalable

### AWS Database Services Quick Reference

**Relational:**
- **RDS:** Managed SQL (MySQL, PostgreSQL, etc.)
- **Aurora:** 5x MySQL / 3x PostgreSQL performance
- **Aurora Serverless:** On-demand Aurora

**NoSQL:**
- **DynamoDB:** ⭐ Flagship, key-value/document, serverless
- **DocumentDB:** MongoDB-compatible
- **Keyspaces:** Cassandra-compatible

**Analytics:**
- **Redshift:** Petabyte-scale data warehouse
- **ElastiCache:** In-memory cache (Redis/Memcached)

**Specialized:**
- **Neptune:** Graph database
- **Timestream:** Time-series (IoT, monitoring)
- **QLDB:** Immutable ledger

**Migration:**
- **DMS:** Database Migration Service

---

### DynamoDB Specifics
1. **Flagship service** - remember this!
2. **Single-digit millisecond** latency
3. **Partition key required**, sort key optional
4. **Capacity modes:** On-Demand vs Provisioned
5. **PartiQL:** SQL-like query language
6. **Serverless** - no server management

### RDS Specifics
1. **6 engines:** MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Aurora
2. **Aurora:** MySQL/PostgreSQL compatible, faster
3. **Multi-AZ:** High availability (production)
4. **Read Replicas:** Scale reads
5. **Automated backups:** 1-35 days

### Redshift Specifics
1. **Data warehouse** service
2. **OLAP** not OLTP
3. **Expensive** but fast for analytics
4. **Column-oriented** storage
5. **Query editor** built into console

---

## 📝 Practice Questions - Hour 2

**Q1:** What database service would you use for a massively scalable, serverless NoSQL database?
<details>
<summary>Answer</summary>
DynamoDB - AWS's flagship database service, serverless key-value/document database
</details>

**Q2:** What's the difference between OLTP and OLAP?
<details>
<summary>Answer</summary>
OLTP = Online Transaction Processing (databases, row-oriented)
OLAP = Online Analytical Processing (data warehouses, column-oriented)
</details>

**Q3:** Which RDS engine is compatible with MySQL but 5x faster?
<details>
<summary>Answer</summary>
Amazon Aurora (MySQL-compatible version)
</details>

**Q4:** What service would you use for IoT time-series data?
<details>
<summary>Answer</summary>
Amazon Timestream - fully managed time-series database
</details>

**Q5:** What are the two capacity modes for DynamoDB?
<details>
<summary>Answer</summary>
On-Demand (pay per request) and Provisioned (guarantee capacity)
</details>

**Q6:** Which database service provides immutable, cryptographically verifiable transaction logs?
<details>
<summary>Answer</summary>
Amazon QLDB (Quantum Ledger Database)
</details>

**Q7:** What tool is needed for heterogeneous database migrations with DMS?
<details>
<summary>Answer</summary>
Schema Conversion Tool (SCT) - converts schema between different database engines
</details>

---

## 🔄 Next Steps

Continue to **Part 3C** for:
- Networking Services (VPC, Subnets, Security Groups)
- CloudFront CDN
- EC2 Deep Dive (Instance Types, Pricing, Placement Groups)
- Hands-on networking configuration

---

**Study Tip:** Focus on knowing WHEN to use each database service rather than memorizing every feature. The exam tests service selection based on use cases.
