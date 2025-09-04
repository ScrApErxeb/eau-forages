# app/schemas/compteur.py
from pydantic import BaseModel
from datetime import datetime

class CompteurCreate(BaseModel):
    client_id: int
    site_id: int
    serie: str
    calibre: str | None = None
    index_initial: float = 0.0

class CompteurOut(BaseModel):
    id: int
    client_id: int
    site_id: int
    serie: str
    calibre: str | None
    index_initial: float
    date_pose: datetime
    actif: int

    model_config = {
    "from_attributes": True
}

