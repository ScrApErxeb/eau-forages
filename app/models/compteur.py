from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Compteur(Base):
    __tablename__ = "compteurs"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)  # <-- important
    serie = Column(String, nullable=False)
    calibre = Column(String)
    index_initial = Column(Float, default=0.0)
    actif = Column(Integer, default=1)
    date_pose = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="compteurs")
    site = relationship("Site", back_populates="compteurs")
