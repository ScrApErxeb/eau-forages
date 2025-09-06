# app/utils/db_utils.py
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

def get_or_404(db: Session, model, obj_id: int, detail: str):
    """Récupère un objet par id ou lève une 404."""
    obj = db.query(model).filter(model.id == obj_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail=detail)
    return obj

def check_unique(db: Session, model, field_name: str, value, exclude_id: Optional[int] = None):
    """Vérifie unicité d'un champ, optionnellement en excluant un id."""
    query = db.query(model).filter(getattr(model, field_name) == value)
    if exclude_id is not None:
        query = query.filter(model.id != exclude_id)
    exists = query.first()
    if exists:
        raise HTTPException(status_code=400, detail=f"{field_name} déjà utilisé")
