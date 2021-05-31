from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from typing import List
from pydantic import parse_obj_as
from sqlalchemy.sql.expression import null


from config import Selenium
from app.schemas.request.accountworker import AccountWorker, Work
from app.schemas.response import StweetInfo
from app.services import AccountFuncs


class Twitter():
    """
    Twitter işlemleri için class. Constructor içinde accountId alarak initialize eder.
    * login gerekitrmeyen işlem yapılacaksa(tweet bilgisi alma gibi) accountId 0 verilir.
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
            'user-data-dir=' + Selenium.ACCOUNTS_PATH + '/' + self.accountId)

        # işlemlerde kullanılacak değerlerin belirlenmesi.
        self.browser: webdriver.Chrome = None
        self.elem = None

    # def test(self):
    #     self.browser = webdriver.Chrome(chrome_options=self.options)
    #     self.browser.

    def open_url(self, url):
        self.browser = webdriver.Chrome(chrome_options=self.options)
        self.browser.get(url)

    def run_works(self, works_dict, delayBetweenTweets=3):
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
                print("LİKE KISMINDA BİTTİ RT YE GEÇİYORUM.")
                # if work.definition.retweet:
                #     sleep(1)
                #     self.retweet_tweet_by_url(work.tweetUrl)
            if work.definition.retweet:
                self.retweet_tweet_by_url(work.tweetUrl)
            if(len(works) != 1):
                sleep(delayBetweenTweets)
            print("ŞUAN BİR WORK BİTMİŞ OLMALI")
        print("tüm WORKler  BİTTİİİİ")

    def like_tweet_by_url(self, tweetUrl):
        """
        url verilen tweete like atar.
        """
        self.browser.get("https://twitter.com/"+tweetUrl)
        try:
            WebDriverWait(self.browser, 5, poll_frequency=0.2).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Beğen"]')))
        except Exception:
            self.close_all()
            print("LİKE KISMINDA PATLADI BULAMADIK.")
        finally:
            self.elem = self.browser.find_element_by_xpath(
                '//div[@aria-label="Beğen"]')
            self.elem.click()
            print("LİKE ATTIM ŞUAN.")

    def retweet_tweet_by_url(self, tweetUrl):
        """
        url verilen tweeti retweet eder.
        """
        self.browser.get("https://twitter.com/"+tweetUrl)
        try:
            WebDriverWait(self.browser, 5, poll_frequency=0.2).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Retweet"]')))
        except Exception:
            self.close_all()
            print("RT BUTONU BULUNAMADI BAK.")
        finally:
            self.elem = self.browser.find_element_by_xpath(
                '//div[@aria-label="Retweet"]')
            self.elem.click()
            sleep(0.2)
            self.elem = self.browser.find_element_by_xpath(
                '//div[@data-testid="retweetConfirm"]')
            self.elem.click()
            print("RTYE TIKLADIM VE CONFİRM ATTIM BAK.")

    def login(self, username, password):
        """
        login işlemi. Yalnızca bu işlemde isInit=True ile construct edilir.
        """
        self.browser = webdriver.Chrome(chrome_options=self.options)
        self.browser.get("https://twitter.com/login")
        try:
            WebDriverWait(self.browser, 2, poll_frequency=0.1).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="session[username_or_email]"]')))
        except TimeoutException:
            self.close_all()
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
                self.close_all()
                print(
                    "BUNLAR DAHA DÜZGÜN LOG İŞLEMİYLE AYARLANACAK. AMA SONRA. AHATA OLDU BU ARADA")

    def get_account_info(self, username: str = None):
        if self.isInit:  # initialize ediliyorsa username e gerek yok. zaten yeni giriş yapılmış. direkt profil açılır ve bilgiler alınır.
            try:
                WebDriverWait(self.browser, 4, poll_frequency=0.2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Profile']")))
                self.elem: WebElement = self.browser.find_element_by_css_selector(
                    "a[aria-label='Profile']")
                self.elem.click()

                try:
                    WebDriverWait(self.browser, 4, poll_frequency=0.2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, f"div[class='{Selenium.ACCOUNT_PROFILE_CLASSES}']")))
                    self.elem: WebElement = self.browser.find_element_by_css_selector(
                        f"div[class='{Selenium.ACCOUNT_PROFILE_CLASSES}']")
                    accountInfo = {}

                    # profile pic url bulunması.
                    accountInfo["profilePicUrl"] = self.elem.find_element_by_tag_name(
                        "img").get_attribute("src")

                    spans = self.elem.find_elements_by_css_selector(
                        f"span[class='{Selenium.TARGET_SPAN_CLASSES}'")

                    # name bulunması
                    accountInfo["name"] = spans[2].text

                    # username bulunması
                    accountInfo["username"] = spans[3].text

                    return accountInfo
                except:
                    pass
            except:
                pass

    def get_tweet_info(self, url: str):
        tweet = {}
        self.browser = webdriver.Chrome(chrome_options=self.options)
        self.browser.get("https://twitter.com/"+url)
        print("try a giricem şimdi, browserdan tweet linkini açtım")
        try:
            WebDriverWait(self.browser, 4, poll_frequency=0.2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"article[class='{Selenium.TARGET_ARTICLE_CLASSES}']")))

            print("devam ediyom imgh den başlıyom")
            # tweet img

            self.elem: WebElement = self.browser.find_element_by_css_selector(
                f"article[class='{Selenium.TARGET_ARTICLE_CLASSES}']")

            tweet["profilePicUrl"] = self.elem.find_element_by_tag_name(
                "img").get_attribute("src")

            # tweet name
            # self.elem: WebElement = self.browser.find_element_by_xpath(
            #     '//span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"')

            textSpans = self.elem.find_elements_by_css_selector(
                f"span[class='{Selenium.TARGET_SPAN_CLASSES}'")

            tweet["name"] = textSpans[1].text

            # tweet username

            tweet["username"] = textSpans[2].text

            # tweet text

            tweet["text"] = f"{textSpans[3].text}  {textSpans[4].text}  {textSpans[5].text}"

            return tweet
        except TimeoutException as e:
            print("2. sıradaki img bulunamadı bulunamadı")
            return "hata verdi" + e.msg
        except Exception as e:
            tweet['sadsad'] = e
            return tweet

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
