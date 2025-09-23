# 📌 Project Overview: **LinkTrail**    

**Tagline:** 👉 *Shorten, share, and track URLs with real-time analytics — a cloud-native serverless backend with a contributor-friendly local environment.*

--- 

## About the Project

I built **LinkTrail** as a personal project to explore cloud-native, serverless development while keeping the system easy for contributors to run locally. 

The goal was to create a URL shortener that not only redirects users but also tracks analytics in real-time — all without requiring users to log in. 

Each URL gets a **secret key** that allows access to its analytics securely. I wanted a system that works fully on **AWS free-tier**, can scale for real-world usage, and is still portable enough to run locally in a **Docker Compose environment**. 

CI/CD pipelines should handle production deployments, so I never have to manually touch AWS for updates.

--- 

## Tech Stack 
**Backend** 
* Python + FastAPI 
* Mangum adapter to run FastAPI on AWS Lambda 
* AWS DynamoDB (NoSQL) for links and click logs 

**Frontend** 
* React for analytics dashboard 
* Hosted on GitHub Pages 

**Infrastructure / CI-CD** 
* AWS SAM templates for Lambda, API Gateway, and DynamoDB 
* GitHub Actions for automated CI/CD
* GitHub Secrets handle all production environment variables 

**Local Development** 
* Docker Compose spins up backend, frontend, and DynamoDB Local 
* Local scripts handle table creation 
* Environment variables are loaded via Docker Compose (.env) 

--- 

## Key Features 

### 1. URL Shortening Users can send a long URL to the API (POST /shorten). The backend generates: 
* short_code (unique short code) 
* analytics_secret (analytics access) 

The response includes both the short code and the analytics secret
--- 

### 2. URL Redirect When someone visits a short link (GET /l/{short_id}): 
* The backend looks up the original URL and redirects the user 
* It logs each click in a **ClickLogs table**: 
  * Timestamp 
  * IP address 
  * User-Agent 

Keeping clicks in a separate table ensures the system can **scale indefinitely** and makes querying analytics fast and efficient. 

--- 

### 3. Analytics Dashboard (No Login) 

Analytics are accessible via the secret key (GET /analytics/{short_code}?analtics_secret={analtics_secret}): 
* Total clicks 
* Clicks over time (daily/hourly) 

The backend validates the secret key and queries the ClickLogs table for analytics. No login is required, but analytics remain secure. 

--- 

### 4. Secret-Key Security 
* Each URL has a **randomly generated secret key** (UUID/HMAC) 
* Required to access analytics 
* Only basic analytics are stored; no PII is collected 

--- 

## Database Schema I designed LinkTrail using a **two-table DynamoDB schema**:

**Links Table** 
| Attribute | Type | Notes |
| ------------------- | ---- | --------------------------- | 
| short_id | S | Primary key | 
| long_url | S | Original URL |
| analytics_secret | S | Secret for analytics access |
| created_at | S | Timestamp | 

**ClickLogs Table** 
| Attribute | Type | Notes | 
| --------------- | ---- | ----------------------------------------- | 
| short_id | S | Partition key | 
| click_timestamp | S | Sort key | 
| client_ip | S | Client's IP address | 
| user_agent  | S | Raw user agent string for future analytics | 

This structure keeps analytics scalable while allowing efficient queries for dashboards. 

--- 

## Project Architecture 

### Production (Serverless AWS) 
* FastAPI running on Lambda (via Mangum) 
* API Gateway for HTTP routing 
* DynamoDB for links and click logs 
* Frontend on GitHub Pages (might change later) 
* CloudWatch logs for monitoring 
* CI/CD handles deployments automatically via GitHub Actions and AWS SAM 

### Local Development 
* Docker Compose spins up: 
  * Backend container (FastAPI) 
  * Frontend container (React dev server) 
  * DynamoDB Local container 
  * DynaoDB web admin GUI container

* Local scripts ensure tables exist and optionally seed test data 
* Environment variables are injected via Docker Compose — the backend never needs dotenv

---
## Planned Folder Structure 

```
linktrail/
├── backend/                          # Backend service (FastAPI)
│   ├── app/
│   │   ├── main.py                   # FastAPI entrypoint + Mangum handler
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   └── core/
│   ├── requirements.txt
│   └── Dockerfile                     # Backend container

├── frontend/                         # Frontend service (React/Next.js)
│   ├── app/                          # React App
│   └── Dockerfile                    # Frontend container

├── infra/                             # Production deployment
│   ├── sam_template.yaml              # AWS Lambda + API Gateway + DynamoDB
│   ├── ci-deploy.yml                  # GitHub Actions workflow
│   └── README.md

├── local/                             # Local development environment
│   ├── docker-compose.yml             # Spins up backend, frontend, DynamoDB Local
│   ├── setup_local_dynamodb.py        # Create tables locally
│   ├── teardown_local_dynamodb.py     # Delete tables locally
│   └── .env                           # Local environment variables

├── .gitignore
└── README.md


```