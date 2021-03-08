class Uvicorn:
    """
    Uvicorn için çalışma ayarları içeren class.

    Parameters:
        HOST: Uvicorn'un çalışacağı host adresi.
        PORT: Uvicorn'un çalışacağı port numarası.
        DEBUG: Hataların console içinde gösterilmesi. Development aşamasında aktif olur.
        RELOAD: Kod üzerindeki değişiklerin canlı olarak yenilenmesi. Development aşamasında aktif olur.

    """
    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = True
    RELOAD = True


class SQLAlchemy:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:asd123@localhost:5432/test12'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class General:
    SECRET_KEY = '4xmWKRSz2GfIwEcIaGwx6F8G1yNeKZDNwzfMrk2MbcH8l7xcuqo6ky1pImu8Nwri'
    TOKEN_BYTE_SİZE = 64
    CACHE_TOKEN_EXPIRE_SECONDS = 1200
    CHROME_DRIVER_PATH = "D:\\App\\chromedriver.exe"
    CHROME_COOKIES_ROOT_PATH = "D:\\app\\Cookies"
