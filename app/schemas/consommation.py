# app/schemas/consommation.py
from pydantic import BaseModel
from datetime import datetime
from app.schemas.abonne import AbonneOut


class ConsommationBase(BaseModel):
    abonne_id: int
    volume: float
    montant: float
    mois_annee: datetime | None = None

class ConsommationCreate(ConsommationBase):
    pass

class ConsommationOut(ConsommationBase):
    id: int
    date_crea: datetime
    abonne: AbonneOut  # ← inclure l'abonné

    class Config:
        from_attributes = True
