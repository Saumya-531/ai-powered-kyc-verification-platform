# AI-Powered KYC Verification Platform

## Features

- User Registration
- JWT Authentication
- Document Upload
- Aadhaar Verification
- PAN Verification
- Risk Scoring
- Fraud Monitoring
- Dashboard Analytics

## Tech Stack

- FastAPI
- MongoDB
- PyMongo
- JWT
- Passlib
- Pydantic

## Architecture

API Layer
↓
Service Layer
↓
Repository Layer
↓
MongoDB

## Setup

pip install -r requirements.txt

uvicorn app.main:app --reload