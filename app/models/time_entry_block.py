from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime, timezone
from app.database.base import Base

class TimeEntryBlock(Base):
    __tablename__ = "time_entry_blocks"

    id: Mapped[int] = mapped_column(primary_key=True)

    time_entry_id: Mapped[int] = mapped_column(ForeignKey("time_entries.id"), nullable=False)

    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    time_entry = relationship("TimeEntry", back_populates="blocks")
