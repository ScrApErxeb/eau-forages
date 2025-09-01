# app/schemas/borne.py
from pydantic import BaseModel
from datetime import datetime

# Input
class BorneCreate(BaseModel):
    site_id: int
    code: str
    description: str | None = None

# Output
class BorneOut(BaseModel):
    id: int
    site_id: int
    code: str
    description: str | None
    actif: int
    date_pose: datetime

    class Config:
        orm_mode = True
