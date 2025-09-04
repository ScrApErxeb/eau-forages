from pydantic import BaseModel

class LigneBase(BaseModel):
    nom: str
    localisation: str | None = None

class LigneCreate(LigneBase):
    pass

class LigneOut(LigneBase):
    id: int

    model_config = {
    "from_attributes": True
}

