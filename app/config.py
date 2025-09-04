# app/config.py

class Settings:
    # Chaîne de connexion PostgreSQL
    DATABASE_URL = "postgresql+psycopg2://postgres:flamme@localhost:5432/eau_forages"

    # Options SQLAlchemy
    SQLALCHEMY_ECHO = True         # True pour dev, False pour prod
    SQLALCHEMY_POOL_SIZE = 10      # Taille du pool de connexion
    SQLALCHEMY_MAX_OVERFLOW = 20   # Connexions supplémentaires autorisées

# Instance unique à importer partout
settings = Settings()
