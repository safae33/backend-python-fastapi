"""
Account
"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean

from app.db.basemodel import Base


class Account(Base):
    """
    Account class.
    Kullanıcıların ekledikleri hesapları içerir.
    """
    id = Column(Integer, primary_key=True)
    proxy = Column(String(128))
    isInit = Column(Boolean)
    userId = Column(Integer, ForeignKey('user.id'))
    username = Column(String(50))
    name = Column(String(50))
    profilePicUrl = Column(String(100))
