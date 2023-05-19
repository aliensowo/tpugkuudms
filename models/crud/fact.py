from sqlalchemy.orm import Session
from models import models
from typing import List, Dict


def create(db: Session, id_work:str, work_name:str, volume: str,
           work_start: str,
           work_end: str,
           work_complete: str):
    db_item = models.Fact(id_work=id_work, work_name=work_name, volume=volume,
                          work_start=work_start,
                          work_end=work_end,
                          work_complete=work_complete)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def list(db: Session):
    l = []
    query = db.query(models.Fact).all()
    for q in query:
        d = q.__dict__
        d.pop('_sa_instance_state', None)
        d.pop('id', None)
        l.append(d)
    return l


def get_by_wid(db: Session, id_work: str):
    return db.query(models.Fact).filter(models.Fact.id_work == id_work)
