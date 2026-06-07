"""FastAPI application entrypoint for the AI-Powered KYC Verification Platform."""

from fastapi import FastAPI

# Authentication
from app.api.v1.auth import router as auth_router

# Documents
from app.api.v1.documents import router as documents_router

# Verification
from app.api.v1.verification import router as verification_router

# Reports
from app.api.v1.reports import router as reports_router

# Logs
from app.api.v1.logs import router as logs_router

# Fraud Monitoring
from app.api.v1.fraud import router as fraud_router

# Dashboard
from app.api.v1.dashboard import router as dashboard_router


app = FastAPI(
    title="AI-Powered KYC Verification & Identity Verification API Platform",
    version="1.0.0",
    description="""
    Enterprise-style KYC Verification Platform built using:

    • FastAPI
    • MongoDB
    • JWT Authentication
    • Aadhaar Verification
    • PAN Verification
    • Fraud Risk Scoring
    • Verification Reports
    • API Audit Logging
    • Failed Verification Tracking
    • Dashboard Analytics
    """,
)

# ==========================
# API Routers
# ==========================

app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    documents_router,
    prefix="/api/v1",
)

app.include_router(
    verification_router,
    prefix="/api/v1",
)

app.include_router(
    reports_router,
    prefix="/api/v1",
)

app.include_router(
    logs_router,
    prefix="/api/v1",
)

app.include_router(
    fraud_router,
    prefix="/api/v1",
)

app.include_router(
    dashboard_router,
    prefix="/api/v1",
)

# ==========================
# Root Endpoint
# ==========================

@app.get("/", tags=["System"])
async def read_root():

    return {
        "message": "KYC Verification Platform Running Successfully"
    }


# ==========================
# Health Check Endpoint
# ==========================

@app.get("/health", tags=["System"])
async def health_check():

    return {
        "status": "healthy"
    }


# ==========================
# Startup Event
# ==========================

@app.on_event("startup")
async def on_startup():

    print(
        "Application Started Successfully"
    )


# ==========================
# Shutdown Event
# ==========================

@app.on_event("shutdown")
async def on_shutdown():

    print(
        "Application Shutdown Successfully"
    )