from logger import initlogger,jobslogger
from grids_v2 import  Grid
from stations import Station, Tube
from settings import BatchStatus, Color, Station9Positions


class Stn9Batch:
    def __init__(self,batchSize):
        self.batchSize=batchSize
        self.tubes=[None] * self.batchSize
        self.status=BatchStatus.Empty 
        self.counter=0
        self.location=None
        self.iterator=0
        self.initTubes()

    def setLocation(self,location):
        self.location=location
    
    async def resetBatch(self):
        self.status = BatchStatus.Empty
        self.counter=0
        self.iterator=0
        for tube in self.tubes:
            tube.color=Color.NONE

    def initTubes(self):        
        for i in range(self.batchSize):
            self.tubes[i]=Tube(i)

    async def isAvailable(self):
        if self.counter < self.batchSize:
            return True
        return False

    async def getNextLocation(self):
        if self.counter < self.batchSize:
            tube=self.tubes[self.counter]
            return tube.location
        return None

    async def updateGridTube(self,color):        
        self.tubes[self.counter].color = color
        self.counter+=1
        jobslogger.info("{0} tube placed at index {1} ".format(color.name,self.counter))

    # need to be called when there are no tubes left in station1
    async def fillBatch(self):
        if self.status== BatchStatus.Empty and self.counter > 0:
            self.status = BatchStatus.Filled
            return True        
        return False

    # need to be called when there are no tubes left in grid
    async def emptyBatch(self):
        if self.status== BatchStatus.Process_Completed and self.counter == self.iterator:
            await self.resetBatch()
            return True
        return False

    # to move to Archive
    async def getNextTube(self):
        if self.status == BatchStatus.Process_Completed: 
            for i in range(self.iterator,self.counter):
                self.iterator+=1
                if(self.tubes[i].color==Color.RED):                    
                    jobslogger.info("{0} tube picked from index {1} ".format(self.tubes[i].color.name,self.iterator))                  
                    return self.tubes[i]
        return None 


class Station9(Station):
    def __init__(self,name,jobs,batchCount=2): 
        super().__init__(name,jobs)
        self.grid:Grid
        self.Iterator=0
        self.gridSize=len(Station9Positions)
        self.tubes=[None] * self.gridSize        
        self.batchSize=int(len(Station9Positions)/2)
        self.batch1=Stn9Batch(self.batchSize)
        self.batch2=Stn9Batch(self.batchSize)
        self.batchCount=batchCount             
        self.batches=[]
        self.initBatches()
        self.initTubes()
        self.batchCounter=0
        self.batchIterator=0

    def initBatches(self):        
        for i in range(self.batchCount):
            batch=Stn9Batch(self.batchSize)
            self.batches.append(batch)

    def initTubes(self):        
        for i in range(self.batchSize):
            for j in range(self.batchCount):
                batch=self.batches[j]
                batch.initTubes()

    async def initGrids(self, ref_rack_1, ref_pose_1, ref_pose_2, ref_rack_2, ref_pose_3, ref_pose_4):    
        self.gridBatch1=Grid(ref_pose_1, ref_pose_1, ref_pose_2, 10, 1)
        self.gridBatch2=Grid(ref_pose_3, ref_pose_3, ref_pose_4, 10, 1)
        for j in range(self.batchCount):
            cnt=0
            initlogger.info("Station 9: {0} grid  batch {1} locations:".format(self.name,j+1))
            for i in range(j*self.batches[j].batchSize, (j+1)*self.batches[j].batchSize):
                location=Station9Positions[i]
                tube=self.batches[j].tubes[cnt]
                if j==0:
                    tube.location=self.gridBatch1.get_target_x_y(location[1])
                elif j==1:
                    tube.location=self.gridBatch2.get_target_x_y(location[1])
                initlogger.info("Index,location :{0}:{1}".format(location,tube.location))
                cnt+=1
            if j==0:
                rackLocation=ref_rack_1
            elif j==1:
                rackLocation=ref_rack_2
            initlogger.info("Batch rack Index,location :{0}:{1}".format(j+1,rackLocation))
            self.batches[j].setLocation(rackLocation)

    #this station as target
    async def updateGrid(self,color):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Empty: 
            jobslogger.info("{0} batch {1} filling".format(self.name,self.batchCounter+1))           
            await batch.updateGridTube(color)

    #this station as target
    async def getNextLocation(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Empty: 
            return await batch.getNextLocation()
        return None  
    
    async def isAvailable(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Empty: 
            return await batch.isAvailable()
        return False

    async def getLocationOfFilledJob(self):
        for batch in self.batches:
            if batch.status == BatchStatus.Filled:
                batch.status=BatchStatus.Process_Running 
                return batch.location
        return None

    async def getLocationOfRunningJob(self):
        for batch in self.batches:
            if batch.status == BatchStatus.Process_Running:
                batch.status=BatchStatus.Process_Completed 
                return batch.location
        return None
    
    # get the tubes count of the batch to start machine
    async def getFilledBatchCount(self):
        for batch in self.batches:
            if batch.status == BatchStatus.Process_Running:
                return batch.counter
        return self.batchSize
    
    # to move to Archive
    async def getNextTubeToArchiv(self):
        batch=self.batches[self.batchIterator]
        tube=await batch.getNextTube()
        return tube

    async def currentBatchEmpty(self):
        batch=self.batches[self.batchIterator]
        if await batch.emptyBatch():
            jobslogger.info("{0} batch {1} made empty".format(self.name,self.batchCounter+1)) 
            self.batchIterator = (self.batchIterator + 1) % self.batchCount
            return True
        return False
    
    # need to be called when there is no tube to pick from previous station
    async def currentBatchFilled(self):
        batch=self.batches[self.batchCounter]
        if await batch.fillBatch():
            jobslogger.info("{0} batch {1} filled".format(self.name,self.batchCounter+1)) 
            self.batchCounter= (self.batchCounter + 1) % 2
            return True
        return False
    
