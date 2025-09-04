# app/routers/interventions.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.intervention import Intervention
from app.schemas.intervention import InterventionCreate, InterventionOut

router = APIRouter(prefix="/interventions", tags=["interventions"])

# --- Création d'une intervention ---
@router.post("/", response_model=InterventionOut, status_code=status.HTTP_201_CREATED)
def create_intervention(intervention: InterventionCreate, db: Session = Depends(get_db)):
    db_intervention = Intervention(**intervention.dict())
    db.add(db_intervention)
    db.commit()
    db.refresh(db_intervention)
    return db_intervention

# --- Lister les interventions avec pagination ---
@router.get("/", response_model=List[InterventionOut])
def list_interventions(skip: int = Query(0, ge=0), limit: int = Query(100, le=500), db: Session = Depends(get_db)):
    return db.query(Intervention).offset(skip).limit(limit).all()

# --- Obtenir une intervention par ID ---
@router.get("/{intervention_id}", response_model=InterventionOut)
def get_intervention(intervention_id: int, db: Session = Depends(get_db)):
    intervention = db.query(Intervention).filter(Intervention.id == intervention_id).first()
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention non trouvée")
    return intervention

# --- Mise à jour partielle d'une intervention ---
@router.put("/{intervention_id}", response_model=InterventionOut)
def update_intervention(intervention_id: int, intervention_data: InterventionCreate, db: Session = Depends(get_db)):
    intervention = db.query(Intervention).filter(Intervention.id == intervention_id).first()
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention non trouvée")

    # Mise à jour partielle : seulement les champs fournis
    for field, value in intervention_data.dict(exclude_unset=True).items():
        setattr(intervention, field, value)

    db.commit()
    db.refresh(intervention)
    return intervention

# --- Supprimer une intervention ---
@router.delete("/{intervention_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_intervention(intervention_id: int, db: Session = Depends(get_db)):
    intervention = db.query(Intervention).filter(Intervention.id == intervention_id).first()
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention non trouvée")
    db.delete(intervention)
    db.commit()
    return
