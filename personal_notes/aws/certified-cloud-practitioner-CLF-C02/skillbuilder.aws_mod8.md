# AWS Module 8 — AI/ML and Data Analytics

---

## 1. Artificial Intelligence vs Machine Learning

### Artificial Intelligence (AI)

AI is the broad field of enabling computers to perform tasks that normally require human intelligence.

**Examples:**
- Speech recognition
- Language translation
- Image recognition
- Decision making
- Conversational assistants

### Machine Learning (ML)

Machine Learning is a subset of AI where systems **learn patterns from data** instead of following explicitly programmed rules.

**Classical Programming:**
```
Data + Rules → Output
```
Programmers define the logic.

```python
# Example
if temperature > 100:
    alert()
```

**Machine Learning:**
```
Data + Output → Model learns rules
```
The model discovers patterns in the data and makes predictions.

**Examples:**
- Fraud detection
- Product recommendations
- Spam filtering
- Image recognition

---

## 2. Types of Machine Learning

### Supervised Learning
- Uses **labeled datasets** to train models
- **Examples:** Email spam detection, credit risk prediction, price prediction
- The model learns a mapping between inputs and known outputs

### Unsupervised Learning
- Uses **unlabeled datasets**
- Goal: discover hidden patterns or structures
- **Examples:** Customer segmentation, anomaly detection, market basket analysis

### Reinforcement Learning
- Model learns by interacting with an environment and receiving **rewards or penalties**
- **Examples:** Robotics, game playing, recommendation systems

---

## 3. The Machine Learning Workflow

### Stage 1 — Data Collection
Gather data from sources such as:
- Applications
- Databases
- Logs
- Sensors
- IoT devices

### Stage 2 — Data Preparation
Data must be cleaned and transformed. Tasks include:
- Removing duplicates
- Handling missing values
- Normalizing formats
- Feature engineering

### Stage 3 — Model Training
- Algorithms learn patterns from historical data
- Requires compute resources and large datasets

### Stage 4 — Model Evaluation
Models are tested against validation datasets. Common metrics:
- Accuracy
- Precision
- Recall
- F1 score

### Stage 5 — Deployment
The trained model is deployed into production where it generates predictions.

---

## 4. Amazon SageMaker

### Core Definition
Amazon SageMaker is a **fully managed service** used to build, train, and deploy machine learning models. It removes the need to manage underlying infrastructure.

### Key Capabilities
- Data preparation
- Model training
- Model tuning
- Deployment
- Monitoring

### Key Features

| Feature | Description |
|---|---|
| SageMaker Studio | Integrated ML development environment |
| Training Jobs | Train models on large datasets |
| Model Hosting | Deploy models to production endpoints |
| AutoML | Automatically builds ML models |
| JumpStart | Pre-built ML solutions |

### When to Use
- Custom machine learning models
- Training models on large datasets
- Deploying ML APIs

---

## 5. AWS Pre-Built AI Services

AWS provides **pre-trained AI services** that do not require ML expertise. These services use ML models behind the scenes.

### Amazon Personalize
Creates **real-time recommendation systems**.
- **Examples:** Product recommendations, media recommendations, personalized search
- **Used by:** E-commerce platforms, streaming platforms, retail websites

### Amazon Comprehend
**Natural Language Processing (NLP)** service used to analyze text.
- **Capabilities:** Sentiment analysis, entity recognition, topic modeling, key phrase extraction
- **Example use case:** Analyzing customer reviews

### Amazon Rekognition
**Image and video analysis** service.
- **Capabilities:** Object detection, facial recognition, activity detection, image moderation
- **Used in:** Security systems, media analysis, content moderation

### Amazon Polly
Converts **text to speech**.
- **Used in:** Voice assistants, audiobooks, accessibility tools, interactive voice responses
- Produces realistic spoken audio

### Amazon Transcribe
Converts **speech to text**.
- **Examples:** Meeting transcription, call center analytics, subtitles for videos

### Amazon Translate
Provides **real-time language translation**.
- **Example:** Translate website content into multiple languages

### Amazon Lex
Used to build **conversational chatbots and voice interfaces**.
- Powers technologies similar to Amazon Alexa
- **Example:** Customer support chatbot

---

## 6. Generative AI and Foundation Models

### Generative AI
Generative AI **creates new content** based on patterns learned from data.
- **Examples:** Text generation, code generation, image generation, audio synthesis

### Foundation Models (FMs)
Large machine learning models trained on **massive datasets**.

**Key Characteristics:**
- Pre-trained on vast datasets
- Can perform multiple tasks
- Adaptable to different use cases

**Examples of tasks:**
- Text summarization
- Chatbots
- Image generation
- Code generation

---

## 7. Amazon Bedrock

Amazon Bedrock is a **fully managed service** for building generative AI applications using foundation models.

### Key Capability
Provides access to multiple foundation models through a **single unified API**.

**Available model providers:**
- Amazon Titan
- Anthropic Claude
- Stability AI
- Meta

### Benefits
- No infrastructure management
- Easy model experimentation
- Secure integration with AWS services

---

## 8. Amazon Q

Amazon Q is an **AI-powered assistant** designed for business and development use cases.

