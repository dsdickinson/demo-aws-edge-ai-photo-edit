Cost-Optimized Edge AI Processing Pipeline

Jetson + AWS Serverless Architecture

🚀 Overview

This project implements a cost-optimized, event-driven edge AI pipeline that processes wildlife images using a GPU-enabled NVIDIA Jetson device and a fully serverless AWS backend.

The system performs:
	1.	Image upload to cloud storage
	2.	Job queueing via message queue
	3.	Edge GPU inference using YOLOv8
	4.	Metadata generation
	5.	Serverless ingestion and storage

Designed to run at $0–$3 per month at demo scale.

⸻

🏗 Architecture

AWS Services Used
	•	Amazon S3 – raw image storage
	•	Amazon SQS – decoupled job queue
	•	Amazon API Gateway – secure ingestion endpoint
	•	AWS Lambda – metadata processor
	•	Amazon DynamoDB – image metadata index

Edge Component:
	•	NVIDIA Jetson running Dockerized YOLOv8 GPU inference

⸻

🔄 Data Flow
	1.	Image uploaded to S3
	2.	S3 object key sent to SQS
	3.	Jetson long-polls queue
	4.	Jetson downloads image
	5.	YOLOv8 GPU inference runs locally
	6.	Metadata POSTed to API Gateway
	7.	Lambda writes structured record to DynamoDB

Fully asynchronous and loosely coupled.

⸻

💡 Design Decisions & Tradeoffs

Why SQS instead of direct Lambda trigger?
	•	Prevents runaway compute costs
	•	Allows offline Jetson processing
	•	Adds retry safety

Why edge inference instead of EC2 GPU?
	•	Zero AWS compute cost
	•	Lower latency
	•	No autoscaling complexity

Why API Gateway instead of direct DynamoDB access?
	•	Separation of concerns
	•	Validation layer
	•	Future authentication support
	•	Clean service boundary

Why DynamoDB On-Demand?
	•	No provisioning required
	•	Auto-scaling
	•	Free tier sufficient for demo scale

⸻

🔐 Security Model
	•	Least-privilege IAM for Jetson
	•	No wildcard policies
	•	No direct database exposure
	•	HTTPS-only ingestion
	•	CloudWatch log retention capped at 7 days

⸻

💰 Cost Analysis
Service      |  Monthly Cost (Demo Scale)
S3           |  ~$0.50
SQS          |   $0
Lambda       |   $0
API Gateway  |   $0
DynamoDB     |   $0
CloudWatch   |  <$1

Estimated total: <$3/month

Budget alerts configured at $10 and $20 thresholds.

📦 Infrastructure as Code

Provisioned via Terraform.

Resources include:
	•	S3 bucket
	•	SQS queue
	•	DynamoDB table
	•	Lambda function
	•	API Gateway
	•	IAM roles & policies

⸻

🧠 Edge Worker
	•	Dockerized Python service
	•	Long polling SQS
	•	YOLOv8n GPU inference
	•	Deletes queue message on successful processing
	•	Resilient to inference failures

⸻

🚨 Failure Modes Considered
	•	Jetson offline → queue buffers safely
	•	Inference crash → message not deleted
	•	Lambda failure → API returns error
	•	S3 object missing → handled gracefully

⸻

📈 Production Improvements (Future Work)
	•	Dead-letter queue (DLQ)
	•	Structured logging & metrics
	•	CloudWatch alarms
	•	IAM authorizer on API Gateway
	•	CI/CD pipeline
	•	S3 lifecycle archival

⸻

🎯 What This Demonstrates
	•	Event-driven architecture
	•	Serverless backend design
	•	Edge AI integration
	•	Cost-aware cloud engineering
	•	Infrastructure as Code
	•	Security best practices

