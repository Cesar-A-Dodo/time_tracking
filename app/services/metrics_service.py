from sqlalchemy.orm import Session
from datetime import timedelta
from app.models.time_entry import TimeEntry
from app.schemas import TimeEntryStatus, FinishType
from app.services.activity_service import get_activity_by_id
from app.services.employee_service import get_employee_by_id


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

def get_activity_summary_metrics(db: Session, activity_id: int) -> dict:
    get_activity_by_id(db, activity_id)

    entries = (
        db.query(TimeEntry)
        .filter(
            TimeEntry.activity_id == activity_id,
            TimeEntry.status == TimeEntryStatus.FINALIZADO,
        )
        .all()
    )

    completed = [e for e in entries if e.finish_type == FinishType.CONCLUIDA]
    canceled = [e for e in entries if e.finish_type == FinishType.CANCELADO]

    if not completed:
        return {
            "activity_id": activity_id,
            "completed_entries": 0,
            "canceled_entries": len(canceled),
            "total_completed_seconds": 0.0,
            "total_completed_minutes": 0.0,
            "average_completed_seconds": 0.0,
            "average_completed_minutes": 0.0,
            "min_completed_seconds": 0.0,
            "min_completed_minutes": 0.0,
            "max_completed_seconds": 0.0,
            "max_completed_minutes": 0.0,
        }

    durations = [e.calculate_total_time() for e in completed]
    total = sum(durations, timedelta())
    avg = total / len(durations)
    min_d = min(durations)
    max_d = max(durations)

    def to_seconds(td: timedelta) -> float:
        return float(td.total_seconds())

    total_s = to_seconds(total)
    avg_s = to_seconds(avg)
    min_s = to_seconds(min_d)
    max_s = to_seconds(max_d)

    return {
        "activity_id": activity_id,
        "completed_entries": len(completed),
        "canceled_entries": len(canceled),
        "total_completed_seconds": total_s,
        "total_completed_minutes": total_s / 60,
        "average_completed_seconds": avg_s,
        "average_completed_minutes": avg_s / 60,
        "min_completed_seconds": min_s,
        "min_completed_minutes": min_s / 60,
        "max_completed_seconds": max_s,
        "max_completed_minutes": max_s / 60,
    }

def get_employee_activity_average_time(
    db: Session,
    employee_id: int,
    activity_id: int,
) -> dict:
    get_employee_by_id(db, employee_id)
    get_activity_by_id(db, activity_id)

    entries = (
        db.query(TimeEntry)
        .filter(
            TimeEntry.employee_id == employee_id,
            TimeEntry.activity_id == activity_id,
            TimeEntry.status == TimeEntryStatus.FINALIZADO,
            TimeEntry.finish_type == FinishType.CONCLUIDA,
        )
        .all()
    )

    if not entries:
        return {
            "employee_id": employee_id,
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
        "employee_id": employee_id,
        "activity_id": activity_id,
        "completed_entries": len(entries),
        "average_seconds": float(avg_seconds),
        "average_minutes": float(avg_seconds / 60),
    }
