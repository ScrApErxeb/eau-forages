from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Borne(Base):
    __tablename__ = "bornes"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    code = Column(String, unique=True, nullable=False)  # code unique
    description = Column(String)
    date_crea = Column(DateTime, default=datetime.utcnow)
    actif = Column(Boolean, default=True)
    date_pose = Column(DateTime, default=datetime.utcnow)

    site = relationship("Site", back_populates="bornes")

    def __repr__(self):
        return f"<Borne(id={self.id}, code='{self.code}', site_id={self.site_id})>"
