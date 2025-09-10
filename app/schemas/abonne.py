# app/schemas/abonne.py
from pydantic import BaseModel
from datetime import datetime

class AbonneBase(BaseModel):
    nom: str
    prenom: str
    num_cnib: str
    numero_abonne: str
    tel: str | None = None

class AbonneCreate(AbonneBase):
    pass

class AbonneUpdate(BaseModel):
    nom: str | None = None
    prenom: str | None = None
    num_cnib: str | None = None
    numero_abonne: str | None = None
    tel: str | None = None

class AbonneOut(AbonneBase):
    id: int
    actif: bool
    date_crea: datetime

    class Config:
        from_attributes = True
