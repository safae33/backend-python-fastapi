from app.celery import app
from app.services.selenium import Twitter
from time import sleep

from pydantic import parse_obj_as
from app.schemas.request.accountworker import AccountWorker, Work
from typing import List


@app.task
def test(aw):
    obj = parse_obj_as(List[Work], aw['works'])
    print(obj)
    return "al işte bak ne oldu şimdi"


@app.task
def twitter_login(mail, pw, accountId):
    try:
        tw = Twitter(accountId, isInit=True)
        tw.login(mail, pw)
        tw.close_all()
        del tw
        return "Başarılı."
    except Exception as e:
        print(e)
        return "Başaramadık abi."


@app.task
def start_works_for_account(accountId, works_dict):
    try:
        tw = Twitter(accountId)
        tw.run_works(works_dict)
        tw.close_all()
        del tw
        return "Başarılı"
    except Exception as e:
        print(e)
        return "work başladı ama buralara patladık abi."


@app.task
def set_workers_for_account(accountWorker):
    try:

        start_works_for_account.delay(
            accountWorker['accountId'], accountWorker['works'])
        return "Başarılı. Parçalara ayırma tamamlandı."
    except Exception as e:
        print(e)
        return "daha set ederken başaramadık abi."
