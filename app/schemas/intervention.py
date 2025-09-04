from pydantic import BaseModel
from datetime import datetime

class InterventionBase(BaseModel):
    description: str
    technicien_id: int
    client_id: int | None = None
    ligne_id: int | None = None

class InterventionCreate(InterventionBase):
    pass

class InterventionOut(InterventionBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True
