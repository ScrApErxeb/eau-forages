from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Compteur(Base):
    __tablename__ = "compteurs"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    serie = Column(String, unique=True, nullable=False)  # numéro de série unique
    calibre = Column(String)
    index_initial = Column(Float, default=0.0)
    actif = Column(Boolean, default=True)
    date_pose = Column(DateTime, default=datetime.utcnow)
    date_crea = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="compteurs")
    site = relationship("Site", back_populates="compteurs")

    def __repr__(self):
        return f"<Compteur(id={self.id}, serie='{self.serie}', client_id={self.client_id}, site_id={self.site_id})>"
