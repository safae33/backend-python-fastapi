from app.db.crud import Crud
from sqlalchemy.orm import session
from pydantic import parse_obj_as
from app.db.models.account import Account
from app.celery import app
from app.services.selenium import Twitter
from app.db.session import SessionLocal

from app.schemas.request.accountworker import AccountWorker, Work
from app.schemas.request.newProcess import ScNewProcess
from app.dependencies import Redis


@app.task
def get_tweet_info(url: str):
    tw = Twitter(0)
    tweet = tw.get_tweet_info(url)
    tw.close_all()
    del tw
    return tweet


@app.task
def start_new_process(newProcess_dict):
    ## start_new_process.request.id task başlayınca oluşan task_id bu.
    try:
        newProcess = parse_obj_as(ScNewProcess, newProcess_dict)
        cache = Redis()

        
    except Exception as e:
        print(e)
        # burda kaldın


@app.task
def twitter_login(mail, pw, userId):
    try:
        new = Account()
        new.userId = userId
        Crud.create(new)
        tw = Twitter(new.id, isInit=True)
        tw.login(mail, pw)
        info: dict = tw.get_account_info()
        Crud.update(Account, new.id, values=info)
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
        print("runworksden çıktım şuan")
        tw.close_all()
        print("CLOSE ALL YAPTIIM")
        del tw
        print("DEL DE YAPTIM")
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


# {
#     "accountId": "2",
#     "works": [
#         {
#             "tweetUrl": "amangorunmeyelm/status/1357127708535361536",
#             "definition": {
#                 "like": true,
#                 "retweet": true
#             }
#         },
#         {
#             "tweetUrl": "amangorunmeyelm/status/1357127710863155203",
#             "definition": {
#                 "like": true,
#                 "retweet": true
#             }
#         }, {
#             "tweetUrl": "amangorunmeyelm/status/1357127712868085764",
#             "definition": {
#                 "like": true,
#                 "retweet": true
#             }
#         }
#     ]
# }
