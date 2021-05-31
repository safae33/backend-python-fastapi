from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import session


from app.dependencies import get_db, Redis
from app.schemas.request import *
from app.schemas.response import *
from app.db.crud import Crud, MultiTable
from app.db.models.user import User
from app.celery import twitter
from config import General

from time import sleep

auth = APIRouter()


@auth.post('/login')
async def token(db: session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends(), cache: Redis = Depends()):
    t, id = MultiTable.login(obj=form_data)
    cache.set(t, id, ex=General.CACHE_TOKEN_EXPIRE_SECONDS)
    sleep(3)
    return t


@auth.post('/logout')
async def token(req: delToken, cache: Redis = Depends()):
    cache.delete(req.token)
    sleep(3)
    return True


@auth.post('/testuu')
def ehue(req: Account):
    print(req.username, req.password)
    return('ehuee')


@auth.post('/addTestUser')
def add(db: session = Depends(get_db)):
    new = User()
    new.mail = 'safa10'
    new.pw_hash = 'asd'
    new1 = User()
    new1.mail = 'safa11'
    new1.pw_hash = 'asd'
    Crud.create(new)
    Crud.create(new1)
    print('Test kullanıcıları safa10 ve safa11 oluşturuldu.')
    return('Test kullanıcıları safa10 ve safa11 oluşturuldu.')


@auth.get('/test')
def test(db: session = Depends(get_db), cache: Redis = Depends()):
    users: list[User] = Crud.get_multi(User)
    for i in users:
        i.accounts

    return users


@auth.delete('/del')
def test(db: session = Depends(get_db)):
    user = Crud.delete(model=User, id=2)
    user = Crud.delete(model=User, id=1)
    return user


# UserBasic(mail="as1ada@asd.com", pw_hash="1231221",
#           type_=2, first_name="asdsa", last_name="qweqw")

@auth.get('/celerytest')
def test(req):
    key = twitter.testCelery.delay(req)
    return key.id
