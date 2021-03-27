from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from fastapi import HTTPException, status


from config import General
from app.schemas.request.accountworker import AccountWorker, Work, WorkDefinition


class Twitter():
    """
    Twitter işlemleri için class. Constructor içinde accountWorker nesnesinin json halini alır.
    *   ilk satırda raw json halinden tekrar pydantic modeline dönüşür.
    *   bunun sebebi celery'nin json olarak serialize etme gerekliliği. önce json yapıp tekrar model yapıyoruz. 
    """

    def __init__(self, userId, accountId):

        self.options = Options()
        self.options.headless = True
        self.options.add_argument(
            "--disable-extensions")
        self.options.add_argument('--no-sandbox')

        # overcome limited resource problems
        self.options.add_argument("--disable-dev-shm-usage")

        self.options.add_argument(
            'user-data-dir=' + General.CHROME_COOKIES_ROOT_PATH + '/' + str(userId) + '/' + str(accountId))
        self.browser: webdriver.Chrome = None
        self.elem = None

    def run_work(self, work_raw):
        print("run worke girdim.")
        work: Work = Work.parse_obj(work_raw)
        self.browser = webdriver.Chrome(chrome_options=self.options)
        print("parseladım ve chrome açtım.")
        if work.definition.like:
            self.like_tweet_by_url(work.tweetUrl)
        if work.definition.retweet:
            self.sl(2)
            self.retweet_tweet_by_url(work.tweetUrl)

    def test(self):
        print("works tümü --> ", self.works)
        i: Work
        for i in self.works:
            print("####################")
            print("tweet url --> "+i.tweetUrl)
            print("tweet like olsun mu --> "+str(i.definition.like))
            print("tweet rt olsun mu --> "+str(i.definition.retweet))
            print("####################")

    def retweet_tweet_by_url(self, tweetUrl):
        """
        url verilen tweet like atar.
        """
        print("retweet içine girdim.")
        self.browser.get("https://twitter.com/"+tweetUrl)
        try:
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Retweet"]')))
        except Exception:
            raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,
                                detail="İşlem zaman aşımına uğradı. Birazdan tekrar denenecek.")
        finally:
            self.elem = self.browser.find_element_by_xpath(
                '//div[@aria-label="Retweet"]')
            self.elem.click()
            self.sl(0.2)
            self.elem = self.browser.find_element_by_xpath(
                '//div[@data-testid="retweetConfirm"]')
            self.elem.click()

    def like_tweet_by_url(self, tweetUrl):
        """
        url verilen tweet like atar.
        """
        print("like girdim")
        self.browser.get("https://twitter.com/"+tweetUrl)
        print("chrome açtm")
        try:
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Like"]')))
        except Exception:
            raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,
                                detail="İşlem zaman aşımına uğradı. Birazdan tekrar denenecek.")
        finally:
            self.elem = self.browser.find_element_by_xpath(
                '//div[@aria-label="Like"]')
            self.elem.click()

    def login(self, username, password):
        self.browser = webdriver.Chrome(chrome_options=self.options)
        self.browser.get("https://twitter.com/login")
        try:
            myElem = WebDriverWait(self.browser, 2, poll_frequency=0.1).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="session[username_or_email]"]')))

        except TimeoutException:
            raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,
                                detail="İşlem zaman aşımına uğradı. Birazdan tekrar denenecek.")
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
                raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,
                                    detail="İşlem zaman aşımına uğradı. Birazdan tekrar denenecek.")

    def close_all(self):
        """
        Driver ile kullanılan tüm kaynaklar release edilir.
        Her işlem sonunda çağırılır.
        """
        self.browser.close()
        self.browser.quit()

    @classmethod
    def sl(cls, sec):
        """time modülünün sleep fonksiyonu için kısa yazım."""
        sleep(sec)