### Amazon Q Business
Helps employees interact with company knowledge.
- **Capabilities:** Answer questions, retrieve internal documentation, summarize company knowledge, assist with decision making
- **Example:** Internal enterprise AI assistant

### Amazon Q Developer
Helps developers with:
- Code generation
- Debugging
- Documentation
- Code explanations

---

## 9. Data Analytics Concepts

Organizations generate large volumes of data. Analytics helps extract insights from this data. Two major storage architectures are used.

### Data Lake
Stores large volumes of **raw, unstructured data**.
- **Examples:** Logs, images, CSV files, JSON, sensor data
- **AWS Service:** Amazon S3

### Data Warehouse
**Structured database** optimized for analytics queries.
- **Examples:** Business intelligence, financial reporting, data dashboards
- **AWS Service:** Amazon Redshift

---

## 10. Data Pipeline Concepts

### Definition
A data pipeline is an **automated process** that collects, transforms, and moves data between systems.
- **Goal:** Deliver clean, usable data to analytics and machine learning systems

### ETL Process

**ETL** stands for **Extract → Transform → Load**

#### Extract
Collect data from sources such as:
- Databases
- Applications
- Logs
- APIs

#### Transform
Clean and modify data. Examples:
- Convert formats
- Remove duplicates
- Normalize fields

#### Load
Store the processed data in a destination. Examples:
- Data lakes
- Data warehouses
- Analytics tools

---

## 11. Real-Time Data Streaming

Some applications require **real-time data ingestion**.

**Examples:**
- Stock trading
- Clickstream analytics
- IoT monitoring

### Amazon Kinesis
AWS service used for **real-time data streaming**.

**Capabilities:**
- Ingest streaming data
- Process data in real time
- Analyze streaming datasets

| Service | Function |
|---|---|
| Kinesis Data Streams | Real-time streaming ingestion |
| Kinesis Data Firehose | Deliver streaming data to S3 or Redshift |
| Kinesis Data Analytics | Real-time analytics |

---

## 12. Example Data Pipeline Architecture

```
Application
   ↓
Amazon DynamoDB
   ↓
Amazon Kinesis Data Streams
   ↓
Amazon Data Firehose
   ↓
Amazon S3 (Data Lake)
   ↓
AWS Glue Data Catalog
   ↓
Amazon Athena
   ↓
Amazon SageMaker
```

### Pipeline Breakdown

| Stage | Service | Description |
|---|---|---|
| Data Ingestion | Amazon Kinesis | Collects streaming data |
| Data Processing | AWS Lambda | Transforms incoming data (e.g., JSON → CSV) |
| Data Storage | Amazon S3 | Acts as the data lake |
| Data Cataloging | AWS Glue Data Catalog | Stores metadata describing datasets |
| Data Querying | Amazon Athena | SQL queries directly on S3 data |
| Machine Learning | Amazon SageMaker | Trains models using stored data |

---

## 13. Amazon Athena

**Serverless query service** that allows SQL queries on data stored in S3.

**Key Features:**
- No infrastructure management
- Pay per query
- Integrates with AWS Glue Data Catalog

**Example query:**
```sql
SELECT * FROM sales_data
WHERE revenue > 10000;
```

---

## 14. Amazon QuickSight

**Business intelligence (BI) service** used to create dashboards, visualizations, and reports.

**Features:**
- Interactive dashboards
- ML-powered insights
- Serverless architecture

---

## 15. Data Analytics Architecture Summary

```
Data Sources
     ↓
Kinesis / Firehose
     ↓
S3 (Data Lake)
     ↓
Glue Data Catalog
     ↓
Athena / Redshift
     ↓
QuickSight Dashboards
```

---

## 16. Core Service Recognition (Exam Focus)

| Requirement | AWS Service |
|---|---|
| Build and train ML models | Amazon SageMaker |
| Recommendation systems | Amazon Personalize |
| Text to speech | Amazon Polly |
| Speech to text | Amazon Transcribe |
| Language translation | Amazon Translate |
| Chatbots | Amazon Lex |
| Image analysis | Amazon Rekognition |
| Text analytics | Amazon Comprehend |
| Generative AI models | Amazon Bedrock |
| Enterprise AI assistant | Amazon Q Business |
| Real-time streaming data | Amazon Kinesis |
| Query data in S3 | Amazon Athena |
| Data lake storage | Amazon S3 |
| Data warehouse analytics | Amazon Redshift |
| Business dashboards | Amazon QuickSight |

---

## Final Mental Model

```
AI Services
    ↓
Pre-built intelligence (Polly, Rekognition, Comprehend, Lex, Translate, Transcribe, Personalize)

Machine Learning Platform
    ↓
SageMaker (build → train → deploy → monitor)

Generative AI
    ↓
Bedrock + Foundation Models (single API, multiple providers)

Enterprise AI Assistant
    ↓
Amazon Q (Business + Developer)

Data Analytics
    ↓
S3 (lake) → Glue (catalog) → Athena (query) → QuickSight (visualize)

Data Warehouse
    ↓
Amazon Redshift

Streaming Data
    ↓
Kinesis (ingest → process → deliver)
```