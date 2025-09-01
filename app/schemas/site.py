# app/schemas/site.py
from pydantic import BaseModel
from datetime import datetime

# Input
class SiteCreate(BaseModel):
    nom: str
    localisation: str | None = None

# Output
class SiteOut(BaseModel):
    id: int
    nom: str
    localisation: str | None
    actif: int
    date_crea: datetime

    class Config:
        orm_mode = True
