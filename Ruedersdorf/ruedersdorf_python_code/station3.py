from typing import List
from grids_v2 import Grid
from settings import Color, Settings,Station3Size, Station3MachineGridSize, Station3Positions
from machine import Machine, MachineStatus
from stations import Station, StationMachine, Tube, processQueue
from logger import jobslogger,initlogger


class Station3Machine(StationMachine):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.machine:Machine=Machine(name,Settings.coagulation_run_time) 
        self.name = name
        self.grid:Grid
        self.counter:int=0
        self.gridSize:int=Station3Size
        self.tubes:list[Tube]=[None] * self.gridSize
        self.iterator:int=0
        self.initTubes()
        self.rackLoc=None
        self.location=None
    
    def initTubes(self):        
        for i in range(self.gridSize):
            self.tubes[i]=Tube(i)

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
        if self.counter > 0 and await self.getStatus() == MachineStatus.On:
            await self.setStatus(MachineStatus.Filled)
            jobslogger.info("{0} machine is filled with tubes".format(self.name)) 
            return True
        return False

    #this station as target
    async def getNextLocation(self):
        if self.counter < self.gridSize:            
            tube=self.tubes[self.counter]
            return tube.location
        return None
    
    async def isAvailable(self):
        if self.counter < self.gridSize and await self.getStatus() == MachineStatus.On:
            return True
        return False    
        
    async def isFirstTube(self):
        return self.counter == 0

    #this station as source
    async def getNextTubeToArchiv(self):
        if self.iterator < self.counter :
            tube=self.tubes[self.iterator]
            self.iterator+=1
            jobslogger.info("{0} tube picked from {1} at index {2} ".format(tube.color.name,self.name,self.iterator))                  
            return tube       
        return None
    
    async def currentBatchEmpty(self):
        if await self.getStatus() == MachineStatus.ReadyToUnload and self.iterator == self.counter:
            jobslogger.info("{0} made empty".format(self.name)) 
            await self.resetTubes()
            return True
        return False

    def getRuntime(self,tubeCount:int):       
        runTime:str=""
        # match tubeCount:
        #     case 1:
        #         runTime= "04:56"
        #     case 2:
        #         runTime= "06:06"
        #     case 3:
        #         runTime= "07:12"
        #     case 4:
        #         runTime= "08:20"
        runTime= "1:00"
        # runTime= "30:00"
        if runTime!="":
            #convert to seconds
            mm, ss = runTime.split(':')
            return int(mm) * 60 + int(ss)     
        return self.machine.runTime
    
    async def startRunTimeAlarmAgain(self):
        await self.setStatus(MachineStatus.Running)
        self.setRuntime(Settings.extra_run_time)
        await self.startRuntimeAlarm()

    async def startMachine(self):
        if await self.getStatus() == MachineStatus.Filled:
            jobId=self.jobs[3].jobId
            await processQueue.enqueue([jobId,jobId])   
            processQueue.destLocation.extend([self.location,self.location])         
            self.setRuntime(self.getRuntime(self.counter))
            jobslogger.info("Rack placed and {0} machine started".format(self.name)) 
            await self.setStatus(MachineStatus.Running)
            await self.startRuntimeAlarm()
            return True
        return False
    
    async def stopMachine(self):
        if await self.getStatus() == MachineStatus.Completed:
            jobId=self.jobs[4].jobId
            await processQueue.enqueue([jobId,jobId]) 
            processQueue.destLocation.extend([self.location,self.location]) 
            jobslogger.info("{0} machine stopped and tried to remove the rack".format(self.name))
            # await self.setStatus(MachineStatus.ReadyToUnload)
            return True
        return False
    
    async def changeStatus(self, status):
        await self.setStatus(status)


