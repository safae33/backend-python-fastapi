from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import session, Query
from werkzeug.security import generate_password_hash

from app.dependencies import get_db, OAuth2
from app.db.crud import Crud, MultiTable
from app.schemas.request import Account as AccountSc
from app.schemas.request.accountworker import AccountWorker
from app.db.models import Account
from app.services.selenium import Twitter
from app.celery.twitter import twitter_login, set_workers_for_account


# twitter = APIRouter(dependencies=[Depends(OAuth2.oauth2_schema)])
twitter = APIRouter()


@twitter.get('/getaccounts')
def getacc(db: session = Depends(get_db)):
    return Crud.get_multi(db, Account)


@twitter.post('/newAccount')
def newAccount(request: AccountSc, db: session = Depends(get_db), userId: int = Depends(OAuth2.get_current_user)):
    new = Account()
    new.userId = userId
    return Crud.create(db, new)


@twitter.post('/startWorker')
def startWorker(request: AccountWorker, db: session = Depends(get_db), userId: int = Depends(OAuth2.get_current_user)):
    request.userId = userId
    return set_workers_for_account.apply_async(args=[request.dict()], countdown=10).task_id


@twitter.post('/testLikeTweet')
def newAccount(userId: int = Depends(OAuth2.get_current_user)):
    # çalışıyo.
    return like_tweet.delay("https://twitter.com/amangorunmeyelm/status/1352393446644977666", userId).task_id


@twitter.post('/testLogin')
def newAccount(userId: int = Depends(OAuth2.get_current_user)):
    # çalışıyo. baya iyi gitti her şey bu gece.
    return twitter_login.delay("trtperko@gmail.com", "ekensafa05", userId, 1).task_id


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
