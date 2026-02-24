from fastapi import FastAPI
from app.router import api_router
from app.exception_handlers import register_exception_handlers

app = FastAPI(
    title="SACD API",
    description="Sistema de Apontamento e Controle de Demandas",
    version="0.1.0"
)

register_exception_handlers(app)
app.include_router(api_router)

@app.get("/")
def health_check():
    return {"status": "ok"}
