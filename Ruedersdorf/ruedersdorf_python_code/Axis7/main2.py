from ast import While
from cmath import pi
import select
import sys
# from telnetlib import DO
import time
import socket
import argparse
from io import BytesIO
import subprocess
from enum import Enum
import asyncio

#Maximum Packet size for UDP
maxUdpSize=8195

#parser = argparse.ArgumentParser()
#parser.add_argument('port', type=int)
#args = parser.parse_args()

host = "192.168.31.10"
port = 9060
data_received_0 = -1
data_received_1 = -1
data_received_2 = "none"

class CommandMsg():
    def __init__(self):
        self.slaveid = 1
        self.velocity = 270  # 0.27 m/s
        self.acceleration = 200 # 0.2 m/s2
        self.deceleration = 200 # 0.2 m/s2
        # self.MSG_EMPTY = bytes("",'ascii') 
        self.HOME_POS_INIT = bytes("home(" + str(self.slaveid) + ")",'ascii') #move Slave with number 1 in home position
        self.MSG_ENABLE = bytes("enable(" + str(self.slaveid) + ")",'ascii') #enable Slave with number 1 (turn on motor power)
        self.MSG_DISABLE = bytes("disable(" + str(self.slaveid) + ")",'ascii')
        self.MSG_EXIT = bytes("exit()",'ascii')
        self.HOME_POS_CAM_1 = bytes("movePosAbs(" + str(self.slaveid) + ",0," + str(self.velocity) + "," + str(self.acceleration) + ","         + str(self.deceleration) +      ")",'ascii') # move Slave 1 to absolute Position 3meters with velocity 1m/s
        self.HOME_POS_CAM_2 = bytes("movePosAbs(" + str(self.slaveid) + ", 250000, "  + str(self.velocity) + "," + str(self.acceleration) + "," + str(self.deceleration) +      ")",'ascii')
        self.HOME_POS_CENTRIFUGE = bytes("movePosAbs(" + str(self.slaveid) + ",2500000, " + str(self.velocity) + "," + str(self.acceleration) + "," + str(self.deceleration) +  ")",'ascii')
        self.HOME_POS_SYSMEX = bytes("movePosAbs(" + str(self.slaveid) + ",2150000," + str(self.velocity) + "," + str(self.acceleration) + "," + str(self.deceleration) +       ")",'ascii')
        self.HOME_POS_COBASPURE = bytes("movePosAbs(" + str(self.slaveid) + ",3000000," + str(self.velocity) + "," + str(self.acceleration) + "," + str(self.deceleration) +    ")",'ascii')

class AxisConn_7():
    def __init__(self):
        self.message = bytes("",'ascii')
        self.commandMsg = CommandMsg()     
        self.connection = None
        self.initCommunication()

    def initCommunication(self):
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_address = (host,port)
            self.tcp_socket.connect(self.server_address)
         # Set up a TCP/IP server
        # try :
        #     self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     # Bind the socket to server address and port
        #     self.tcp_socket.bind((host, port))
        #     # Listen on port 81
        #     self.tcp_socket.listen(self.commandMsg.slaveid)
        #     #Waiting for connection, start DiaAxis7.exe now!
        #     # subprocess.run(["..\DiaAxis7\Release\DiaAxis7.exe","\\Device\\NPF_{08944A45-5A55-47EF-8518-32A88DA099A1}","8000","127.0.0.1","9095","1000"])
        #     # subprocess.call(["axis7.bat"])
           
        # except Exception as e :
        #     print(e)

    async def recvMessage(self):
        try:
            while True:
                #in this loop we read data byte by byte from the socket
                #we ignore all bytes, unless we receive <STX>.
                #after receiving <STX> we read until we receive <ETX> which indicates, that we received a complete message
                data = bytes("", 'ascii')
                bIgnoreCurrentByte = True
                while True:
                        current = self.tcp_socket.recv(1)
                        if(current == b'\x02'): #if it is <STX>
                            bIgnoreCurrentByte = False

                        if(bIgnoreCurrentByte == False):
                            data = data + current

                        if(bIgnoreCurrentByte == False and current == b'\x03'):
                            break; 
                if(data==(b'\x02' + bytes("listen",'ascii') + b'\x03')):
                    print("Client is Ready to receive next Command.")
                    # break #break and go to next command... (This is the only position, where we leave this receive loop!)
                    return True
                elif(data==(b'\x02' + bytes("startProcessing",'ascii') + b'\x03')):
                    print("Command received...now wait for result")
                    continue #continue and wait for result (success/failed)
                elif(data==(b'\x02' + bytes("success",'ascii') + b'\x03')):
                    print("Executing the command is finished, everything is ok!")
                    return True
                elif(data==(b'\x02' + bytes("failed",'ascii') + b'\x03')):
                    print("Executing the command failed, do some Error handling!")
                    print("Abnormal termination of 7th Axis!")
                    await asyncio.sleep(2)
                    return False
        except TimeoutError:
            print("Timeout error while Receiving data")

    async def sendMessage(self, message=bytes("", 'ascii')):
        try:
            # output = b'\x02' + message + b'\x03'
            # self.tcp_socket.send(output)
            # retVal = await self.recvMessage()
            # return retVal
            retVal = await self.recvMessage()
            if(retVal == True):
                output = b'\x02' + message + b'\x03'
                self.tcp_socket.sendall(output)
                retVal = await self.recvMessage()
                return retVal
            else:
                return False
        except TimeoutError:
            print("Timeout error while Sending data")
        # finally:
        #     print("Closing the socket")
        #     self.tcp_socket.close()


async def main():
    axis_7 = AxisConn_7()
    await axis_7.sendMessage(axis_7.commandMsg.MSG_ENABLE)
    # await axis_7.sendMessage(axis_7.commandMsg.HOME_POS_INIT)
    # while (True):
    #     await axis_7.sendMessage(axis_7.commandMsg.HOME_POS_CENTRIFUGE)
    #     await asyncio.sleep(1)
    #     await axis_7.sendMessage(axis_7.commandMsg.HOME_POS_CAM_2)
    #     await asyncio.sleep(1)
    #     await axis_7.sendMessage(axis_7.commandMsg.HOME_POS_COBASPURE)
    #     await asyncio.sleep(1)
    #     await axis_7.sendMessage(axis_7.commandMsg.HOME_POS_CAM_1)
    #     await asyncio.sleep(1)

    axis_7.tcp_socket.close()
if __name__ == '__main__':
    asyncio.run(main())