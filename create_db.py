from app.db import create_all
from sqlalchemy.exc import OperationalError
if __name__ == "__main__":
    try:
        create_all()
    except OperationalError as e:
        print("HATA: Tablo yapılarının oluşturulması için öncelikle config içerisinde belirtilen veritabanı isminde bir"
              "veritabanı oluşturmanız gerekmektedir.")
    else:
        print("Veritabanı başarıyla oluşturuldu.")
