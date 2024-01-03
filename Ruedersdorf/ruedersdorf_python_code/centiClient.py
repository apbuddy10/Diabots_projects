import asyncio
from datetime import datetime
from centrifugeConnector import CentrifugeInterface
from settings import Settings
import time

import os


async def test():
    client = CentrifugeInterface()
    # print(datetime.now().time())
    # print(await client.hatch_close())
    print(await client.check_lock())
    # print(datetime.now().time())
    print(await client.hatch_open())
    print(datetime.now().time())
    print(await client.set_rotor_position(1))
    print(datetime.now().time())
    print(await client.set_rotor_position(2))
    print(datetime.now().time())
    print(await client.set_rotor_position(3))
    print(datetime.now().time())
    print(await client.set_rotor_position(4))
    print(datetime.now().time())
    print(await client.hatch_close())
    # print(datetime.now().time())
    # print(await client.start_centrifuge())
    # print(datetime.now().time())
    # print(await client.is_running())
    # time.sleep(100)
    # print(datetime.now().time())
    # print(await client.hatch_open())

    
    # path = "C:\\Users\\user\\Desktop\\NG"
    # path = os.path.realpath(path)
    # os.startfile(path)

    # folderPath = Settings.destpath
    # file = open(os.path.join(folderPath,"resultst.csv"), "w")
    # file.write("Color: GREEN, Barcode: 7123456789, Blood level: 30, Plasma level: 40")
    # file.close()


asyncio.run (test())