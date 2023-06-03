from sqlalchemy.orm import Session
from models import models


def all(db: Session):
    l = []
    query = db.query(models.CustomUsers).filter(models.CustomUsers.role == "default")
    for q in query:
        d = q.__dict__
        d.pop('_sa_instance_state', None)
        l.append(d)
    return l


def get_user(db: Session, username: str, password: str):
    return db.query(models.CustomUsers).filter(
        models.CustomUsers.username == username,
        models.CustomUsers.password == password
    ).first()


def create_user(db: Session, username: str, password: str):
    db_item = models.CustomUsers(username=username, password=password, role="default")
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def add_role(db: Session, username:str, role_name: str):
    obj = db.query(models.CustomUsers).filter(
        models.CustomUsers.username == username,
    ).first()
    obj.role = role_name
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj