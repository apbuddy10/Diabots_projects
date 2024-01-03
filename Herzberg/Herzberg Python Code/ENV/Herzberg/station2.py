from logger import initlogger,jobslogger
from grids import  GridChemistry
from grids_v2 import Grid
from stations import Station, Rack, processQueue
from settings import BatchStatus, Station2Positions


class Stn2Batch:
    def __init__(self,batchSize):
        self.batchSize=batchSize
        self.racks=[None] * self.batchSize
        # self.status = BatchStatus.Empty
        self.status=BatchStatus.Door_Closed 
        self.counter=0
        self.location=None
        self.iterator=0
        self.initRacks()

    def setLocation(self,location):
        self.location=location
    
    async def resetBatch(self):
        self.status = BatchStatus.Empty
        self.counter=0
        self.iterator=0

    def initRacks(self):        
        for i in range(self.batchSize):
            self.racks[i]=Rack(i)

    async def isAvailable(self):
        if self.counter <= self.batchSize:
            return True
        return False

    async def getNextLocation(self):
        if self.counter < self.batchSize:
            rack=self.racks[self.counter]
            return rack.location
        return None

    async def updateGridRack(self, batchCounter):
        self.counter+=1
        jobslogger.info("Cobas Pure Rack picked from batch {0} at index {1} ".format(batchCounter, self.counter))

    # need to be called when there are no racks left in batch
    async def emptyBatch(self):
        if self.counter == self.batchSize:
            await self.resetBatch()
            return True
        return False


class Station2(Station):
    def __init__(self,name,jobs,batchCount=3): 
        super().__init__(name,jobs)
        # self.grid:GridChemistry
        self.grid:Grid
        self.Iterator=0
        self.gridSize=len(Station2Positions)
        self.racks=[None] * self.gridSize
        self.batchSize=int(len(Station2Positions)/3)
        self.batch1=Stn2Batch(self.batchSize)
        self.batch2=Stn2Batch(self.batchSize)
        self.batch3=Stn2Batch(self.batchSize)
        self.batchCount=batchCount             
        self.batches=[]
        self.initBatches()
        self.initRacks()
        self.batchCounter=0
        self.batchIterator=0

    def initBatches(self):        
        for i in range(self.batchCount):
            batch=Stn2Batch(self.batchSize)
            self.batches.append(batch)

    def initRacks(self):        
        for i in range(self.batchSize):
            for j in range(self.batchCount):
                batch=self.batches[j]
                batch.initRacks()

    # async def initGrids(self,id, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5, ref_pose_6):
    #     self.grid=GridChemistry(id, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5, ref_pose_6)        
    #     for j in range(self.batchCount):
    #         cnt=0
    #         initlogger.info("Station 2: {0} grid  batch {1} locations:".format(self.name,j+1))
    #         for i in range(j* self.batches[j].batchSize, (j+1)*self.batches[j].batchSize):
    #             location=Station2Positions[i]
    #             rack=self.batches[j].racks[cnt]
    #             rack.location=self.grid.get_target_pose_rack(location[0], location[1])
    #             initlogger.info("Index, location :{0}:{1}".format(location[1],rack.location))
    #             cnt+=1

    async def initGrids(self,id, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5, ref_pose_6):
        # self.grid=GridChemistry(id, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5, ref_pose_6)       
        self.grid_1=Grid(ref_pose_1, ref_pose_2, ref_pose_1,1,10)    
        self.grid_2=Grid(ref_pose_3, ref_pose_4, ref_pose_3,1,10)    
        self.grid_3=Grid(ref_pose_5, ref_pose_6, ref_pose_5,1,10)    
        for j in range(self.batchCount):
            cnt=0
            initlogger.info("Station 2: {0} grid  batch {1} locations:".format(self.name,j+1))
            for i in range(j* self.batches[j].batchSize, (j+1)*self.batches[j].batchSize):
                location=Station2Positions[i]
                rack=self.batches[j].racks[cnt]
                # rack.location=self.grid.get_target_pose_rack(location[0], location[1])
                if ( j == 0 ):
                    rack.location=self.grid_1.get_target_x_y(location[1])
                elif ( j == 1 ):
                    rack.location=self.grid_2.get_target_x_y(location[1])
                elif ( j == 2 ):
                    rack.location=self.grid_3.get_target_x_y(location[1])
                initlogger.info("Index, location :{0}:{1}".format(location[1],rack.location))
                cnt+=1

    # this station as target
    async def updateGrid(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Door_Opened:            
            await batch.updateGridRack(self.batchCounter+1)

    # this station as target
    async def getNextLocation(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Door_Opened: 
            return await batch.getNextLocation()
        return None  
    
    async def isAvailable(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Door_Opened: 
            return await batch.isAvailable()
        return False

    # need to be called when there is no rack to pick from current batch
    async def isCurrentBatchEmpty(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Door_Opened:
            if await batch.emptyBatch():
                jobslogger.info("{0} batch {1} emptied, so door closed".format(self.name,self.batchCounter+1))
                jobId = await self.getCurrentBatchCloseDoorJobID()
                await processQueue.enqueue([jobId,jobId])
                if self.batchCounter >= self.batchCount - 1:
                     jobId = self.jobs[9].jobId
                     await processQueue.enqueue([jobId,jobId])
                self.batchCounter = (self.batchCounter + 1) % self.batchCount
                return True
            return False
      
    async def getCurrentBatchOpenDoorJobID(self):
        # Job(23,"Door 1 open"),
        # Job(25,"Door 2 open"),
        # Job(27,"Door 3 open"),
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Door_Closed:
            jobId = 0
            if self.batchCounter == 0:
                jobId = self.jobs[3].jobId
                batch.status = BatchStatus.Door_Opened
            elif self.batchCounter == 1:
                jobId = self.jobs[5].jobId
                batch.status = BatchStatus.Door_Opened
            elif self.batchCounter == 2:
                jobId = self.jobs[7].jobId
                batch.status = BatchStatus.Door_Opened
            jobslogger.info("Door {0} is opened from {1}".format(self.batchCounter+1, self.name))
            await processQueue.enqueue([jobId,jobId])
    
    async def getCurrentBatchCloseDoorJobID(self):
        # Job(24,"Door 1 close"),
        # Job(26,"Door 2 close"),
        # Job(28,"Door 3 close") 
        batch=self.batches[self.batchCounter]
        if self.batchCounter == 0:
            batch.status = BatchStatus.Door_Closed
            return self.jobs[4].jobId
        elif self.batchCounter == 1:
            batch.status = BatchStatus.Door_Closed
            return self.jobs[6].jobId
        elif self.batchCounter == 2:
            batch.status = BatchStatus.Door_Closed
            return self.jobs[8].jobId
        return 0
    
    async def getCurrentBatchStatus(self):
        batch=self.batches[self.batchCounter]
        return batch.status
    
    

