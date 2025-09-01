from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Borne(Base):
    __tablename__ = "bornes"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)  # <- clé étrangère obligatoire
    code = Column(String, nullable=False)
    description = Column(String)
    date_crea = Column(DateTime, default=datetime.utcnow)
    actif = Column(Integer, default=1)
    date_pose = Column(DateTime, default=datetime.utcnow)
    
    site = relationship("Site", back_populates="bornes")  # <- doit correspondre à Site.bornes
