# app/routers/bornes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.db import get_db
from app.models.borne import Borne
from app.schemas.borne import BorneCreate, BorneOut

router = APIRouter(prefix="/bornes", tags=["bornes"])

# ✅ Créer une borne
@router.post("/", response_model=BorneOut, status_code=status.HTTP_201_CREATED)
def create_borne(borne: BorneCreate, db: Session = Depends(get_db)):
    db_borne = Borne(
        site_id=borne.site_id,
        code=borne.code,
        description=borne.description,
        actif=1,  # valeur par défaut
        date_pose=datetime.utcnow()  # valeur par défaut
    )
    db.add(db_borne)
    db.commit()
    db.refresh(db_borne)
    return db_borne

# ✅ Lister toutes les bornes
@router.get("/", response_model=List[BorneOut])
def list_bornes(db: Session = Depends(get_db)):
    bornes = db.query(Borne).all()
    return bornes

# ✅ Obtenir une borne par id
@router.get("/{borne_id}", response_model=BorneOut)
def get_borne(borne_id: int, db: Session = Depends(get_db)):
    borne = db.query(Borne).filter(Borne.id == borne_id).first()
    if not borne:
        raise HTTPException(status_code=404, detail="Borne non trouvée")
    return borne

# ✅ Mettre à jour une borne
@router.put("/{borne_id}", response_model=BorneOut)
def update_borne(borne_id: int, borne_data: BorneCreate, db: Session = Depends(get_db)):
    borne = db.query(Borne).filter(Borne.id == borne_id).first()
    if not borne:
        raise HTTPException(status_code=404, detail="Borne non trouvée")

    # Mettre à jour uniquement les champs fournis
    borne.code = borne_data.code
    borne.description = borne_data.description
    borne.site_id = borne_data.site_id
    db.commit()
    db.refresh(borne)
    return borne

# ✅ Supprimer une borne
@router.delete("/{borne_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_borne(borne_id: int, db: Session = Depends(get_db)):
    borne = db.query(Borne).filter(Borne.id == borne_id).first()
    if not borne:
        raise HTTPException(status_code=404, detail="Borne non trouvée")
    db.delete(borne)
    db.commit()
    return
