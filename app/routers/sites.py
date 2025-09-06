# app/routers/sites.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteOut
from app.utils.db_utils import get_or_404
from app.utils.pagination import paginate

router = APIRouter(prefix="/sites", tags=["sites"])

@router.post("/", response_model=SiteOut, status_code=status.HTTP_201_CREATED)
def create_site(data: SiteCreate, db: Session = Depends(get_db)):
    site = Site(**data.dict())
    db.add(site)
    db.commit()
    db.refresh(site)
    return site

@router.get("/", response_model=List[SiteOut])
def list_sites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return paginate(db.query(Site), skip, limit)

@router.get("/{site_id}", response_model=SiteOut)
def get_site(site_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Site, site_id, "Site non trouvé")

@router.put("/{site_id}", response_model=SiteOut)
def update_site(site_id: int, data: SiteCreate, db: Session = Depends(get_db)):
    site = get_or_404(db, Site, site_id, "Site non trouvé")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(site, field, value)
    db.commit()
    db.refresh(site)
    return site

@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_site(site_id: int, db: Session = Depends(get_db)):
    site = get_or_404(db, Site, site_id, "Site non trouvé")
    db.delete(site)
    db.commit()
    return
