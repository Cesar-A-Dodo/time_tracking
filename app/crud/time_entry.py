from sqlalchemy.orm import Session
from app.models.time_entry import TimeEntry


def create_time_entry(db: Session, time_entry: TimeEntry) -> TimeEntry:
    db.add(time_entry)
    db.commit()
    db.refresh(time_entry)
    return time_entry

def get_time_entry_by_id(db: Session, time_entry_id: int) -> TimeEntry | None:
    return db.query(TimeEntry).filter(TimeEntry.id == time_entry_id).first()

def get_open_time_entry_by_employee(db: Session, employee_id: int) -> TimeEntry | None:
    return (
        db.query(TimeEntry)
        .filter(
            TimeEntry.employee_id == employee_id,
            TimeEntry.end_time.is_(None)
        )
        .first()
    )

def update_time_entry(db: Session, time_entry: TimeEntry) -> TimeEntry:
    db.commit()
    db.refresh(time_entry)
    return time_entry

def delete_time_entry(db: Session, time_entry: TimeEntry) -> None:
    db.delete(time_entry)
    db.commit()
