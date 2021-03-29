from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import session, Query
from werkzeug.security import generate_password_hash

from app.dependencies import get_db, OAuth2
from app.db.crud import Crud, MultiTable
from app.schemas.request import Account as AccountSc, delAcc
from app.schemas.request.accountworker import AccountWorker
from app.db.models import Account, Auth
from app.services.selenium import Twitter
from app.celery.twitter import twitter_login, set_workers_for_account, test


# twitter = APIRouter(dependencies=[Depends(OAuth2.oauth2_schema)])
twitter = APIRouter()


@twitter.get('/getaccounts', tags="t")
def getacc(db: session = Depends(get_db)):
    return Crud.get_multi(db, Account)


@twitter.delete('/delAccount', tags="t")
def getacc(d: delAcc, db: session = Depends(get_db)):
    return Crud.delete(db, Account, d.id)


@twitter.delete('/dene', tags="t")
def getacc(request: AccountWorker):
    return test.delay(request.dict()).task_id


@twitter.get('/getlogs', tags="t")
def getacc(db: session = Depends(get_db)):
    return Crud.get_multi(db, Auth)


@twitter.post('/newAccount')
def newAccount(request: AccountSc, db: session = Depends(get_db), userId: int = Depends(OAuth2.get_current_user)):
    new = Account()
    new.userId = userId
    new = Crud.create(db, new)
    return twitter_login.delay(request.username, request.password, new.id).task_id


@twitter.post('/startWorker')
def startWorker(request: AccountWorker, db: session = Depends(get_db), userId: int = Depends(OAuth2.get_current_user)):
    return set_workers_for_account.apply_async(args=[request.dict()], countdown=1).task_id


# @twitter.post('/testLogin')
# def newAccount(userId: int = Depends(OAuth2.get_current_user)):
#     # çalışıyo. baya iyi gitti her şey bu gece.
#     return twitter_login.delay("trtperko@gmail.com", "ekensafa05", userId, 1).task_id
