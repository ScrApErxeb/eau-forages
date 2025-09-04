from pydantic import BaseModel

class LigneBase(BaseModel):
    nom: str
    localisation: str | None = None

class LigneCreate(LigneBase):
    pass

class LigneOut(LigneBase):
    id: int

    class Config:
        from_attributes = True
