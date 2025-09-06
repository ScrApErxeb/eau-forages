# app/routers/techniciens.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.technicien import Technicien
from app.schemas.technicien import TechnicienCreate, TechnicienOut
from app.utils.db_utils import get_or_404
from app.utils.pagination import paginate

router = APIRouter(prefix="/techniciens", tags=["techniciens"])

@router.post("/", response_model=TechnicienOut, status_code=status.HTTP_201_CREATED)
def create_technicien(data: TechnicienCreate, db: Session = Depends(get_db)):
    tech = Technicien(**data.dict())
    db.add(tech)
    db.commit()
    db.refresh(tech)
    return tech

@router.get("/", response_model=List[TechnicienOut])
def list_techniciens(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return paginate(db.query(Technicien), skip, limit)

@router.get("/{technicien_id}", response_model=TechnicienOut)
def get_technicien(technicien_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Technicien, technicien_id, "Technicien non trouvé")

@router.put("/{technicien_id}", response_model=TechnicienOut)
def update_technicien(technicien_id: int, data: TechnicienCreate, db: Session = Depends(get_db)):
    tech = get_or_404(db, Technicien, technicien_id, "Technicien non trouvé")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(tech, field, value)
    db.commit()
    db.refresh(tech)
    return tech

@router.delete("/{technicien_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_technicien(technicien_id: int, db: Session = Depends(get_db)):
    tech = get_or_404(db, Technicien, technicien_id, "Technicien non trouvé")
    db.delete(tech)
    db.commit()
    return
