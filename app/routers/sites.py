# app/routers/sites.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteOut

router = APIRouter(prefix="/sites", tags=["sites"])

# --- Création d'un site ---
@router.post("/", response_model=SiteOut, status_code=status.HTTP_201_CREATED)
def create_site(site: SiteCreate, db: Session = Depends(get_db)):
    db_site = Site(**site.dict())
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

# --- Lister les sites avec pagination ---
@router.get("/", response_model=List[SiteOut])
def list_sites(skip: int = Query(0, ge=0), limit: int = Query(100, le=500), db: Session = Depends(get_db)):
    return db.query(Site).offset(skip).limit(limit).all()

# --- Obtenir un site par ID ---
@router.get("/{site_id}", response_model=SiteOut)
def get_site(site_id: int, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site non trouvé")
    return site

# --- Mise à jour partielle d'un site ---
@router.put("/{site_id}", response_model=SiteOut)
def update_site(site_id: int, site_data: SiteCreate, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site non trouvé")

    # Mise à jour partielle : seulement les champs fournis
    for field, value in site_data.dict(exclude_unset=True).items():
        setattr(site, field, value)

    db.commit()
    db.refresh(site)
    return site

# --- Supprimer un site ---
@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_site(site_id: int, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site non trouvé")
    db.delete(site)
    db.commit()
    return
