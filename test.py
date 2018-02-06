from bluepy import btle


class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotifications(self, cHandle, data):
        print("A notification was received: %s" %data)





def main():
    try:
        heartrate = btle.Peripheral("d2:89:67:b7:bc:aa", btle.ADDR_TYPE_RANDOM)
        heartrate.setDelegate(MyDelegate())
        print("done")
        # for descriptor in heartrate.getDescriptors():
        #     if str(descriptor.uuid).startswith("00002902"):
        #         print(descriptor.valHandle)
        heartrate.writeCharacteristic(15, "\x01\x00".encode())
        while True:
            if heartrate.waitForNotifications(1.0):
                print("waiting for notifications")
                continue
    except Exception as e:
        print(e)



if __name__ == "__main__":
    main()
