import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:flamme@localhost:5432/eau_forages"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ Importer tous les modèles pour qu'Alembic les voie
from app.models.client import Client
from app.models.site import Site
from app.models.compteur import Compteur
from app.models.borne import Borne


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
