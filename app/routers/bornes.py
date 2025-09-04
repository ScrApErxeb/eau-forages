# app/routers/bornes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.db import get_db
from app.models.borne import Borne
from app.schemas.borne import BorneCreate, BorneOut

router = APIRouter(prefix="/bornes", tags=["bornes"])

# --- Création d'une borne avec unicité vérifiée ---
@router.post("/", response_model=BorneOut, status_code=status.HTTP_201_CREATED)
def create_borne(borne: BorneCreate, db: Session = Depends(get_db)):
    existing = db.query(Borne).filter(
        Borne.code == borne.code,
        Borne.site_id == borne.site_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Code déjà utilisé pour ce site")

    db_borne = Borne(
        site_id=borne.site_id,
        code=borne.code,
        description=borne.description
        # SQLAlchemy gère actif=1 et date_pose=datetime.utcnow() par défaut
    )
    db.add(db_borne)
    db.commit()
    db.refresh(db_borne)
    return db_borne

# --- Lister les bornes avec pagination ---
@router.get("/", response_model=List[BorneOut])
def list_bornes(skip: int = Query(0, ge=0), limit: int = Query(100, le=500), db: Session = Depends(get_db)):
    return db.query(Borne).offset(skip).limit(limit).all()

# --- Obtenir une borne par ID ---
@router.get("/{borne_id}", response_model=BorneOut)
def get_borne(borne_id: int, db: Session = Depends(get_db)):
    borne = db.query(Borne).filter(Borne.id == borne_id).first()
    if not borne:
        raise HTTPException(status_code=404, detail="Borne non trouvée")
    return borne

# --- Mise à jour partielle d'une borne ---
@router.put("/{borne_id}", response_model=BorneOut)
def update_borne(borne_id: int, borne_data: BorneCreate, db: Session = Depends(get_db)):
    # Récupération de l'objet depuis la DB
    borne = db.query(Borne).filter(Borne.id == borne_id).first()
    if not borne:
        raise HTTPException(status_code=404, detail="Borne non trouvée")

    # Extraire les valeurs Python
    current_code = getattr(borne, "code")
    current_site_id = getattr(borne, "site_id")

    # Vérification unicité
    if (current_code != borne_data.code) or (current_site_id != borne_data.site_id):
        existing = db.query(Borne).filter(
            Borne.code == borne_data.code,
            Borne.site_id == borne_data.site_id,
            Borne.id != borne_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Code déjà utilisé pour ce site")


    # Mise à jour partielle : seuls les champs fournis sont modifiés
    for field, value in borne_data.dict(exclude_unset=True).items():
        setattr(borne, field, value)

    db.commit()
    db.refresh(borne)
    return borne

# --- Supprimer une borne ---
@router.delete("/{borne_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_borne(borne_id: int, db: Session = Depends(get_db)):
    borne = db.query(Borne).filter(Borne.id == borne_id).first()
    if not borne:
        raise HTTPException(status_code=404, detail="Borne non trouvée")
    db.delete(borne)
    db.commit()
    return
  