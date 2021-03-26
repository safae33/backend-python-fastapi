from config import Celery as CeleryOpt
from celery import Celery


app = Celery('app', broker=CeleryOpt.BROKER_CONNECTION_URL,
             backend=CeleryOpt.CELERY_RESULT_BACKEND,
             include=['app.celery.twitter'])


def check(id):
    return app.AsyncResult(id).state
