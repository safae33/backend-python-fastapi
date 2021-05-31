from subprocess import Popen

Popen('watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery --app=app.celery worker --loglevel=INFO  --concurrency=1 --uid=nobody --gid=nogroup -E', shell=True)
