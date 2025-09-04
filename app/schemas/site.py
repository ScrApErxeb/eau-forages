from pydantic import BaseModel
from datetime import datetime

class SiteCreate(BaseModel):
    nom: str
    localisation: str | None = None

class SiteOut(BaseModel):
    id: int
    nom: str
    localisation: str | None
    actif: int
    date_crea: datetime

    class Config:
        from_attributes = True
