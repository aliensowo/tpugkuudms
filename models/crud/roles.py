from sqlalchemy.orm import Session
from models import models


def all(db: Session):
    l = []
    query = db.query(models.Roles).all()
    for q in query:
        d = q.__dict__
        d.pop('_sa_instance_state', None)
        l.append(d)
    return l
