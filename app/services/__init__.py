# import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_bytes
from base64 import b64encode
from subprocess import Popen

from config import General, Selenium


class Token:
    """
    login olan kişiler için Config içinde belirlenen sayıda bytedan oluşan random bir token oluşturur.
    """
    @classmethod
    def create_token(cls):
        return b64encode(token_bytes(General.TOKEN_BYTE_SİZE)).decode()


class PasswordHash:
    """
    Şifrelerin hashlenmesi ve kontrolü işlemleri
    """

    @classmethod
    def hash_password(cls, passwd: str):
        """
        verilen şifreyi hashleyerek geri döndürür.
        """
        return generate_password_hash(passwd)

    @classmethod
    def check_password(cls, hashed: str, passwd):
        """
        veritabanından gelecek hashlenmiş şifre ile login aşamasında girilen şifreyi kontrol eder. Eşleşiyorsa True döner.
        """
        return check_password_hash(hashed, passwd)


class AccountFuncs:
    """
    Account verilerinin işletim sistemi üzerindeki işlemleri.
    """
    @classmethod
    def clearData(cls, accountId: str):
        """
        işlemi tamamlanan, accountId'si verilen kullanıcıya ait verileri kaldırmak için bir subprocess çalıştırır.
        """
        Popen(f'rm -rf {Selenium.ACCOUNTS_PATH}/{accountId}', shell=True)

    @classmethod
    def zip_account(cls, accountId: str):
        """
        initialize işleminde kullanılır. oluşturulan dosyalar önce ziplenir sonra silinir.
        """
        Popen(f'zip -q -r {Selenium.ACCOUNTS_PATH}/{accountId}.zip {Selenium.ACCOUNTS_PATH}/{accountId}; rm -rf {Selenium.ACCOUNTS_PATH}/{accountId}', shell=True)

    @classmethod
    def unzip_account(cls, accountId: str):
        """
        kullanıcı ile işlem yapılabilmesi için dosyalar unzip ile çıkartılır.
        """
        f = Popen(
            f'unzip -q {Selenium.ACCOUNTS_PATH}/{accountId}.zip -d /', shell=True)
