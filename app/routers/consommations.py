# app/routers/consommations.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.consommation import Consommation
from app.models.abonne import Abonne
from app.schemas.consommation import ConsommationCreate, ConsommationOut
from app.utils.db_utils import get_or_404
from app.utils.pagination import paginate

router = APIRouter(prefix="/consommations", tags=["consommations"])

@router.post("/", response_model=ConsommationOut, status_code=status.HTTP_201_CREATED)
def create_consommation(data: ConsommationCreate, db: Session = Depends(get_db)):
    abonne = get_or_404(db, Abonne, data.abonne_id, "Abonné non trouvé")
    consommation = Consommation(**data.dict())
    db.add(consommation)
    db.commit()
    db.refresh(consommation)
    return consommation


@router.get("/", response_model=List[ConsommationOut])
def list_consommations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return paginate(db.query(Consommation), skip, limit)

@router.get("/{consommation_id}", response_model=ConsommationOut)
def get_consommation(consommation_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Consommation, consommation_id, "Consommation non trouvée")

@router.put("/{consommation_id}", response_model=ConsommationOut)
def update_consommation(consommation_id: int, data: ConsommationCreate, db: Session = Depends(get_db)):
    consommation = get_or_404(db, Consommation, consommation_id, "Consommation non trouvée")
    get_or_404(db, Abonne, data.abonne_id, "Abonné non trouvé")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(consommation, field, value)
    db.commit()
    db.refresh(consommation)
    return consommation

@router.delete("/{consommation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_consommation(consommation_id: int, db: Session = Depends(get_db)):
    consommation = get_or_404(db, Consommation, consommation_id, "Consommation non trouvée")
    db.delete(consommation)
    db.commit()
    return
