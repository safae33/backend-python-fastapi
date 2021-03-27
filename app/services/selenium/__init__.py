import time

from fastapi import HTTPException, status

from config import General

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class Twitter():

    def __init__(self, userId: int):
        self.options = Options()
        self.options.headless = True
        self.options.add_argument("--disable-extensions"); # disabling extensions
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
        self.options.add_argument(
            'user-data-dir=' + General.CHROME_COOKIES_ROOT_PATH + '/' + str(userId) + '/' + '1')
        self.browser = webdriver.Chrome(chrome_options=self.options)
        self.elem = None

    def open_twitter(self):
        self.browser.get("https://twitter.com")

    def close_all(self):
        self.browser.close()
        self.browser.quit()

    def like_tweet_by_url(self, tweetUrl):
        self.browser.get(tweetUrl)
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
        self.browser.get("https://twitter.com/login")
        print("sayfayı açtım")
        try:
            myElem = WebDriverWait(self.browser, 1, poll_frequency=0.1).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="session[username_or_email]"]')))
            print("try içindeym")
        except TimeoutException:
            print("except içindeym")
            raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,
                                detail="İşlem zaman aşımına uğradı. Birazdan tekrar denenecek.")
        finally:
            print("finally içindeym")
            self.elem = self.browser.find_element_by_xpath(
                '//input[@name="session[username_or_email]"]')
            self.elem.send_keys(username)
            self.elem = self.browser.find_element_by_xpath(
                '//input[@name="session[password]"]')
            self.elem.send_keys(password)
            print("şifreyi de girdim ooh.")
            self.elem.send_keys(Keys.ENTER)
            try:
                myElem = WebDriverWait(self.browser, 1, poll_frequency=0.1).until(
                    EC.presence_of_element_located((By.ID, 'react-root')))

            except TimeoutException:
                raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,
                                    detail="İşlem zaman aşımına uğradı. Birazdan tekrar denenecek.")

    @ classmethod
    def sl(cls, sec):
        """time modülünün sleep fonksiyonu için kısa yazım."""
        time.sleep(sec)
