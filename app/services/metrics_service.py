from sqlalchemy.orm import Session
from datetime import timedelta
from app.models.time_entry import TimeEntry
from app.schemas import TimeEntryStatus, FinishType
from app.services.activity_service import get_activity_by_id


def get_activity_average_time(db: Session, activity_id: int) -> dict:
    get_activity_by_id(db, activity_id)

    entries = (
        db.query(TimeEntry)
        .filter(
            TimeEntry.activity_id == activity_id,
            TimeEntry.status == TimeEntryStatus.FINALIZADO,
            TimeEntry.finish_type == FinishType.CONCLUIDA,
        )
        .all()
    )

    if not entries:
        return {
            "activity_id": activity_id,
            "completed_entries": 0,
            "average_seconds": 0.0,
            "average_minutes": 0.0,
        }

    total = timedelta()
    for entry in entries:
        total += entry.calculate_total_time()

    avg = total / len(entries)
    avg_seconds = avg.total_seconds()

    return {
        "activity_id": activity_id,
        "completed_entries": len(entries),
        "average_seconds": float(avg_seconds),
        "average_minutes": float(avg_seconds / 60),
    }