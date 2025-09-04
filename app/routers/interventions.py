from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.intervention import Intervention
from app.schemas.intervention import InterventionCreate, InterventionOut

router = APIRouter(prefix="/interventions", tags=["interventions"])

# Créer une intervention
@router.post("/", response_model=InterventionOut, status_code=status.HTTP_201_CREATED)
def create_intervention(intervention: InterventionCreate, db: Session = Depends(get_db)):
    db_intervention = Intervention(**intervention.dict())
    db.add(db_intervention)
    db.commit()
    db.refresh(db_intervention)
    return db_intervention

# Lister toutes les interventions
@router.get("/", response_model=list[InterventionOut])
def list_interventions(db: Session = Depends(get_db)):
    return db.query(Intervention).all()

# Obtenir une intervention par id
@router.get("/{intervention_id}", response_model=InterventionOut)
def get_intervention(intervention_id: int, db: Session = Depends(get_db)):
    intervention = db.query(Intervention).filter(Intervention.id == intervention_id).first()
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention non trouvée")
    return intervention

# Supprimer une intervention
@router.delete("/{intervention_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_intervention(intervention_id: int, db: Session = Depends(get_db)):
    intervention = db.query(Intervention).filter(Intervention.id == intervention_id).first()
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention non trouvée")
    db.delete(intervention)
    db.commit()
    return
