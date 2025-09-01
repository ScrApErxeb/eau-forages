# app/routers/compteurs.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.compteur import Compteur
from app.schemas.compteur import CompteurCreate, CompteurOut
from app.models.client import Client

router = APIRouter(prefix="/compteurs", tags=["compteurs"])

# Créer un compteur
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

# Lister tous les compteurs
@router.get("/", response_model=list[CompteurOut])
def list_compteurs(db: Session = Depends(get_db)):
    compteurs = db.query(Compteur).all()
    return compteurs

# Obtenir un compteur par id
@router.get("/{compteur_id}", response_model=CompteurOut)
def get_compteur(compteur_id: int, db: Session = Depends(get_db)):
    compteur = db.query(Compteur).filter(Compteur.id == compteur_id).first()
    if not compteur:
        raise HTTPException(status_code=404, detail="Compteur non trouvé")
    return compteur

# Mettre à jour un compteur
@router.put("/{compteur_id}", response_model=CompteurOut)
def update_compteur(compteur_id: int, compteur_data: CompteurCreate, db: Session = Depends(get_db)):
    compteur = db.query(Compteur).filter(Compteur.id == compteur_id).first()
    if not compteur:
        raise HTTPException(status_code=404, detail="Compteur non trouvé")
    for key, value in compteur_data.dict().items():
        setattr(compteur, key, value)
    db.commit()
    db.refresh(compteur)
    return compteur

# Supprimer un compteur
@router.delete("/{compteur_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_compteur(compteur_id: int, db: Session = Depends(get_db)):
    compteur = db.query(Compteur).filter(Compteur.id == compteur_id).first()
    if not compteur:
        raise HTTPException(status_code=404, detail="Compteur non trouvé")
    db.delete(compteur)
    db.commit()
    return
