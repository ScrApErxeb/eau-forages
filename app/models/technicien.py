from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base

class Technicien(Base):
    __tablename__ = "techniciens"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=True)
    specialite = Column(String, nullable=True)

    interventions = relationship("Intervention", back_populates="technicien")
