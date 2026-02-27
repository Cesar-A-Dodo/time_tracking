from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.schemas import ActivityAverageTimeRead
from app.services.metrics_service import get_activity_average_time

router = APIRouter(prefix="/metrics", tags=["Metrics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/activities/{activity_id}/average-time", response_model=ActivityAverageTimeRead)
def activity_average_time(activity_id: int, db: Session = Depends(get_db)):
    return get_activity_average_time(db, activity_id)
