from grids import Grid
from stations import  processQueue,Station, Tube
from settings import Color
from logger import jobslogger,initlogger


class Station15(Station):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.grid:Grid 
        self.counter=0
        self.iterator=0
        self.gridSize=32
        self.tubes=[None] * self.gridSize
        self.initTubes()

    def initTubes(self):        
        for i in range(self.gridSize):
            self.tubes[i]=Tube(i)

    async def initGrids(self,id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        self.grid=Grid(id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)        
        initlogger.info("Grid locations Station15:{0}".format(self.name))
        for tube in self.tubes:
            tube.location=self.grid.get_target_x_y(self.tubes.index(tube)+1)
            initlogger.info("Index,location :{0}:{1}".format(self.tubes.index(tube)+1,tube.location))  

    async def resetTubes(self):
        self.iterator=0
        self.counter=0
        for tube in self.tubes:
            tube.color=Color.NONE  

    async def updateGrid(self,color):
        self.tubes[self.counter].color=color
        self.counter+=1
        jobslogger.info("{0} tube placed in {1} at index {2} ".format(color.name,self.name,self.counter))
        if self.counter == self.gridSize:
            self.counter=0
            jobId=self.jobs[3].jobId 
            await processQueue.enqueue([jobId,jobId])
            jobslogger.info("{0} grid filled. Display popup".format(self.name))

    # this station as destination
    async def getNextEmptyLocation(self):
        if self.counter < self.gridSize :
            tube=self.tubes[self.counter]
            return tube.location
        return None
    
    # this station as source
    async def getNextFilledTube(self):
        if self.iterator < self.counter:
            tube=self.tubes[self.iterator]
            # self.iterator+=1
            # jobslogger.info("{0} tube picked from {1} at index {2} ".format(tube.color.name,self.name,self.iterator))
            # await self.currentBatchEmpty()
            return tube
        return None

    # this station as source
    async def updateFilledTube(self, tube):
        self.iterator+=1
        jobslogger.info("{0} tube picked from {1} at index {2} ".format(tube.color.name,self.name,self.iterator))
        await self.currentBatchEmpty()
        return None
    
    async def isAvailable(self):
        if self.counter < self.gridSize:
            return True
        return False 
    
    async def currentBatchEmpty(self):
        if self.iterator == self.counter:
            jobslogger.info("{0} made empty".format(self.name)) 
            await self.resetTubes()
            return True
        return False
    