from pydantic import BaseModel

class TechnicienBase(BaseModel):
    nom: str
    specialite: str | None = None

class TechnicienCreate(TechnicienBase):
    pass

class TechnicienOut(TechnicienBase):
    id: int

    model_config = {
    "from_attributes": True
}

