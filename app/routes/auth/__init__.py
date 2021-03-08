from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import session, Query

from app.dependencies import get_db, OAuth2, Redis
from app.schemas.request import *
from app.schemas.response import *
from app.db.crud import Crud, MultiTable
from app.db.models.user import UserBasic, UserDetails
from app.services import Token
from config import General


auth = APIRouter()


@auth.post('/login')
async def token(db: session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends(), cache: Redis = Depends()):
    t, id = MultiTable.login(db, obj=form_data)
    cache.set(t, id, ex=General.CACHE_TOKEN_EXPIRE_SECONDS)
    return {'access_token': t}


@auth.get('/test')
def test(db: session = Depends(get_db), cache: Redis = Depends(), userId: int = Depends(OAuth2.get_current_user)):
    return Crud.get(db, UserBasic, 10)


@auth.delete('/del')
def test(db: session = Depends(get_db)):
    user = Crud.delete(db=db, model=UserBasic, id=request.id)
    return user


@auth.put('/put')
def test(db: session = Depends(get_db)):
    user = Crud.update(db=db, model=UserBasic,
                       id=request.id, key="type_", value=6)
    return user


@auth.post('/new_details')
def test(db: session = Depends(get_db)):
    user = Crud.create(db=db, obj=UserDetails(
        user_id=3, title="ehueheuheuehueheuheu"))
    return user

# UserBasic(mail="as1ada@asd.com", pw_hash="1231221",
#           type_=2, first_name="asdsa", last_name="qweqw")
