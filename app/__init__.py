from app.db.models.account import Account
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.db import session

from .routes.auth import auth
from .routes.twitter import twitter
from app.db import create_all
from app.db.crud import Crud
from app.db.models.user import User


from app.dependencies import OAuth2
from config import General

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    """
        Program ilk defa çlıştırılıyors ve veritbanı henüz hazır değilse bu işlemi yapar.
    """
    try:
        Crud.get(User, 0)
    except Exception as e:
        create_all()
        initUser = User()
        initUser.id = 0
        initUser.mail = 'created'
        Crud.create(initUser)


@app.get('/checkCelerytestttttttt')
def tes1t(userId: int = Depends(OAuth2.get_current_user)):
    return {'yess': userId}


app.include_router(auth, prefix='/auth', tags=['Auth'])
app.include_router(twitter, prefix='/twitter', tags=['Twitter İşlemleri'])
