from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.models.time_entry import TimeEntry
from app.schemas import TimeEntryStatus, FinishType
from app.crud.employee import create_employee, get_employee, list_employees
from app.crud.time_entry_block import get_open_block, close_block
from app.services.exceptions import EmployeeNotFoundError, EmployeeAlreadyInactiveError


def create_new_employee(db: Session, *, name: str, role: str) -> Employee:
    employee = Employee(name = name, role = role, is_active = True)

    create_employee(db, employee)
    db.commit()
    db.refresh(employee)
    return employee


def get_employee_by_id(db: Session, employee_id: int) -> Employee:
    employee = get_employee(db, employee_id)
    if not employee:
        raise EmployeeNotFoundError("Funcionário não encontrado!")
    return employee


def list_all_employees(db: Session, *, only_active: bool = False) -> list[Employee]:
    return list_employees(db, only_active=only_active)


def update_employee(
        db: Session,
        employee_id: int,
        *,
        name: str | None = None,
        role: str | None = None,
) -> Employee:
    employee = get_employee_by_id(db, employee_id)

    if name is not None:
        employee.name = name
    if role is not None:
        employee.role = role

    db.commit
    db.refresh(employee)
    return employee


def disable_employee(
        db: Session,
        employee_id: int,
        *,
        cancel_reason: str | None = None,
) -> Employee:
    employee = get_employee_by_id(db, employee_id)

    if not employee.is_active:
        raise EmployeeAlreadyInactiveError("Funcionário já está inativo!")
    
    employee.is_active = False

    reason = cancel_reason or "AUTO_CANCEL_ON_EMPLOYEE_DEACTIVATION"

    open_entries = (
        db.query(TimeEntry)
        .filter(
            TimeEntry.employee_id == employee_id,
            TimeEntry.status.in_([TimeEntryStatus.INICIADO, TimeEntryStatus.PAUSADO]),
        )
        .all()
    )

    for entry in open_entries:
        block = get_open_block(db, entry.id)
        if block:
            close_block(db, block)

        entry.status = TimeEntryStatus.FINALIZADO
        entry.finish_type = FinishType.CANCELADO
        entry.cancel_reason = reason
    
    db.commit()
    db.refresh(employee)
    return employee