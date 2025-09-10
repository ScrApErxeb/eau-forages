from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.compteur import Compteur
from app.models.abonne import Abonne

class CompteurService:
    @staticmethod
    def create_compteur(db: Session, compteur_data):
        abonne = db.query(Abonne).filter(Abonne.id == compteur_data.abonne_id).first()
        if not abonne:
            raise HTTPException(status_code=404, detail="Abonne non trouvé")
        db_compteur = Compteur(**compteur_data.dict())
        db.add(db_compteur)
        db.commit()
        db.refresh(db_compteur)
        return db_compteur

    @staticmethod
    def update_compteur(db: Session, compteur_id: int, compteur_data):
        compteur = db.query(Compteur).filter(Compteur.id == compteur_id).first()
        if not compteur:
            raise HTTPException(status_code=404, detail="Compteur non trouvé")

        if compteur_data.abonne_id and compteur_data.abonne_id != compteur.abonne_id:
            abonne = db.query(Abonne).filter(Abonne.id == compteur_data.abonne_id).first()
            if not abonne:
                raise HTTPException(status_code=404, detail="Abonne non trouvé")

        for field, value in compteur_data.dict(exclude_unset=True).items():
            setattr(compteur, field, value)

        db.commit()
        db.refresh(compteur)
        return compteur

    @staticmethod
    def delete_compteur(db: Session, compteur_id: int):
        compteur = db.query(Compteur).filter(Compteur.id == compteur_id).first()
        if not compteur:
            raise HTTPException(status_code=404, detail="Compteur non trouvé")
        db.delete(compteur)
        db.commit()
        return compteur

    @staticmethod
    def get_compteur(db: Session, compteur_id: int):
        compteur = db.query(Compteur).filter(Compteur.id == compteur_id).first()
        if not compteur:
            raise HTTPException(status_code=404, detail="Compteur non trouvé")
        return compteur

    @staticmethod
    def list_compteurs(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Compteur).offset(skip).limit(limit).all()
