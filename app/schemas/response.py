from pydantic import BaseModel
from typing import List


class UserDetails(BaseModel):

    title: str
    user_id: int

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    mail: str
    id: int
    details: UserDetails

    class Config:
        orm_mode = True
