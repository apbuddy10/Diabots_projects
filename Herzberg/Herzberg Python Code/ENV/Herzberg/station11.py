from grids import Grid
from stations import  processQueue, Station, Tube
from settings import Color
from logger import jobslogger,initlogger


class Station11(Station):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.grid:Grid 
        self.counter=0
        self.batchCounter = 0
        self.gridSize=128
        self.batchCount = 4
        self.batchSize = int(self.gridSize / self.batchCount)
        self.tubes=[None] * self.gridSize    
        self.initTubes()

    def initTubes(self):        
        for i in range(self.gridSize):
            self.tubes[i]=Tube(i)

    async def initGrids(self,id, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5, ref_pose_6, ref_pose_7, ref_pose_8, ref_pose_9, ref_pose_10, ref_pose_11, ref_pose_12, rows, columns):
        self.grid1=Grid(id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
        self.grid2=Grid(id, ref_pose_4, ref_pose_5, ref_pose_6, rows, columns)
        self.grid3=Grid(id, ref_pose_7, ref_pose_8, ref_pose_9, rows, columns)
        self.grid4=Grid(id, ref_pose_10, ref_pose_11, ref_pose_12, rows, columns)
        initlogger.info("Grid locations Station11:{0}".format(self.name))
        for n, tube in enumerate(self.tubes):
            if n < self.batchSize:
                tube.location=self.grid1.get_target_x_y((n%self.batchSize)+1)
            elif (n >= self.batchSize) and (n < (2*self.batchSize)):
                tube.location=self.grid2.get_target_x_y((n%self.batchSize)+1)
            elif (n >= (2*self.batchSize)) and (n < (3*self.batchSize)):
                tube.location=self.grid3.get_target_x_y((n%self.batchSize)+1)
            elif (n >= (3*self.batchSize)) and (n < self.gridSize):
                tube.location=self.grid4.get_target_x_y((n%self.batchSize)+1)
            initlogger.info("Index,location :{0}:{1}".format(self.tubes.index(tube)+1,tube.location))   

    async def updateGrid(self,color):
        self.tubes[self.counter].color=color
        self.counter+=1
        jobslogger.info("{0} tube placed in {1} at index {2} ".format(color.name,self.name,self.counter))
        if self.counter == self.gridSize:
            self.counter=0
            jobId=self.jobs[3].jobId 
            await processQueue.enqueue([jobId,jobId])
            jobslogger.info("{0} grid filled. Display popup".format(self.name))

    #this station as target
    async def getNextLocation(self):
        if self.counter < self.gridSize :
            tube=self.tubes[self.counter]
            return tube.location
        return None
    

    