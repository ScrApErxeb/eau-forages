from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientOut

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    # Vérif si CNIB déjà existant
    if db.query(Client).filter(Client.num_cnib == client.num_cnib).first():
        raise HTTPException(status_code=400, detail="CNIB déjà utilisé")
    # Vérif si tel déjà existant
    if client.tel and db.query(Client).filter(Client.tel == client.tel).first():
        raise HTTPException(status_code=400, detail="Téléphone déjà utilisé")

    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client
