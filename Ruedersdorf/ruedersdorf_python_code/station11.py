from typing import List

from grids_v2 import Grid
from logger import initlogger, jobslogger
from settings import Station11Size, dummyLocation
from stations import Fridge, Rack, Station, Tube, processQueue


class Station11(Station):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.grid:Grid 
        self.counter=0
        self.gridSize=Station11Size 
        self.fridgeCount = 2
        self.batchSize = int(self.gridSize / self.fridgeCount)
        self.tubes:List[Tube]=[None] * self.gridSize   
        self.fridges:List[Fridge]=[None] * (self.fridgeCount) 
        self.initTubes()

    def initTubes(self):        
        for i in range(self.fridgeCount):
            self.fridges[i]=Fridge(self.gridSize,i+1)
            self.fridges[i].initTubes()
    
    async def initGrids(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns,fridgeNo:int):
        grid=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
        initlogger.info("Grid locations of fridge {0} Station 11 :{1}".format(fridgeNo,self.name))
        fridge=self.fridges[fridgeNo-1]        
        for tube in fridge.tubes:
            tube.location=grid.get_target_x_y(fridge.tubes.index(tube)+1)
            initlogger.info("Index,location :{0}:{1}".format(fridge.tubes.index(tube)+1,tube.location))

    async def updateGrid(self,color):
        for fridge in self.fridges:
            if fridge.counter < fridge.size:            
                tube=fridge.tubes[fridge.counter]
                tube.color=color
                fridge.counter=fridge.counter+1
                jobslogger.info("{0} tube placed in {1} at fridge {2} in position {3} ".format(color.name,self.name,self.fridges.index(fridge)+1,fridge.counter))
                return True
        return False
    
    async def getArchiveFilledJob(self):
        if not await self.isAvailable():
            await self.closeDoor()
            jobId=self.jobs[7].jobId 
            await processQueue.enqueue([jobId,jobId])
            processQueue.destLocation.extend(dummyLocation)
            jobslogger.info("{0} grid filled. Display reset popup".format(self.name))
            return True
        return False
    
    async def resetArchive(self, reset):
        if reset:
            for fridge in self.fridges:
                fridge.resetTubes()
    
    async def isAvailable(self):        
        for fridge in self.fridges:
            if fridge.counter < fridge.size: 
                return True
        return False
    
    async def getNextAvailableFridgeNo(self):
        for fridge in self.fridges:
            if fridge.counter < fridge.size:
                return fridge.fridgeNo        
        return 0
    
    #this station as target
    async def getNextLocation(self):
        for fridge in self.fridges:
            if fridge.counter < fridge.size:            
                tube=fridge.tubes[fridge.counter]
                return tube.location
        return None 
    
    async def openDoor(self):
        fridgeNo=await self.getNextAvailableFridgeNo()
        if not self.fridges[fridgeNo-1].isDoorOpened:
            await self.closeOtherDoors(fridgeNo)
            self.fridges[fridgeNo-1].isDoorOpened=True
            jobId=self.jobs[4].jobId
            await processQueue.enqueue([jobId,jobId])
            processQueue.destLocation.extend([[fridgeNo,0,0,0,0,0],[fridgeNo,0,0,0,0,0]])
            jobslogger.info("{0}- {1} door opened".format(self.name,fridgeNo))
        return True
    
    async def getOpenedFridgeNo(self):
        for fridge in self.fridges:
            if fridge.isDoorOpened:
                return fridge.fridgeNo
        return None
    
    async def closeDoor(self,fridgeNo:int=None):
        if not fridgeNo:
            fridgeNo=await self.getOpenedFridgeNo()
        if fridgeNo and self.fridges[fridgeNo-1].isDoorOpened:
            self.fridges[fridgeNo-1].isDoorOpened=False
            jobId=self.jobs[3].jobId
            await processQueue.enqueue([jobId,jobId])
            processQueue.destLocation.extend([[fridgeNo,0,0,0,0,0],[fridgeNo,0,0,0,0,0]])
            jobslogger.info("{0}: {1} fridge door closed".format(self.name,fridgeNo))
            return True
        return False
    
    async def closeOtherDoors(self,fridgeNo:int):
        for n,fridge in enumerate(self.fridges):
            if fridgeNo-1 != n:
                await self.closeDoor(fridgeNo)

    