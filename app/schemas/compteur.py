from pydantic import BaseModel
from datetime import datetime

class CompteurBase(BaseModel):
    abonne_id: int
    site_id: int
    serie: str
    calibre: str | None = None
    index_initial: float = 0.0

class CompteurCreate(CompteurBase):
    pass

class CompteurUpdate(BaseModel):
    abonne_id: int | None = None
    site_id: int | None = None
    serie: str | None = None
    calibre: str | None = None
    index_initial: float | None = None

class CompteurOut(CompteurBase):
    id: int
    actif: bool
    date_pose: datetime
    date_crea: datetime

    class Config:
        from_attributes = True
