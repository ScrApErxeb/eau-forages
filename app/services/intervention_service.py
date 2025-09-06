from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.intervention import Intervention

class InterventionService:
    @staticmethod
    def create_intervention(db: Session, intervention_data):
        db_intervention = Intervention(**intervention_data.dict())
        db.add(db_intervention)
        db.commit()
        db.refresh(db_intervention)
        return db_intervention

    @staticmethod
    def update_intervention(db: Session, intervention_id: int, intervention_data):
        intervention = db.query(Intervention).filter(Intervention.id == intervention_id).first()
        if not intervention:
            raise HTTPException(status_code=404, detail="Intervention non trouvée")

        for field, value in intervention_data.dict(exclude_unset=True).items():
            setattr(intervention, field, value)

        db.commit()
        db.refresh(intervention)
        return intervention

    @staticmethod
    def delete_intervention(db: Session, intervention_id: int):
        intervention = db.query(Intervention).filter(Intervention.id == intervention_id).first()
        if not intervention:
            raise HTTPException(status_code=404, detail="Intervention non trouvée")
        db.delete(intervention)
        db.commit()
        return intervention

    @staticmethod
    def get_intervention(db: Session, intervention_id: int):
        intervention = db.query(Intervention).filter(Intervention.id == intervention_id).first()
        if not intervention:
            raise HTTPException(status_code=404, detail="Intervention non trouvée")
        return intervention

    @staticmethod
    def list_interventions(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Intervention).offset(skip).limit(limit).all()
