from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base

class Ligne(Base):
    __tablename__ = "lignes"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    localisation = Column(String, nullable=True)

    interventions = relationship("Intervention", back_populates="ligne")
