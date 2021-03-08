# import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_bytes
from base64 import b64encode

from config import General


class Token:

    # @classmethod
    # def createToken(cls, payload: dict = {"": ""}):
    #     return jwt.encode(payload=payload, key=General.SECRET_KEY, algorithm='HS512')

    # @classmethod
    # def decodeToken(cls, token: str):
    #     return jwt.decode(jwt=token, key=General.SECRET_KEY, algorithms='HS256')

    @classmethod
    def create_token(cls):
        return b64encode(token_bytes(General.TOKEN_BYTE_SİZE)).decode()


class PasswordHash:

    @classmethod
    def hash_password(cls, passwd: str):
        return generate_password_hash(passwd)

    @classmethod
    def check_password(cls, hashed: str, passwd):
        return check_password_hash(hashed, passwd)
