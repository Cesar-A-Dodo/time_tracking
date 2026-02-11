from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from typing import List
from app.database.base import Base

class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    time_entries: Mapped[List["TimeEntry"]] = relationship(
        back_populates="employee"
    )
