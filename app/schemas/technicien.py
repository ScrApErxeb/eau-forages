from pydantic import BaseModel

class TechnicienBase(BaseModel):
    nom: str
    prenom: str | None = None
    specialite: str | None = None

class TechnicienCreate(TechnicienBase):
    pass

class TechnicienUpdate(BaseModel):
    nom: str | None = None
    prenom: str | None = None
    specialite: str | None = None

class TechnicienOut(TechnicienBase):
    id: int

    class Config:
        from_attributes = True
