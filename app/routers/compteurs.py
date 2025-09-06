# app/routers/compteurs.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.compteur import Compteur
from app.models.client import Client
from app.schemas.compteur import CompteurCreate, CompteurOut
from app.utils.db_utils import get_or_404
from app.utils.pagination import paginate

router = APIRouter(prefix="/compteurs", tags=["compteurs"])

@router.post("/", response_model=CompteurOut, status_code=status.HTTP_201_CREATED)
def create_compteur(data: CompteurCreate, db: Session = Depends(get_db)):
    get_or_404(db, Client, data.client_id, "Client non trouvé")
    compteur = Compteur(**data.dict())
    db.add(compteur)
    db.commit()
    db.refresh(compteur)
    return compteur

@router.get("/", response_model=List[CompteurOut])
def list_compteurs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return paginate(db.query(Compteur), skip, limit)

@router.get("/{compteur_id}", response_model=CompteurOut)
def get_compteur(compteur_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Compteur, compteur_id, "Compteur non trouvé")

@router.put("/{compteur_id}", response_model=CompteurOut)
def update_compteur(compteur_id: int, data: CompteurCreate, db: Session = Depends(get_db)):
    compteur = get_or_404(db, Compteur, compteur_id, "Compteur non trouvé")
    if compteur.client_id != data.client_id:
        get_or_404(db, Client, data.client_id, "Client non trouvé")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(compteur, field, value)
    db.commit()
    db.refresh(compteur)
    return compteur

@router.delete("/{compteur_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_compteur(compteur_id: int, db: Session = Depends(get_db)):
    compteur = get_or_404(db, Compteur, compteur_id, "Compteur non trouvé")
    db.delete(compteur)
    db.commit()
    return
