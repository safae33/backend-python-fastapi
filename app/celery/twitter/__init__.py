from app.celery import app
from app.services.selenium import Twitter


@app.task
def twitter_login(mail, pw, userId, accountId):
    try:
        tw = Twitter(userId, accountId)
        tw.login(mail, pw)
        tw.close_all()
        del tw
        return "Başarılı."
    except Exception as e:
        print(e)
        return "Başaramadık abi."


@app.task  # taslak
def like_tweet(url, accountWorker):
    try:
        tw = Twitter(userId)
        tw.like_tweet_by_url(url)
        tw.close_all()
        del tw
        return "Başarılı."
    except Exception as e:
        print(e)
        return "Başaramadık abi."


@app.task
def start_work(userId, accountId, work_raw):
    try:
        tw = Twitter(userId, accountId)
        tw.run_work(work_raw)
        tw.close_all()
        del tw
        return "Başarılı"
    except Exception as e:
        print(e)
        return "work başladı ama buralara patladık abi."


@app.task
def set_workers_for_account(accountWorker):
    try:
        start_work.delay(
            accountWorker['userId'], accountWorker['accountId'], accountWorker['works'][0])
        return "Bekleniyor..."
    except Exception as e:
        print(e)
        return "daha set ederken başaramadık abi."
