from pydantic import BaseModel
from datetime import datetime

class InterventionBase(BaseModel):
    description: str
    technicien_id: int
    abonne_id: int | None = None
    ligne_id: int | None = None

class InterventionCreate(InterventionBase):
    pass

class InterventionUpdate(BaseModel):
    description: str | None = None
    technicien_id: int | None = None
    abonne_id: int | None = None
    ligne_id: int | None = None

class InterventionOut(InterventionBase):
    id: int
    date: datetime
    date_crea: datetime

    class Config:
        from_attributes = True
