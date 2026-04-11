from typing import Optional
from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from pydantic import BaseModel

from database import get_session
from models import MaintenanceRecord, MAINTENANCE_CATEGORIES

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])


class MaintenanceCreate(BaseModel):
    property_id: int
    asset_id: Optional[int] = None
    service_date: date
    category: str
    description: str
    vendor: Optional[str] = None
    cost: Decimal = Decimal("0")
    warranty_expires: Optional[date] = None
    notes: Optional[str] = None


class MaintenanceUpdate(BaseModel):
    asset_id: Optional[int] = None
    service_date: Optional[date] = None
    category: Optional[str] = None
    description: Optional[str] = None
    vendor: Optional[str] = None
    cost: Optional[Decimal] = None
    warranty_expires: Optional[date] = None
    notes: Optional[str] = None


@router.get("/categories")
def get_maintenance_categories():
    return MAINTENANCE_CATEGORIES


@router.post("/")
def create_record(data: MaintenanceCreate, session: Session = Depends(get_session)):
    record = MaintenanceRecord(**data.model_dump())
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


@router.get("/")
def list_records(property_id: int = Query(...), session: Session = Depends(get_session)):
    records = session.exec(
        select(MaintenanceRecord)
        .where(MaintenanceRecord.property_id == property_id)
        .order_by(MaintenanceRecord.service_date.desc())
    ).all()
    return records


@router.patch("/{record_id}")
def update_record(record_id: int, data: MaintenanceUpdate, session: Session = Depends(get_session)):
    record = session.get(MaintenanceRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(record, key, value)
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


@router.delete("/{record_id}")
def delete_record(record_id: int, session: Session = Depends(get_session)):
    record = session.get(MaintenanceRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    session.delete(record)
    session.commit()
    return {"message": f"Maintenance record {record_id} deleted"}
