from grids_v2 import Grid
from stations import Station, Rack
from settings import RackStatus, Station2Positions
from logger import jobslogger,initlogger


class Station2(Station):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.grid_1:Grid 
        self.grid_2:Grid 
        self.counter = 0
        self.iterator = 0
        self.gridSize=int(Station2Positions)
        self.racks=[None] * self.gridSize
        self.rackLocations=[]
        self.initRacks()

    def initRacks(self):        
        for i in range(self.gridSize):
            self.racks[i]=Rack(i)
        for rack in self.racks:
            rack.status = RackStatus.Filled

    async def initGrids(self, ref_pose_1, ref_pose_2, ref_pose_3,ref_pose_4, rows, columns):
        self.grid_1=Grid(ref_pose_1, ref_pose_2, ref_pose_1, rows, columns)    
        self.grid_2=Grid(ref_pose_3, ref_pose_4, ref_pose_3, rows, columns)            
        initlogger.info("Grid locations Station2, cobas pure racks storage :{0}".format(self.name))
        for rack in self.racks:
            if self.racks.index(rack) < columns:
                rack.location=self.grid_1.get_target_x_y(self.racks.index(rack)+1)
                initlogger.info("Index,location :{0}:{1}".format(self.racks.index(rack)+1,rack.location)) 
                self.rackLocations.append(rack.location) 
            else:
                rack.location=self.grid_2.get_target_x_y(self.racks.index(rack)+1 - columns)
                initlogger.info("Index,location :{0}:{1}".format(self.racks.index(rack)+1,rack.location)) 
                self.rackLocations.append(rack.location) 
        for i in range(20):
            self.rackLocations.pop(0)

    async def updateGridPick(self):
        self.counter+=1
        if self.counter == self.gridSize:
            self.counter = 0
            
    async def getNextLocationToPick(self):
        rack=self.racks[self.counter]
        if rack.status == RackStatus.Filled:
            jobslogger.info("{0}, rack is picked at index {1}".format(self.name,self.counter+1))
            await self.updateGridPick()
            rack.status = RackStatus.Empty
            return rack.location
        return None

    async def updateGridPlace(self):
        self.iterator+=1
        if self.iterator == self.gridSize:
            self.iterator = 0

    async def getNextLocationToPlace(self):
        rack=self.racks[self.iterator]
        if rack.status == RackStatus.Empty:
            jobslogger.info("{0}, rack is placed at index {1}".format(self.name,self.iterator))
            await self.updateGridPlace()
            rack.status = RackStatus.Filled
            return rack.location
        return None

    
    
    

    