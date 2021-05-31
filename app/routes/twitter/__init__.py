from app.db.models.user import User
from app.schemas.response import StweetInfo
from fastapi import APIRouter, Depends
from sqlalchemy.orm import session
from werkzeug.security import generate_password_hash

from app.dependencies import get_db, OAuth2
from app.db.crud import Crud
from app.schemas.request import Account as AccountSc, StwitterUrl, delAcc
from app.schemas.request.accountworker import AccountWorker
from app.db.models import Account, Auth
from app.services.selenium import Twitter
from app.celery.twitter import get_tweet_info, twitter_login, set_workers_for_account
from app.schemas.request import SCheckCelery
from app.schemas.response import SCeleryCheckResponse
from app.celery import check


# twitter = APIRouter(dependencies=[Depends(OAuth2.oauth2_schema)])
twitter = APIRouter()


@twitter.post('/checkCelery')
def test(req: SCheckCelery):
    res = {}
    res['status'] = check(req.taskId)
    if res['status'] == 'SUCCESS':
        res['account'] = Crud.get_multi(Account)[-1]
    return res


@twitter.get('/dbTeeeess')
def tes12311t(db: session = Depends(get_db)):
    return Crud.get_multi(User)


@twitter.get('/getaccounts', tags="t")
def getacc(db: session = Depends(get_db)):
    return Crud.get_multi(Account)


@twitter.delete('/delAccount', tags="t")
def getacc(d: delAcc, db: session = Depends(get_db)):
    return Crud.delete(Account, d.id)


@twitter.get('/getlogs', tags="t")
def getacc(db: session = Depends(get_db)):
    return Crud.get_multi(Auth)


@twitter.post('/newAccount')
def newAccount(request: AccountSc, userId: int = Depends(OAuth2.get_current_user)):
    return {'taskId': twitter_login.delay(request.username, request.password, userId).task_id}


@twitter.post('/startWorker')
def startWorker(request: AccountWorker, db: session = Depends(get_db), userId: int = Depends(OAuth2.get_current_user)):
    return set_workers_for_account.apply_async(args=[request.dict()], countdown=1).task_id


@twitter.post('/getTweetInfo', response_model=StweetInfo)
def gettweetinfo(request: StwitterUrl):
    tw = Twitter(0)
    tweet = {}
    tweet = tw.get_tweet_info(request.url)
    tw.close_all()
    del tw
    tweet['url'] = request.url
    return tweet

    # return get_tweet_info.delay(request.url)


@twitter.post('/createDefautCookies')
def startWorker():
    tw = Twitter(0, isInit=True)
    tw.open_url('https://twitter.com/vaziyetcomtr/status/1398203430670376960')
    tw.close_all()
    del tw
    return True


# @twitter.post('/testLogin')
# def newAccount(userId: int = Depends(OAuth2.get_current_user)):
#     # çalışıyo. baya iyi gitti her şey bu gece.
#     return twitter_login.delay("trtperko@gmail.com", "ekensafa05", userId, 1).task_id
