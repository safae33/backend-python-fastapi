from pydantic import BaseModel
from typing import Optional


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    mail: str
    id: int

    class Config:
        orm_mode = True


class StweetInfo(BaseModel):
    profilePicUrl: str
    name: str
    username: str
    text: str
    url: str


class SAccountInfo(BaseModel):
    id: int
    name: str
    username: str
    profilePicUrl: str


class SCeleryCheckResponse(BaseModel):
    status: str
    account: Optional[SAccountInfo] = None
