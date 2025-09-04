from pydantic import BaseModel

class TechnicienBase(BaseModel):
    nom: str
    prenom: str | None = None
    specialite: str | None = None

class TechnicienCreate(TechnicienBase):
    pass

class TechnicienOut(TechnicienBase):
    id: int

    class Config:
        from_attributes = True
