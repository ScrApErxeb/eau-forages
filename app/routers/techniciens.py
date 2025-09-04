# app/routers/techniciens.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.technicien import Technicien
from app.schemas.technicien import TechnicienCreate, TechnicienOut

router = APIRouter(prefix="/techniciens", tags=["techniciens"])

# --- Création d'un technicien ---
@router.post("/", response_model=TechnicienOut, status_code=status.HTTP_201_CREATED)
def create_technicien(technicien: TechnicienCreate, db: Session = Depends(get_db)):
    db_technicien = Technicien(**technicien.dict())
    db.add(db_technicien)
    db.commit()
    db.refresh(db_technicien)
    return db_technicien

# --- Lister les techniciens avec pagination ---
@router.get("/", response_model=List[TechnicienOut])
def list_techniciens(skip: int = Query(0, ge=0), limit: int = Query(100, le=500), db: Session = Depends(get_db)):
    return db.query(Technicien).offset(skip).limit(limit).all()

# --- Obtenir un technicien par ID ---
@router.get("/{technicien_id}", response_model=TechnicienOut)
def get_technicien(technicien_id: int, db: Session = Depends(get_db)):
    technicien = db.query(Technicien).filter(Technicien.id == technicien_id).first()
    if not technicien:
        raise HTTPException(status_code=404, detail="Technicien non trouvé")
    return technicien

# --- Mise à jour partielle d'un technicien ---
@router.put("/{technicien_id}", response_model=TechnicienOut)
def update_technicien(technicien_id: int, technicien_data: TechnicienCreate, db: Session = Depends(get_db)):
    technicien = db.query(Technicien).filter(Technicien.id == technicien_id).first()
    if not technicien:
        raise HTTPException(status_code=404, detail="Technicien non trouvé")

    # Mise à jour partielle : seulement les champs fournis
    for field, value in technicien_data.dict(exclude_unset=True).items():
        setattr(technicien, field, value)

    db.commit()
    db.refresh(technicien)
    return technicien

# --- Supprimer un technicien ---
@router.delete("/{technicien_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_technicien(technicien_id: int, db: Session = Depends(get_db)):
    technicien = db.query(Technicien).filter(Technicien.id == technicien_id).first()
    if not technicien:
        raise HTTPException(status_code=404, detail="Technicien non trouvé")
    db.delete(technicien)
    db.commit()
    return
