from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Transaction, SCHEDULE_E_CATEGORIES

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# CRUD operations for transactions

@router.get("/tax-categories")
def get_tax_categories():
    return SCHEDULE_E_CATEGORIES

@router.post("/") # CREATE
def create_transaction(item: Transaction, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.get("/") #READ
def read_transaction(offset: int = 0, limit: int = 50, session: Session = Depends(get_session)):
    return session.exec(select(Transaction).offset(offset).limit(limit)).all()

@router.get("/{transaction_id}") # READ ONE
def read_one_transaction(transaction_id: int, session: Session = Depends(get_session)):
    item = session.get(Transaction, transaction_id)
    if not item:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return item

@router.patch("/{transaction_id}") # UPDATE
def update_transaction(transaction_id: int, transaction_data: Transaction, session: Session = Depends(get_session)):
    # fetch the transaction
    item = session.get(Transaction, transaction_id)
    if not item:
        raise HTTPException(status_code=404, detail="Transaction not found")
    # extract only the fields that the user is updating
    update_data = transaction_data.model_dump(exclude_unset=True)
    # apply the changes to the transaction
    for key, value in update_data.items():
        setattr(item, key, value)
    # save and commit the corrected record
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.delete("/{transaction_id}") #DELETE
def delete_transaction(transaction_id: int, session: Session = Depends(get_session)):
    # fetch the transaction
    item = session.get(Transaction, transaction_id)
    # check if it exists
    if not item:
        raise HTTPException(status_code=404, detail="Transaction not found")
    # delete and commit the change
    session.delete(item)
    session.commit()
    return {"message": f"Transaction {transaction_id} deleted successfully"}

