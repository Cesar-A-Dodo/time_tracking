from app.database.base import Base
from app.database.session import engine
from app.models import employee, activity, time_entry, time_entry_block

Base.metadata.create_all(bind=engine)
