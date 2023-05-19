from sqlalchemy.orm import Session
from models import models
from typing import List, Dict


def create(db: Session, id_directory: str,
           directory_name: str,
           directory_start: str,
           directory_end: str):
    db_item = models.NeighborhoodDirectory(id_directory=id_directory,
                                      directory_name=directory_name,
                                      directory_start=directory_start,
                                      directory_end=directory_end)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def list(db: Session):
    l = []
    query = db.query(models.NeighborhoodDirectory).all()
    for q in query:
        d = q.__dict__
        d.pop('_sa_instance_state', None)
        l.append(d)
    return l
