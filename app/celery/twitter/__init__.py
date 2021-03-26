from time import sleep

from app.celery import app
from app.services.selenium import Twitter



@app.task
def testCelery(n):
    print("evet oldu uyutcam şimdi 5sn")
    sleep(n)
    print("evet oldu bvak")
    return "güzel bitti işte bu return12"

@app.task
def twitter_login(mail, pw, userId):
    try:
        tw = Twitter(userId)
        tw.login(mail, pw)
        tw.close_all()
        del tw
        return "Başarılı."
    except Exception as e:
        print(e)
        return "Başaramadık abi."