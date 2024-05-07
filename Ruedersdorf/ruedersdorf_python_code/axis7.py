import asyncio
import socket
from enum import Enum
from logger import errorlogger, jobslogger
from settings import Settings

class Axis7Resp(Enum):    
    listen = 0,
    startProcessing=1,    
    success = 2,
    failed=3,
    timeout=4

class CommandMsg():
    def __init__(self):
        self.slaveid = 1
        self.velocity =1000 # 2500
        self.acceleration = 2000 # 3000
        self.deceleration = 2000 # 3000
        # self.MSG_EMPTY = bytes("",'ascii') 
        self.HOME_POS_INIT       = bytes("home("    + str(self.slaveid) + ")",'ascii') #move Slave with number 1 in home position
        self.MSG_ENABLE          = bytes("enable("  + str(self.slaveid) + ")",'ascii') #enable Slave with number 1 (turn on motor power)
        self.MSG_DISABLE         = bytes("disable(" + str(self.slaveid) + ")",'ascii')
        self.MSG_EXIT            = bytes("exit()",'ascii')           
    
    def posStr(self, posSpeed):
        return bytes("movePosAbs(" + str(self.slaveid) + ","+str(posSpeed[0])+"," + str(posSpeed[1]) + "," + str(posSpeed[2]) + "," + str(posSpeed[3]) + ")", 'ascii')

class AxisConn_7():
    def __init__(self,host = "127.0.0.1", port = 9060):
        self.message = bytes("", 'ascii')
        self.commandMsg = CommandMsg()
        self.connection = None
        self.tcp_socket = None
        self.host=host
        self.port =int(port)
        self.initCommunication()

    def initCommunication(self):
        if self.tcp_socket is not None:
            self.tcp_socket.close()
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.settimeout(15)
        self.server_address = (self.host, self.port)
        self.tcp_socket.connect(self.server_address)
        self.currentPose = None
        self.newPose = None

    async def reset(self, homing=False):
        self.initCommunication()
        await self.sendMessage(self.commandMsg.MSG_DISABLE)
        await self.sendMessage(self.commandMsg.MSG_ENABLE)
        if homing:
            await self.sendMessage(self.commandMsg.HOME_POS_INIT)

    #appends start and end characters
    async def getBytes(self,resp:Axis7Resp):
        return b'\x02'+ bytes(resp.name, 'ascii') +b'\x03'

    async def recvMessage(self):
        data = await self.readNextPacket()
        print("data", data)
        if data.startswith(await self.getBytes(Axis7Resp.success)):
            print("Executing the command is finished, everything is ok!")
            return True
        elif data.startswith(await self.getBytes(Axis7Resp.timeout)):
            print("Axis 7 internal timeout occured or safety stop enabled")
            jobslogger.info(
                "Axis 7 internal timeout occured or safety stop enabled")
            return False
        elif data.startswith(await self.getBytes(Axis7Resp.failed)):
            print("Executing the command failed, do some Error handling!")
            jobslogger.info(
                "Executing the command failed, do some Error handling!")
            return False
        else:
            print(
                "else data:  -------------     ", data)        
        

    async def readNextPacket(self):
        # in this loop we read data byte by byte from the socket
        # we ignore all bytes, unless we receive <STX>.
        # after receiving <STX> we read until we receive <ETX> which indicates, that we received a complete message
        data = bytes("", 'ascii')
        bIgnoreCurrentByte = True
        while True:
            current = self.tcp_socket.recv(1)
            if (current == b'\x02'):  # if it is <STX>
                bIgnoreCurrentByte = False

            if (bIgnoreCurrentByte == False):
                data = data + current

            if (bIgnoreCurrentByte == False and current == b'\x03'):
                break
        return data

    async def waitUntilListen(self):
        try:
            while (await self.readNextPacket() == await self.getBytes(Axis7Resp.listen)):
                print("Client is Ready to receive next Command.")
                break
        except socket.timeout:
            print("Axis 7 scocket timeout received")
            await self.reset()
            await self.waitUntilListen()

    async def waitForStartProcessing(self):
        try:
            while (await self.readNextPacket() == await self.getBytes(Axis7Resp.startProcessing)):
                print("Started Processing...now wait for result.")
                break
        except socket.timeout:
            print("Axis 7 scocket timeout received")
            await self.reset()
            await self.waitForStartProcessing()

    async def sendMessage(self, message=bytes("", 'ascii')):
        try:
            if self.newPose is not None and self.newPose == self.currentPose:
                print("Same pose", self.newPose, self.currentPose)
                jobslogger.info("7th Axis, Same pose: {0}, {1}".format(self.newPose, self.currentPose))
                return
            await self.waitUntilListen()
            output = b'\x02' + message + b'\x03'
            print("Message",output)
            self.tcp_socket.sendall(output)
            await self.waitForStartProcessing()
            retVal = await self.recvMessage()
            if not retVal:
                await self.reset()
                await self.sendMessage(message)    
            if self.newPose is not None:
                self.currentPose = self.newPose
                self.newPose = None        
        except TimeoutError:
            print("Timeout error while Sending data")
            await self.reset()
            await self.sendMessage(message)
        except Exception as e:
            errorlogger.exception(e)
            jobslogger.info("Unknown exception occured")
            await self.reset()
            await self.sendMessage(message)

    def posStr(self,posSpeed:list):        
        self.newPose = posSpeed[0]
        jobslogger.info("7th Axis, Command Pose Received: {0}".format(posSpeed[0]))
        return self.commandMsg.posStr(posSpeed)

async def main():
    axis_7 = AxisConn_7(Settings.Axis7Host,Settings.Axis7Port)
    await axis_7.reset(True)
    # await axis_7.sendMessage(axis_7.posStr(Settings.HOME_POS_COBAS_MACHINE))
    #await asyncio.sleep(1) 
    # await axis_7.sendMessage(axis_7.posStr(Settings.HOME_POS_COBAS_SLIDE_15))
    # await asyncio.sleep(1) 
    await axis_7.sendMessage(axis_7.posStr(Settings.HOME_POS_CAM_1))
    await asyncio.sleep(1) 
    # while (True):
    #     await axis_7.sendMessage(axis_7.posStr(Settings.HOME_POS_COBAS_BASKET_15))
    #     await asyncio.sleep(1) 
    #     await axis_7.sendMessage(axis_7.posStr(Settings.HOME_POS_COBAS_MACHINE))
    #     await asyncio.sleep(1) 
    #     # break
    # counter = 1
            # retFlag = False
            # retVal = False
            # while(retFlag == False or counter > 3):
            #     retVal = await self.recvMessage()
            #     if(retVal == True):
            #         output = b'\x02' + message + b'\x03'
            #         self.tcp_socket.sendall(output)
            #         retVal = await self.recvMessage()
            #         if(retVal == True):
            #             retFlag = True
            #     counter+= 1
            # return retVal
    axis_7.tcp_socket.close()
if __name__ == '__main__':
    asyncio.run(main())