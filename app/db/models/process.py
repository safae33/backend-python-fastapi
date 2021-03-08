"""
ProcessType, Process, ProcessGroup
"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean, Uni

from app.db.basemodel import Base


class Type(Base):
    """
    Process tipini belirleyen class. Şuanlık doğal olarak 3 adet ancak dinamikliği sağlamak amaçlı ayrı tutuluyor.
    """
    id = Column(Integer, primary_key=True)
    name = Column(String(length=10), unique=True)


class Target(Base):
    """
    Process Target class.
    Tanımlanan Process'ler içinde hedef twitleri tutar.
    * Her zaman twitter.com/ ibaresinde sonraki kısım tutulur. Ör;
    https://twitter.com/Reuters/status/1367644803899523075 için url alanında Reuters/status/1367644803899523075 tutulur.
    """
    id = Column(Integer, primary_key=True)
    url = Column(String(length=100), unique=True)


class Process(Base):
    id = Column(Integer, primary_key=True)
    accountId = Column(Integer, ForeignKey('account.id'))
    typeId = Column(Integer, ForeignKey('type.id'))
    targetId = Column(Integer, ForeignKey('target.id'))
    organicDelay = Column(Boolean)  # BURDA KALDIN. DAHASI VARDI AMA UNUTTUM
