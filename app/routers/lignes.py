from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.ligne import Ligne
from app.schemas.ligne import LigneCreate, LigneOut

router = APIRouter(prefix="/lignes", tags=["lignes"])

# Créer une ligne
@router.post("/", response_model=LigneOut, status_code=status.HTTP_201_CREATED)
def create_ligne(ligne: LigneCreate, db: Session = Depends(get_db)):
    db_ligne = Ligne(**ligne.dict())
    db.add(db_ligne)
    db.commit()
    db.refresh(db_ligne)
    return db_ligne

# Lister toutes les lignes
@router.get("/", response_model=list[LigneOut])
def list_lignes(db: Session = Depends(get_db)):
    return db.query(Ligne).all()

# Obtenir une ligne par id
@router.get("/{ligne_id}", response_model=LigneOut)
def get_ligne(ligne_id: int, db: Session = Depends(get_db)):
    ligne = db.query(Ligne).filter(Ligne.id == ligne_id).first()
    if not ligne:
        raise HTTPException(status_code=404, detail="Ligne non trouvée")
    return ligne

# Supprimer une ligne
@router.delete("/{ligne_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ligne(ligne_id: int, db: Session = Depends(get_db)):
    ligne = db.query(Ligne).filter(Ligne.id == ligne_id).first()
    if not ligne:
        raise HTTPException(status_code=404, detail="Ligne non trouvée")
    db.delete(ligne)
    db.commit()
    return
