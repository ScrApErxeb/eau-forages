# app/routers/interventions.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.intervention import Intervention
from app.schemas.intervention import InterventionCreate, InterventionOut
from app.utils.db_utils import get_or_404
from app.utils.pagination import paginate

router = APIRouter(prefix="/interventions", tags=["interventions"])

@router.post("/", response_model=InterventionOut, status_code=status.HTTP_201_CREATED)
def create_intervention(data: InterventionCreate, db: Session = Depends(get_db)):
    intervention = Intervention(**data.dict())
    db.add(intervention)
    db.commit()
    db.refresh(intervention)
    return intervention

@router.get("/", response_model=List[InterventionOut])
def list_interventions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return paginate(db.query(Intervention), skip, limit)

@router.get("/{intervention_id}", response_model=InterventionOut)
def get_intervention(intervention_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Intervention, intervention_id, "Intervention non trouvée")

@router.put("/{intervention_id}", response_model=InterventionOut)
def update_intervention(intervention_id: int, data: InterventionCreate, db: Session = Depends(get_db)):
    intervention = get_or_404(db, Intervention, intervention_id, "Intervention non trouvée")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(intervention, field, value)
    db.commit()
    db.refresh(intervention)
    return intervention

@router.delete("/{intervention_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_intervention(intervention_id: int, db: Session = Depends(get_db)):
    intervention = get_or_404(db, Intervention, intervention_id, "Intervention non trouvée")
    db.delete(intervention)
    db.commit()
    return
