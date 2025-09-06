# app/routers/lignes.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.ligne import Ligne
from app.schemas.ligne import LigneCreate, LigneOut
from app.utils.db_utils import get_or_404
from app.utils.pagination import paginate

router = APIRouter(prefix="/lignes", tags=["lignes"])

@router.post("/", response_model=LigneOut, status_code=status.HTTP_201_CREATED)
def create_ligne(data: LigneCreate, db: Session = Depends(get_db)):
    ligne = Ligne(**data.dict())
    db.add(ligne)
    db.commit()
    db.refresh(ligne)
    return ligne

@router.get("/", response_model=List[LigneOut])
def list_lignes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return paginate(db.query(Ligne), skip, limit)

@router.get("/{ligne_id}", response_model=LigneOut)
def get_ligne(ligne_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Ligne, ligne_id, "Ligne non trouvée")

@router.put("/{ligne_id}", response_model=LigneOut)
def update_ligne(ligne_id: int, data: LigneCreate, db: Session = Depends(get_db)):
    ligne = get_or_404(db, Ligne, ligne_id, "Ligne non trouvée")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(ligne, field, value)
    db.commit()
    db.refresh(ligne)
    return ligne

@router.delete("/{ligne_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ligne(ligne_id: int, db: Session = Depends(get_db)):
    ligne = get_or_404(db, Ligne, ligne_id, "Ligne non trouvée")
    db.delete(ligne)
    db.commit()
    return
