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


class ActivityCreate(BaseModel):
    name: str
    client_id: int
    estimated_time_minutes: int | None = None


class ActivityRead(BaseModel):
    id: int
    name: str
    client_id: int
    estimated_time_minutes: int | None = None
    is_active: bool

    class Config:
        from_attributes = True

class ActivityAverageTimeRead(BaseModel):
    activity_id: int
    completed_entries: int
    average_seconds: float
    average_minutes: float

    class Config:
        from_attributes = True


class ClientCreate(BaseModel):
    name: str


class ClientRead(BaseModel):
    id: int
    name: str
    is_active: bool

    class Config:
        from_attributes = True


class ActivitySummaryMetricsRead(BaseModel):
    activity_id: int

    completed_entries: int
    canceled_entries: int

    total_completed_seconds: float
    total_completed_minutes: float

    average_completed_seconds: float
    average_completed_minutes: float

    min_completed_seconds: float
    min_completed_minutes: float

    max_completed_seconds: float
    max_completed_minutes: float

    class Config:
        from_attributes = True
