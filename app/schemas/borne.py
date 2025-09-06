from pydantic import BaseModel
from datetime import datetime

class BorneBase(BaseModel):
    site_id: int
    code: str
    description: str | None = None

class BorneCreate(BorneBase):
    pass

class BorneUpdate(BaseModel):
    site_id: int | None = None
    code: str | None = None
    description: str | None = None

class BorneOut(BorneBase):
    id: int
    actif: bool
    date_pose: datetime
    date_crea: datetime

    class Config:
        from_attributes = True
