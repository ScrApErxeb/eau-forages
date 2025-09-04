from pydantic import BaseModel
from datetime import datetime

class ClientCreate(BaseModel):
    nom: str
    prenom: str
    num_cnib: str
    tel: str | None = None

class ClientOut(BaseModel):
    id: int
    nom: str
    prenom: str
    num_cnib: str
    tel: str | None
    actif: int
    date_crea: datetime

    class Config:
        from_attributes = True
