from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class TimeEntryStatus(str, Enum):
    INICIADO = "INICIADO"
    PAUSADO = "PAUSADO"
    FINALIZADO = "FINALIZADO"

class FinishType(str, Enum):
    CONCLUIDA = "CONCLUIDA"
    CANCELADO = "CANCELADO"

class EmployeeBase(BaseModel):
    name: str
    role: str

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeRead(EmployeeBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class ActivityBase(BaseModel):
    name: str
    client: str

class ActivityCreate(ActivityBase):
    pass

class ActivityRead(ActivityBase):
    id: int
    is_active: bool
    estimated_time_minutes: int | None = None

    class Config:
        from_attributes = True


class TimeEntryBase(BaseModel):
    employee_id: int
    activity_id: int

class TimeEntryCreate(TimeEntryBase):
    start_time: datetime

class TimeEntryRead(TimeEntryBase):
    id: int
    status: TimeEntryStatus
    finish_type: FinishType | None = None
    cancel_reason: str | None = None

    class Config:
        from_attributes = True
