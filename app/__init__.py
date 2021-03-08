from fastapi import FastAPI

from .routes.auth import auth
from .routes.twitter import twitter

app = FastAPI()

app.include_router(auth, prefix='/auth', tags=['Auth'])
app.include_router(twitter, prefix='/twitter', tags=['Twitter İşlemleri'])
