from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.borne import Borne

class BorneService:
    @staticmethod
    def create_borne(db: Session, borne_data):
        existing = db.query(Borne).filter(
            Borne.code == borne_data.code,
            Borne.site_id == borne_data.site_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Code déjà utilisé pour ce site")
        db_borne = Borne(**borne_data.dict())
        db.add(db_borne)
        db.commit()
        db.refresh(db_borne)
        return db_borne

    @staticmethod
    def update_borne(db: Session, borne_id: int, borne_data):
        borne = db.query(Borne).filter(Borne.id == borne_id).first()
        if not borne:
            raise HTTPException(status_code=404, detail="Borne non trouvée")

        # Vérification unicité si code ou site_id changés
        if (borne_data.code and borne_data.code != borne.code) or \
           (borne_data.site_id and borne_data.site_id != borne.site_id):
            existing = db.query(Borne).filter(
                Borne.code == (borne_data.code or borne.code),
                Borne.site_id == (borne_data.site_id or borne.site_id),
                Borne.id != borne_id
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="Code déjà utilisé pour ce site")

        for field, value in borne_data.dict(exclude_unset=True).items():
            setattr(borne, field, value)

        db.commit()
        db.refresh(borne)
        return borne

    @staticmethod
    def delete_borne(db: Session, borne_id: int):
        borne = db.query(Borne).filter(Borne.id == borne_id).first()
        if not borne:
            raise HTTPException(status_code=404, detail="Borne non trouvée")
        db.delete(borne)
        db.commit()
        return borne

    @staticmethod
    def get_borne(db: Session, borne_id: int):
        borne = db.query(Borne).filter(Borne.id == borne_id).first()
        if not borne:
            raise HTTPException(status_code=404, detail="Borne non trouvée")
        return borne

    @staticmethod
    def list_bornes(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Borne).offset(skip).limit(limit).all()
