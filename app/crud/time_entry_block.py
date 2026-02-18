from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.time_entry_block import TimeEntryBlock


def create_block(db: Session, time_entry_id: int) -> TimeEntryBlock:
    block = TimeEntryBlock(time_entry_id = time_entry_id, start_time = datetime.now(timezone.utc))
    db.add(block)
    db.flush()
    return block

def get_open_block(db: Session, time_entry_id: int) -> TimeEntryBlock | None:
    return (
        db.query(TimeEntryBlock)
        .filter(
            TimeEntryBlock.time_entry_id == time_entry_id,
            TimeEntryBlock.end_time.is_(None)
        )
        .first()
    )

def close_block(db: Session, block: TimeEntryBlock) -> TimeEntryBlock:
    block.end_time = datetime.now(timezone.utc)
    db.flush()
    return block
