"""
Auth
"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship

from app.db.basemodel import Base


class Auth(Base):
    """
        Auth tablosu için SQLAlchemy class.
        **Parameters**
    * 'userId': Oluşturuan log kaydının ait olduğu user'a ait id değeri. Foreign Key.
    * 'token': Oluşturulan token.
    * 'tokenCreate': Token oluşturulduğu tarih.
    """
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.id'))
    token = Column(String(length=200))
    tokenCreate = Column(DateTime)
