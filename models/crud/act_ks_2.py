from sqlalchemy.orm import Session
from models import models
from typing import List, Dict


def create(db: Session,
           id_work: str,
           number: str,

           smeta_number: str,
           unit_number: str,
           measure: str,
           work_count: str,
           work_unit: str,
           work_cost: str
           ):
    db_item = models.ActKS2(
        id_work=id_work,
        number=number,
        smeta_number=smeta_number,
        unit_number=unit_number,
        measure=measure,
        work_count=work_count,
        work_unit=work_unit,
        work_cost=work_cost
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def list(db: Session):
    l = []
    query = db.query(models.ActKS2).all()
    for q in query:
        d = q.__dict__
        d.pop('_sa_instance_state', None)
        d.pop('id', None)
        l.append(d)
    return l


def get_by_code_work(db: Session, id_work: str):
    return db.query(models.ActKS2).filter(models.ActKS2.id_work == id_work).first()