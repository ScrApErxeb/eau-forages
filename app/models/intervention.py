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
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    ligne_id = Column(Integer, ForeignKey("lignes.id"), nullable=True)

    technicien = relationship("Technicien", back_populates="interventions")
    client = relationship("Client", back_populates="interventions")
    ligne = relationship("Ligne", back_populates="interventions")

    def __repr__(self):
        return f"<Intervention(id={self.id}, technicien_id={self.technicien_id}, client_id={self.client_id})>"
