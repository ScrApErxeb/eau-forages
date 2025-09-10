from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime

class Intervention(Base):
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    date_crea = Column(DateTime, default=datetime.utcnow)

    technicien_id = Column(Integer, ForeignKey("techniciens.id"), nullable=False)
    abonne_id = Column(Integer, ForeignKey("abonnes.id"), nullable=True)  # changement ici
    ligne_id = Column(Integer, ForeignKey("lignes.id"), nullable=True)

    technicien = relationship("Technicien", back_populates="interventions")
    abonne = relationship("Abonne", back_populates="interventions")  # changement ici
    ligne = relationship("Ligne", back_populates="interventions")

    def __repr__(self):
        return f"<Intervention(id={self.id}, technicien_id={self.technicien_id}, abonne_id={self.abonne_id})>"
