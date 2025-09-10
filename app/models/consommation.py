from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Consommation(Base):
    __tablename__ = "consommations"

    id = Column(Integer, primary_key=True, index=True)
    abonne_id = Column(Integer, ForeignKey("abonnes.id"), nullable=False)
    mois_annee = Column(String(7), nullable=False, default=lambda: datetime.utcnow().strftime("%Y-%m"))
    volume = Column(Float, nullable=False)
    montant = Column(Float, nullable=False)

    abonne = relationship("Abonne", back_populates="consommations")
