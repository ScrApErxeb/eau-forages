from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.client import Client

class ClientService:
    @staticmethod
    def create_client(db: Session, client_data):
        if db.query(Client).filter(Client.num_cnib == client_data.num_cnib).first():
            raise HTTPException(status_code=400, detail="CNIB déjà utilisé")
        if client_data.tel and db.query(Client).filter(Client.tel == client_data.tel).first():
            raise HTTPException(status_code=400, detail="Téléphone déjà utilisé")
        db_client = Client(**client_data.dict())
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client

    @staticmethod
    def update_client(db: Session, client_id: int, client_data):
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client non trouvé")

        if client_data.num_cnib and client_data.num_cnib != client.num_cnib:
            if db.query(Client).filter(Client.num_cnib == client_data.num_cnib, Client.id != client_id).first():
                raise HTTPException(status_code=400, detail="CNIB déjà utilisé")

        if client_data.tel and client_data.tel != client.tel:
            if db.query(Client).filter(Client.tel == client_data.tel, Client.id != client_id).first():
                raise HTTPException(status_code=400, detail="Téléphone déjà utilisé")

        for field, value in client_data.dict(exclude_unset=True).items():
            setattr(client, field, value)

        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    def delete_client(db: Session, client_id: int):
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client non trouvé")
        db.delete(client)
        db.commit()
        return client

    @staticmethod
    def get_client(db: Session, client_id: int):
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client non trouvé")
        return client

    @staticmethod
    def list_clients(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Client).offset(skip).limit(limit).all()
