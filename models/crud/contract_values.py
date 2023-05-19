from sqlalchemy.orm import Session
from models import models
from typing import List, Dict


def create(db: Session, id_object: str, object_name: str, work_name: str,
           work_value: str):
    db_item = models.ContractValues(id_object=id_object,
                                    object_name=object_name,
                                    work_name=work_name,
                                    work_value=work_value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def list(db: Session):
    l = []
    query = db.query(models.ContractValues).all()
    for q in query:
        d = q.__dict__
        d.pop('_sa_instance_state', None)
        # d.pop('id', None)
        l.append(d)
    return l
