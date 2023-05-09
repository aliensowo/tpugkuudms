from sqlalchemy.orm import Session
from models import models


def get_criteria_list(db: Session):
    return db.query(models.Criteria).all()


def get_by_id(db: Session, criteria_id: int):
    return db.query(models.Criteria).filter(models.Criteria.id_criteria == criteria_id).first()


def get_by_name(db: Session, criteria_name: str):
    return db.query(models.Criteria).filter(models.Criteria.criteria_name == criteria_name).first()


def create_criteria(db: Session, criteria_name: str):
    db_item = models.Criteria(criteria_name=criteria_name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def edit(db: Session, criteria_id: int, criteria_name: str):
    db_item = db.query(models.Criteria).filter(
        models.Criteria.id_criteria == criteria_id
    ).first()
    db_item.criteria_name = criteria_name
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def criteria_delete(db: Session, criteria_id: int):
    db.query(models.Criteria).filter(models.Criteria.id_criteria == criteria_id).delete()
    db.commit()
