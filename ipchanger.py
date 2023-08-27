from time import sleep
from requests import get
from ppadb.client import Client as AdbClient

def connect():
    client = AdbClient(host="127.0.0.1", port=5037) # Default is "127.0.0.1" and 5037

    devices = client.devices()

    if len(devices) == 0:
        print('No devices')
        quit()

    device = devices[0]

    #print(f'Connected to {device}')

    return device, client


def changeIp():
    device, client = connect()
    device.shell('cmd connectivity airplane-mode enable')
    sleep(10)
    device.shell('cmd connectivity airplane-mode disable')
    #print('done')
    #ip = get('https://api.ipify.org').content.decode('utf8')
    #print('My public IP address is: {}'.format(ip))




# adb start-server
# scrcpy
