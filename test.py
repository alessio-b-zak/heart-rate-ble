from bluepy import btle


def main():
    try:
        heartrate = btle.Peripheral("d2:89:67:b7:bc:aa", btle.ADDR_TYPE_RANDOM)
        print("done")
        for service in heartrate.getServices():
            print(service.uuid)
    except Exception as e:
        print(e)



if __name__ == "__main__":
    main()
