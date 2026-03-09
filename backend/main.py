from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import init_db, get_session
from models import Property, Transaction, Asset
from routes import properties

# Startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db() # this ensures that all tables defined in models are ready
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(properties.router)