from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.schemas import ActivityRead
from app.services.activity_service import (
    create_new_activity,
    list_all_activities,
    get_activity_by_id,
    update_activity,
    disable_activity,
)

router = APIRouter(prefix="/activities", tags=["Activities"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ActivityCreateRequest(BaseModel):
    name: str
    client: str
    estimated_time_minutes: int | None = None


class ActivityUpdate(BaseModel):
    name: str | None = None
    client: str | None = None
    estimated_time_minutes: int | None = None


@router.post("/", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
def create_activity(payload: ActivityCreateRequest, db: Session = Depends(get_db)):
    return create_new_activity(
        db,
        name=payload.name,
        client=payload.client,
        estimated_time_minutes=payload.estimated_time_minutes,
    )


@router.get("/", response_model=list[ActivityRead])
def list_activities(only_active: bool = False, db: Session = Depends(get_db)):
    return list_all_activities(db, only_active=only_active)


@router.get("/{activity_id}", response_model=ActivityRead)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    return get_activity_by_id(db, activity_id)


@router.patch("/{activity_id}", response_model=ActivityRead)
def patch_activity(activity_id: int, payload: ActivityUpdate, db: Session = Depends(get_db)):
    return update_activity(
        db,
        activity_id,
        name=payload.name,
        client=payload.client,
        estimated_time_minutes=payload.estimated_time_minutes,
    )


@router.post("/{activity_id}/disable", response_model=ActivityRead)
def disable_activity_route(activity_id: int, db: Session = Depends(get_db)):
    return disable_activity(db, activity_id)
