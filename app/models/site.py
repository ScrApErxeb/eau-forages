from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    localisation = Column(String)
    actif = Column(Integer, default=1)
    date_crea = Column(DateTime, default=datetime.utcnow)

    # Un site peut avoir plusieurs compteurs et bornes
    compteurs = relationship("Compteur", back_populates="site")
    bornes = relationship("Borne", back_populates="site")  # <- vérifie que Borne a 'site'
