from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False, unique=True)  # nom unique
    localisation = Column(String)
    actif = Column(Boolean, default=True)
    date_crea = Column(DateTime, default=datetime.utcnow)

    bornes = relationship("Borne", back_populates="site", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Site(id={self.id}, nom='{self.nom}')>"
