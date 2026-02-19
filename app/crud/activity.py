from sqlalchemy.orm import Session
from app.models.activity import Activity


def create_activity(db: Session, activity: Activity) -> Activity:
    db.add(activity)
    return activity


def get_activity(db: Session, activity_id: int) -> Activity | None:
    return db.get(Activity, activity_id)


def list_activities(db: Session, *, only_active: bool = False) -> list[Activity]:
    q = db.query(Activity)
    if only_active:
        q = q.filter(Activity.is_active == True)
    return q.order_by(Activity.id.asc()).all()

