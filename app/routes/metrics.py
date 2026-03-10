from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.schemas import ActivityAverageTimeRead, ActivitySummaryMetricsRead, EmployeeActivityAverageTimeRead
from app.services.metrics_service import get_activity_average_time, get_activity_summary_metrics, get_employee_activity_average_time

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

@router.get("/activities/{activity_id}/summary", response_model=ActivitySummaryMetricsRead)
def activity_summary(activity_id: int, db: Session = Depends(get_db)):
    return get_activity_summary_metrics(db, activity_id)

@router.get(
    "/employees/{employee_id}/activities/{activity_id}/average-time",
    response_model=EmployeeActivityAverageTimeRead,
)
def employee_activity_average_time(
    employee_id: int,
    activity_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    return get_employee_activity_average_time(
        db,
        employee_id,
        activity_id,
        start_date=start_date,
        end_date=end_date,
    )
