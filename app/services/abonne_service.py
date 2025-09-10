# app/services/abonne_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.abonne import Abonne
from app.schemas.abonne import AbonneCreate, AbonneUpdate

class AbonneService:
    @staticmethod
    def create_abonne(db: Session, abonne_data: AbonneCreate):
        if db.query(Abonne).filter(Abonne.num_cnib == abonne_data.num_cnib).first():
            raise HTTPException(status_code=400, detail="CNIB déjà utilisé")
        if db.query(Abonne).filter(Abonne.numero_abonne == abonne_data.numero_abonne).first():
            raise HTTPException(status_code=400, detail="Numéro d'abonné déjà utilisé")
        if abonne_data.tel and db.query(Abonne).filter(Abonne.tel == abonne_data.tel).first():
            raise HTTPException(status_code=400, detail="Téléphone déjà utilisé")

        db_abonne = Abonne(**abonne_data.dict())
        db.add(db_abonne)
        db.commit()
        db.refresh(db_abonne)
        return db_abonne

    @staticmethod
    def update_abonne(db: Session, abonne_id: int, abonne_data: AbonneUpdate):
        abonne = db.query(Abonne).filter(Abonne.id == abonne_id).first()
        if not abonne:
            raise HTTPException(status_code=404, detail="Abonné non trouvé")

        if abonne_data.num_cnib and abonne_data.num_cnib != abonne.num_cnib:
            if db.query(Abonne).filter(Abonne.num_cnib == abonne_data.num_cnib, Abonne.id != abonne_id).first():
                raise HTTPException(status_code=400, detail="CNIB déjà utilisé")

        if abonne_data.numero_abonne and abonne_data.numero_abonne != abonne.numero_abonne:
            if db.query(Abonne).filter(Abonne.numero_abonne == abonne_data.numero_abonne, Abonne.id != abonne_id).first():
                raise HTTPException(status_code=400, detail="Numéro d'abonné déjà utilisé")

        if abonne_data.tel and abonne_data.tel != abonne.tel:
            if db.query(Abonne).filter(Abonne.tel == abonne_data.tel, Abonne.id != abonne_id).first():
                raise HTTPException(status_code=400, detail="Téléphone déjà utilisé")

        for field, value in abonne_data.dict(exclude_unset=True).items():
            setattr(abonne, field, value)

        db.commit()
        db.refresh(abonne)
        return abonne

    @staticmethod
    def delete_abonne(db: Session, abonne_id: int):
        abonne = db.query(Abonne).filter(Abonne.id == abonne_id).first()
        if not abonne:
            raise HTTPException(status_code=404, detail="Abonné non trouvé")
        db.delete(abonne)
        db.commit()
        return abonne

    @staticmethod
    def get_abonne(db: Session, abonne_id: int):
        abonne = db.query(Abonne).filter(Abonne.id == abonne_id).first()
        if not abonne:
            raise HTTPException(status_code=404, detail="Abonné non trouvé")
        return abonne

    @staticmethod
    def list_abonnes(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Abonne).offset(skip).limit(limit).all()
