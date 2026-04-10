import os
from pathlib import Path
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel

# Load the .env from the root path
BASE_DIR = Path(__file__).resolve().parent # this line looks at the current file and determines its parent directory
load_dotenv(dotenv_path=BASE_DIR.parent / ".env", override=True) # it then uses that info to say okay this is where to look for the .env

# Get the connection string
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the sql engine
engine = create_engine(DATABASE_URL, echo=True)

# Initializer function that raches out to postgres and builds tables
def init_db():
    SQLModel.metadata.create_all(engine)

# Provides database session to api routes
def get_session():
    with Session(engine) as session:
        yield session