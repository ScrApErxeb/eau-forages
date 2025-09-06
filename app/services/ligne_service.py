from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.ligne import Ligne

class LigneService:
    @staticmethod
    def create_ligne(db: Session, ligne_data):
        db_ligne = Ligne(**ligne_data.dict())
        db.add(db_ligne)
        db.commit()
        db.refresh(db_ligne)
        return db_ligne

    @staticmethod
    def update_ligne(db: Session, ligne_id: int, ligne_data):
        ligne = db.query(Ligne).filter(Ligne.id == ligne_id).first()
        if not ligne:
            raise HTTPException(status_code=404, detail="Ligne non trouvée")
        for field, value in ligne_data.dict(exclude_unset=True).items():
            setattr(ligne, field, value)
        db.commit()
        db.refresh(ligne)
        return ligne

    @staticmethod
    def delete_ligne(db: Session, ligne_id: int):
        ligne = db.query(Ligne).filter(Ligne.id == ligne_id).first()
        if not ligne:
            raise HTTPException(status_code=404, detail="Ligne non trouvée")
        db.delete(ligne)
        db.commit()
        return ligne

    @staticmethod
    def get_ligne(db: Session, ligne_id: int):
        ligne = db.query(Ligne).filter(Ligne.id == ligne_id).first()
        if not ligne:
            raise HTTPException(status_code=404, detail="Ligne non trouvée")
        return ligne

    @staticmethod
    def list_lignes(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Ligne).offset(skip).limit(limit).all()
