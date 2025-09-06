# app/routers/bornes.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.borne import Borne
from app.schemas.borne import BorneCreate, BorneOut
from app.utils.db_utils import get_or_404, check_unique
from app.utils.pagination import paginate

router = APIRouter(prefix="/bornes", tags=["bornes"])

@router.post("/", response_model=BorneOut, status_code=status.HTTP_201_CREATED)
def create_borne(borne_data: BorneCreate, db: Session = Depends(get_db)):
    check_unique(db, Borne, "code", borne_data.code)
    db_borne = Borne(**borne_data.dict())
    db.add(db_borne)
    db.commit()
    db.refresh(db_borne)
    return db_borne

@router.get("/", response_model=List[BorneOut])
def list_bornes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return paginate(db.query(Borne), skip, limit)

@router.get("/{borne_id}", response_model=BorneOut)
def get_borne(borne_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Borne, borne_id, "Borne non trouvée")

@router.put("/{borne_id}", response_model=BorneOut)
def update_borne(borne_id: int, borne_data: BorneCreate, db: Session = Depends(get_db)):
    borne = get_or_404(db, Borne, borne_id, "Borne non trouvée")
    if borne.code != borne_data.code:
        check_unique(db, Borne, "code", borne_data.code, exclude_id=borne_id)
    for field, value in borne_data.dict(exclude_unset=True).items():
        setattr(borne, field, value)
    db.commit()
    db.refresh(borne)
    return borne

@router.delete("/{borne_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_borne(borne_id: int, db: Session = Depends(get_db)):
    borne = get_or_404(db, Borne, borne_id, "Borne non trouvée")
    db.delete(borne)
    db.commit()
    return
