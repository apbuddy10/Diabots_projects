from datetime import datetime
from aiohttp import web
from aiohttp_xmlrpc import handler
import asyncio

from timer import Timer
from MicroSipCalling import microSipCalling
from fritzLogger import callslogger


systemip="192.168.20.222"
systemport="9097"
fritzCallTime = 30


class MainApp:
    def __init__(self):
        self.lastPingTime=None
        self.fritzCall = True
        self.callTimer = Timer()        
        print("Micro SIP Calling Service is running... at {0} - {1}".format(systemip,systemport)) 

    async def connectToMicroSipCaller(self, mobile_number,sleepBetweenCalls, totalCalling):
        self.lastPingTime = None
        self.myIP = systemip
        try:
            callslogger.info("New Micro SIP Connection Established")
            await microSipCalling.initMicroSipCalling( mobile_number,sleepBetweenCalls, totalCalling)          
        except Exception as e: 
            print(e)

    def activateCalling(self):        
        self.fritzCall = True
        self.callTimer.cancel_alarm()
        callslogger.info("Micro SIP Calling Timer Cancelled")

    async def ping(self):
        try:
            currentTime=datetime.now()
            if self.lastPingTime == None:
                self.lastPingTime = currentTime
            diffTime = currentTime - self.lastPingTime 
            self.lastPingTime = currentTime
            diff = diffTime.total_seconds()*1000
            if diff > 200:                 
                if self.fritzCall:     
                    callslogger.info("ping interrupted for:{0} milli seconds ".format(diff))               
                    # self.fritzCall = False
                    callNum = 0
                    while callNum < microSipCalling.totalCallTimes:
                        callslogger.info("Micro SIP Calling Timer started. Time : {0}".format(microSipCalling.sleepBetweenCalls))
                        await microSipCalling.startCallMicroSipCalling()
                        callNum+=1
                        await asyncio.sleep(microSipCalling.sleepBetweenCalls)  
                        await microSipCalling.endCallMicroSipCalling()
                        callslogger.info("Micro SIP Calling Cancelled")
                    self.lastPingTime = None        
                    # self.fritzCall = True                              
                    # self.callTimer.set_alarm(fritzCallTime, self.activateCalling)
        except Exception as e: 
            print(e)

    async def callFehler(self,sleepBetweenFehler, totalCallingFehler):
        try:
            callNum = 0
            while callNum < totalCallingFehler:
                callslogger.info("Micro SIP Calling Timer started. Time : {0}".format(sleepBetweenFehler))
                await microSipCalling.startCallMicroSipCalling()
                callNum+=1
                await asyncio.sleep(sleepBetweenFehler)  
                await microSipCalling.endCallMicroSipCalling()
                callslogger.info("Micro SIP Calling Timer Cancelled")
        except Exception as e: 
            print(e)
   
mainObj=MainApp()


class XMLRPCHandler(handler.XMLRPCView):
    async def rpc_ping(self):
        return await mainObj.ping()
    async def rpc_connect_to_micro_sip_caller(self,mobile_number, sleepBetweenCalls, totalCalling):
        return await mainObj.connectToMicroSipCaller(mobile_number,sleepBetweenCalls, totalCalling)
    async def rpc_call_fehler(self, sleepBetweenFehler, totalCallingFehler):
        return await mainObj.callFehler(sleepBetweenFehler, totalCallingFehler)
app = web.Application()
app.router.add_route("*", "/", XMLRPCHandler)
web.run_app(app, host=systemip, port=systemport)
    
        