from fastapi import FastAPI
from sqlalchemy.orm import session

from .routes.auth import auth
from .routes.twitter import twitter
from app.db.session import SessionLocal
from app.db import create_all
from app.db.crud import Crud
from app.db.models.user import User

app = FastAPI()

@app.on_event("startup")
def startup():
    """
        Program ilk defa çlıştırılıyors ve veritbanı henüz hazır değilse bu işlemi yapar.
    """
    db:session = SessionLocal() 
    try:
        Crud.get(db, User, 0)
        db.close()
    except Exception as e:
        db.close()
        db:session = SessionLocal()
        create_all()
        initUser = User()
        initUser.id = 0
        initUser.mail = 'created'
        Crud.create(db, initUser)


app.include_router(auth, prefix='/auth', tags=['Auth'])
app.include_router(twitter, prefix='/twitter', tags=['Twitter İşlemleri'])
