from pydantic import BaseModel
from datetime import datetime

class BorneCreate(BaseModel):
    site_id: int
    code: str
    description: str | None = None

class BorneOut(BaseModel):
    id: int
    site_id: int
    code: str
    description: str | None
    actif: int
    date_pose: datetime

    class Config:
        from_attributes = True
