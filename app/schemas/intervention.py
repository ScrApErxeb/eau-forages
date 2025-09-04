from pydantic import BaseModel
from datetime import datetime

class InterventionBase(BaseModel):
    description: str
    date: datetime
    technicien_id: int
    ligne_id: int

class InterventionCreate(InterventionBase):
    pass

class InterventionOut(InterventionBase):
    id: int

    model_config = {
    "from_attributes": True
}

