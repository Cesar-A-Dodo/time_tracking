from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.crud.activity import create_activity, get_activity, list_activities
from app.services.exceptions import ActivityNotFoundError, ActivityAlreadyInactiveError


def create_new_activity(
        db: Session,
        *,
        name: str,
        client: str,
        estimated_time_minutes: int | None = None,
) -> Activity:
    activity = Activity(
        name = name,
        client = client,
        estimated_time_minutes = estimated_time_minutes,
        is_active = True,
    )

    create_activity(db, activity)
    db.commit()
    db.refresh(activity)
    return activity


def get_activity_by_id(db: Session, activity_id: int) -> Activity:
    activity = get_activity(db, activity_id)
    if not activity:
        raise ActivityNotFoundError("Atividade não encontrada!")
    return activity


def list_all_activities(db: Session, *, only_active: bool = False) -> list[Activity]:
    return list_activities(db, only_active = only_active)


def update_activity(
        db: Session,
        activity_id: int,
        *,
        name: str | None = None,
        client: str | None = None,
        estimated_time_minutes: int | None = None,
) -> Activity:
    activity = get_activity_by_id(db, activity_id)

    if name is not None:
        activity.name = name
    if client is not None:
        activity.client = client

    activity.estimated_time_minutes = estimated_time_minutes

    db.commit()
    db.refresh(activity)
    return activity


def disable_activity(db: Session, activity_id: int) -> Activity:
    activity = get_activity_by_id(db, activity_id)
    
    if not activity.is_active:
        raise ActivityAlreadyInactiveError("Atividade já está inativa!")
    
    activity.is_active = False

    db.commit()
    db.refresh(activity)
    return activity
