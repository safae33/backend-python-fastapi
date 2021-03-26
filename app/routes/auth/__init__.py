from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import session 

from app.dependencies import get_db, OAuth2, Redis
from app.schemas.request import *
from app.schemas.response import *
from app.db.crud import Crud, MultiTable
from app.db.models.user import User
from app.services import Token
from app.celery import twitter, check
from config import General


auth = APIRouter()


@auth.post('/login')
async def token(db: session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends(), cache: Redis = Depends()):
    t, id = MultiTable.login(db, obj=form_data)
    cache.set(t, id, ex=General.CACHE_TOKEN_EXPIRE_SECONDS)
    return {'access_token': t}

@auth.post('/addTestUser')
def add(db: session = Depends(get_db)):
    new = User()
    new.mail = 'safa10'
    new.pw_hash = 'asd'
    new1 = User()
    new1.mail = 'safa11'
    new1.pw_hash = 'asd'
    Crud.create(db, new)
    Crud.create(db, new1)
    print('Test kullanıcıları safa10 ve safa11 oluşturuldu.')
    return('Test kullanıcıları safa10 ve safa11 oluşturuldu.')

@auth.get('/test')
def test(db: session = Depends(get_db), cache: Redis = Depends()):
    return Crud.get_multi(db, User)


@auth.delete('/del')
def test(db: session = Depends(get_db)):
    user = Crud.delete(db=db, model=User, id=2)
    user = Crud.delete(db=db, model=User, id=1)
    return user


@auth.put('/put')
def test(db: session = Depends(get_db)):
    user = Crud.update(db=db, model=UserBasic,
                       id=request.id, key="type_", value=6)
    return user


# UserBasic(mail="as1ada@asd.com", pw_hash="1231221",
#           type_=2, first_name="asdsa", last_name="qweqw")

@auth.get('/celerytest')
def test(userId: int = Depends(OAuth2.get_current_user)):
    key = twitter.testCelery.delay()
    return key.id


@auth.post('/celerycheck')
def test(req: CheckCelery, userId: int = Depends(OAuth2.get_current_user)):
    return check(req.id)
