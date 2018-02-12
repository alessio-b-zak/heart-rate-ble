from flask import Flask
from bluepy import btle
import struct
import threading
import atexit 



class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        global heartrateCurrent
        data_ints = struct.unpack('<' + 'B'*len(data), data)
        heartrateCurrent = data


        #Averages number of beats per minute

POOL_TIME = 5 #Seconds

# variables that are accessible from anywhere
commonDataStruct = {'peripheral' : None, 'heartrateP' : None}

# lock to control access to variable
dataLock = threading.Lock()
# thread handler
yourThread = threading.Thread()



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
            if (not commonDataStruct['heartrateP'] == None):
                commonDataStruct['heartrateP'] += 10
            else:
                commonDataStruct['heartrateP'] = 0

        # Set the next thread to happen
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()   

    def doStuffStart():
        # Do initialisation stuff here
        global yourThread
        # Create your thread
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()

    # Initiate
    doStuffStart()
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    return app

server = create_app()

#def poll_heart_rate():
#    # while True:
#    print("Hello")
#    global heartrateCurrent
#    heartrateCurrent += 20
#        # if heartrateP.waitForNotifications(2.0):
#        #     continue
#        # else:
#        #     print("no notification found")
#
#
#
#@server.before_first_request
#def startup():
#    global heartrateP
#    try:
#        # heartrateP = btle.Peripheral("d2:89:67:b7:bc:aa", btle.ADDR_TYPE_RANDOM)
#        # heartrateP.setDelegate(Deleate())
#        task = poll_heart_rate.delay()
#    except Exception as e:
#        print(e)


def calculate_heart():
    global commonDataStruct
    return str(commonDataStruct['heartrateP'])




@server.route('/')
def index():
    return calculate_heart()


from server import routes
