from grids import  Grid, GridBatch
from stations import processQueue, Station, Tube
from settings import BatchStatus, Color, Station5Positions, Settings
from logger import initlogger, jobslogger


class Stn5Batch:
    def __init__(self,batchSize):
        self.batchSize=batchSize
        self.tubes=[Tube] * self.batchSize
        self.status=BatchStatus.Empty        
        self.greenCounter=0
        self.orangeCounter=0
        self.counter=0
        self.locations=[0,1,3,2]
        self.gridSize = 4
        self.grids = [Tube] * self.gridSize
        self.gridIterator=0
        self.initTubes()
        self.greenIterator=0
        self.orangeIterator=0
        self.counterTube:Tube=Tube(0,None,Color.COUNTER)
        self.isCounterFilled=False

    def setLocation(self,location):
        self.location=location
    
    def setCounterTubeLocation(self,location):
        self.counterTube.location=location

    def getCounterTubeLocation(self):
        return self.counterTube.location
    
    async def resetBatch(self):
        self.status = BatchStatus.Empty
        self.orangeIterator=0
        self.greenIterator=0
        self.counter=0        
        for tube in self.tubes:
            tube.color=Color.NONE

    def initTubes(self):        
        for i in range(self.batchSize):
            self.tubes[i]=Tube(i,None,Color.NONE)

        for i in range(self.gridSize):
            self.grids[i]=Tube(i,None,Color.NONE)

    async def isAvailableForGreen(self):
        if self.greenCounter < Settings.green_max:
            return True
        return False

    async def isAvailableForOrange(self):
        if self.orangeCounter < Settings.orange_max:
            return True
        return False

    async def getNextLocation(self):
        if self.counter < self.batchSize:
            tube=self.tubes[self.counter]
            return tube.location
        return None

    async def updateGridTube(self,color): 
         if self.counter < self.batchSize:       
            self.tubes[self.counter].color = color
            self.counter+=1
            jobslogger.info("{0} tube placed at index {1} ".format(color.name,self.counter))
            if color == Color.GREEN:
                self.greenCounter+=1
            elif color == Color.ORANGE:
                self.orangeCounter+=1   
            elif color == Color.COUNTER:
                self.isCounterFilled=True
            jobslogger.info("Total Green: {0} ,Orange: {1} ,Counter Filled: {2} ".format(self.greenCounter,self.orangeCounter,self.isCounterFilled))
            """ if self.counter == self.batchSize:
                await self.fillBatch() """

    # need to be called when there are no tubes left in station1
    async def fillBatch(self):
        if self.status== BatchStatus.Empty and (self.greenCounter > 0 or self.orangeCounter > 0):
            self.status = BatchStatus.Filled
            return True
        return False            

    # need to be called when there are no tubes left in station5 batch
    async def emptyBatch(self):
        if self.status== BatchStatus.Process_Completed and self.greenCounter == 0 and self.orangeCounter == 0 and not(self.isCounterFilled):
            await self.resetBatch()
            return True
        return False
            
    # to move to station 6
    async def getBatchLocations(self):
        locations=[]
        for i in self.locations:
            locations.append(self.grids[i].location)
        return locations
    
     # to move to station 3
    async def getNextGreenTubeAvailable(self):
        if self.status == BatchStatus.Process_Completed:
            for i in range(0,self.batchSize):
                if(self.tubes[i].color==Color.GREEN):
                    jobslogger.info("Green tubes available in stago ")                                      
                    return True
        return False
        
    # to move to station 3
    async def getNextGreenTube(self):
        if self.status == BatchStatus.Process_Completed:
            for i in range(self.greenIterator,self.batchSize):
                self.greenIterator+=1
                if(self.tubes[i].color==Color.GREEN):
                    self.greenCounter-=1
                    jobslogger.info("{0} tube picked from index {1} ".format(self.tubes[i].color.name,self.greenIterator))                                      
                    return self.tubes[i]
        return None

    # to move to station 2
    async def getNextOrangeTube(self):
        if self.status == BatchStatus.Process_Completed:
            for i in range(self.orangeIterator,self.batchSize):
                self.orangeIterator+=1
                if(self.tubes[i].color==Color.ORANGE):
                    self.orangeCounter-=1
                    jobslogger.info("{0} tube picked from index {1} ".format(self.tubes[i].color.name,self.orangeIterator))    
                    return self.tubes[i]
        return None
    
    # to move back to counter weight
    async def getNextCounterTube(self):
        if not(self.isCounterFilled):
            return None 
        if self.status == BatchStatus.Process_Completed:
            for i in range(self.batchSize):
                if(self.tubes[i].color==Color.COUNTER):
                    self.isCounterFilled=False
                    jobslogger.info("{0} tube moved back  ".format(self.tubes[i].color.name))
                    return self.tubes[i]
        return None


