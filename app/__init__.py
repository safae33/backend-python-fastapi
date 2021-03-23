from fastapi import FastAPI, Depends

from .routes.auth import auth
from .routes.twitter import twitter
from app.dependencies import get_db
from app.db import create_all
from app.db.crud import Crud
from app.db.models.user import User

app = FastAPI()

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


app.include_router(auth, prefix='/auth', tags=['Auth'])
app.include_router(twitter, prefix='/twitter', tags=['Twitter İşlemleri'])
