
from ast import List

from logger import initlogger
from machine import Machine, MachineStatus
from settings import Color, FridgeRackType, TubeType


class Job:
    def __init__(self,jobId,jobName):
        self.jobId=jobId
        self.jobName=jobName
        
class Tube:
    def __init__(self,index=None,location=None,color=None,barcode=None,level=None):
        self.index=index
        self.color=color
        self.barcode=barcode
        self.level=level 
        self.location=location  
        self.type=TubeType.NONE

    async def setTube(self,color,barcode,level):
        self.color=color
        self.barcode=barcode
        self.level=level

    async def assignTogrid(self,gridId,position):
        self.gridId=gridId
        self.position=position

class Rack:
    def __init__(self,index=None,location=None,status=None):
        self.index=index
        self.location=location  
        self.status=status

    async def assignTogrid(self,gridId,position):
        self.gridId=gridId
        self.position=position
        
class Station:    
    def __init__(self,name,jobs):
        self.name = name
        self.jobs:list[Job]=jobs   

class StationMachine(Station):    
    def __init__(self,name,jobs):
        super().__init__(name,jobs)
        self.machine:Machine=None
        self.isInitialized=False
    
    def setRuntime(self,time:int):
        self.machine.runTime=time

    async def setStatus(self, status:MachineStatus):
        await self.machine.setStatus(status)
            
    async def getStatus(self):
        return self.machine.status
    
    # async def startInitTimer(self):
    #     if await self.getStatus() != MachineStatus.Off:
    #         self.isInitialized=False
    #         await self.machine.setInitAlarm(self.startStandbyTimer)

    # async def startStandbyTimer(self):
    #     self.isInitialized=True
    #     self.machine.standbyTimer.cancel_alarm()
    #     await self.machine.setStandbyAlarm(self.refreshStandbyAlarm)
        
    # async def refreshStandbyAlarm(self):
    #     timerlogger.info("{0} Standby timer refresh. Time : {1}".format(self.name,self.machine.standbyTime))
    #     if await self.getStatus() != MachineStatus.Off:
    #         jobid=self.jobs[0].jobId
    #         await processQueue.enqueue([jobid,jobid],True)

    async def startRuntimeAlarm(self):
            # self.machine.standbyTimer.cancel_alarm()
            # timerlogger.info("{0} Standby timer canceled".format(self.name))            
            await self.machine.setRuntimeAlarm(self.machineStatusCompleted)

    async def machineStatusCompleted(self):        
        await self.setStatus(MachineStatus.Completed)
        # await self.startStandbyTimer()
        # await commManager.sendMessage("{0} wird entladen.".format(self.name))
    
    async def prepareInitJobWithStatus(self,isOn):
        await self.setStatus(MachineStatus.On if isOn else MachineStatus.Off)
        # if isOn:
        #     jobId=self.jobs[0].jobId
        #     await processQueue.enqueue([jobId,jobId])
    
    async def cancelTimers(self):
        await self.machine.cancelTimers()
 
class ProcessQueue:
    def __init__(self):
        self.jobs=[]
        self.pingJobs=[]
        self.destLocation=[]
        self.stn5GridLocations=[]

    async def enqueue(self,item,isPingJob=False,index=0,):
        if not isPingJob:
            if index > 0:
                self.jobs.insert(index,item)
            else:
                self.jobs.append(item)
        else:
            if index > 0:
                self.pingJobs.insert(index,item)
            else:
                self.pingJobs.append(item)

    async def dequeue(self,index=0):
        if len(self.pingJobs) > 0:
            return self.pingJobs.pop(index)
        if len(self.jobs) > 0:
            return self.jobs.pop(index)
        else:
            return None
            
    async def isEmpty(self):
        return len(self.pingJobs) == 0 and len(self.jobs) == 0

    def reset(self):
        self.jobs=[]
        self.pingJobs=[]
        self.destLocation=[]
        self.stn5GridLocations=[]

processQueue:ProcessQueue=ProcessQueue()
  
class CommonError(Exception):
    def __init__(self, message="Error occured"):
        super().__init__(message)

class Stn4ColorError(Exception):
    def __init__(self, message="Error occured"):
        super().__init__(message)

class Fridge:
    def __init__(self,size:int,fridgeNo:int):
        self.counter=0
        self.iterator=0
        self.location=None
        self.size=size
        self.tubes:List[Tube]=[Tube] * self.size
        self.isDoorOpened=False
        self.fridgeNo=fridgeNo

    def initTubes(self):        
        for i in range(self.size):
            self.tubes[i]=Tube(i)
        for tube in self.tubes:
            tube.location=[self.tubes.index(tube)+1,0,0,0,0,0]
            initlogger.info("Index,location :{0}:{1}".format(self.tubes.index(tube)+1,tube.location))

    def resetTubes(self):
        self.counter=0
        self.iterator=0
        for tube in self.tubes:
            tube.color=Color.NONE