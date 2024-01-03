from grids_v2 import Grid
from stations import  processQueue, Station, Tube
from logger import jobslogger,initlogger
from settings import Station11Size


class Station11(Station):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.grid:Grid 
        self.counter=0
        self.batchCounter = 0
        self.gridSize=Station11Size
        self.batchCount = 4
        self.batchSize = int(self.gridSize / self.batchCount)
        self.tubes=[None] * self.gridSize    
        self.initTubes()

    def initTubes(self):        
        for i in range(self.gridSize):
            self.tubes[i]=Tube(i)

    async def initGrids_1_2(self, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5, ref_pose_6, rows, columns):
        self.grid1=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
        self.grid2=Grid(ref_pose_4, ref_pose_5, ref_pose_6, rows, columns)
        initlogger.info("Grid locations Station11:{0}".format(self.name))
        for n in range(0*self.batchSize, 2*self.batchSize):
            if n < self.batchSize:
                self.tubes[n].location=self.grid1.get_target_x_y((n%self.batchSize)+1)
            elif (n >= self.batchSize) and (n < (2*self.batchSize)):
                self.tubes[n].location=self.grid2.get_target_x_y((n%self.batchSize)+1)
            initlogger.info("Index,location :{0}:{1}".format(n+1,self.tubes[n].location))

    async def initGrids_3_4(self, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5, ref_pose_6, rows, columns):
        self.grid3=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
        self.grid4=Grid(ref_pose_4, ref_pose_5, ref_pose_6, rows, columns)
        for n in range(2*self.batchSize, self.gridSize):
            if (n >= (2*self.batchSize)) and (n < (3*self.batchSize)):
                self.tubes[n].location=self.grid3.get_target_x_y((n%self.batchSize)+1)
            elif (n >= self.batchSize) and (n < (4*self.batchSize)):
                self.tubes[n].location=self.grid4.get_target_x_y((n%self.batchSize)+1)
            initlogger.info("Index,location :{0}:{1}".format(n+1,self.tubes[n].location))

    async def updateGrid(self,color):
        self.tubes[self.counter].color=color
        self.counter+=1
        jobslogger.info("{0} tube placed in {1} at index {2} ".format(color.name,self.name,self.counter))
        if self.counter == self.gridSize:
            self.counter=0
            jobId=self.jobs[3].jobId 
            await processQueue.enqueue([jobId,jobId])
            processQueue.destLocation.extend([[0,0,0,0,0,0],[0,0,0,0,0,0]])
            jobslogger.info("{0} grid filled. Display popup".format(self.name))

    #this station as target
    async def getNextLocation(self):
        if self.counter < self.gridSize :
            tube=self.tubes[self.counter]
            return tube.location
        return None
    

    