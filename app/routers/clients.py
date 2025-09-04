# app/routers/clients.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientOut

router = APIRouter(prefix="/clients", tags=["clients"])

# --- Création d'un client avec vérification CNIB et tel ---
@router.post("/", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    if db.query(Client).filter(Client.num_cnib == client.num_cnib).first():
        raise HTTPException(status_code=400, detail="CNIB déjà utilisé")
    if client.tel and db.query(Client).filter(Client.tel == client.tel).first():
        raise HTTPException(status_code=400, detail="Téléphone déjà utilisé")

    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# --- Lister les clients avec pagination ---
@router.get("/", response_model=List[ClientOut])
def list_clients(skip: int = Query(0, ge=0), limit: int = Query(100, le=500), db: Session = Depends(get_db)):
    return db.query(Client).offset(skip).limit(limit).all()

# --- Obtenir un client par ID ---
@router.get("/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client

# --- Mise à jour partielle ---
@router.put("/{client_id}", response_model=ClientOut)
def update_client(client_id: int, client_data: ClientCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    # Vérifier unicité CNIB et tel si changés
    current_cnib = getattr(client, "num_cnib")
    current_tel = getattr(client, "tel")

    if current_cnib != client_data.num_cnib:
        existing = db.query(Client).filter(
            Client.num_cnib == client_data.num_cnib,
            Client.id != client_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="CNIB déjà utilisé")

    if current_tel != client_data.tel:
        existing = db.query(Client).filter(
            Client.tel == client_data.tel,
            Client.id != client_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Téléphone déjà utilisé")

    for field, value in client_data.dict(exclude_unset=True).items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)
    return client

# --- Supprimer un client ---
@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    db.delete(client)
    db.commit()
    return
