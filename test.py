from bluepy import btle
import struct


class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        data_ints = struct.unpack('<' + 'B'*len(data), data)
        print (data_ints)
        print("Your heartbeat is : %d" %(data[1]))





def main():
    try:
        heartrateP = btle.Peripheral("d2:89:67:b7:bc:aa", btle.ADDR_TYPE_RANDOM)
        heartrateP.setDelegate(MyDelegate())
        for characteristic in heartrateP.getCharacteristics():
            #print(characteristic.properties);
            print(characteristic.uuid);
            print(characteristic.getHandle())


        #for descriptor in heartrate.getDescriptors():
        #if str(descriptor.uuid).startswith("00002902"):
        #         print(descriptor.valHandle)
        # struct.pack('<bb', 0x01, 0x00)

        print(heartrateP.writeCharacteristic(15, struct.pack('<bb',1,0),True));

        while True:
            if heartrateP.waitForNotifications(2.0):
                print("waiting for notifications")
                continue
            else:
                print("no notification found")
    except Exception as e:
        print(e)
    finally:
        heartrateP.disconnect()



if __name__ == "__main__":
    main()
