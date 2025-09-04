# app/routers/lignes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.ligne import Ligne
from app.schemas.ligne import LigneCreate, LigneOut

router = APIRouter(prefix="/lignes", tags=["lignes"])

# --- Création d'une ligne ---
@router.post("/", response_model=LigneOut, status_code=status.HTTP_201_CREATED)
def create_ligne(ligne: LigneCreate, db: Session = Depends(get_db)):
    db_ligne = Ligne(**ligne.dict())
    db.add(db_ligne)
    db.commit()
    db.refresh(db_ligne)
    return db_ligne

# --- Lister les lignes avec pagination ---
@router.get("/", response_model=List[LigneOut])
def list_lignes(skip: int = Query(0, ge=0), limit: int = Query(100, le=500), db: Session = Depends(get_db)):
    return db.query(Ligne).offset(skip).limit(limit).all()

# --- Obtenir une ligne par ID ---
@router.get("/{ligne_id}", response_model=LigneOut)
def get_ligne(ligne_id: int, db: Session = Depends(get_db)):
    ligne = db.query(Ligne).filter(Ligne.id == ligne_id).first()
    if not ligne:
        raise HTTPException(status_code=404, detail="Ligne non trouvée")
    return ligne

# --- Mise à jour partielle d'une ligne ---
@router.put("/{ligne_id}", response_model=LigneOut)
def update_ligne(ligne_id: int, ligne_data: LigneCreate, db: Session = Depends(get_db)):
    ligne = db.query(Ligne).filter(Ligne.id == ligne_id).first()
    if not ligne:
        raise HTTPException(status_code=404, detail="Ligne non trouvée")

    # Mise à jour partielle : seulement les champs fournis
    for field, value in ligne_data.dict(exclude_unset=True).items():
        setattr(ligne, field, value)

    db.commit()
    db.refresh(ligne)
    return ligne

# --- Supprimer une ligne ---
@router.delete("/{ligne_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ligne(ligne_id: int, db: Session = Depends(get_db)):
    ligne = db.query(Ligne).filter(Ligne.id == ligne_id).first()
    if not ligne:
        raise HTTPException(status_code=404, detail="Ligne non trouvée")
    db.delete(ligne)
    db.commit()
    return
