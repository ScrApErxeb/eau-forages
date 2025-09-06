from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    role: str | None = "user"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    email: str | None = None
    role: str | None = None
    password: str | None = None

class UserOut(UserBase):
    id: int
    is_active: bool
    date_crea: datetime

    class Config:
        from_attributes = True
