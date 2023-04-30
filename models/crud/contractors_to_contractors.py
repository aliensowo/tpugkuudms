from sqlalchemy.orm import Session
from models import models


def get_list(db: Session):
    return db.query(models.ContractorsToContractors).all()


def get_limit_offset(db: Session, limit: int = 5, offset: int = 0):
    return db.query(models.ContractorsToContractors).limit(limit).offset(offset)

def get_by_criteria_id(db: Session, id_crit: bool):
    return db.query(models.ContractorsToContractors).filter(
        models.ContractorsToContractors.id_criteria == id_crit
    ).all()


def get_by_ids(db: Session, c1: int, c2: int, id_crit: int, compare_id: int):
    return db.query(models.ContractorsToContractors).filter(
        models.ContractorsToContractors.id_contractor_one == c1,
        models.ContractorsToContractors.id_contractor_two == c2,
        models.ContractorsToContractors.id_criteria == id_crit,
        models.ContractorsToContractors.id_compare == compare_id
    ).first()


def edit(db: Session, c1: int, c2: int, id_crit: int, value: str, compare_id: int):
    db_item = db.query(models.ContractorsToContractors).filter(
        models.ContractorsToContractors.id_contractor_one == c1,
        models.ContractorsToContractors.id_contractor_two == c2,
        models.ContractorsToContractors.id_criteria == id_crit,
        models.ContractorsToContractors.id_compare == compare_id
    ).first()
    db_item.value = value
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create(
        db: Session,
        id_contractor_one: str,
        id_contractor_two: str,
        value: str,
        id_criteria: int,
        id_compare: int,
):
    db_item = models.ContractorsToContractors(
        id_contractor_one=id_contractor_one, id_contractor_two=id_contractor_two, value=value,
        id_criteria=id_criteria, id_compare=id_compare
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete(db: Session):
    db.query(models.ContractorsToContractors).delete()
    db.commit()
