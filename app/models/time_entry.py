from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.schemas import TimeEntryStatus, FinishType

class TimeEntry(Base):
    __tablename__ = "time_entries"

    id: Mapped[int] = mapped_column(primary_key=True)

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=False
    )

    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activities.id"),
        nullable=False
    )

    status: Mapped[TimeEntryStatus] = mapped_column(
        Enum(TimeEntryStatus),
        default=TimeEntryStatus.CRIADO,
        nullable=False,
    )

    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    finish_type: Mapped[FinishType | None] = mapped_column(
        Enum(FinishType),
        nullable=True,
    )

    employee: Mapped["Employee"] = relationship(
        back_populates="time_entries"
    )

    activity: Mapped["Activity"] = relationship(
        back_populates="time_entries"
    )
