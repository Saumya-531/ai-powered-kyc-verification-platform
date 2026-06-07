# AI-Powered KYC Verification & Identity Verification API Platform

## Overview

AI-Powered KYC Verification & Identity Verification API Platform is a backend system built using FastAPI and MongoDB that simulates how real-world KYC providers, identity verification companies, and digital document verification platforms operate.

The platform allows users to register, authenticate using JWT tokens, upload identity documents, validate Aadhaar and PAN details, perform identity verification against a simulated government database, calculate fraud risk scores, generate verification reports, monitor API activity, and track suspicious verification attempts.

This project was designed to demonstrate industry-standard backend development practices including authentication, authorization, layered architecture, API development, database integration, audit logging, and fraud detection workflows.

---

# Key Features

## Authentication & Security

* User Registration
* User Login
* JWT Authentication
* Password Hashing using Passlib + Bcrypt
* Protected Endpoints
* OAuth2 Bearer Token Support

## Document Management

* Document Upload API
* Secure File Storage
* Document Metadata Management
* User-wise Document Ownership

## Identity Verification

* Aadhaar Number Extraction
* PAN Number Extraction
* Aadhaar Format Validation using Regex
* PAN Format Validation using Regex
* Identity Verification against MongoDB Government Database Simulation

## Fraud Detection & Risk Analysis

* AI-Based Risk Scoring Engine
* Invalid Aadhaar Detection
* Invalid PAN Detection
* Identity Mismatch Detection
* Failed Verification Tracking
* Fraud Monitoring APIs

## Reporting & Analytics

* Verification Report Generation
* Verification History
* Audit Logging
* Dashboard Analytics
* Verification Statistics

---

# Risk Scoring Engine

The platform calculates fraud risk based on multiple verification parameters.

### Current Rules

| Condition                | Risk Score |
| ------------------------ | ---------- |
| Invalid Aadhaar Format   | +40        |
| Invalid PAN Format       | +40        |
| Identity Not Found       | +20        |
| Multiple Failed Attempts | +30        |

### Risk Levels

| Score Range | Level  |
| ----------- | ------ |
| 0 - 30      | Low    |
| 31 - 70     | Medium |
| 71 - 100    | High   |

---

# Project Architecture

The project follows a layered architecture.

```text
Client
   ↓
FastAPI Routers
   ↓
Service Layer
   ↓
Repository Layer
   ↓
MongoDB
```

### Layers

#### API Layer

Responsible for:

* Request Handling
* Response Generation
* Authentication Enforcement

#### Service Layer

Responsible for:

* Business Logic
* Verification Logic
* Fraud Detection Logic

#### Repository Layer

Responsible for:

* MongoDB Queries
* Data Persistence
* Collection Operations

#### Database Layer

Responsible for:

* User Data
* Documents
* Reports
* Logs
* Fraud Monitoring Data

---

# Project Structure

```text
kyc-platform/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── documents.py
│   │       ├── verification.py
│   │       ├── reports.py
│   │       ├── logs.py
│   │       ├── fraud.py
│   │       └── dashboard.py
│   │
│   ├── core/
│   │   ├── security.py
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   └── middleware.py
│   │
│   ├── repositories/
│   ├── services/
│   ├── schemas/
│   ├── database.py
│   ├── config.py
│   └── main.py
│
├── uploads/
├── tests/
├── .env
├── requirements.txt
└── README.md
```

---

# Database Collections

### users

Stores user accounts.

### documents

Stores uploaded document metadata.

### verification_reports

Stores verification reports.

### api_logs

Stores API activity logs.

### failed_attempts

Stores failed verification attempts.

### dummy_identities

Simulated government identity database.

---

# Technology Stack

### Backend

* Python
* FastAPI

### Database

* MongoDB
* PyMongo

### Security

* JWT
* Passlib
* Bcrypt

### Validation

* Pydantic
* Python Regex

### Documentation

* Swagger UI
* OpenAPI

---

# API Endpoints

## Authentication

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
```

## Documents

```http
POST /api/v1/documents/upload
```

## Verification

```http
GET /api/v1/verification/{document_id}
```

## Reports

```http
GET /api/v1/reports
```

## Logs

```http
GET /api/v1/logs
```

## Fraud Monitoring

```http
GET /api/v1/fraud/attempts
```

## Dashboard

```http
GET /api/v1/dashboard/stats
```

---

# Running the Project

## Clone Repository

```bash
git clone <repository-url>
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start MongoDB

```bash
mongod
```

## Run FastAPI

```bash
uvicorn app.main:app --reload
```

---

# Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

---

# Sample Verification Flow

```text
User Uploads Document
       ↓
Text Extraction
       ↓
Aadhaar Detection
       ↓
PAN Detection
       ↓
Regex Validation
       ↓
Identity Database Lookup
       ↓
Risk Score Calculation
       ↓
Report Generation
       ↓
Response Returned
```

---

# Future Enhancements

The following features are planned for future versions:

## AI & Machine Learning

* Machine Learning Based Fraud Detection
* Behavioral Risk Analysis
* Identity Confidence Scoring
* Anomaly Detection

## OCR & Document Processing

* OCR using Tesseract
* PDF Processing
* Image Verification
* Face Matching
* Selfie Verification

## Enterprise Features

* API Key Management
* Multi-Tenant Architecture
* Rate Limiting
* Request Quotas
* Webhook Support

## Security Improvements

* Refresh Tokens
* Role Based Access Control (RBAC)
* Multi-Factor Authentication (MFA)
* Encryption at Rest


# Resume Highlights

* Developed a secure KYC verification platform using FastAPI, MongoDB, JWT Authentication, and layered architecture.
* Built Aadhaar and PAN verification APIs with automated validation and fraud risk scoring.
* Implemented verification reporting, audit logging, dashboard analytics, and fraud monitoring workflows.
* Designed scalable service and repository layers following industry-standard backend architecture practices.

---

# Author

Saumya Gupta

Backend Developer | Python | FastAPI | MongoDB | API Development
