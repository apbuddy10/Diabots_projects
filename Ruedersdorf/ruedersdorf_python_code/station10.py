from grids_v2 import Grid
from logger import initlogger, jobslogger
from settings import Color, Settings, dummyLocation, Station10Size
from stations import Station, Tube, processQueue


class Station10(Station):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.grid:Grid 
        self.counter=0
        self.gridSize= Station10Size
        self.tubes=[None] * self.gridSize
        self.initTubes()

    def initTubes(self):        
        for i in range(self.gridSize):
            self.tubes[i]=Tube(i)

    async def initGrids(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        self.grid=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)        
        initlogger.info("Grid locations Station10:{0}".format(self.name))
        for tube in self.tubes:
            tube.location=self.grid.get_target_x_y(self.tubes.index(tube)+1)
            initlogger.info("Index,location :{0}:{1}".format(self.tubes.index(tube)+1,tube.location))   

    async def updateGrid(self,type):
        self.tubes[self.counter].type=type
        self.counter+=1
        jobslogger.info("{0} tube placed in {1} at index {2} ".format(type.name,self.name,self.counter))
        
    async def isFehlerFilled(self):
        if self.counter == self.gridSize:
            jobslogger.info("{0} grid filled. Display reset popup".format(self.name))
            return True
        return False
    
    async def getFehlerFilledJob(self):
        jobId=self.jobs[3].jobId 
        await processQueue.enqueue([jobId,jobId])
        processQueue.destLocation.extend(dummyLocation)
    
    async def resetFehler(self, reset):
        if reset:
            self.counter=0

    #this station as target
    async def getNextLocation(self):
        if self.counter < self.gridSize :
            tube=self.tubes[self.counter]
            return tube.location
        return None
    