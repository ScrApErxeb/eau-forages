from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")  # 'user' ou 'admin'
    is_active = Column(Integer, default=1)
    date_crea = Column(DateTime, default=datetime.utcnow)
