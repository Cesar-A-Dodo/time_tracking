from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import List, TYPE_CHECKING
from app.database.base import Base

if TYPE_CHECKING:
    from app.models.time_entry import TimeEntry

class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    client: Mapped[str] = mapped_column(String(100), nullable=False)
    estimated_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    time_entries: Mapped[List["TimeEntry"]] = relationship(
        back_populates="activity"
    )
