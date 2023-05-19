from sqlalchemy.orm import Session
from models import models
from typing import List, Dict


def create(db: Session, id_work: str,
work_name: str):
    db_item = models.Work(id_work=id_work,
work_name=work_name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def list(db: Session):
    l = []
    query = db.query(models.Work).all()
    for q in query:
        d = q.__dict__
        d.pop('_sa_instance_state', None)
        l.append(d)
    return l


def get(db: Session, id_o: str):
    return db.query(models.Work).filter(models.Work.id_work == id_o).first()