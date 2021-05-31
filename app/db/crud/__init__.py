from sqlalchemy.orm import Session, session
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import false

from app.db.basemodel import Base
from app.db.session import SessionLocal
from app.db.models import *
from app.schemas.request import Login
from app.services import PasswordHash, Token


class Crud:
    """
        cls.db, model ve işlemin gerektirdiği parametreler ile CRUD işlemleri yapan fonksiyonların bulunduğu class.
    """

    db: session = SessionLocal()

    @classmethod
    def create(cls, obj):
        """
            Veritabanında yeni veri oluşturmak.
            **Parameters**
        * 'cls.db': Generated cls.db SessionLocal nesnesi. Router içinde Depends ile gelen cls.db gönderilir.
        * 'obj': Eklenecek SQLAlchemy Model instance

            **Returns**
        * instance olarak döndürür.
        """
        cls.db.add(obj)
        cls.db.commit()
        cls.db.refresh(obj)
        return obj

    @classmethod
    def get(cls,  model: Base, id, mapped: bool = True):
        """
            Veritabanınından tekli veri okumak.
            **Parameters**
        * 'cls.db': Generated cls.db SessionLocal nesnesi. Router içinde Depends ile gelen cls.db gönderilir.
        * 'model': İşlem yapılacak SQLAlchemy Model classı
        * 'id': İstenen verinin Primary Keyi
        * 'mapped': Verinin instance halinde mapped işlemi yapılıp gerektiğinde liste olarak dönmesi için. Default True.

            **Returns**
        * 'mapped' parametresine göre Query objesi olarak veya instance olarak döndürür.
        """
        return cls.db.query(model).filter(model.id == id).first() if mapped else cls.db.query(model).filter(model.id == id)

    @classmethod
    def get_multi(cls,  model: Base, skip: int = 0, limit: int = 0, mapped: bool = True):
        """
            Veritabanında çoklu veri okumak.
            **Parameters**
        * 'cls.db': Generated cls.db SessionLocal nesnesi. Router içinde Depends ile gelen cls.db gönderilir.
        * 'model': İşlem yapılacak SQLAlchemy Model classı
        * 'skip': İstenilen verinin soldan kesinti noktası. Default değer 0'dır.
        * 'limit': İstenilen verinin sağdan kesinti noktası Default değer 0'dır.
        * 'mapped': Verinin instance halinde mapped işlemi yapılıp gerektiğinde liste olarak dönmesi için. Default True.

        * 'skip' ve 'limit' değerleri girilmezse tablodaki tüm değerleri döndürür. 'mapped' parametresi bu durumu etkilemez.

            **Returns**
        * 'mapped' parametresine göre Query objesi olarak veya instance olarak döndürür.
        """

        return cls.db.query(model).offset(skip).limit(limit).all() if skip + limit != 0 else cls.db.query(model).all() if mapped else cls.db.query(model).offset(skip).limit(limit) if skip + limit != 0 else cls.db.query(model)

    @classmethod
    def get_filtered(cls,  model: Base, key, value, mapped: bool = True):
        """
            Veritabanında çoklu veri okumak.
            **Parameters**
        * 'cls.db': Generated cls.db SessionLocal nesnesi. Router içinde Depends ile gelen cls.db gönderilir.
        * 'model': İşlem yapılacak SQLAlchemy Model classı
        * 'key': Filtrelenecek alan ismi
        * 'limit': Filtrelenecek değer
        * 'mapped': Verinin instance halinde mapped işlemi yapılıp gerektiğinde liste olarak dönmesi için. Default True.

        * 'skip' ve 'limit' değerleri girilmezse tablodaki tüm değerleri döndürür. 'mapped' parametresi bu durumu etkilemez.

            **Returns**
        * 'mapped' parametresine göre Query objesi olarak veya instance olarak döndürür.
        * sonuç boş ise None döner.
        """

        res = cls.db.query(model).filter(getattr(model, key) == value).all(
        ) if mapped else cls.db.query(model).filter(getattr(model, key) == value)
        if len(res) == 1:
            return res[0]
        return res if res != [] else None

    @classmethod
    def delete(cls,  model: Base, id: int):
        """
            Veritabanında veri silmek için.
            **Parameters**
        * 'cls.db': Generated cls.db SessionLocal nesnesi. Router içinde Depends ile gelen cls.db gönderilir.
        * 'model': İşlem yapılacak SQLAlchemy Model classı
        * 'id': İstenen verinin Primary Keyi

            **Returns**
        * Silinen verinin 'id' alanı döndürülür.
        """

        obj = cls.db.query(model).get(id)
        if obj == None:
            return None
        cls.db.delete(obj)
        cls.db.commit()
        return obj.id

    @classmethod
    def update(cls, model: Base, id: int, key: str = None, value: str = None, values: dict = None, mapped: bool = True):
        """
            Veritabanında veri güncelemek.
            **Parameters**
        * 'cls.db': Generated cls.db SessionLocal nesnesi. Router içinde Depends ile gelen cls.db gönderilir.
        * 'model': İşlem yapılacak SQLAlchemy Model classı
        * 'id': Güncellenecek verinin Primary Keyi
        * 'key': Güncellenmek istenen alan ismi
        * 'value': Yeni değer

            **Returns**
        * 'mapped' parametresine göre Query objesi olarak veya instance olarak döndürülür.
        """
        obj = cls.db.query(model).get(id)
        if values == None:
            setattr(obj, key, value)
        else:
            for key in values.keys():
                setattr(obj, key, values[key])
        cls.db.commit()
        return cls.db.query(model).filter(model.id == obj.id).first() if mapped else cls.db.query(model).filter(model.id == obj.id)


class MultiTable:
    @classmethod
    def login(cls, obj: Login):
        """(Session, Login ) -> str
        """
        user: User = Crud.get_filtered(
            User, 'mail', obj.username)
        if user == None:
            # raise RowNotFound
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Kullanıcı bulunamadı.")
        # elif not PasswordHash.check_password(user.pw_hash, obj.passwd): test amaçlı ele kullanıcı ekleynce hash ile uğraşmak istemedim. ayarlarız bunu
        elif not user.pw_hash == obj.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Şifre Eşleşmiyor.")
        else:
            token = Token.create_token()
            Crud.create(obj=Auth(
                userId=user.id, tokenCreate=datetime.now()))
            return token, user.id
