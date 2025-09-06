from pydantic import BaseModel

class LigneBase(BaseModel):
    nom: str
    localisation: str | None = None

class LigneCreate(LigneBase):
    pass

class LigneUpdate(BaseModel):
    nom: str | None = None
    localisation: str | None = None

class LigneOut(LigneBase):
    id: int

    class Config:
        from_attributes = True
