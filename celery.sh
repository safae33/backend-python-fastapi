#!/usr/bin/env bash

chown -R nobody:nogroup /var/accounts /var/celery/log

exec pipenv run watchmedo auto-restart --directory=./backend --pattern=*.py --recursive -- celery \
	    --app=backend.celery worker \
            --loglevel=INFO --logfile=/var/celery/log/worker.log \
	    --concurrency=1 \
            --uid=nobody --gid=nogroup \
	    -E