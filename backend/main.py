from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from contextlib import asynccontextmanager

from database import init_db, get_session
from models import Property

# Startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db() # this ensures that all tables defined in models are ready
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/properties")
def create_property(prop: Property, session: Session = Depends(get_session)):
    session.add(prop) # stage the data
    session.commit() # save the data
    session.refresh(prop) # get the new id back from the database
    return prop # send that result to the user

@app.get("/properties")
def read_properties(session: Session = Depends(get_session)):
    statement = select(Property) # creates a search command
    results = session.exec(statement) # execute the search
    return results.all() # convert and send the results to the user

@app.delete("/properties/{property_id}")
def delete_property(property_id: int, session: Session = Depends(get_session)):
    prop = session.get(Property, property_id)
    if not prop:
        return {"message": "Property not found"}
    
    session.delete(prop)
    session.commit()
    return {"message": f"Property {property_id} deleted successfully"}