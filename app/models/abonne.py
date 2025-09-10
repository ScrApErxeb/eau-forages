from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from app.db import Base

class Abonne(Base):
    __tablename__ = "abonnes"  # anciennement "clients"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    num_cnib = Column(String, unique=True, index=True, nullable=False)
    numero_abonne = Column(String, unique=True, index=True, nullable=False)  # nouveau champ
    tel = Column(String, unique=True, index=True)
    actif = Column(Boolean, default=True)
    date_crea = Column(DateTime, default=datetime.utcnow)

    interventions = relationship(
        "Intervention", back_populates="abonne", cascade="all, delete-orphan"
    )
    consommations = relationship(
        "Consommation", back_populates="abonne", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Abonne(id={self.id}, nom='{self.nom}', prenom='{self.prenom}')>"
