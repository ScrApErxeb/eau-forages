from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.technicien import Technicien

class TechnicienService:
    @staticmethod
    def create_technicien(db: Session, technicien_data):
        db_technicien = Technicien(**technicien_data.dict())
        db.add(db_technicien)
        db.commit()
        db.refresh(db_technicien)
        return db_technicien

    @staticmethod
    def update_technicien(db: Session, technicien_id: int, technicien_data):
        tech = db.query(Technicien).filter(Technicien.id == technicien_id).first()
        if not tech:
            raise HTTPException(status_code=404, detail="Technicien non trouvé")
        for field, value in technicien_data.dict(exclude_unset=True).items():
            setattr(tech, field, value)
        db.commit()
        db.refresh(tech)
        return tech

    @staticmethod
    def delete_technicien(db: Session, technicien_id: int):
        tech = db.query(Technicien).filter(Technicien.id == technicien_id).first()
        if not tech:
            raise HTTPException(status_code=404, detail="Technicien non trouvé")
        db.delete(tech)
        db.commit()
        return tech

    @staticmethod
    def get_technicien(db: Session, technicien_id: int):
        tech = db.query(Technicien).filter(Technicien.id == technicien_id).first()
        if not tech:
            raise HTTPException(status_code=404, detail="Technicien non trouvé")
        return tech

    @staticmethod
    def list_techniciens(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Technicien).offset(skip).limit(limit).all()