class Station5(Station):
    def __init__(self,name,jobs,batchCount=2): 
        super().__init__(name,jobs)
        self.grid:GridBatch
        self.gridSize=len(Station5Positions)
        self.batchSize=int(len(Station5Positions)/2)   
        self.batchCount=batchCount             
        self.batches=[]
        self.initBatches()
        self.initTubes()
        self.batchCounter=0
        self.batchIterator=0

    def initBatches(self):        
        for i in range(self.batchCount):
            batch=Stn5Batch(self.batchSize)
            self.batches.append(batch)

    def initTubes(self):        
        for i in range(self.batchSize):
            for j in range(self.batchCount):
                batch=self.batches[j]
                batch.initTubes()

    async def initGrids(self, ref_pose_1, ref_pose_2, ref_pose_3, p_rows, p_columns, ref_pose_4, ref_pose_5, ch_rows, ch_columns):
        self.grid=GridBatch(ref_pose_1, ref_pose_2, ref_pose_3, p_rows, p_columns, ref_pose_4, ref_pose_5, ch_rows, ch_columns)
        for j in range(self.batchCount):
            initlogger.info("Station 5 grid  batch {0} locations:".format(j+1))
            cnt=0
            for i in range(j* self.batches[j].batchSize, (j+1)*self.batches[j].batchSize):
                location=Station5Positions[i]
                tube=self.batches[j].tubes[cnt]
                tube.location=self.grid.get_target_x_y(location[0],location[1])
                initlogger.info("Index,location :{0}:{1}".format(location,tube.location))
                cnt+=1 

    async def initBatchGrids(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        self.grid=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
        for j in range(self.batchCount):
            initlogger.info("Station 5 grid  batch {0} rack locations:".format(j+1))            
            cnt=0
            for i in range(j* self.batches[j].gridSize, (j+1)*self.batches[j].gridSize):
                grid=self.batches[j].grids[cnt]
                grid.location= self.grid.get_target_x_y(i+1)
                initlogger.info("Index,location :{0}:{1}".format(grid.index+1,grid.location))
                cnt+=1

    async def initCounterGrids(self, ref_pose_1, ref_pose_2):
        self.batches[0].setCounterTubeLocation(ref_pose_1)
        self.batches[1].setCounterTubeLocation(ref_pose_2)
        initlogger.info("counter tube locations :{0},{1}".format(ref_pose_1,ref_pose_2))

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

    #this station as target
    async def isAvailableForGreen(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Empty: 
            return await batch.isAvailableForGreen()
        return False 

    #this station as target
    async def isAvailableForOrange(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Empty: 
            return await batch.isAvailableForOrange()
        return False 
   
    async def currentBatchFilled(self):
        batch=self.batches[self.batchCounter]
        if await batch.fillBatch():
            jobslogger.info("{0} batch {1} filled".format(self.name,self.batchCounter+1)) 
            self.batchCounter= (self.batchCounter + 1) % 2
            return True
        return False
    
    # this station as source to Station 6
    async def getFilledBatchLocations(self): 
        for batchNum, batch in enumerate(self.batches):
            if batch.status == BatchStatus.Filled:
                batch.status=BatchStatus.Process_Running 
                # return await batch.getBatchLocations()
                return [batchNum+1,0,0,0,0,0]
        return None 

    # this station as source to Station 6
    async def getRunningBatchLocations(self):
        for batchNum, batch in enumerate(self.batches):
            if batch.status == BatchStatus.Process_Running:
                batch.status=BatchStatus.Process_Completed 
                # return await batch.getBatchLocations()
                return [batchNum+1,0,0,0,0,0]
        return None
    
    # this station as source to station 3
    async def getNextGreenTube(self):
        batch=self.batches[self.batchIterator]
        if batch.status != BatchStatus.Process_Completed:
            return None
        tube=await batch.getNextGreenTube()
        if tube is None:
            if await batch.emptyBatch():
                jobslogger.info("{0} batch {1} made empty".format(self.name,self.batchCounter+1))
                self.batchIterator = (self.batchIterator + 1) % self.batchCount
        return tube

    async def getNextGreenTubeAvailable(self):
        batch=self.batches[self.batchIterator]
        if batch.status != BatchStatus.Process_Completed:
            return None
        return await batch.getNextGreenTubeAvailable()

    # this station as source to station 2
    async def getNextOrangeTube(self):
        batch=self.batches[self.batchIterator]
        if batch.status != BatchStatus.Process_Completed:
            return None
        tube=await batch.getNextOrangeTube()
        if tube is None:            
            if await batch.emptyBatch():
                jobslogger.info("{0} batch {1} made empty".format(self.name,self.batchIterator+1))
                self.batchIterator = (self.batchIterator + 1) % self.batchCount
        return tube
    
    # this station as source to counter weight tubes
    async def getNextCounterTube(self):
        batch=self.batches[self.batchIterator]
        if batch.status != BatchStatus.Process_Completed:
            return False
        tube= await batch.getNextCounterTube()
        if tube is not None:
            srcJobId=self.jobs[1].jobId 
            destJobId=self.jobs[5].jobId
            await processQueue.enqueue([srcJobId,destJobId])
            src=tube.location
            dest=batch.getCounterTubeLocation()
            processQueue.destLocation.extend([src,dest])
            jobslogger.info("{0} tube moved from {1}".format(tube.color.name,self.name))
            return True
        if await batch.emptyBatch():
            jobslogger.info("{0} batch {1} made empty".format(self.name,self.batchCounter+1))
            self.batchIterator = (self.batchIterator + 1) % self.batchCount
        return False
    
    async def prepareCounterWeightJobs(self): 
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Empty:
            filledCount=len(list(filter(lambda tube: tube.color !=Color.NONE,batch.tubes)))
            if filledCount %2 != 0:
                srcJobId=self.jobs[4].jobId 
                destJobId=self.jobs[2].jobId
                await processQueue.enqueue([srcJobId,destJobId])
                tube=batch.counterTube
                src=tube.location
                dest=await self.getNextLocation()
                processQueue.destLocation.extend([src,dest])                      
                await self.updateGrid(tube.color)
                jobslogger.info("{0} tube moved from {1} - {2} ".format(tube.color.name,self.name,self.batchCounter+1)) 
                return True
        return False
    


