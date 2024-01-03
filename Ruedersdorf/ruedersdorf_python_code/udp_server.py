import asyncio
import interface_buffer
import socket


class UDPServer(asyncio.DatagramProtocol):
    def __init__(self,taskIdArray):
        self.taskIdArray = taskIdArray
        self.taskID = -1
        self.interfaceIn = interface_buffer.InterfaceIn()
        self.interfaceOut = interface_buffer.InterfaceOut()

    def connection_made(self, transport):
        self.transport = transport
        
    def datagram_received(self, data, addr):
        loop = asyncio.get_event_loop()
        loop.create_task(self.handle_incoming_packet(data, addr))
        
    async def handle_incoming_packet(self,data,addr):
        await self.handling_buffer(data,addr)

    async def handling_buffer(self,data,addr):
        data = data.decode('utf-8')
        self.interfaceIn.setData(data)
        if(self.interfaceIn.dataFromRobot[0] == 1): # new connection
            print("new connection established")
            self.interfaceOut.stateOfHandshake = 0
        if(self.interfaceIn.dataFromRobot[1] == 1 and self.interfaceOut.stateOfHandshake == 0):
            if(self.interfaceIn.dataFromRobot[4] == 1):  # Initialization of camera 1 (mac ID)
                pose_1 = self.interfaceIn.dataFromRobot[6:12]
                pose_2 = self.interfaceIn.dataFromRobot[12:18]
                pose_3 = self.interfaceIn.dataFromRobot[18:24]
                self.cameraInitPoseDict = {'pose_1':pose_1,'pose_2':pose_2,'pose_3':pose_3}
            if(self.interfaceIn.dataFromRobot[4] == 3):  # Compact Max initialization
                pose_1 = self.interfaceIn.dataFromRobot[6:12]
                pose_2 = self.interfaceIn.dataFromRobot[12:18]
                pose_3 = self.interfaceIn.dataFromRobot[18:24]
                self.compactMaxInitPoseDict = {'pose_1':pose_1,'pose_2':pose_2,'pose_3':pose_3}
            if(self.interfaceIn.dataFromRobot[4] == 5):  # Centrifuge Racks initialization
                pose_1 = self.interfaceIn.dataFromRobot[6:12]
                pose_2 = self.interfaceIn.dataFromRobot[12:18]
                pose_3 = self.interfaceIn.dataFromRobot[18:24]
                self.centrifugeRackInitPoseDict = {'pose_1':pose_1,'pose_2':pose_2,'pose_3':pose_3}
            if(self.interfaceIn.dataFromRobot[4] == 6):  # Centrifuge TubePos initialization
                pose_1 = self.interfaceIn.dataFromRobot[6:12]
                pose_2 = self.interfaceIn.dataFromRobot[12:18]
                pose_3 = self.interfaceIn.dataFromRobot[18:24]
                pose_4 = self.interfaceIn.dataFromRobot[24:30]
                pose_5 = self.interfaceIn.dataFromRobot[30:36]
                self.centrifugeInitPoseDict = {'pose_1':pose_1,'pose_2':pose_2,'pose_3':pose_3,'pose_4':pose_4,'pose_5':pose_5}
            if(self.interfaceIn.dataFromRobot[4] == 10):  # Fehler stand initialization
                pose_1 = self.interfaceIn.dataFromRobot[6:12]
                pose_2 = self.interfaceIn.dataFromRobot[12:18]
                pose_3 = self.interfaceIn.dataFromRobot[18:24]
                self.fehlerStandInitPosDict = {'pose_1':pose_1,'pose_2':pose_2,'pose_3':pose_3}
            elif(self.interfaceIn.dataFromRobot[4] == 0):  # Starting of Job Id
                if(self.taskIdArray):
                    [srcJob,destJob] = self.taskIdArray.pop(0)
                    self.interfaceOut.srcJob = srcJob
                    self.interfaceOut.destJob = destJob
                    if(self.interfaceOut.srcJob == 11):
                        self.interfaceOut.srcPos = self.interfaceIn.dataFromRobot[6:12]
                        self.interfaceOut.destPos = self.interfaceIn.dataFromRobot[12:18]
                    if(self.interfaceOut.srcJob == 3):
                        self.interfaceOut.srcPos = self.interfaceIn.dataFromRobot[12:18]
                        self.interfaceOut.destPos = self.interfaceIn.dataFromRobot[18:24]
                    print('Send srcJob %r to %s' % (self.interfaceOut.srcJob, addr))
                    print('Send destJob %r to %s' % (self.interfaceOut.destJob, addr))
                else:
                    [srcJob,destJob] = [0,0]
                    self.interfaceOut.srcJob    = srcJob
                    self.interfaceOut.destJob   = destJob
                    self.interfaceOut.srcPos    = [0,0,0,0,0,0]
                    self.interfaceOut.destPos   = [0,0,0,0,0,0]
                    print('Send srcJob %r to %s' % (self.interfaceOut.srcJob, addr))
                    print('Send destJob %r to %s' % (self.interfaceOut.destJob, addr))
            print("isAlive")
            self.interfaceOut.stateOfHandshake = 1
            self.transport.sendto(self.interfaceOut.getData().encode(), addr)     
        if(self.interfaceIn.dataFromRobot[1] == 0 and self.interfaceOut.stateOfHandshake == 1):
            self.interfaceOut.stateOfHandshake = 0
            self.transport.sendto(self.interfaceOut.getData().encode(),addr)


async def main():
    print("Starting UDP server")

    taskIdArray = [[11,41],[0,0]]
    cameraInitPoseDict = {}
    compactMaxInitPoseDict = {}
    centrifugeRackInitPoseDict = {}
    centrifugeInitPoseDict = {}
    fehlerStandInitPosDict = {}


    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UDPServer(taskIdArray),
        # local_addr=('0.0.0.0', 6201),
        local_addr=('192.168.1.21', 6201),
        family=socket.AF_INET)
    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()


asyncio.run(main())