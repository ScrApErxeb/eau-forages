from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db import Base
from sqlalchemy.orm import relationship


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)          # Nom de famille
    prenom = Column(String, nullable=False)       # Prénom
    num_cnib = Column(String, unique=True, index=True, nullable=False)  # Numéro de CNIB
    tel = Column(String, unique=True, index=True) # Téléphone
    actif = Column(Integer, default=1)
    date_crea = Column(DateTime, default=datetime.utcnow)

    # Relation avec Compteur
    compteurs = relationship("Compteur", back_populates="client", cascade="all, delete-orphan")
