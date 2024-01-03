from logger import initlogger,jobslogger
from grids_v2 import Grid
from stations import Station, Tube
from settings import BatchStatus, Color, TubeType, Station9Positions


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
        if self.status == BatchStatus.Process_Completed and self.counter == self.iterator:
            await self.resetBatch()
            return True
        return False

    # to move to Archive
    async def getNextTube(self):
        if self.status == BatchStatus.Process_Completed: 
            for i in range(self.iterator,self.counter):
                self.iterator+=1
                if(self.tubes[i].color==Color.RED or self.tubes[i].color==Color.CRED):                    
                    jobslogger.info("{0} tube picked from index {1} ".format(self.tubes[i].color.name,self.iterator))                  
                    return self.tubes[i]
        return None 


class Station9(Station):
    def __init__(self,name,jobs,batchCount=4): 
        super().__init__(name,jobs)
        self.grid:Grid
        self.Iterator=0
        self.gridSize=len(Station9Positions)
        self.tubes=[None] * self.gridSize        
        self.batchSize=int(len(Station9Positions)/batchCount)
        self.batchCount=batchCount             
        self.batches=[]        
        self.batchCounterAdult=0
        self.batchIteratorAdult=0
        self.batchCounterChild=0
        self.batchIteratorChild=0
        self.batchesAdult = [0,1]
        self.batchesChild = [2,3]
        self.batchesFilled = []
        self.batchesCompleted = []
        self.initBatches()
        self.initTubes()

    def initBatches(self):        
        for i in range(self.batchCount):
            batch=Stn9Batch(self.batchSize)
            self.batches.append(batch)

    def initTubes(self):        
        for i in range(self.batchSize):
            for j in range(self.batchCount):
                batch=self.batches[j]
                batch.initTubes()

    async def initGrids(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):    
        self.grid=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
        for j in range(self.batchCount):
            cnt=0
            initlogger.info("Station 9: {0} grid  batch {1} locations:".format(self.name,j+1))
            for i in range(j*self.batches[j].batchSize, (j+1)*self.batches[j].batchSize):
                location=Station9Positions[i]
                tube=self.batches[j].tubes[cnt]
                tube.location=self.grid.get_target_x_y(location[1])
                initlogger.info("Index,location :{0}:{1}".format(location,tube.location))
                cnt+=1

    async def initRackGrid(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):    
        self.grid=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
        for j in range(self.batchCount):            
            rackLocation=self.grid.get_target_x_y(j+1)            
            self.batches[j].setLocation(rackLocation)
            initlogger.info("Batch rack Index,location :{0}:{1}".format(j+1,rackLocation))

    #this station as target
    async def updateGrid(self,color):
        if color == Color.RED:
            batchNum=self.batchesAdult[self.batchCounterAdult]
        elif color == Color.CRED:
            batchNum=self.batchesChild[self.batchCounterChild]
        batch=self.batches[batchNum]
        if batch.status == BatchStatus.Empty: 
            jobslogger.info("{0} batch {1} filling".format(self.name,batchNum+1))           
            await batch.updateGridTube(color)

    #this station as target
    async def getNextLocation(self, tubeType):
        if tubeType == TubeType.ADULT:
            batchNum=self.batchesAdult[self.batchCounterAdult]
        elif tubeType == TubeType.CHILD:
            batchNum=self.batchesChild[self.batchCounterChild]
        batch=self.batches[batchNum]
        if batch.status == BatchStatus.Empty: 
            return await batch.getNextLocation()
        return None  

    async def isAvailable(self, tubeType):
        if tubeType == TubeType.ADULT:
            batchNum=self.batchesAdult[self.batchCounterAdult]
        elif tubeType == TubeType.CHILD:
            batchNum=self.batchesChild[self.batchCounterChild]
        batch=self.batches[batchNum]
        if batch.status == BatchStatus.Empty: 
            return await batch.isAvailable()
        return False

    async def getLocationOfFilledJob(self):
        if len(self.batchesFilled) != 0:
            for batchNum in self.batchesFilled:
                batch = self.batches[batchNum]
                if batch.status == BatchStatus.Filled:
                    batch.status=BatchStatus.Process_Running 
                    return batch.location
        return None

    async def getLocationOfRunningJob(self):
        if len(self.batchesFilled) != 0:
            for batchNum in self.batchesFilled:
                batch = self.batches[batchNum]
                if batch.status == BatchStatus.Process_Running:
                    batch.status=BatchStatus.Process_Completed 
                    return batch.location
        return None
    
    # get the tubes count of the batch to start machine
    async def getFilledBatchCount(self):
        if len(self.batchesFilled) != 0:
            for batchNum in self.batchesFilled:
                batch = self.batches[batchNum]
                if batch.status == BatchStatus.Process_Running:
                    return batch.counter
        return self.batchSize
    
    # to move to Archive
    async def getNextTubeToArchiv(self):
        batchNum=self.batchesAdult[self.batchIteratorAdult]
        batch = self.batches[batchNum]
        tube=await batch.getNextTube()
        if tube is None:
            batchNum=self.batchesChild[self.batchIteratorChild]
            batch = self.batches[batchNum]
            tube=await batch.getNextTube()
        return tube
    
    async def moveBatchFromFilledToCompleted(self):
        # jobslogger.info("{0} Completed batches before append {1}".format(self.name, self.batchesCompleted)) 
        self.batchesCompleted.append(self.batchesFilled[0])
        # jobslogger.info("{0} Completed batches after append {1}".format(self.name, self.batchesCompleted))
        # jobslogger.info("{0} filled batches before pop {1}".format(self.name, self.batchesFilled)) 
        self.batchesFilled.pop(0)
        # jobslogger.info("{0} filled batches after pop {1}".format(self.name, self.batchesFilled)) 


    async def currentBatchEmpty(self):
        batchNum=self.batchesAdult[self.batchIteratorAdult]
        batch = self.batches[batchNum]
        emptyBatch = await batch.emptyBatch()
        if emptyBatch:   
            # jobslogger.info("{0} Completed batches before pop {1}".format(self.name, self.batchesCompleted)) 
            self.batchesCompleted.pop(0)
            # jobslogger.info("{0} Completed batches after pop {1}".format(self.name, self.batchesCompleted))          
            jobslogger.info("{0} Adult batch {1} made empty".format(self.name, batchNum+1)) 
            self.batchIteratorAdult = (self.batchIteratorAdult + 1) % 2
            return True
        else:       
            batchNum=self.batchesChild[self.batchIteratorChild]
            batch = self.batches[batchNum]
            if await batch.emptyBatch():
                # jobslogger.info("{0} Completed batches before pop {1}".format(self.name, self.batchesCompleted)) 
                self.batchesCompleted.pop(0)
                # jobslogger.info("{0} Completed batches after pop {1}".format(self.name, self.batchesCompleted))
                jobslogger.info("{0} Child batch {1} made empty".format(self.name,batchNum+1)) 
                self.batchIteratorChild = (self.batchIteratorChild + 1) % 2
                return True      
        return False
    
    # need to be called when there is no tube to pick from previous station
    async def currentBatchFilled(self):
        batchNum=self.batchesAdult[self.batchCounterAdult]
        batch = self.batches[batchNum]
        fillBatch = await batch.fillBatch()
        if fillBatch:
            #jobslogger.info("{0} filled batches before append {1}".format(self.name, self.batchesFilled)) 
            self.batchesFilled.append(batchNum)
            #jobslogger.info("{0} filled batches after append {1}".format(self.name, self.batchesFilled))            
            jobslogger.info("{0} Adult batch {1} filled with {2} tubes".format(self.name,batchNum+1,batch.counter)) 
            self.batchCounterAdult = (self.batchCounterAdult + 1) % 2
            return True
        else:            
            batchNum=self.batchesChild[self.batchCounterChild]
            batch = self.batches[batchNum]
            if await batch.fillBatch():
                #jobslogger.info("{0} filled batches before append {1}".format(self.name, self.batchesFilled)) 
                self.batchesFilled.append(batchNum)
                #jobslogger.info("{0} filled batches after append {1}".format(self.name, self.batchesFilled))  
                jobslogger.info("{0} Child batch {1} filled with {2} tubes".format(self.name,batchNum+1,batch.counter)) 
                self.batchCounterChild = (self.batchCounterChild + 1) % 2
                return True        
        return False
    
