from fastapi import FastAPI
from app.routers import health

# Initialize FastAPI application
app = FastAPI(
    title="AlterDay API",
    description="Backend service for ML simulations and data processing.",
    version="1.0.0"
)

# Include routers from the routers directory
app.include_router(health.router)