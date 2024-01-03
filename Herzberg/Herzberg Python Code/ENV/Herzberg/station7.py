from machine import Machine,MachineStatus
from grids import GridBatch
from stations import  processQueue,  StationMachine, Tube
from settings import Color,Settings, Station7Positions
from logger import jobslogger,initlogger


class Station7(StationMachine):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.grid:GridBatch        
        self.gridSize=len(Station7Positions)
        self.tubes=[None] * self.gridSize
        self.machine:Machine=Machine("Sysmex XN-550",Settings.haematology_init_time,Settings.haematology_run_time,Settings.haematology_standby_time)
        self.initTubes()
        self.isDoorOpened=False   
        self.maxAdultTubeLocation = 0
        self.maxChildTubeLocation = 0
        self.statusAdult = MachineStatus.Off
        self.statusChild = MachineStatus.Off
        self.counter=0
        self.iterator=0
        self.counter_child=0    
        self.iterator_child=0

    def initTubes(self):        
        for i in range(self.gridSize):
            self.tubes[i]=Tube(i)
    
    async def setTogetherTubesMax(self, maxBoth):
        if maxBoth:
            self.statusAdult = MachineStatus.On
            self.maxAdultTubeLocation = int(self.gridSize / 2)
            self.statusChild = MachineStatus.On
            self.maxChildTubeLocation = self.gridSize
            self.counter_child=self.maxAdultTubeLocation
            self.iterator_child=self.maxAdultTubeLocation
    
    # async def setIndividualTubesMax(self, maxAdult):
    #     if maxAdult:
    #         self.statusAdult = MachineStatus.On
    #         self.maxAdultTubeLocation = self.gridSize
    #         self.statusChild = MachineStatus.Off
    #         self.counter_child=0
    #         self.iterator_child=0
    #     else:
    #         self.statusAdult = MachineStatus.Off
    #         self.statusChild = MachineStatus.On
    #         self.maxChildTubeLocation = self.gridSize
    #         self.maxAdultTubeLocation = 0

    async def resetTubes(self):
        await self.setStatus(MachineStatus.On)
        self.counter=0        
        self.iterator=0
        self.counter_child=self.maxAdultTubeLocation
        self.iterator_child=self.maxAdultTubeLocation
        # if self.statusChild == MachineStatus.Off:
        #     self.counter_child=self.maxAdultTubeLocation 
        # else:
        #     self.counter_child=0
        #     self.iterator_child=0        
        for tube in self.tubes:
            tube.color=Color.NONE

    async def initGrids(self,id, ref_pose_1, ref_pose_2, ref_pose_3, p_rows, p_columns, ref_pose_4, ref_pose_5, ch_rows, ch_columns):
        self.grid=GridBatch(id, ref_pose_1, ref_pose_2, ref_pose_3, p_rows, p_columns, ref_pose_4, ref_pose_5, ch_rows, ch_columns)
        initlogger.info("Station 7: {0} grid  locations:".format(self.name))
        for i in range(self.gridSize):
            location=Station7Positions[i]
            tube=self.tubes[i]
            tube.location=self.grid.get_target_x_y(location[0],location[1])
            initlogger.info("Index,location :{0}:{1}".format(location,tube.location))
        return
    
    # to Place to Station7
    async def updateGridAdult(self, color=Color.RED):
        if self.counter < self.maxAdultTubeLocation:
            self.tubes[self.counter].color=color
            self.counter+=1
            jobslogger.info("{0} tube placed in {1} at index {2} ".format(color.name,self.name,self.counter))
        if self.counter == self.maxAdultTubeLocation and self.counter_child == self.maxChildTubeLocation:
            await self.setMachineFilled()

    async def updateGridChild(self, color=Color.CRED):
        if self.counter_child < self.maxChildTubeLocation:
            self.tubes[self.counter_child].color=color
            self.counter_child+=1
            jobslogger.info("{0} tube placed in {1} at index {2} ".format(color.name,self.name,self.counter_child))
        if self.counter == self.maxAdultTubeLocation and self.counter_child == self.maxChildTubeLocation:
            await self.setMachineFilled()

    async def setMachineFilled(self):
        if self.counter > 0 or self.counter_child > self.maxAdultTubeLocation:
            await self.setStatus(MachineStatus.Filled)
            jobslogger.info("{0} is filled with tubes".format(self.name))
            return True
        return False

    # to Place to Station7 Adult tubes
    async def getNextLocationAdult(self):
        if self.counter < self.maxAdultTubeLocation :
            tube=self.tubes[self.counter]
            return tube.location
        return None
    
    # to Place to Station7 Child tubes
    async def getNextLocationChild(self):
        if self.counter_child < self.maxChildTubeLocation :
            tube=self.tubes[self.counter_child]
            return tube.location
        return None
    
    async def isAvailableAdult(self):
        if self.counter < self.maxAdultTubeLocation and await self.getStatus() == MachineStatus.On and self.statusAdult == MachineStatus.On:
            return True
        return False
    
    async def isAvailableChild(self):
        if self.counter_child < self.maxChildTubeLocation and await self.getStatus() == MachineStatus.On and self.statusChild == MachineStatus.On:
            return True
        return False

    # this station as source
    async def getNextTubeToBin(self):
        if self.iterator < self.counter and self.statusAdult == MachineStatus.On:
            tube=self.tubes[self.iterator]
            self.iterator+=1
            jobslogger.info("{0} tube picked from {1} at index {2} ".format(tube.color.name,self.name,self.iterator))
            return tube
        if self.iterator_child < self.counter_child and self.statusChild == MachineStatus.On:
            tube=self.tubes[self.iterator_child]
            self.iterator_child+=1
            jobslogger.info("{0} tube picked from {1} at index {2} ".format(tube.color.name,self.name,self.iterator_child))
            return tube
        await self.resetTubes()
        return None
    
    async def closeDoors(self):
        if not self.isDoorOpened:
            jobId=self.jobs[4].jobId
            await processQueue.enqueue([jobId,jobId])
            jobslogger.info("{0} doors opened".format(self.name)) 
            self.isDoorOpened=True

    async def refreshStandbyAlarm(self):        
        if self.counter > 0 or self.counter_child > self.maxAdultTubeLocation:
            await self.startMachine()
        else:
            self.isDoorOpened=False
            await super().refreshStandbyAlarm()

    def getRuntime(self,tubeCount:int):       
        runTime:str=""
        match tubeCount:
            case 1:
                runTime= "4:56"
            case 2:
                runTime= "07:00"
            case 3:
                runTime= "07:12"
            case 4:
                runTime= "08:20"
            case 5:
                runTime= "09:30"
            case 6|7:
                runTime= "12:16"
            case 8|9|10:
                runTime= "16:20"
        if tubeCount > 10:
            runTime= "26:40"
        if runTime!="":
            #convert to seconds
            mm, ss = runTime.split(':')
            return int(mm) * 60 + int(ss)     
        return self.machine.runTime

    async def startMachine(self):
        self.setRuntime(self.getRuntime(self.counter + self.counter_child - self.maxAdultTubeLocation))
        if self.isDoorOpened:
            jobId=self.jobs[5].jobId
            await processQueue.enqueue([jobId,jobId])
            self.isDoorOpened=False
        jobId=self.jobs[3].jobId
        await processQueue.enqueue([jobId,jobId])
        jobslogger.info("{0} started".format(self.name)) 
        await self.setStatus(MachineStatus.Running)
        return True 
    
    async def areTubesFilledInMachine(self):
        if self.counter > 0 or self.counter_child > self.maxAdultTubeLocation:
            self.isDoorOpened = True
            return True
        else:
            False

    #to start and stop coagulation machine
    async def getStation7Jobs(self):
        if not self.isInitialized:
            return False
        if await self.getStatus() == MachineStatus.Filled:
            return await self.startMachine()                   
        return False