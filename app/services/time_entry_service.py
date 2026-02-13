from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.time_entry import TimeEntry, TimeEntryStatus
from app.crud.time_entry import create_time_entry, get_open_time_entry_by_employee, get_time_entry_by_id, update_time_entry

class TimeEntryAlreadyOpenError(Exception):
    pass

class TimeEntryNotFoundError(Exception):
    pass

class TimeEntryAlreadyFinishedError(Exception):
    pass

def start_time_entry(db: Session, employee_id: int, activity_id: int) -> TimeEntry:
    open_entry = get_open_time_entry_by_employee(db, employee_id)

    if open_entry:
        raise TimeEntryAlreadyOpenError("Funcionário já possui um apontamento aberto.")

    time_entry = TimeEntry(
        employee_id = employee_id,
        activity_id = activity_id,
        start_time = datetime.now(timezone.utc),
        status = TimeEntryStatus.CRIADO
    )

    return create_time_entry(db, time_entry)

def finish_time_entry(db: Session, time_entry_id: int) -> TimeEntry:
    time_entry = get_time_entry_by_id(db, time_entry_id)

    if not time_entry:
        raise TimeEntryNotFoundError("Apontamento não encontrado.")
    
    if time_entry.end_time is not None:
        raise TimeEntryAlreadyFinishedError("Apontamento ja foi finalizado.")
    
    time_entry.end_time = datetime.now(timezone.utc)
    time_entry.status = TimeEntryStatus.FINALIZADO

    return update_time_entry(db, time_entry)
