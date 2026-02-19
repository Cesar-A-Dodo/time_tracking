from sqlalchemy.orm import Session
from app.models.employee import Employee


def create_employee(db: Session, employee: Employee) -> Employee:
    db.add(employee)
    return employee


def get_employee(db: Session, employee_id: int) -> Employee | None:
    return db.get(Employee, employee_id)


def list_employees(db: Session, *, only_active: bool = False) -> list[Employee]:
    q = db.query(Employee)
    if only_active:
        q = q.filter(Employee.is_active == True)
    return q.order_by(Employee.id.asc()).all()
