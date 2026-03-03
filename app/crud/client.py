from sqlalchemy.orm import Session
from app.models.client import Client


def create_client(db: Session, name: str) -> Client:
    client = Client(name=name)
    db.add(client)
    db.flush()
    return client


def get_client_by_id(db: Session, client_id: int) -> Client | None:
    return db.get(Client, client_id)


def get_client_by_name(db: Session, name: str) -> Client | None:
    return db.query(Client).filter(Client.name == name).first()


def list_clients(db: Session, only_active: bool = False) -> list[Client]:
    query = db.query(Client)
    if only_active:
        query = query.filter(Client.is_active.is_(True))
    return query.all()