class Station3(Station):
    def __init__(self,name,jobs):
        super().__init__(name,jobs)
        self.machineCount=Station3MachineGridSize             
        self.machines:List[Station3Machine]=[]
        self.initMachines()
        self.batchCounter=0
        self.batchIterator=0
        self.batchRemoveIterator=0
        self.status:MachineStatus=MachineStatus.Off
    
    def initMachines(self):        
        for i in range(self.machineCount):
            machine=Station3Machine(self.name+str(i+1),self.jobs)
            self.machines.append(machine)

    async def initGrids(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):    
        self.grid=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
        for j in range(self.machineCount):
            cnt=0
            initlogger.info("Station 3: {0} grid  machine {1} locations:".format(self.name,j+1))
            for i in range(j*self.machines[j].gridSize, (j+1)*self.machines[j].gridSize):
                location=Station3Positions[i]
                tube=self.machines[j].tubes[cnt]
                tube.location=self.grid.get_target_x_y(location[1])
                initlogger.info("Index,location :{0}:{1}".format(location,tube.location))
                cnt+=1

    async def initMachinesGrid(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        grid=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)        
        initlogger.info("Grid locations Station8 Machine:{0}".format(self.name))
        for machine in self.machines:
            index=self.machines.index(machine)+1
            machine.location=grid.get_target_x_y(index)
            initlogger.info("Index,location :{0}:{1}".format(index,machine.location))
    
    async def isAvailable(self):
        machine=self.machines[self.batchCounter]
        return await machine.isAvailable()
    
    #this station as target
    async def updateGrid(self,color):
        machine=self.machines[self.batchCounter]
        if await machine.getStatus() == MachineStatus.On:
            jobslogger.info("{0} machine {1} filling".format(self.name,self.batchCounter+1))              
            await machine.updateGrid(color)

    #this station as target
    async def getNextLocation(self):
        machine=self.machines[self.batchCounter]
        if await machine.getStatus() == MachineStatus.On:
            return await machine.getNextLocation()
        return None
    
    async def startMachine(self):
        # if not self.isSetOn:
        #     return False
        machine=self.machines[self.batchCounter]
        start = await machine.startMachine()
        if start:
            self.batchCounter = (self.batchCounter + 1) % self.machineCount
        return start
    
    async def stopMachine(self):
        # if not self.isSetOn:
        #     return False
        machine=self.machines[self.batchRemoveIterator]
        stop = await machine.stopMachine()
        # if stop:
        #     self.batchRemoveIterator = (self.batchRemoveIterator + 1) % self.machineCount
        return stop
    
    async def stopMachineSuccess(self, success):
        jobId=0
        machine=self.machines[self.batchRemoveIterator]
        if int(success) == 1:
            await machine.changeStatus(MachineStatus.ReadyToUnload)
            self.batchRemoveIterator = (self.batchRemoveIterator + 1) % self.machineCount
            jobId=self.jobs[3].jobId
        else:
            await machine.startRunTimeAlarmAgain()
        return jobId
    # to move to Archive
    async def getNextTubeToArchiv(self):
        machine=self.machines[self.batchIterator]
        return await machine.getNextTubeToArchiv()
    
    async def currentBatchEmpty(self):
        machine=self.machines[self.batchIterator]
        empty = await machine.currentBatchEmpty()
        if empty:
            await machine.setStatus(MachineStatus.On)
            self.batchIterator = (self.batchIterator + 1) % self.machineCount
        return empty
    
    async def setMachineFilled(self):
        machine=self.machines[self.batchCounter]
        filled = await machine.setMachineFilled()
        return filled
    
    async def getStatusLoad(self):
        machine=self.machines[self.batchCounter]
        return await machine.getStatus()
    
    async def getStatusUnload(self):
        machine=self.machines[self.batchIterator]
        return await machine.getStatus()
    
    async def prepareInitJobWithStatus(self,isOn):
        for machine in self.machines:
            await machine.prepareInitJobWithStatus(isOn)
            
    async def cancelTimers(self):
        for machine in self.machines:
            await machine.cancelTimers()

    async def setStatus(self, status:MachineStatus):
        self.status:MachineStatus=status
            
    async def getStatus(self):
        return self.status