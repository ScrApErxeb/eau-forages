from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.technicien import Technicien
from app.schemas.technicien import TechnicienCreate, TechnicienOut

router = APIRouter(prefix="/techniciens", tags=["techniciens"])

# Créer un technicien
@router.post("/", response_model=TechnicienOut, status_code=status.HTTP_201_CREATED)
def create_technicien(technicien: TechnicienCreate, db: Session = Depends(get_db)):
    db_technicien = Technicien(**technicien.dict())
    db.add(db_technicien)
    db.commit()
    db.refresh(db_technicien)
    return db_technicien

# Lister tous les techniciens
@router.get("/", response_model=list[TechnicienOut])
def list_techniciens(db: Session = Depends(get_db)):
    return db.query(Technicien).all()

# Obtenir un technicien par id
@router.get("/{technicien_id}", response_model=TechnicienOut)
def get_technicien(technicien_id: int, db: Session = Depends(get_db)):
    technicien = db.query(Technicien).filter(Technicien.id == technicien_id).first()
    if not technicien:
        raise HTTPException(status_code=404, detail="Technicien non trouvé")
    return technicien

# Supprimer un technicien
@router.delete("/{technicien_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_technicien(technicien_id: int, db: Session = Depends(get_db)):
    technicien = db.query(Technicien).filter(Technicien.id == technicien_id).first()
    if not technicien:
        raise HTTPException(status_code=404, detail="Technicien non trouvé")
    db.delete(technicien)
    db.commit()
    return
