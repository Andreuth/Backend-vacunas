from sqlalchemy.orm import Session
from app.models.parent_child import ParentChild

def is_child_of_parent(db: Session, parent_id: int, child_id: int) -> bool:
    return db.query(ParentChild).filter(
        ParentChild.parent_id == parent_id,
        ParentChild.child_id == child_id,
        ParentChild.activo == True
    ).first() is not None
