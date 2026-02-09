from fastapi import FastAPI
from app.router import api_router

app = FastAPI(
    title="SACD API",
    description="Sistema de Apontamento e Controle de Demandas",
    version="0.1.0"
)

app.include_router(api_router)

@app.get("/")
def health_check():
    return {"status": "ok"}
