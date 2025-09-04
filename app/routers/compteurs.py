# app/routers/compteurs.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.compteur import Compteur
from app.models.client import Client
from app.schemas.compteur import CompteurCreate, CompteurOut

router = APIRouter(prefix="/compteurs", tags=["compteurs"])

# --- Création d'un compteur ---
@router.post("/", response_model=CompteurOut, status_code=status.HTTP_201_CREATED)
def create_compteur(compteur: CompteurCreate, db: Session = Depends(get_db)):
    # Vérifier que le client existe
    client = db.query(Client).filter(Client.id == compteur.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    db_compteur = Compteur(**compteur.dict())
    db.add(db_compteur)
    db.commit()
    db.refresh(db_compteur)
    return db_compteur

# --- Lister les compteurs avec pagination ---
@router.get("/", response_model=List[CompteurOut])
def list_compteurs(skip: int = Query(0, ge=0), limit: int = Query(100, le=500), db: Session = Depends(get_db)):
    return db.query(Compteur).offset(skip).limit(limit).all()

# --- Obtenir un compteur par ID ---
@router.get("/{compteur_id}", response_model=CompteurOut)
def get_compteur(compteur_id: int, db: Session = Depends(get_db)):
    compteur = db.query(Compteur).filter(Compteur.id == compteur_id).first()
    if not compteur:
        raise HTTPException(status_code=404, detail="Compteur non trouvé")
    return compteur

# --- Mise à jour partielle d'un compteur ---
@router.put("/{compteur_id}", response_model=CompteurOut)
def update_compteur(compteur_id: int, compteur_data: CompteurCreate, db: Session = Depends(get_db)):
    compteur = db.query(Compteur).filter(Compteur.id == compteur_id).first()
    if not compteur:
        raise HTTPException(status_code=404, detail="Compteur non trouvé")

    # Récupérer les valeurs Python pour éviter ColumnElement
    current_client_id = getattr(compteur, "client_id")
    current_site_id = getattr(compteur, "site_id")

    # Vérifier que le client existe si changement
    if current_client_id != compteur_data.client_id:
        client = db.query(Client).filter(Client.id == compteur_data.client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client non trouvé")

    # Mise à jour partielle : seulement les champs fournis
    for field, value in compteur_data.dict(exclude_unset=True).items():
        setattr(compteur, field, value)

    db.commit()
    db.refresh(compteur)
    return compteur

# --- Supprimer un compteur ---
@router.delete("/{compteur_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_compteur(compteur_id: int, db: Session = Depends(get_db)):
    compteur = db.query(Compteur).filter(Compteur.id == compteur_id).first()
    if not compteur:
        raise HTTPException(status_code=404, detail="Compteur non trouvé")
    db.delete(compteur)
    db.commit()
    return
