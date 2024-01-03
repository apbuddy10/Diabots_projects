from grids_v2 import  Grid, GridBatch
from stations import processQueue, Station, Tube
from settings import BatchStatus, Color, Station5Positions, Settings,TubeType
from logger import initlogger, jobslogger


class Stn5Batch:
    def __init__(self,batchSize):
        self.batchSize=batchSize
        self.tubes=[Tube] * self.batchSize
        self.status=BatchStatus.Empty        
        self.greenCounter=0
        self.orangeCounter=0
        self.brownCounterConstant=16
        self.brownCounter=0
        self.yellowCounter=0
        # self.counter=0
        self.locations=[0,1,3,2]
        self.gridSize = 4
        self.grids = [Tube] * self.gridSize
        self.gridIterator=0
        self.initTubes()
        self.greenIterator=0
        self.orangeIterator=0
        self.brownIterator=0
        self.yellowIterator=0
        # self.counterTube:Tube=Tube(0,None,Color.COUNTER)
        # self.isCounterFilled=False
        self.isBigCounterFilled=False
        self.isSmallCounterFilled=False
        self.bigCounterTube:Tube=Tube(0,None,Color.COUNTERBIG)
        self.smallCounterTube:Tube=Tube(0,None,Color.COUNTERSMALL)

    def setLocation(self,location):
        self.location=location

    def setSmallCounterTubeLocation(self,location):
        self.smallCounterTube.location=location

    def setBigCounterTubeLocation(self,location):
        self.bigCounterTube.location=location

    def getSmallCounterTubeLocation(self):
        return self.smallCounterTube.location

    def getBigCounterTubeLocation(self):
        return self.bigCounterTube.location
    
    async def resetBatch(self):
        self.status = BatchStatus.Empty        
        self.greenIterator=0
        self.orangeIterator=0
        self.brownIterator=self.brownCounterConstant
        self.yellowIterator=0
        # self.counter=0     
        self.greenCounter=0
        self.orangeCounter=0
        self.brownCounter=0
        self.yellowCounter=0   
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

    async def isAvailableForOrangeYellow(self):
        if self.orangeCounter+self.yellowCounter < Settings.orangeYellow_max:
            return True
        return False
    
    async def isAvailableForBrown(self):
        if self.brownCounter < Settings.brown_max:
            return True
        return False

    async def getNextLocationSmall(self):
        count = self.greenCounter + self.orangeCounter + self.yellowCounter
        if count < self.batchSize:
            tube=self.tubes[count]
            return tube.location
        return None
    
    async def getNextLocationBig(self):
        if self.brownCounter+self.brownCounterConstant < self.batchSize:
            tube=self.tubes[self.brownCounter+self.brownCounterConstant]
            return tube.location
        return None

    async def updateGridTube(self,color,type): 
         totalCount = self.greenCounter + self.orangeCounter + self.brownCounter + self.yellowCounter
         if totalCount < self.batchSize: 
            if color == Color.BROWN:                
                self.tubes[self.brownCounter+self.brownCounterConstant].color = color
                self.tubes[self.brownCounter+self.brownCounterConstant].type = type
                jobslogger.info("{0} tube placed at index {1} and type {2} ".format(color.name,self.brownCounter+self.brownCounterConstant,type))
                self.brownCounter+=1
            elif color == Color.COUNTERBIG:
                self.tubes[self.brownCounter+self.brownCounterConstant].color = color
                self.tubes[self.brownCounter+self.brownCounterConstant].type = type
                jobslogger.info("{0} Big Counter tube placed at index {1} and type {2} ".format(color.name,self.brownCounter+self.brownCounterConstant,type))
                self.isBigCounterFilled=True
                jobslogger.info(" Big Counter Filled: {0} ".format(self.isBigCounterFilled))
            else:
                smallCount = self.greenCounter+self.orangeCounter+self.yellowCounter
                self.tubes[smallCount].color = color
                self.tubes[smallCount].type = type
                jobslogger.info("{0} tube placed at index {1} and type {2} ".format(color.name,smallCount,type))
                if color == Color.GREEN:
                    self.greenCounter+=1
                elif color == Color.ORANGE:
                    self.orangeCounter+=1                   
                elif color == Color.YELLOW:
                    self.yellowCounter+=1
                elif color == Color.COUNTERSMALL:
                    self.isSmallCounterFilled=True
                # elif color == Color.COUNTERBIG:
                #     self.isBigCounterFilled=True
            jobslogger.info("Total Green: {0} ,Orange: {1}, Brown: {2}, Yellow: {3}, Small Counter Filled: {4}, Big Counter Filled: {5} ".format(self.greenCounter,self.orangeCounter,self.brownCounter, self.yellowCounter,self.isSmallCounterFilled, self.isBigCounterFilled))

    # need to be called when there are no tubes left in station1
    async def fillBatch(self):
        if self.status == BatchStatus.Empty and (self.greenCounter > 0 or self.orangeCounter > 0 or self.brownCounter > 0 or self.yellowCounter > 0):
            self.status = BatchStatus.Filled
            return True
        return False            

    # need to be called when there are no tubes left in station5 batch
    async def emptyBatch(self):
        if self.status == BatchStatus.Process_Completed and self.greenCounter == 0 and self.orangeCounter == 0 and self.brownCounter == 0 and self.yellowCounter == 0 and not(self.isSmallCounterFilled) and not(self.isBigCounterFilled):
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
    async def getNextGreenTube(self):
        if self.status == BatchStatus.Process_Completed:
            for i in range(self.greenIterator,self.batchSize):
                self.greenIterator+=1
                if(self.tubes[i].color==Color.GREEN):
                    self.greenCounter-=1
                    jobslogger.info("{0} tube picked from index {1} ".format(self.tubes[i].color.name,self.greenIterator))                                      
                    return self.tubes[i]
        return None

    async def getNextOrangeTube(self):
        if self.status == BatchStatus.Process_Completed:
            for i in range(self.orangeIterator,self.batchSize):
                self.orangeIterator+=1
                if(self.tubes[i].color==Color.ORANGE):
                    self.orangeCounter-=1
                    jobslogger.info("{0} tube picked from index {1} ".format(self.tubes[i].color.name,self.orangeIterator))    
                    return self.tubes[i]
        return None
    
    async def getNextBrownTube(self):
        if self.status == BatchStatus.Process_Completed:
            for i in range(self.brownIterator,self.batchSize):
                self.brownIterator+=1
                if(self.tubes[i].color==Color.BROWN):
                    self.brownCounter-=1
                    jobslogger.info("{0} tube picked from index {1} ".format(self.tubes[i].color.name,self.brownIterator))    
                    return self.tubes[i]
        return None
    
    async def getNextYellowTube(self):
        if self.status == BatchStatus.Process_Completed:
            for i in range(self.yellowIterator,self.batchSize):
                self.yellowIterator+=1
                if(self.tubes[i].color==Color.YELLOW):
                    self.yellowCounter-=1
                    jobslogger.info("{0} tube picked from index {1} ".format(self.tubes[i].color.name,self.yellowIterator))    
                    return self.tubes[i]
        return None
    
    # to move back to counter weight
    async def  getNextCounterTube(self):
        if not(self.isBigCounterFilled) and not(self.isSmallCounterFilled):
            return None 
        if self.status == BatchStatus.Process_Completed:
            for i in range(self.batchSize):
                if(self.tubes[i].color==Color.COUNTERSMALL and self.isSmallCounterFilled):
                    self.isSmallCounterFilled=False
                    jobslogger.info("{0} tube moved back from racks to counter tubes location and Small Counter Filled: {1}, Big Counter Filled: {2}".format(self.tubes[i].color.name,self.isSmallCounterFilled, self.isBigCounterFilled))
                    return self.tubes[i]
                if(self.tubes[i].color==Color.COUNTERBIG and self.isBigCounterFilled):
                    self.isBigCounterFilled=False
                    jobslogger.info("{0} tube moved back from racks to counter tubes location and Small Counter Filled: {1}, Big Counter Filled: {2}".format(self.tubes[i].color.name,self.isSmallCounterFilled, self.isBigCounterFilled))
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

    async def initCounterGrids(self, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4):
        self.batches[0].setBigCounterTubeLocation(ref_pose_1)
        self.batches[0].setSmallCounterTubeLocation(ref_pose_2)
        self.batches[1].setBigCounterTubeLocation(ref_pose_3)
        self.batches[1].setSmallCounterTubeLocation(ref_pose_4)
        initlogger.info("Small counter tube locations :{0},{1}".format(ref_pose_2,ref_pose_4))
        initlogger.info("Big counter tube locations :{0},{1}".format(ref_pose_1,ref_pose_3))

    #this station as target
    async def updateGrid(self,color,type):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Empty:
            jobslogger.info("{0} batch {1} filling".format(self.name,self.batchCounter+1))              
            await batch.updateGridTube(color,type)

    #this station as target
    async def getNextLocationSmall(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Empty: 
            return await batch.getNextLocationSmall()
        return None
    
    #this station as target
    async def getNextLocationBig(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Empty: 
            return await batch.getNextLocationBig()
        return None

    #this station as target
    async def isAvailableForGreen(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Empty: 
            return await batch.isAvailableForGreen()
        return False 

    #this station as target
    async def isAvailableForOrangeYellow(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Empty: 
            return await batch.isAvailableForOrangeYellow()
        return False 
    
    #this station as target
    async def isAvailableForBrown(self):
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Empty: 
            return await batch.isAvailableForBrown()
        return False 
   
    async def currentBatchFilled(self):
        batch=self.batches[self.batchCounter]
        if await batch.fillBatch():
            jobslogger.info("{0} batch {1} filled".format(self.name,self.batchCounter+1)) 
            self.batchCounter= (self.batchCounter + 1) % 2
            return True
        return False
    
    async def testFillBatch(self):
        batch=self.batches[self.batchCounter]
        batch.status = BatchStatus.Filled
        jobslogger.info("{0} batch {1} filled".format(self.name,self.batchCounter+1)) 
        batch.status=BatchStatus.Process_Completed
        self.batchCounter= (self.batchCounter + 1) % 2
    
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
                jobslogger.info("{0} batch {1} made empty".format(self.name,self.batchIterator+1))
                self.batchIterator = (self.batchIterator + 1) % self.batchCount
        return tube

    # this station as source to station 2
    async def getNextOrangeTube(self):
        batch=self.batches[self.batchIterator]
        if batch.status != BatchStatus.Process_Completed:
            return None
        tube=await batch.getNextOrangeTube()
        if tube is None:
            tube=await batch.getNextYellowTube()
        if tube is None:            
            if await batch.emptyBatch():
                jobslogger.info("{0} batch {1} made empty".format(self.name,self.batchIterator+1))
                self.batchIterator = (self.batchIterator + 1) % self.batchCount
        return tube
    
    # this station as source to station 2
    async def getNextBrownTube(self):
        batch=self.batches[self.batchIterator]
        if batch.status != BatchStatus.Process_Completed:
            return None
        tube=await batch.getNextBrownTube()
        if tube is None:            
            if await batch.emptyBatch():
                jobslogger.info("{0} batch {1} made empty".format(self.name,self.batchIterator+1))
                self.batchIterator = (self.batchIterator + 1) % self.batchCount
        return tube
    
    # this station as source to station 2
    async def getNextYellowTube(self):
        batch=self.batches[self.batchIterator]
        if batch.status != BatchStatus.Process_Completed:
            return None
        tube=await batch.getNextYellowTube()
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
            if(tube.color==Color.COUNTERSMALL):
                tubeType=TubeType.SMALL
                destLoc=batch.getSmallCounterTubeLocation()
            else:
                tubeType=TubeType.BIG
                destLoc=batch.getBigCounterTubeLocation()
            await processQueue.enqueue([srcJobId,destJobId,tubeType]) 
            srcLoc=tube.location
            processQueue.destLocation.extend([srcLoc,destLoc])
            jobslogger.info("{0} tube moved from {1}".format(tube.color.name,self.name))
            return True
        if await batch.emptyBatch():
            jobslogger.info("{0} batch {1} made empty".format(self.name,self.batchIterator+1))
            self.batchIterator = (self.batchIterator + 1) % self.batchCount
        return False
    
    def filterBigTubes(self,tube):
        return tube.color == Color.BROWN
    
    def filterSmallTubes(self,tube):
        return tube.color == Color.GREEN or tube.color == Color.ORANGE or tube.color == Color.YELLOW
    
    async def prepareCounterWeightJobs(self):
        isSuccess=False 
        batch=self.batches[self.batchCounter]
        if batch.status == BatchStatus.Empty:
            filledCount=len(list(filter(lambda tube: self.filterSmallTubes(tube) ,batch.tubes)))
            if filledCount % 2 != 0:
                srcJobId=self.jobs[4].jobId 
                destJobId=self.jobs[2].jobId
                await processQueue.enqueue([srcJobId,destJobId,TubeType.SMALL])
                srcLoc=batch.getSmallCounterTubeLocation()
                destLoc=await self.getNextLocationSmall()
                processQueue.destLocation.extend([srcLoc,destLoc])                      
                await self.updateGrid(Color.COUNTERSMALL,TubeType.SMALL)
                jobslogger.info("CounterSmall tube placed in {0}  BatchNo: - {1} ".format(self.name,self.batchCounter+1)) 
                isSuccess=True
            filledCount=len(list(filter(lambda tube: self.filterBigTubes(tube) ,batch.tubes)))
            if filledCount % 2 != 0:
                srcJobId=self.jobs[4].jobId 
                destJobId=self.jobs[2].jobId
                await processQueue.enqueue([srcJobId,destJobId,TubeType.BIG])
                srcLoc=batch.getBigCounterTubeLocation()
                destLoc=await self.getNextLocationBig()
                processQueue.destLocation.extend([srcLoc,destLoc])                      
                await self.updateGrid(Color.COUNTERBIG,TubeType.BIG)
                jobslogger.info("CounterBig tube placed in {0}  BatchNo: - {1} ".format(self.name,self.batchCounter+1)) 
                isSuccess=True
        return isSuccess


