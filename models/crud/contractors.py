from sqlalchemy.orm import Session
from models import models


def get_list(db: Session):
    return db.query(models.Contractors).all()

def get_by_name(db: Session, name: str):
    return db.query(models.Contractors).filter(models.Contractors.contractor_name == name).first()

def get_limit_offset(db: Session, limit: int =5, offset: int =0):
    return db.query(models.Contractors).limit(limit).offset(offset)


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
