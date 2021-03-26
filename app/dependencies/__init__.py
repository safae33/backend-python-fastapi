import redis
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Optional

from app.db.session import SessionLocal
from config import Redis as RedisConf


def get_db():
    """
    get_db func. db kullanacak fonksiyonlar için Depends yazmak amacıyla. her routes içinde import ediliyor.
    generator kullanılıyor.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Redis:
    def __init__(self):
        self.redis = redis.Redis(host=RedisConf.URL, port=6379, db=0)

    def get(self, key):
        try:
            return int(self.redis.get(name=key).decode("utf-8"))
        except AttributeError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Girişiniz zaman aşımına uğradı. Lütfen tekrar giriş yapınız.")

    def set(self, key: str, value: str, ex: int = None):
        """
        * (key:str, value:str, ex:int) -> str

        * ex: saniye bazında expire süresi. Default None
        """
        return self.redis.set(key, value, ex=ex)


class OAuth2:

    oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

    @classmethod
    def get_current_user(cls, token: str = Depends(oauth2_schema), cache: Redis = Depends(Redis)):
        return cache.get(token)
