from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.time_entry import TimeEntry
from app.models.employee import Employee
from app.schemas import TimeEntryStatus, FinishType
from app.crud.time_entry_block import create_block, get_open_block, close_block
from app.crud.activity import get_activity
from app.crud.employee import get_employee
from app.services.exceptions import ActivityNotFoundError, ActivityInactiveError
from app.services.exceptions import (
    EmployeeInactiveError,
    OpenTimeEntryExistsError,
    InvalidStatusTransitionError,
    TimeEntryAlreadyFinalizedError,
)

def start_time_entry(db: Session, employee_id: int, activity_id: int) -> TimeEntry:
    employee = get_employee(db, employee_id)
    
    if not employee or not employee.is_active:
        raise EmployeeInactiveError("Funcionário inativo ou inexistente!")
    
    activity = get_activity(db, activity_id)
    
    if not activity:
        raise ActivityNotFoundError("Atividade inexistente!")
    if not activity.is_active:
        raise ActivityInactiveError("Atividade inativa!")
    
    open_entry = (
        db.query(TimeEntry)
        .filter(
            TimeEntry.employee_id == employee_id,
            TimeEntry.status.in_([TimeEntryStatus.INICIADO, TimeEntryStatus.PAUSADO]),
        )
        .first()
    )

    if open_entry:
        raise OpenTimeEntryExistsError("Funcionário já possui apontamento aberto!")
    
    time_entry = TimeEntry(
        employee_id = employee_id,
        activity_id = activity_id,
        status = TimeEntryStatus.INICIADO,
    )

    db.add(time_entry)
    db.flush()

    create_block(db, time_entry.id)

    db.commit()
    db.refresh(time_entry)

    return time_entry


def pause_time_entry(db: Session, time_entry_id) -> TimeEntry:
    time_entry = db.get(TimeEntry, time_entry_id)

    if not time_entry:
        raise ValueError("Apontamento não encontrado!")
    
    if time_entry.status != TimeEntryStatus.INICIADO:
        raise InvalidStatusTransitionError("Só é possivel pausar se estiver INICIADO!")
    
    block = get_open_block(db, time_entry.id)

    if not block:
        raise InvalidStatusTransitionError("Nenhum bloco aberto para pausar!")
    
    close_block(db, block)

    time_entry.status = TimeEntryStatus.PAUSADO

    db.commit()
    db.refresh(time_entry)

    return time_entry


def resume_time_entry(db: Session, time_entry_id: int) -> TimeEntry:
    time_entry = db.get(TimeEntry, time_entry_id)

    if not time_entry:
        raise InvalidStatusTransitionError("Só é possível retomar se estiver PAUSADO!")
    
    create_block(db, time_entry.id)

    time_entry.status = TimeEntryStatus.INICIADO

    db.commit()
    db.refresh(time_entry)

    return time_entry


def finish_time_entry(db: Session, time_entry_id: int) -> TimeEntry:
    time_entry = db.get(TimeEntry, time_entry_id)

    if not time_entry:
        raise ValueError("Apontamento não encontrado!")
    
    if time_entry.status == TimeEntryStatus.FINALIZADO:
        raise TimeEntryAlreadyFinalizedError("Apontamento já foi finalizado!")
    
    block = get_open_block(db, time_entry.id)

    if block:
        close_block(db, block)

    time_entry.status = TimeEntryStatus.FINALIZADO
    time_entry.finish_type = FinishType.CONCLUIDA

    db.commit()
    db.refresh(time_entry)

    return time_entry


def cancel_time_entry(db: Session, time_entry_id: int) -> TimeEntry:
    time_entry = db.get(TimeEntry, time_entry_id)

    if not time_entry:
        raise ValueError("Apontamento não encontrado!")
    
    if time_entry.status == TimeEntryStatus.FINALIZADO:
        raise TimeEntryAlreadyFinalizedError("Apontamento já foi finalizado!")
    
    block = get_open_block(db, time_entry.id)

    if block:
        close_block(db, block)

    time_entry.status = TimeEntryStatus.FINALIZADO
    time_entry.finish_type = FinishType.CANCELADO

    db.commit()
    db.refresh(time_entry)

    return time_entry
