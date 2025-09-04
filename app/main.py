from fastapi import FastAPI
from app.routers import clients, sites,techniciens, lignes, interventions, bornes, compteurs

app = FastAPI(title="Gestion Eau Forages API", version="0.1.0")

app.include_router(clients.router)
app.include_router(sites.router)
app.include_router(bornes.router)
app.include_router(compteurs.router)
app.include_router(techniciens.router)
app.include_router(lignes.router)
app.include_router(interventions.router)

@app.get("/")
def root():
    return {"msg": "API Eau Forages prête"}
