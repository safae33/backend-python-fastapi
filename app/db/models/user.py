"""
UserBasic, UserDetails
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, SmallInteger
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app.db.basemodel import Base


class User(Base):
    """ Temel user class. id mail pw ve type içerir. kalan bilgiler gerektiğinde userdetailsden çekilir """
    id = Column(Integer, primary_key=True)
    mail = Column(String(50), unique=True)
    pw_hash = Column(String(128))
    type_ = Column(SmallInteger, )
    first_name = Column(String(50))
    last_name = Column(String(50))
    isActive = Column(Boolean)
    isDeleted = Column(Boolean)

    # details = relationship('UserDetails', cascade="all,delete",
    #                        backref='userbasic', uselist=False)  # one-to-many den farklı
    # # olarak yalnızca uselist=False ekleniyor relationship e o kadar. çohyi.
