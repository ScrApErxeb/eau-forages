# app/routers/sites.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteOut

router = APIRouter(prefix="/sites", tags=["sites"])

# Créer un site
@router.post("/", response_model=SiteOut, status_code=status.HTTP_201_CREATED)
def create_site(site: SiteCreate, db: Session = Depends(get_db)):
    db_site = Site(**site.dict())
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

# Lister tous les sites
@router.get("/", response_model=list[SiteOut])
def list_sites(db: Session = Depends(get_db)):
    sites = db.query(Site).all()
    return sites

# Obtenir un site par id
@router.get("/{site_id}", response_model=SiteOut)
def get_site(site_id: int, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site non trouvé")
    return site

# Mettre à jour un site
@router.put("/{site_id}", response_model=SiteOut)
def update_site(site_id: int, site_data: SiteCreate, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site non trouvé")
    for key, value in site_data.dict().items():
        setattr(site, key, value)
    db.commit()
    db.refresh(site)
    return site

# Supprimer un site
@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_site(site_id: int, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site non trouvé")
    db.delete(site)
    db.commit()
    return
