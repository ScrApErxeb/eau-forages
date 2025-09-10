from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ← ajouté
from app.routers import (
    abonnes,
    sites,
    bornes,
    techniciens,
    lignes,
    interventions,
    users,
    consommations,
)

app = FastAPI(
    title="Gestion Eau Forages API",
    version="0.1.0",
    description="API pour gérer les sites, bornes, compteurs, abonnes et interventions"
)

# --- Configurer CORS pour le frontend React
origins = [
    "http://localhost:5173",  # port de ton frontend Vite
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # autorise le frontend
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, PUT, DELETE…
    allow_headers=["*"],         # headers autorisés
)

# Inclure les routers
app.include_router(abonnes.router, prefix="/abonnes", tags=["Abonnes"])
app.include_router(sites.router, prefix="/sites", tags=["Sites"])
app.include_router(bornes.router, prefix="/bornes", tags=["Bornes"])
#app.include_router(compteurs.router, prefix="/compteurs", tags=["Compteurs"])
app.include_router(techniciens.router, prefix="/techniciens", tags=["Techniciens"])
app.include_router(lignes.router, prefix="/lignes", tags=["Lignes"])
app.include_router(interventions.router, prefix="/interventions", tags=["Interventions"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(consommations.router, prefix="/consommations", tags=["Consommations"])


# Route racine
@app.get("/", tags=["Root"])
def root():
    return {"message": "API Eau Forages prête"}
