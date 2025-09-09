# app/routers/bornes.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.borne import Borne
from app.schemas.borne import BorneCreate, BorneOut
from app.utils.db_utils import get_or_404
from app.utils.pagination import paginate

router = APIRouter(prefix="/bornes", tags=["bornes"])

@router.post("/", response_model=BorneOut, status_code=status.HTTP_201_CREATED)
def create_borne(borne_data: BorneCreate, db: Session = Depends(get_db)):
    # Vérification unicité code par site
    exists = db.query(Borne).filter(
        Borne.code == borne_data.code,
        Borne.site_id == borne_data.site_id
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Code déjà utilisé pour ce site")

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

    # Vérification unicité code par site si code ou site_id changent
    if borne.code != borne_data.code or borne.site_id != borne_data.site_id:
        exists = db.query(Borne).filter(
            Borne.code == borne_data.code,
            Borne.site_id == borne_data.site_id,
            Borne.id != borne_id
        ).first()
        if exists:
            raise HTTPException(status_code=400, detail="Code déjà utilisé pour ce site")

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
