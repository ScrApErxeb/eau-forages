# app/routers/clients.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientOut
from app.utils.db_utils import get_or_404, check_unique
from app.utils.pagination import paginate

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def create_client(client_data: ClientCreate, db: Session = Depends(get_db)):
    check_unique(db, Client, "num_cnib", client_data.num_cnib)
    if client_data.tel:
        check_unique(db, Client, "tel", client_data.tel)
    client = Client(**client_data.dict())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@router.get("/", response_model=List[ClientOut])
def list_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return paginate(db.query(Client), skip, limit)

@router.get("/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Client, client_id, "Client non trouvé")

@router.put("/{client_id}", response_model=ClientOut)
def update_client(client_id: int, client_data: ClientCreate, db: Session = Depends(get_db)):
    client = get_or_404(db, Client, client_id, "Client non trouvé")
    if client.num_cnib != client_data.num_cnib:
        check_unique(db, Client, "num_cnib", client_data.num_cnib, exclude_id=client_id)
    if client_data.tel and client.tel != client_data.tel:
        check_unique(db, Client, "tel", client_data.tel, exclude_id=client_id)
    for field, value in client_data.dict(exclude_unset=True).items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = get_or_404(db, Client, client_id, "Client non trouvé")
    db.delete(client)
    db.commit()
    return
