from logger import initlogger,jobslogger
from grids_v2 import  Grid
from stations import Station, Tube
from settings import BatchStatus, HolderStatus, Station17_18Positions


class Stn17Batch:
    def __init__(self,batchSize):
        self.batchSize=batchSize
        self.tubes=[None] * self.batchSize
        self.status = BatchStatus.Empty        
        self.counter=0
        self.location=None
        self.tubesCount = 0
        self.initTubes()

    def setLocation(self,location):
        self.location=location
    
    async def resetBatch(self):
        self.status = BatchStatus.Empty
        self.counter = 0

    def initTubes(self):        
        for i in range(self.batchSize):
            self.tubes[i]=Tube(i)

    async def getNextLocationToArchiv(self, batchCounter):
        if self.counter < self.batchSize and self.status == BatchStatus.Filled:
            tube=self.tubes[self.counter]
            await self.updateGridTube(batchCounter)            
            return tube.location
        return None

    async def updateGridTube(self, batchCounter):
        self.counter+=1
        jobslogger.info("Tube picked at filled rack holder 1 from batch {0} at index {1} and moved to Archiv".format(batchCounter, self.counter))

    async def currentRackEmpty(self):
        if self.counter == self.tubesCount:
            await self.resetBatch() 
            return True
        return False


class Station17(Station):
    def __init__(self,name,jobs,batchCount=10): 
        super().__init__(name,jobs)
        self.grid:Grid
        self.Iterator=0
        self.gridSize=len(Station17_18Positions)
        self.racks=[None] * batchCount
        self.batchSize=int(self.gridSize/batchCount)
        self.batchCount=batchCount             
        self.batches=[]
        self.initBatches()
        self.initTubes()
        self.batchCounter=0
        self.holderStatus = HolderStatus.Empty
        self.testRacksArray = []

    def initBatches(self):        
        for i in range(self.batchCount):
            batch=Stn17Batch(self.batchSize)
            self.batches.append(batch)

    def initTubes(self):        
        for i in range(self.batchSize):
            for j in range(self.batchCount):
                batch=self.batches[j]
                batch.initTubes()

    async def initGrids(self, ref_rack_1, ref_rack_2, r_rows, r_columns, ref_tube_1, ref_tube_2, ref_tube_3, t_rows, t_columns):
        self.gridRacks = Grid(ref_rack_1, ref_rack_2,ref_rack_1, r_rows, r_columns)
        self.gridTubes=Grid(ref_tube_1, ref_tube_2, ref_tube_3, t_rows, t_columns)
        for j in range(self.batchCount):
            cnt = 0
            initlogger.info(
                "Station 17: {0} grid  batch {1} locations:".format(self.name, j+1))
            for i in range(j* self.batches[j].batchSize, (j+1)*self.batches[j].batchSize):
                location=Station17_18Positions[i]
                tube=self.batches[j].tubes[cnt]
                tube.location=self.gridTubes.get_target_x_y(location)
                initlogger.info("Rack,Tube,location :{0}-{1}:{2}".format(j+1,cnt+1,tube.location))
                cnt+=1
            rackLocation = self.gridRacks.get_target_x_y(j+1)
            initlogger.info(
                "Rack Index,location :{0}:{1}".format(j+1, rackLocation))
            self.batches[j].setLocation(rackLocation)
            self.testRacksArray.append(rackLocation)

    # to move to Racks storage
    async def getNextRackLocation(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Empty and self.holderStatus == HolderStatus.Filled:
            jobslogger.info("{0} batch {1} picked".format(self.name,self.batchCounter+1))
            await self.updateGridRacks()
            return batch.location
        return None

    #this station as destination
    async def updateGridRacks(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Empty and self.holderStatus == HolderStatus.Filled: 
            # jobslogger.info("{0} batch {1} emptying".format(self.name,self.batchCounter+1))
            if self.batchCounter == self.batchCount-1:
                await self.emptyHolder()
            self.batchCounter = (self.batchCounter + 1) % self.batchCount
            
    # this station as source for tubes
    async def getNextTubeLocation(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Filled and self.holderStatus == HolderStatus.Filled: 
            return await batch.getNextLocationToArchiv(self.batchCounter)
        return None
    
    async def currentRackEmpty(self):
        batch=self.batches[self.batchCounter]
        if await batch.currentRackEmpty() and self.holderStatus == HolderStatus.Filled:
            jobslogger.info("{0} batch {1} made empty".format(self.name,self.batchCounter+1))
            batch.status = BatchStatus.Empty                                
            return True
        return False
    
    async def fillHolder(self):
        if self.holderStatus == HolderStatus.Empty:
            jobslogger.info("First filled racks holder made Filled")
            self.holderStatus = HolderStatus.Filled

    async def emptyHolder(self):
        if self.holderStatus == HolderStatus.Filled:
            jobslogger.info("First filled racks holder made Empty")
            self.holderStatus = HolderStatus.Empty

    async def getHolderStatus(self):
        return self.holderStatus
    
    async def setTubesCountInBatches(self, stn8Batches):
        for i in range(self.batchCount):
            # stn8 first rack tubes count must be in stn17 last rack
            batchNum = (self.batchCount-1-i)%self.batchCount
            batch = self.batches[batchNum]
            stn8batch = stn8Batches[i]
            batch.tubesCount = await stn8batch.getTubesCount()
            batch.status = BatchStatus.Filled
            jobslogger.info("{0}, Tubes in batch {1} : {2}".format(self.name, batchNum, batch.tubesCount))
            



    
