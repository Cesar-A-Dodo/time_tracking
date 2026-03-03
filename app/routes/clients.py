from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.schemas import ClientCreate, ClientRead
from app.services.client_service import (
    create_new_client,
    list_all_clients,
    get_client,
    disable_client,
)

router = APIRouter(prefix="/clients", tags=["Clients"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
def create_client_route(payload: ClientCreate, db: Session = Depends(get_db)):
    return create_new_client(db, name=payload.name)


@router.get("/", response_model=list[ClientRead])
def list_clients_route(only_active: bool = False, db: Session = Depends(get_db)):
    return list_all_clients(db, only_active=only_active)


@router.get("/{client_id}", response_model=ClientRead)
def get_client_route(client_id: int, db: Session = Depends(get_db)):
    return get_client(db, client_id)


@router.post("/{client_id}/disable", response_model=ClientRead)
def disable_client_route(client_id: int, db: Session = Depends(get_db)):
    return disable_client(db, client_id)
