import asyncio
import time
import interface_buffer

class SendMessageClass:
    def __init__(self,transport):
        self.transport = transport

    async def sendMsg(self,message):
        print('Send:', message)     
        self.transport.sendto(message.encode())

class UDPClient(asyncio.DatagramProtocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost
        self.transport = None
        self.interfaceIn = interface_buffer.InterfaceIn()
        self.interfaceOut = interface_buffer.InterfaceOut()

    def connection_made(self, transport):
        self.transport = transport
        # sendMessage = SendMessageClass(self.transport)
        print('Send:', self.message)
        self.interfaceIn.stateOfHandshake = 1
        self.transport.sendto(self.interfaceIn.getData())
        # self.transport.sendto(str(self.interfaceIn.getData()).encode())

    def datagram_received(self, data, addr):
        loop = asyncio.get_event_loop()
        loop.create_task(self.handle_incoming_packet(data, addr))
        
    async def handle_incoming_packet(self,data,addr):
        # taskID = "none"
        # sendMessage = SendMessageClass(self.transport)

        # if(data.decode().isdigit()):
        #    taskID = int(data.decode())
        # print("Received:", data.decode())
        # if taskID == "none":
        #     print("Close the socket")
        #     self.transport.close()
        # elif taskID == 0:
        #     # print("go to next task")
        #     await sendMessage.sendMsg("get task")
        # elif taskID > 0:
        #     print("Wait for 5 sec")
        #     await asyncio.sleep(5)
        #     await sendMessage.sendMsg("get task")
        await self.handling_buffer(data,addr)
    
    async def handling_buffer(self,data,addr):
        taskID = -1
        # data = data.decode()
        self.interfaceOut.setData(data)
        taskID = self.interfaceOut.jobID
        if(self.interfaceIn.stateOfHandshake == 1 and self.interfaceOut.stateOfHandshake == 1 ):
            if taskID == -1:
                print("Close the socket")
                self.transport.close()
            elif taskID == 0:
                print('taskID:', taskID)
                self.interfaceIn.stateOfHandshake = 0
                self.transport.sendto(self.interfaceIn.getData())
                print("go to next task")
            elif taskID > 0:
                print("Wait for 5 sec")
                await asyncio.sleep(5)
                self.interfaceIn.stateOfHandshake = 0
                self.transport.sendto(self.interfaceIn.getData())

        if(self.interfaceIn.stateOfHandshake == 0 and self.interfaceOut.stateOfHandshake == 0):
            self.interfaceIn.stateOfHandshake = 1
            self.transport.sendto(self.interfaceIn.getData())
    
    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Connection closed")
        self.on_con_lost.set_result(True)


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    message = "get task"

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UDPClient(message, on_con_lost),
        remote_addr=('127.0.0.1', 9999))

    try:
        await on_con_lost
    finally:
        transport.close()


asyncio.run(main())