from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.schemas import EmployeeCreate, EmployeeRead
from app.services.employee_service import (
    create_new_employee,
    list_all_employees,
    get_employee_by_id,
    update_employee,
    disable_employee,
)
from app.services.exceptions import EmployeeNotFoundError, EmployeeAlreadyInactiveError


router = APIRouter(prefix="/employees", tags=["Employess"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class EmployeeUpdate(BaseModel):
    name: str | None = None
    role: str | None = None


class DisableEmployeeRequest(BaseModel):
    cancel_reason: str | None = None


@router.post("/", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    return create_new_employee(db, name=payload.name, role=payload.role)


@router.get("/", response_model=list[EmployeeRead])
def list_employees(only_active: bool = False, db: Session = Depends(get_db)):
    return list_all_employees(db, only_active=only_active)


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: int,db: Session = Depends(get_db)):
    try:
        return get_employee_by_id(db, employee_id)
    except EmployeeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.patch("/{employee_id}", response_model=EmployeeRead)
def patch_employee(employee_id: int, payload: EmployeeUpdate, db: Session = Depends(get_db)):
    try:
        return update_employee(db, employee_id, name=payload.name, role=payload.role)
    except EmployeeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{employee_id}/disable", response_model=EmployeeRead)
def disable_employee_route(employee_id: int, payload: DisableEmployeeRequest | None = None, db: Session = Depends(get_db)):
    try:
        return disable_employee(
            db,
            employee_id,
            cancel_reason=(payload.cancel_reason if payload else None),
        )
    except EmployeeNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except EmployeeAlreadyInactiveError as e:
        raise HTTPException(status_code=409, detail=str(e))
