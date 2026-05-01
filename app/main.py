from fastapi import FastAPI
from app.routers import health
from app.routers import entries

app = FastAPI(
    title="AlterDay API",
    description="Backend service for ML simulations and data processing.",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(entries.router)
