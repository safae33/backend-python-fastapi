from app.db.models.account import Account
from typing import List
from app.db.models.user import User
from config import Celery as CeleryOpt
from celery import Celery


# test için importlar
from time import sleep
from app.db.session import SessionLocal
from sqlalchemy.orm import session
from app.db.crud import Crud
from pydantic import parse_obj_as

app = Celery('app', broker=CeleryOpt.BROKER_CONNECTION_URL,
             backend=CeleryOpt.CELERY_RESULT_BACKEND,
             include=['app.celery.twitter'])


def check(id):
    return app.AsyncResult(id).state


@app.task
def test12():
    db: session = SessionLocal()
    info = {}
    info["name"] = "budur bee"
    info["username"] = "budur bee sadasdqwewq"
    info["profilePicUrl"] = "olduue"
    Crud.update(Account, 6, values=info)

    # print(Crud.get_multi(db, User))
    return "list"
