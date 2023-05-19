from sqlalchemy.orm import Session
from models import models
from typing import List, Dict


def create(db: Session,
           id_work: str,
           number: str,
           smeta_number: str,
           unit_number: str,
           measure: str,
           cost_for_unit: str,
           work_count_smeta: str,
           smeta_cost: str,
           month: str,
           count: str,
           cost: str,
           cost_fact: str
           ):
    db_item = models.ActKS6a(
        id_work=id_work,
        number=number,
        smeta_number=smeta_number,
        unit_number=unit_number,
        measure=measure,
        cost_for_unit=cost_for_unit,
        work_count_smeta=work_count_smeta,
        smeta_cost=smeta_cost,
        month=month,
        count=count,
        cost=cost,
        cost_fact=cost_fact
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def list(db: Session):
    l = []
    query = db.query(models.ActKS6a).all()
    for q in query:
        d = q.__dict__
        d.pop('_sa_instance_state', None)
        d.pop('id', None)
        l.append(d)
    return l

def get_by_code_work(db: Session, id_work: str):
    l = []
    query = db.query(models.ActKS2).filter(models.ActKS2.id_work == id_work)
    for q in query:
        d = q.__dict__
        d.pop('_sa_instance_state', None)
        d.pop('id', None)
        l.append(d)
    return l