from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Asset

router = APIRouter(prefix="/assets", tags=["Assets"])

@router.post("/")
def create_asset(item: Asset, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.get("/")
def read_assets(offset: int=0, limit: int = 50, session: Session = Depends(get_session)):
    return session.exec(select(Asset).offset(offset).limit(limit)).all()

@router.get("/categories")
def get_asset_categories():
    return[
        "appliance",    # Fridge, Oven, Washer
        "systems",      # HVAC, Water Heater, Electrical Panel
        "tool",         # Lawn Mower, Yard Equipment
        "furnature",    # Couch, Outdoor Furnature 
        "structural",   # Windows, Doors, Roof, Foundation
        "utility",      # Sump Pump, Smart Home Hubs
        "safety",       # Smoke Detectors, Fire Extinguishers    
        "electronics",  # Smart Locks, Routers
        "landscaping",  # Plants, Fences, Sheds, Retaining Walls
        "other"         # Anything else
    ]

@router.patch("/{asset_id}")
def update_asset(asset_id: int, asset_data: Asset, session: Session = Depends(get_session)):
    item = session.get(Asset, asset_id)
    if not item:
        raise HTTPException(status_code=404, detail="Asset not found")

    update_data = asset_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.delete("/{asset_id}")
def delete_asset(asset_id: int, session: Session = Depends(get_session)):
    item = session.get(Asset, asset_id)
    if not item:
        raise HTTPException(status_code=404, detail="Asset not found")
    session.delete(item)
    session.commit()
    return {"message": f"Asset {asset_id} deleted successfully"}