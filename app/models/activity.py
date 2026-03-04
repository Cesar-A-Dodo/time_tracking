from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey
from typing import List, TYPE_CHECKING
from app.database.base import Base

if TYPE_CHECKING:
    from app.models.time_entry import TimeEntry
    from app.models.client import Client


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"),
        nullable=False
    )

    estimated_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    client: Mapped["Client"] = relationship(back_populates="activities")

    time_entries: Mapped[List["TimeEntry"]] = relationship(
        back_populates="activity"
    )
