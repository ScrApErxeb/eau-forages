from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.db import Base
from sqlalchemy.orm import relationship

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    num_cnib = Column(String, unique=True, index=True, nullable=False)
    tel = Column(String, unique=True, index=True)
    actif = Column(Boolean, default=True)
    date_crea = Column(DateTime, default=datetime.utcnow)

    interventions = relationship("Intervention", back_populates="client", cascade="all, delete-orphan")
    compteurs = relationship("Compteur", back_populates="client", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Client(id={self.id}, nom='{self.nom}', prenom='{self.prenom}')>"
