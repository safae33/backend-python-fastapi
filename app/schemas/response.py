from pydantic import BaseModel
from typing import List


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    mail: str
    id: int

    class Config:
        orm_mode = True
