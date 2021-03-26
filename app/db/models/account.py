"""
Account
"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean

from app.db.basemodel import Base


class Account(Base):
    id = Column(Integer, primary_key=True)
    proxy = Column(String(128))
    isInit = Column(Boolean)
    userId = Column(Integer, ForeignKey('user.id'))
