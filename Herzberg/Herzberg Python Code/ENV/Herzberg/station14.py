from grids import Grid
from stations import  processQueue,Station, Tube
from settings import BatchStatus, HolderStatus, Station14Positions
from logger import jobslogger,initlogger


class Station14(Station):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.grid:Grid 
        self.counter=0
        self.gridSize=int(len(Station14Positions))
        self.holderStatus=HolderStatus.Empty 
        self.tubesStatus=BatchStatus.Empty
        self.tubes=[None] * self.gridSize
        self.initTubes()

    def initTubes(self):        
        for i in range(self.gridSize):
            self.tubes[i]=Tube(i)

    async def initGrids(self,id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        self.grid=Grid(id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)        
        initlogger.info("Grid locations Station14:{0}".format(self.name))
        for tube in self.tubes:
            tube.location=self.grid.get_target_x_y(self.tubes.index(tube)+1)
            initlogger.info("Index,location :{0}:{1}".format(self.tubes.index(tube)+1,tube.location))   

    async def updateGrid(self,color):
        self.tubes[self.counter].color=color
        self.counter+=1
        jobslogger.info("{0} tube placed in {1} at index {2} ".format(color.name,self.name,self.counter))
        if self.counter == self.gridSize:
            await self.fillTubesGrid()
    
    async def placeRackInMachine(self):
        if self.holderStatus == HolderStatus.Filled and self.tubesStatus == BatchStatus.Filled:
            jobId=self.jobs[1].jobId # Job(141,"pick rack")
            await processQueue.enqueue([jobId,jobId])
            await self.resetTubesGrid()
            await self.emptyHolder()
            jobslogger.info("{0}, Resetting the number of tubes in grid, as it is filled with {1} tubes".format(self.name, self.gridSize))
            jobslogger.info("Placed the rack in cobas pure machine from holder")
            return True
        return False

    async def getNextLocation(self):
        if self.counter < self.gridSize and self.holderStatus == HolderStatus.Filled:
            tube=self.tubes[self.counter]
            return tube.location
        return None
    
    async def resetTubesGrid(self):
        self.counter = 0
        self.tubesStatus = BatchStatus.Empty

    async def fillTubesGrid(self):
        if self.counter > 0:
            self.tubesStatus = BatchStatus.Filled
            return True
        return False

    async def getTubesStatus(self):
        return self.tubesStatus

    async def emptyHolder(self):
        self.holderStatus = HolderStatus.Empty

    async def isHolderEmpty(self):
        if self.holderStatus == HolderStatus.Empty:
            return True
        return False
    
    async def fillHolder(self):
        if self.holderStatus == HolderStatus.Empty:
            self.holderStatus = HolderStatus.Filled

    async def getHolderStatus(self):
        return self.holderStatus
    
    async def isAvailable(self):
        if self.counter <= self.gridSize:
            return True
        return False
    

    