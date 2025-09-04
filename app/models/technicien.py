from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime

class Technicien(Base):
    __tablename__ = "techniciens"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=True)
    specialite = Column(String, nullable=True)
    actif = Column(Boolean, default=True)
    date_crea = Column(DateTime, default=datetime.utcnow)

    interventions = relationship("Intervention", back_populates="technicien", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Technicien(id={self.id}, nom='{self.nom}', prenom='{self.prenom}')>"
