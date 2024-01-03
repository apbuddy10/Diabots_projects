from centrifugeConnector import CentrifugeInterface
from machine import Machine,MachineStatus
from stations import CommonError,StationMachine
from settings import Settings
from logger import initlogger,jobslogger


class Station6(StationMachine):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.machine:Machine=Machine("centrifuge",Settings.centrifuge_run_time)
        self.centrifugeClient=None

    async def isAvailable(self):        
        return await self.getStatus() == MachineStatus.On
    
    async def resetConnections(self):
        if self.centrifugeClient:
            self.centrifugeClient.closeConnection()
        
    async def initCentrifuge(self):
        if await self.getStatus()== MachineStatus.On:
            self.centrifugeClient=CentrifugeInterface()            
            if self.centrifugeClient is None:
                raise CommonError('Not able to connect to centrifuge')
            await self.checkLock()
            runtime=await self.centrifugeClient.getRunTime()   
            self.setRuntime(runtime + Settings.centrifuge_run_time_buffer)
            self.isInitialized=True
            initlogger.info("{0} is initialized".format(self.name))        

    async def checkLock(self):
        counter=0
        while counter <3:
            isSuccess=await self.centrifugeClient.check_lock()
            if isSuccess:
                jobslogger.info("Check lock success for {0}".format(self.name))
                return True
            counter+=1
        raise CommonError("check lock operation failed")
    
    async def setRotorPosition(self,position):
        counter=0
        while counter <3:
            isSuccess=await self.centrifugeClient.set_rotor_position(position)
            if isSuccess:
                jobslogger.info("Rotor position set to  {0}".format(position))
                return True
            counter+=1
        raise CommonError("set rotor position operation failed")
    
    async def hatchOpen(self):
        counter=0
        while counter <3:
            isSuccess=await self.centrifugeClient.hatch_open()
            if isSuccess:
                jobslogger.info("Hatch opened for {0}".format(self.name))
                return True
            counter+=1
        raise CommonError("hatch open operation failed")
    
    async def hatchClose(self):
        counter=0
        while counter <3:
            isSuccess=await self.centrifugeClient.hatch_close()
            if isSuccess:
                jobslogger.info("Hatch closed for {0}".format(self.name))
                return True
            counter+=1
        raise CommonError("hatch close operation failed")
    
    async def startCentrifuge(self):
        counter=0
        while counter <3:
            isSuccess=await self.centrifugeClient.start_centrifuge()
            if isSuccess:
                jobslogger.info("{0} machine started".format(self.name))
                return True
            counter+=1
        raise CommonError("hatch close operation failed")

    async def isCompleted(self):        
        return await self.getStatus() == MachineStatus.Completed
    
    async def machineStatusCompleted(self):        
        await self.setStatus(MachineStatus.Completed)
        jobslogger.info("skipped standby timer and skype message for {0}".format(self.name))
