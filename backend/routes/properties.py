from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from database import get_session
from models import Property

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.post("/")
def create_property(prop: Property, session: Session = Depends(get_session)):
    session.add(prop) # stage the data
    session.commit() # save the data
    session.refresh(prop) # get the new id back from the database
    return prop # send that result to the user

@router.get("/")
def read_properties(session: Session = Depends(get_session)):
    statement = select(Property) # creates a search command
    results = session.exec(statement) # execute the search
    return results.all() # convert and send the results to the user

@router.patch("/{property_id}")
def update_property(property_id: int, property_data: Property, session: Session = Depends(get_session)):
    prop = session.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, details="Property not found")
    update_data = property_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(prop, key, value)
    
    session.add(prop)
    session.commit()
    session.refresh(prop)
    return prop

@router.delete("/{property_id}")
def delete_property(property_id: int, session: Session = Depends(get_session)):
    prop = session.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    try:  
        session.delete(prop)
        session.commit()
        return {"message": f"Property {property_id} deleted successfully"}
    except IntegrityError:
        # Catches any violations from transactions, assets or appliances
        session.rollback()
        raise HTTPException(status_code=400, detail="Delete blocked: This property has linked transactions or assets. Archive it instead.")