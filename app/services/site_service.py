from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.site import Site

class SiteService:
    @staticmethod
    def create_site(db: Session, site_data):
        db_site = Site(**site_data.dict())
        db.add(db_site)
        db.commit()
        db.refresh(db_site)
        return db_site

    @staticmethod
    def update_site(db: Session, site_id: int, site_data):
        site = db.query(Site).filter(Site.id == site_id).first()
        if not site:
            raise HTTPException(status_code=404, detail="Site non trouvé")
        for field, value in site_data.dict(exclude_unset=True).items():
            setattr(site, field, value)
        db.commit()
        db.refresh(site)
        return site

    @staticmethod
    def delete_site(db: Session, site_id: int):
        site = db.query(Site).filter(Site.id == site_id).first()
        if not site:
            raise HTTPException(status_code=404, detail="Site non trouvé")
        db.delete(site)
        db.commit()
        return site

    @staticmethod
    def get_site(db: Session, site_id: int):
        site = db.query(Site).filter(Site.id == site_id).first()
        if not site:
            raise HTTPException(status_code=404, detail="Site non trouvé")
        return site

    @staticmethod
    def list_sites(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Site).offset(skip).limit(limit).all()
