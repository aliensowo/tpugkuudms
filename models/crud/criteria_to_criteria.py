from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import models


def get_list(db: Session):
    return db.query(models.CriteriaToCriteria).all()


def get_limit_offset(db: Session, limit: int = 5, offset: int = 0):
    return db.query(models.CriteriaToCriteria).limit(limit).offset(offset)


def get_by_ids(db: Session, c1: int, c2: int, id_compare: int):
    return db.query(models.CriteriaToCriteria).filter(
        models.CriteriaToCriteria.id_criteria_one == c1,
        models.CriteriaToCriteria.id_criteria_two == c2,
        models.CriteriaToCriteria.id_compare == id_compare,
    ).first()


def get_by_one_of_id(db: Session, c1: int, c2: int,  id_compare: int):
    return db.query(models.CriteriaToCriteria).filter(
        or_(
            models.CriteriaToCriteria.id_criteria_one == c1,
            models.CriteriaToCriteria.id_criteria_two == c1,
        ),
        or_(
            models.CriteriaToCriteria.id_criteria_one == c2,
            models.CriteriaToCriteria.id_criteria_two == c2,
        ),
        models.CriteriaToCriteria.id_compare == id_compare,
    ).first()


def edit(db: Session, c1: int, c2: int, value: str, id_compare: int):
    db_item = db.query(models.CriteriaToCriteria).filter(
        models.CriteriaToCriteria.id_criteria_one == c1,
        models.CriteriaToCriteria.id_criteria_two == c2,
        models.CriteriaToCriteria.id_compare == id_compare
    ).first()
    db_item.value = value
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create(
        db: Session,
        id_criteria_one: str,
        id_criteria_two: str,
        value: str,
        id_compare: int,
):
    db_item = models.CriteriaToCriteria(
        id_criteria_one=id_criteria_one, id_criteria_two=id_criteria_two, value=value,
        id_compare=id_compare
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete(db: Session):
    db.query(models.CriteriaToCriteria).delete()
    db.commit()
