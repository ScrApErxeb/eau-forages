from pydantic import BaseModel
from datetime import datetime

class ClientBase(BaseModel):
    nom: str
    prenom: str
    num_cnib: str
    tel: str | None = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    nom: str | None = None
    prenom: str | None = None
    num_cnib: str | None = None
    tel: str | None = None

class ClientOut(ClientBase):
    id: int
    actif: bool
    date_crea: datetime

    class Config:
        from_attributes = True
