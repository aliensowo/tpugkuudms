from sqlalchemy.orm import Session
from models import models


def get_list(db: Session):
    return db.query(models.Contractors).all()


def get_by_id(db: Session, contractor_id: int):
    return db.query(models.Contractors).filter(models.Contractors.id_contractor == contractor_id).first()


def get_by_name(db: Session, name: str):
    return db.query(models.Contractors).filter(models.Contractors.contractor_name == name).first()


def get_limit_offset(db: Session, limit: int = 5, offset: int = 0):
    return db.query(models.Contractors).limit(limit).offset(offset)


def edit(db: Session, contractor_id: int, **kwargs):
    db_item = db.query(models.Contractors).filter(
        models.Contractors.id_contractor == contractor_id
    ).first()
    for k, v in kwargs.items():
        setattr(db_item, k, v)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create(
        db: Session,
        contractor_name: str, work_cost: str, availability_of_technology: str,
        tech_equipment: str, availability_of_production_facilities: str,
        qualified_human_resources_personnel: str
):
    db_item = models.Contractors(
        contractor_name=contractor_name, work_cost=work_cost, availability_of_technology=availability_of_technology,
        tech_equipment=tech_equipment, availability_of_production_facilities=availability_of_production_facilities,
        qualified_human_resources_personnel=qualified_human_resources_personnel
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def criteria_delete(db: Session, id_contractor: int):
    db.query(models.Contractors).filter(models.Contractors.id_contractor == id_contractor).delete()
    db.commit()
