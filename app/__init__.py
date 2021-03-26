<<<<<<< HEAD
from fastapi import FastAPI
from sqlalchemy.orm import session

from .routes.auth import auth
from .routes.twitter import twitter
from app.db.session import SessionLocal
=======
from fastapi import FastAPI, Depends

from .routes.auth import auth
from .routes.twitter import twitter
from app.dependencies import get_db
>>>>>>> 0bcd303da8d7601518af880ceb8cf72aec3c8d25
from app.db import create_all
from app.db.crud import Crud
from app.db.models.user import User

app = FastAPI()

<<<<<<< HEAD
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
=======
app.on_event("startup")
async def startup(db: Depends(get_db)):
    """
        Program ilk defa çlıştırılıyors ve veritbanı henüz hazır değilse bu işlemi yapar.
    """
    try:
        Crud.get(db, User, 0)
    except Exception as e:
        initUser = User()
        initUser.id = 0
        Crud.create(db, initUser)
        create_all()
>>>>>>> 0bcd303da8d7601518af880ceb8cf72aec3c8d25


app.include_router(auth, prefix='/auth', tags=['Auth'])
app.include_router(twitter, prefix='/twitter', tags=['Twitter İşlemleri'])
