from sqlalchemy.orm import Session
from models import models


def get(db: Session, name: str):
    return db.query(models.Compare).filter(
        models.Compare.name == name
    ).first()


def create(
        db: Session,
        name: str,
):
    db_item = models.Compare(
        name=name
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete(db: Session):
    db.query(models.Compare).delete()
    db.commit()
