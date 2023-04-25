from sqlalchemy.orm import Session
from models import models, schemas


def get_user(db: Session, username: str, password: str):
    return db.query(models.CustomUsers).filter(
        models.CustomUsers.username == username,
        models.CustomUsers.password == password
    ).first()


def create_user(db: Session, username: str, password: str):
    db_item = models.CustomUsers(username=username, password=password)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
