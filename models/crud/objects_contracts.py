import time

from sqlalchemy.orm import Session
from models import models
from typing import List, Dict


def create(db: Session, id_object: str,
           object_name: str,
           date_start: str,
           date_end: str):
    db_item = models.ObjectsContracts(id_object=id_object,
                                      object_name=object_name,
                                      date_start=date_start,
                                      date_end=date_end)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get(db: Session, id_o: str):
    return db.query(models.ObjectsContracts).filter(models.ObjectsContracts.id_object == id_o).first()

def list(db: Session):
    l = []
    query = db.query(models.ObjectsContracts).all()
    for q in query:
        d = q.__dict__
        d.pop('_sa_instance_state', None)
        l.append(d)
    return l

def list_current_y(db: Session):
    l = []
    query = db.query(models.ObjectsContracts).all()
    for q in query:
        d = q.__dict__
        d.pop('_sa_instance_state', None)
        if d["date_end"].split(".")[-1] == f"{time.gmtime().tm_year}":
            l.append(d)
    return l