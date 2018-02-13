from flask import Flask
from bluepy import btle
import struct
import threading
import atexit

commonDataStruct = {'peripheral' : None, 'heartrateP' : None}
POOL_TIME = 1 #Seconds
# lock to control access to variable
dataLock = threading.Lock()
# thread handler
yourThread = threading.Thread()

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        global commonDataStruct
        data_ints = struct.unpack('<' + 'B'*len(data), data)
        print("handling notification")
        print(data)
        commonDataStruct['heartrateP'] = data_ints[1]


def create_app():
    app = Flask(__name__)

    def interrupt():
        global yourThread
        yourThread.cancel()

    def doStuff():
        global commonDataStruct
        global yourThread
        with dataLock:
        # Do your stuff with commonDataStruct Here
            while True:
                if commonDataStruct['peripheral'].waitForNotifications(2.0):
                    continue
                else:
                    print("no notification found")

    def doStuffStart():
        # Do initialisation stuff here
        global yourThread
        # Create your thread
        try:
            commonDataStruct['peripheral'] = btle.Peripheral("d2:89:67:b7:bc:aa", btle.ADDR_TYPE_RANDOM)
            commonDataStruct['peripheral'].setDelegate(MyDelegate())
            # task = poll_heart_rate.delay()
            commonDataStruct['peripheral'].writeCharacteristic(15, struct.pack('<bb',1,0),True)
            print("Connected to peripheral")
        except Exception as e:
            print(e)
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()

    # Initiate
    doStuffStart()
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    return app

server = create_app()

def calculate_heart():
    global commonDataStruct
    return str(commonDataStruct['heartrateP'])

@server.route('/')
def index():
    return calculate_heart()


from server import routes
