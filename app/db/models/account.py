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
    # şimdilik buna yazıcam usernameleri. yeniden uğraşmak sitemedim
    proxy = Column(String(128))
    # username = Column(String(128))
    isInit = Column(Boolean)
    userId = Column(Integer, ForeignKey('user.id'))
