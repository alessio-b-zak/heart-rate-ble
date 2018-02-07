from bluepy import btle
import struct


class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        data_ints = struct.unpack('<' + 'B'*len(data), data)


        #Averages number of beats per minute
        print("Your heartbeat is : %d" %(data_ints[1]))

        #Display RR Interval
        for i in range(2, len(data_ints), 2):
            rr_interval = 16 * data_ints[i] + data_ints[i+1];
            print("RR_interval measured (peak to peak of heart beat): %d ms" %(rr_interval));

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

        try:
            while True:
                if heartrateP.waitForNotifications(2.0):

                    continue
                else:
                    print("no notification found")
        except KeyboardInterrupt:
            heartrateP.disconnect()
    except Exception as e:
        print(e)



if __name__ == "__main__":
    main()
