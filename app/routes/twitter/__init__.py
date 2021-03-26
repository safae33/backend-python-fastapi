from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import session, Query
from werkzeug.security import generate_password_hash

from app.dependencies import get_db, OAuth2
from app.db.crud import Crud, MultiTable
from app.schemas.request import Account as AccountSc
from app.db.models import Account
from app.services.selenium import Twitter
from app.celery.twitter import testCelery, twitter_login


# twitter = APIRouter(dependencies=[Depends(OAuth2.oauth2_schema)])
twitter = APIRouter()


@twitter.post('/newAccount')
def newAccount(request: AccountSc, db: session = Depends(get_db), userId: int = Depends(OAuth2.get_current_user)):
    return Crud.create(db, Account(username=request.username, password=generate_password_hash(request.password), userId=userId))


@twitter.post('/testLikeTweet')
def newAccount(bgTask: BackgroundTasks, userId: int = Depends(OAuth2.get_current_user)):
    tw = Twitter(userId)
    tw.like_tweet_by_url(
        "https://twitter.com/trthaber/status/1366897105210597376")
    tw.sl(2)
    bgTask.add_task(tw.close_all)
    return {'userId oldu laaan olduu': userId}


@twitter.post('/testLogin')
def newAccount(userId: int = Depends(OAuth2.get_current_user)):
    return twitter_login.delay("trtperko@gmail.com", "ekensafa05", userId).task_id


@twitter.post('/testIsLogged')
async def newAccount(bgTask: BackgroundTasks, userId: int = Depends(OAuth2.get_current_user)):
    tw = Twitter(userId)
    tw.open_twitter()
    tw.sl(3)
    bgTask.add_task(tw.close_all)
    return None

@twitter.post('/testCelerycikeheh')
async def test():
    testCelery.delay((5))