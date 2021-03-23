from app.celery import app
from time import sleep


@app.task
def testCelery():
    print("evet oldu uyutcam şimdi 5sn")
    sleep(5)
    print("evet oldu bvak")
    return "güzel bitti işte bu return"
