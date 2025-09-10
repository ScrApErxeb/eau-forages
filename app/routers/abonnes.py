from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.abonne import Abonne
from app.schemas.abonne import AbonneCreate, AbonneUpdate, AbonneOut
from app.utils.db_utils import get_or_404, check_unique
from app.utils.pagination import paginate

router = APIRouter(prefix="/abonnes", tags=["abonnes"])

@router.post("/", response_model=AbonneOut, status_code=status.HTTP_201_CREATED)
def create_abonne(abonne_data: AbonneCreate, db: Session = Depends(get_db)):
    check_unique(db, Abonne, "num_cnib", abonne_data.num_cnib)
    check_unique(db, Abonne, "numero_abonne", abonne_data.numero_abonne)
    if abonne_data.tel:
        check_unique(db, Abonne, "tel", abonne_data.tel)
    abonne = Abonne(**abonne_data.dict())
    db.add(abonne)
    db.commit()
    db.refresh(abonne)
    return abonne

@router.get("/", response_model=List[AbonneOut])
def list_abonnes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return paginate(db.query(Abonne), skip, limit)

@router.get("/{abonne_id}", response_model=AbonneOut)
def get_abonne(abonne_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Abonne, abonne_id, "Abonné non trouvé")

@router.put("/{abonne_id}", response_model=AbonneOut)
def update_abonne(abonne_id: int, abonne_data: AbonneUpdate, db: Session = Depends(get_db)):
    abonne = get_or_404(db, Abonne, abonne_id, "Abonné non trouvé")

    if abonne_data.num_cnib and abonne.num_cnib != abonne_data.num_cnib:
        check_unique(db, Abonne, "num_cnib", abonne_data.num_cnib, exclude_id=abonne_id)
    if abonne_data.numero_abonne and abonne.numero_abonne != abonne_data.numero_abonne:
        check_unique(db, Abonne, "numero_abonne", abonne_data.numero_abonne, exclude_id=abonne_id)
    if abonne_data.tel and abonne.tel != abonne_data.tel:
        check_unique(db, Abonne, "tel", abonne_data.tel, exclude_id=abonne_id)

    for field, value in abonne_data.dict(exclude_unset=True).items():
        setattr(abonne, field, value)
    db.commit()
    db.refresh(abonne)
    return abonne

@router.delete("/{abonne_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_abonne(abonne_id: int, db: Session = Depends(get_db)):
    abonne = get_or_404(db, Abonne, abonne_id, "Abonné non trouvé")
    db.delete(abonne)
    db.commit()
    return
