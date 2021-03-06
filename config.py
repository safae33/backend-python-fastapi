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
    # localhost yerine postgresql yazılıyor çünkü docker network içinde aranacak adres gerekli.
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:asd123@postgresql:5432/test321'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Redis:
    URL = "redis"


class General:
    SECRET_KEY = '4xmWKRSz2GfIwEcIaGwx6F8G1yNeKZDNwzfMrk2MbcH8l7xcuqo6ky1pImu8Nwri'
    TOKEN_BYTE_SİZE = 64
    CACHE_TOKEN_EXPIRE_SECONDS = 12000
    CHROME_DRIVER_PATH = ""
    LIKE_PROCESS_ID = 0
    RETWEET_PROCESS_ID = 1
    ORIGINS = [
        "https://localhost",
        "http://localhost",
        # "http://localhost:61621/",
        # "http://localhost:8080",
    ]


class Celery:
    # docker içindeki redis service ismi yazılıyor localhost yerine.
    BROKER_CONNECTION_URL = "redis://redis/1"
    CELERY_RESULT_BACKEND = "redis://redis:6379/2"


class Selenium:
    ACCOUNTS_PATH = "/var/accounts"

    TARGET_ARTICLE_CLASSES = "css-1dbjc4n r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh"
    TARGET_SPAN_CLASSES = "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"

    ACCOUNT_PROFILE_CLASSES = "css-1dbjc4n r-1ifxtd0 r-ymttw5 r-ttdzmv"
