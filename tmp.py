import main
import ipchanger
from time import sleep
import os.path

path = 'xxx.txt'

if not os.path.exists(path):
    f = open(path, 'w')
    f.write('0')
    f.close()


while True:
    try:
        main.main()
    except Exception as e: 
        print(e)
        ipchanger.changeIp()
        sleep(3)


        

