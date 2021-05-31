from typing import Optional

from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class Account(BaseModel):
    username: str
    password: str


class SCheckCelery(BaseModel):
    taskId: str


class delAcc(BaseModel):
    # yalnızca test için hızlıca account silmek için
    id: int


class delToken(BaseModel):
    # token silmek için request scheması. yalnızca token içeirr
    token: str


class StwitterUrl(BaseModel):
    url: str
