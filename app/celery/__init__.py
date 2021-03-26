<<<<<<< HEAD
from config import Celery as CeleryOpt
=======
from config import CeleryOpt
>>>>>>> 0bcd303da8d7601518af880ceb8cf72aec3c8d25
from celery import Celery


app = Celery('app', broker=CeleryOpt.BROKER_CONNECTION_URL,
             backend=CeleryOpt.CELERY_RESULT_BACKEND,
             include=['app.celery.twitter'])


<<<<<<< HEAD

=======
>>>>>>> 0bcd303da8d7601518af880ceb8cf72aec3c8d25
def check(id):
    return app.AsyncResult(id).state
