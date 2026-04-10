from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import init_db, get_session
from models import Property, Transaction, Asset, Deal, Loan
from routes import properties, transactions, assets, dashboard, deals, loans, portfolio

# Startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db() # this ensures that all tables defined in models are ready
    yield

app = FastAPI(lifespan=lifespan, title="tapre-api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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