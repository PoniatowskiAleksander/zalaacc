import main
import ipchanger
from time import sleep


while True:
    try:
        main.main()
    except Exception as e: 
        print(e)
        ipchanger.changeIp()
        sleep(3)

