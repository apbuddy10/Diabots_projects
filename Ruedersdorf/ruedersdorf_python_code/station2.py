from grids_v2 import Grid
from logger import initlogger, jobslogger
from settings import RackStatus, Station2Positions
from stations import Fridge, Rack, Station


class Station2(Station):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.grid_1:Grid 
        self.grid_2:Grid 
        self.counter = 0
        self.iterator = 0
        self.gridSize=int(Station2Positions)
        self.racks=[None] * self.gridSize
        self.initRacks()

    def initRacks(self):        
        for i in range(self.gridSize):
            self.racks[i]=Rack(i)
        for rack in self.racks:
            rack.status = RackStatus.Filled

    async def initGrids_1(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        self.grid_1=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)  
        initlogger.info("Grid locations Station2, cobas pure racks storage :{0}".format(self.name))
        for rack in self.racks:
            if self.racks.index(rack) < columns:
                rack.location=self.grid_1.get_target_x_y(self.racks.index(rack)+1)
                initlogger.info("Index,location :{0}:{1}".format(self.racks.index(rack)+1,rack.location))   

    async def initGrids_2(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        self.grid_2=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)  
        initlogger.info("Grid locations Station2, cobas pure racks storage :{0}".format(self.name))
        for rack in self.racks:
            if self.racks.index(rack) >= 10 and self.racks.index(rack) < 20:
                rack.location=self.grid_2.get_target_x_y(self.racks.index(rack)+1 - 10)
                initlogger.info("Index,location :{0}:{1}".format(self.racks.index(rack)+1,rack.location))   

    async def initGrids_3(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        self.grid_3=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)  
        initlogger.info("Grid locations Station2, cobas pure racks storage :{0}".format(self.name))
        for rack in self.racks:
            if self.racks.index(rack) >= 20 and self.racks.index(rack) < 30:
                rack.location=self.grid_3.get_target_x_y(self.racks.index(rack)+1 - 20)
                initlogger.info("Index,location :{0}:{1}".format(self.racks.index(rack)+1,rack.location))  

    async def initGrids_4(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        self.grid_4=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)  
        initlogger.info("Grid locations Station2, cobas pure racks storage :{0}".format(self.name))
        for rack in self.racks:
            if self.racks.index(rack) >= 30 and self.racks.index(rack) < 40:
                rack.location=self.grid_4.get_target_x_y(self.racks.index(rack)+1 - 30)
                initlogger.info("Index,location :{0}:{1}".format(self.racks.index(rack)+1,rack.location))  

    async def updateGridPick(self):
        self.counter+=1
        if self.counter == self.gridSize:
            self.counter = 0
    
    async def getPickRackStatus(self):
        rack=self.racks[self.counter]
        if rack.status == RackStatus.Filled:
            return True
        return False

    async def getNextLocationToPick(self):
        rack=self.racks[self.counter]
        if rack.status == RackStatus.Filled:
            index=self.counter+1
            jobslogger.info("{0}, rack is picked at index {1}".format(self.name,index))
            await self.updateGridPick()
            rack.status = RackStatus.Empty
            return index,rack.location
        return None

    async def updateGridPlace(self):
        self.iterator+=1
        if self.iterator == self.gridSize:
            self.iterator = 0

    async def getPlaceRackStatus(self):
        rack=self.racks[self.iterator]
        if rack.status == RackStatus.Empty:
            return True
        return False

    async def getNextLocationToPlace(self):
        rack=self.racks[self.iterator]
        if rack.status == RackStatus.Empty:
            index=self.iterator+1
            jobslogger.info("{0}, rack is placed at index {1}".format(self.name,index))
            await self.updateGridPlace()
            rack.status = RackStatus.Filled
            return index,rack.location
        return None

    
    
    

    