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

host = "127.0.0.1"
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
        self.HOME_POS_CAM_1 = bytes("movePosAbs(" + str(self.slaveid) + ", 0, " + str(self.velocity) + "," + str(self.acceleration) + "," + str(self.deceleration) + ")",'ascii') # move Slave 1 to absolute Position 3meters with velocity 1m/s
        self.HOME_POS_CAM_2 = bytes("movePosAbs(" + str(self.slaveid) + ", 250000, " + str(self.velocity) + "," + str(self.acceleration) + "," + str(self.deceleration) +  ")",'ascii')
        self.HOME_POS_CENTRIFUGE = bytes("movePosAbs(" + str(self.slaveid) + ",250000, " + str(self.velocity) + "," + str(self.acceleration) + "," + str(self.deceleration) +  ")",'ascii')
        self.HOME_POS_SYSMEX = bytes("movePosAbs(" + str(self.slaveid) + ", 2150000, " + str(self.velocity) + "," + str(self.acceleration) + "," + str(self.deceleration) +  ")",'ascii')
        self.HOME_POS_COBASPURE = bytes("movePosAbs(" + str(self.slaveid) + ", 3000000, " + str(self.velocity) + "," + str(self.acceleration) + "," + str(self.deceleration) +  ")",'ascii')

class AxisConn_7():
    def __init__(self):
        self.message = bytes("",'ascii')
        self.commandMsg = CommandMsg()     
        self.connection = None
        self.initCommunication()

    def initCommunication(self):
        self.tcp_socket = socket.create_connection(host,port)

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

    async def sendMessage(self, message=bytes("", 'ascii')):
        try:
            output = b'\x02' + message + b'\x03'
            self.tcp_socket.sendall(output)
        finally:
            print("Closing the socket")
            self.tcp_socket.close()

    # async def connectionSendRecv(self,message = bytes("",'ascii')):
    #     # await self.connectionRecv()
    #     while True:  
    #         self.connection, self.client = self.tcp_socket.accept()
    #         print("Connected to client IP: {}".format(self.client))
    #         try:
    #         # output = b'\x02' + self.commandMsg.MSG_ENABLE + b'\x03'
    #         # await self.connection.send(output)
    #             while True:
    #                 data = bytes("", 'ascii')
    #                 while True:
    #                     current = self.connection.recv(1)
    #                     data = data + current
    #                     if(current == b'\x03'):
    #                         break; 

    #                 if(data==(b'\x02' + bytes("listen",'ascii') + b'\x03')):
    #                     print("Client is Ready to receive next Command.")
    #                     break

    #             output = b'\x02' + message + b'\x03'
    #             response = self.connection.send(output)
    #             print(response)

    #             # data = bytes("", 'ascii')
    #             # while True:
    #             #     current = self.connection.recv(1)
    #             #     data = data + current
    #             #     if(current == b'\x03'):
    #             #         break; 
    #             # if(data==(b'\x02' + bytes("startProcessing",'ascii') + b'\x03')):
    #             #     print("Command received...now wait for result")
    #             # else:
    #             #     print("something went wrong...the command was not received (wrong spelling is also simply ignored.....)")

    #             # data = bytes("", 'ascii')
    #             # while True:
    #             #         current = self.connection.recv(1)
    #             #         data = data + current
    #             #         if(current == b'\x03'):
    #             #             break;   
    #             # if(data==(b'\x02' + bytes("success",'ascii') + b'\x03')):
    #             #     print("Executing the command is finished, everything is ok!")
    #             # else:
    #             #     print("Executing the command failed...somethings wrong...")

    #             await asyncio.sleep(5) #wait a moment
    #         except Exception as e:
    #             print(e)
    #         finally:
    #             self.connection.close()

async def main():
    axis_7 = AxisConn_7()
    axis_7.initCommunication()
    await axis_7.sendMessage(axis_7.commandMsg.MSG_ENABLE)
if __name__ == '__main__':
    asyncio.run(main())