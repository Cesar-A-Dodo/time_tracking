from datetime import timedelta
from sqlalchemy import ForeignKey, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.schemas import TimeEntryStatus, FinishType
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.models.employee import Employee
    from app.models.activity import Activity
    from app.models.time_entry_block import TimeEntryBlock


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
        default=TimeEntryStatus.INICIADO,
        nullable=False,
    )

    finish_type: Mapped[FinishType | None] = mapped_column(
        Enum(FinishType),
        nullable=True,
    )

    cancel_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    employee: Mapped["Employee"] = relationship(
        back_populates="time_entries"
    )

    activity: Mapped["Activity"] = relationship(
        back_populates="time_entries"
    )

    blocks: Mapped[List["TimeEntryBlock"]] = relationship(back_populates="time_entry", cascade="all, delete-orphan")

    def calculate_total_time(self) -> timedelta:
        total = timedelta()

        for block in self.blocks:
            if block.end_time:
                total += block.end_time - block.start_time
        return total
