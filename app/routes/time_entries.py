from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.schemas import TimeEntryRead
from app.services.time_entry_service import (
    start_time_entry,
    pause_time_entry,
    resume_time_entry,
    finish_time_entry,
    cancel_time_entry,
)

router = APIRouter(prefix="/time_entries", tags=["Time Entry"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class StartTimeEntryRequest(BaseModel):
    employee_id: int
    activity_id: int


@router.post("/start", response_model=TimeEntryRead, status_code=status.HTTP_201_CREATED)
def start(payload: StartTimeEntryRequest, db: Session = Depends(get_db)):
    return start_time_entry(db, payload.employee_id, payload.activity_id)


@router.post("/{time_entry_id}/pause", response_model=TimeEntryRead)
def pause(time_entry_id: int, db: Session = Depends(get_db)):
    return pause_time_entry(db, time_entry_id)


@router.post("/{time_entry_id}/resume", response_model=TimeEntryRead)
def resume(time_entry_id: int, db: Session = Depends(get_db)):
    return resume_time_entry(db, time_entry_id)


@router.post("/{time_entry_id}/finish", response_model=TimeEntryRead)
def finish(time_entry_id: int, db: Session = Depends(get_db)):
    return finish_time_entry(db, time_entry_id)


@router.post("/{time_entry_id}/cancel", response_model=TimeEntryRead)
def cancel(time_entry_id: int, db: Session = Depends(get_db)):
    return cancel_time_entry(db, time_entry_id)