from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from typing import List
from pydantic import parse_obj_as


from config import General
from app.schemas.request.accountworker import AccountWorker, Work
from app.services import AccountFuncs


class Twitter():
    """
    Twitter işlemleri için class. Constructor içinde accountId alarak initialize eder.
    """

    def __init__(self, accountId, isInit=False):
        self.accountId = str(accountId)
        self.isInit = isInit

        # initialize işlemi değilse kayıtlı kişinin browser dosyalarını unziple.
        if not self.isInit:
            AccountFuncs.unzip_account(self.accountId)

        # browser Options ayarlanıyor. debian sistemde sorunsuz çalışması için yeterli ayarlar.
        self.options = Options()
        self.options.headless = True
        self.options.add_argument(
            "--disable-extensions")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument(
            'user-data-dir=' + General.ACCOUNTS_PATH + '/' + self.accountId)

        # işlemlerde kullanılacak değerlerin belirlenmesi.
        self.browser: webdriver.Chrome = None
        self.elem = None

    def run_works(self, works_dict, delayBetweenTweets=4):
        """
        account için works tanımı uygular. bu bir kullanıcı için bir tweeti like ve retweet emri içerir. mention daha sonra*
        * ilk satırda raw dict halinden tekrar pydantic modeline dönüşür. bunun sebebi celery'nin dict veya json olarak serialize etme gerekliliği.
        * 
        """
        works: List[Work] = parse_obj_as(List[Work], works_dict)
        self.browser = webdriver.Chrome(chrome_options=self.options)
        for work in works:
            if work.definition.like:
                self.like_tweet_by_url(work.tweetUrl)
                if work.definition.retweet:
                    sleep(1)
                    self.retweet_tweet_by_url(work.tweetUrl)
            if work.definition.retweet:
                self.retweet_tweet_by_url(work.tweetUrl)
            sleep(delayBetweenTweets)

    def retweet_tweet_by_url(self, tweetUrl):
        """
        url verilen tweeti retweet eder.
        """
        self.browser.get("https://twitter.com/"+tweetUrl)
        try:
            WebDriverWait(self.browser, 5, poll_frequency=0.2).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Retweet"]')))
        except Exception:
            print(
                "BUNLAR DAHA DÜZGÜN LOG İŞLEMİYLE AYARLANACAK. AMA SONRA. AHATA OLDU BU ARADA")
        finally:
            self.elem = self.browser.find_element_by_xpath(
                '//div[@aria-label="Retweet"]')
            self.elem.click()
            sleep(0.2)
            self.elem = self.browser.find_element_by_xpath(
                '//div[@data-testid="retweetConfirm"]')
            self.elem.click()

    def like_tweet_by_url(self, tweetUrl):
        """
        url verilen tweete like atar.
        """
        self.browser.get("https://twitter.com/"+tweetUrl)
        try:
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Like"]')))
        except Exception:
            print(
                "BUNLAR DAHA DÜZGÜN LOG İŞLEMİYLE AYARLANACAK. AMA SONRA. AHATA OLDU BU ARADA")
        finally:
            self.elem = self.browser.find_element_by_xpath(
                '//div[@aria-label="Like"]')
            self.elem.click()

    def login(self, username, password):
        """
        login işlemi. Yalnızca bu işlemde isInit=True ile construct edilir.
        """
        self.browser = webdriver.Chrome(chrome_options=self.options)
        self.browser.get("https://twitter.com/login")
        try:
            myElem = WebDriverWait(self.browser, 2, poll_frequency=0.1).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="session[username_or_email]"]')))
        except TimeoutException:
            print(
                "BUNLAR DAHA DÜZGÜN LOG İŞLEMİYLE AYARLANACAK. AMA SONRA. AHATA OLDU BU ARADA")
        finally:
            self.elem = self.browser.find_element_by_xpath(
                '//input[@name="session[username_or_email]"]')
            self.elem.send_keys(username)
            self.elem = self.browser.find_element_by_xpath(
                '//input[@name="session[password]"]')
            self.elem.send_keys(password)

            self.elem.send_keys(Keys.ENTER)
            try:
                myElem = WebDriverWait(self.browser, 2, poll_frequency=0.1).until(
                    EC.presence_of_element_located((By.ID, 'react-root')))

            except TimeoutException:
                print(
                    "BUNLAR DAHA DÜZGÜN LOG İŞLEMİYLE AYARLANACAK. AMA SONRA. AHATA OLDU BU ARADA")

    def test(self):
        print("works tümü --> ", self.works)
        i: Work
        for i in self.works:
            print("####################")
            print("tweet url --> "+i.tweetUrl)
            print("tweet like olsun mu --> "+str(i.definition.like))
            print("tweet rt olsun mu --> "+str(i.definition.retweet))
            print("####################")

    def close_all(self):
        """
        Browser ile kullanılan tüm kaynaklar release edilir.
        * isInit parametresi True gelirse zip işlemi de yapar. Yalnızca ilk login işleminden sonra kapatılırken bu True olur.
        """
        self.browser.close()
        self.browser.quit()
        if self.isInit:
            AccountFuncs.zip_account(self.accountId)
        else:
            AccountFuncs.clearData(self.accountId)
