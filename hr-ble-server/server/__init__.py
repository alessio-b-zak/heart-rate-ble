from flask import Flask
from bluepy import btle
from celery import Celery
import struct

server = Flask(__name__)
server.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'

celery = Celery(server.name, broker=server.config['CELERY_BROKER_URL'])

heartrateP = None
heartrateCurrent = 0

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        global heartrateCurrent
        data_ints = struct.unpack('<' + 'B'*len(data), data)
        heartrateCurrent = data


        #Averages number of beats per minute



@celery.task
def poll_heart_rate():
    # while True:
    print("Hello")
    global heartrateCurrent
    heartrateCurrent += 20
        # if heartrateP.waitForNotifications(2.0):
        #     continue
        # else:
        #     print("no notification found")



@server.before_first_request
def startup():
    global heartrateP
    try:
        # heartrateP = btle.Peripheral("d2:89:67:b7:bc:aa", btle.ADDR_TYPE_RANDOM)
        # heartrateP.setDelegate(Deleate())
        task = poll_heart_rate.delay()
    except Exception as e:
        print(e)


def calculate_heart():
    global heartrateCurrent
    return str(heartrateCurrent)




@server.route('/')
def index():
    return calculate_heart()


from server import routes
