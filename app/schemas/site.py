from pydantic import BaseModel
from datetime import datetime

class SiteBase(BaseModel):
    nom: str
    localisation: str | None = None

class SiteCreate(SiteBase):
    pass

class SiteUpdate(BaseModel):
    nom: str | None = None
    localisation: str | None = None

class SiteOut(SiteBase):
    id: int
    actif: bool
    date_crea: datetime

    class Config:
        from_attributes = True
