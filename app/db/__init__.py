"""
db'nin bir python subpackage olduğunu tanımlıyoruz.
"""

from .session import engine, SessionLocal
from app.db.basemodel import Base


from .models.user import *
# from .models.auth_log import *


def create_all():
    """Yazılmış modellerden bir tablo yapısı create eder. Öncelikle Config içerisinde belirtilmiş bir veritabanı
        oluşturulmuş olmalı.
    """
    Base.metadata.create_all(bind=engine)
