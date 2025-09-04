from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime

class Ligne(Base):
    __tablename__ = "lignes"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False, unique=True)  # nom unique
    localisation = Column(String, nullable=True)
    actif = Column(Boolean, default=True)
    date_crea = Column(DateTime, default=datetime.utcnow)

    interventions = relationship("Intervention", back_populates="ligne", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Ligne(id={self.id}, nom='{self.nom}')>"
