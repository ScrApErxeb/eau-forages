from fastapi import FastAPI
from app.routers import (
    clients,
    sites,
    bornes,
    compteurs,
    techniciens,
    lignes,
    interventions,
    users,
)

app = FastAPI(
    title="Gestion Eau Forages API",
    version="0.1.0",
    description="API pour gérer les sites, bornes, compteurs, clients et interventions"
)

# Inclure les routers
app.include_router(clients.router, prefix="/clients", tags=["Clients"])
app.include_router(sites.router, prefix="/sites", tags=["Sites"])
app.include_router(bornes.router, prefix="/bornes", tags=["Bornes"])
app.include_router(compteurs.router, prefix="/compteurs", tags=["Compteurs"])
app.include_router(techniciens.router, prefix="/techniciens", tags=["Techniciens"])
app.include_router(lignes.router, prefix="/lignes", tags=["Lignes"])
app.include_router(interventions.router, prefix="/interventions", tags=["Interventions"])
app.include_router(users.router, prefix="/users", tags=["Users"])
# Route racine
@app.get("/", tags=["Root"])
def root():
    return {"message": "API Eau Forages prête"}
