from logger import initlogger,jobslogger,timerlogger
from machine import Machine, MachineStatus
from grids import  GridCoagulation
from stations import processQueue, StationMachine, Tube
from settings import Color, Settings, Station3Positions


class Station3(StationMachine):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.grid:GridCoagulation
        self.counter:int=0
        self.gridSize:int=len(Station3Positions)
        self.tubes:list[Tube]=[None] * self.gridSize
        self.machine:Machine=Machine("ACL elite PRO",Settings.coagulation_init_time,Settings.coagulation_run_time,Settings.coagulation_standby_time)
        self.initTubes()
        self.iterator:int=0

    def initTubes(self):        
        for i in range(self.gridSize):
            self.tubes[i]=Tube(i)

    async def initGrids(self,id, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5,ref_pose_6, ref_pose_7, ref_pose_8):
        self.grid=GridCoagulation(id, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5,ref_pose_6, ref_pose_7, ref_pose_8)
        initlogger.info("Station 3 grid locations:")
        for i in range(self.gridSize):
            location=Station3Positions[i]
            tube=self.tubes[i]
            tube.location=self.grid.get_pose_circle(location)
            initlogger.info("Index,location :{0}:{1}".format(location,tube.location))

    async def resetTubes(self):
        await self.setStatus(MachineStatus.On)
        self.iterator=0
        self.counter=0
        for tube in self.tubes:
            tube.color=Color.NONE        

    #this station as target
    async def updateGrid(self,color):
        self.tubes[self.counter].color=color
        self.counter+=1
        jobslogger.info("{0} tube placed in {1} at index {2} ".format(color.name,self.name,self.counter))
        if self.counter == self.gridSize:
            await self.setMachineFilled()

    async def setMachineFilled(self):
        if self.counter > 0:
            await self.setStatus(MachineStatus.Filled)
            jobslogger.info("{0} machine is filled with tubes".format(self.name)) 
            return True
        return False

    #this station as target
    async def getNextLocation(self):
        if self.counter < self.gridSize :
            tube=self.tubes[self.counter]
            return tube.location
        return None

    #this station as target
    async def getAngle(self):
        return self.grid.get_angle(Station3Positions[self.counter-1])
    
    async def isAvailable(self):
        if self.counter < self.gridSize and await self.getStatus() == MachineStatus.On:
            return True
        return False    
        
    async def isFirstTube(self):
        return self.counter == 0

    #this station as source
    async def getNextTube(self):
        if self.iterator < self.counter :
            # if self.iterator==0:
            #     jobId=self.jobs[4].jobId
            #     await processQueue.enqueue([jobId,jobId])
            #     jobslogger.info("{0} machine pop up closed".format(self.name)) 
            tube=self.tubes[self.iterator]
            self.iterator+=1
            jobslogger.info("{0} tube picked from {1} at index {2} ".format(tube.color.name,self.name,self.iterator))                           
            return tube       
        return None
    
    async def close_check_popup(self):
        if self.iterator == self.counter:
            jobId=self.jobs[4].jobId
            await processQueue.enqueue([jobId,jobId])
            jobslogger.info("{0} machine check pop up closed".format(self.name)) 

    async def currentBatchEmpty(self):
        if self.machine.status == MachineStatus.Completed and self.iterator == self.counter:
            jobslogger.info("{0} made empty".format(self.name)) 
            await self.resetTubes()
            return True
        return False

    async def refreshStandbyAlarm(self):
        timerlogger.info("{0} Standby timer refresh. Time : {1}".format(self.name,self.machine.standbyTime))
        if await self.getStatus() != MachineStatus.Off:
            jobid=self.jobs[5].jobId
            await processQueue.enqueue([jobid,jobid],True)

    def getRuntime(self,tubeCount:int):       
        runTime:str=""
        match tubeCount:
            case 1:
                runTime= "5:00"
            case 2|3:
                runTime= "9:00"
            case 4|5:
                runTime= "17:00"
            case 6|7:
                runTime= "25:00"
            case 8|9|10:
                runTime= "33:00"
        if tubeCount > 10:
            runTime= "57:00"
        if runTime!="":
            #convert to seconds
            mm, ss = runTime.split(':')
            return int(mm) * 60 + int(ss)     
        return self.machine.runTime

    async def startMachine(self):
        self.setRuntime(self.getRuntime(self.counter))    
        jobId=self.jobs[3].jobId
        await processQueue.enqueue([jobId,jobId])
        jobslogger.info("{0} machine started".format(self.name)) 
        await self.setStatus(MachineStatus.Running)
        return True
    
    #to start and stop couglation machine
    async def getStation3Jobs(self):
        if not self.isInitialized:
            return False
        if await self.getStatus() == MachineStatus.Filled:            
            return await self.startMachine()       
        return False