import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import init_db, get_session
from models import Property, Transaction, Asset, Deal, Loan, MaintenanceRecord, Reminder, Document
from routes import properties, transactions, assets, dashboard, deals, loans, portfolio, maintenance

# Startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db() # this ensures that all tables defined in models are ready
    yield

app = FastAPI(lifespan=lifespan, title="TAP·re API")

# CORS_ORIGINS: comma-separated list of allowed origins.
# Dev default: http://localhost:5173 (Vite dev server).
# In Docker, nginx proxies requests so the browser never hits the backend directly —
# CORS is not triggered, but keep the var set for flexibility.
_cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(properties.router)
app.include_router(transactions.router)
app.include_router(assets.router)
app.include_router(dashboard.router)
app.include_router(deals.router)
app.include_router(loans.router)
app.include_router(portfolio.router)
app.include_router(maintenance.router)