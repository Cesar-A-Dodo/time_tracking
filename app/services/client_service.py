from sqlalchemy.orm import Session
from app.crud.client import (
    create_client,
    get_client_by_id,
    get_client_by_name,
    list_clients,
)
from app.services.exceptions import (
    ClientNotFoundError,
    ClientAlreadyInactiveError,
)


def create_new_client(db: Session, name: str):
    existing = get_client_by_name(db, name)
    if existing:
        raise ValueError("Client name already exists.")

    client = create_client(db, name)
    db.commit()
    db.refresh(client)
    return client


def list_all_clients(db: Session, only_active: bool = False):
    return list_clients(db, only_active=only_active)


def get_client(db: Session, client_id: int):
    client = get_client_by_id(db, client_id)
    if not client:
        raise ClientNotFoundError("Client not found.")
    return client


def disable_client(db: Session, client_id: int):
    client = get_client(db, client_id)

    if not client.is_active:
        raise ClientAlreadyInactiveError("Client already inactive.")

    client.is_active = False
    db.commit()
    db.refresh(client)
    return client
