from settings import Settings
from machine import Machine, MachineStatus
from stations import StationMachine
from logger import jobslogger


class Station7(StationMachine):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.machine:Machine=Machine("Sysmex ",Settings.haematology_run_time) 
        self.status:MachineStatus=MachineStatus.Off
        self.gridLocation:int=1
    
    async def setDestLocation(self,location):
        self.gridLocation=location
     
    def getRuntime(self,tubeCount:int):       
        runTime:str=""
        match tubeCount:
            case 1:
                runTime= "04:56"
            case 2:
                runTime= "06:06"
            case 3:
                runTime= "07:12"
            case 4:
                runTime= "08:20"
            case 5:
                runTime= "09:30"
            case 6|7:
                runTime= "12:16"
            case 8|9|10:
                runTime= "16:00"
        if tubeCount > 10:
            runTime= "26:40"
        # runTime= "2:00"
        if runTime!="":
            #convert to seconds
            mm, ss = runTime.split(':')
            return int(mm) * 60 + int(ss)     
        return self.machine.runTime
    
    async def startMachine(self,tubeCount:int):
        self.setRuntime(self.getRuntime(tubeCount))
        jobslogger.info("{0} machine started".format(self.name)) 
        await self.setStatus(MachineStatus.Running)
        return True
    
    async def isAvailable(self):
        return await self.getStatus() == MachineStatus.On