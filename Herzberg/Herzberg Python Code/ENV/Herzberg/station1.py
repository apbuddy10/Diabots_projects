from logger import initlogger,jobslogger
from grids import Grid
from stations import Station, Tube
from settings import Color, Station1Positions
from machine import MachineStatus
from station7 import Station7


class Station1(Station):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.grid:Grid  
        self.redIterator=0
        self.redIterator_child=0
        self.greenIterator=0
        self.orangeIterator=0
        self.gridSize=len(Station1Positions)
        self.tubes=[Tube] * self.gridSize
        self.cam1Counter=0
        self.initTubes()
        self.isRefreshCamera1Results=True
        self.isGreenAvailable=False
        self.isOrangeAvailable=False
        self.isRedAvailable=False
        self.isCRedAvailable=False

    def initTubes(self):        
        for i in range(self.gridSize):
            self.tubes[i]=Tube(i)

    async def initGrids(self,id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        self.grid=Grid(id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
        initlogger.info("Grid locations Station:{0}".format(self.name))
        for tube in self.tubes:
            tube.location=self.grid.get_target_x_y(self.tubes.index(tube)+1)
            initlogger.info("Index,location :{0}:{1}".format(self.tubes.index(tube)+1,tube.location))

    async def updateGrid(self,rows):          
        rows.sort(key=lambda x: int(x.get('position')))
        for row in rows:
            position=int(row["position"])-1
            color=Color(int(row["color"]))
            if position < len(Station1Positions):
                self.tubes[position].color=color
        self.updateRefreshCounter(rows)

    def updateRefreshCounter(self,rows):
        self.isGreenAvailable = any(Color(int(row["color"])) == Color.GREEN for row in rows)
        self.isOrangeAvailable =any(Color(int(row["color"])) == Color.ORANGE for row in rows)            
        self.isRedAvailable = any(Color(int(row["color"])) == Color.RED for row in rows)    
        self.isCRedAvailable = any(Color(int(row["color"])) == Color.CRED for row in rows)    
        if self.isGreenAvailable or self.isOrangeAvailable or self.isRedAvailable or self.isCRedAvailable:
            self.cam1Counter=0            
        else:
            self.cam1Counter+=1
        if self.cam1Counter == 3:
            self.isRefreshCamera1Results = False
            initlogger.info("Stopped hitting V.Q400 for cam1 results")                

    async def getNextRedTubeAdult(self):
        positions:list=list(range(self.redIterator,self.gridSize))
        positions.extend(list(range(0,self.redIterator)))
        for i in positions:
            self.redIterator=i+1
            if(self.tubes[i].color==Color.RED):
                jobslogger.info("{0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.redIterator))
                return self.tubes[i]
        return None

    async def getNextRedTubeChild(self):        
        positions:list=list(range(self.redIterator_child,self.gridSize))
        positions.extend(list(range(0,self.redIterator_child)))
        for i in positions:
            self.redIterator_child=i+1
            if(self.tubes[i].color==Color.CRED):
                jobslogger.info("{0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.redIterator_child))
                return self.tubes[i]
        return None
    
    # async def getNextRedTube(self):
    #     if Station7.statusAdult == MachineStatus.On and await Station7.isAvailableAdult():
    #         tubeAdult = await self.getNextRedTubeAdult()
    #         if tubeAdult is not None:
    #             return tubeAdult
    #     if Station7.statusChild == MachineStatus.On and await Station7.isAvailableChild():
    #         tubeChild = await self.getNextRedTubeChild()
    #         if tubeChild is not None:
    #             return tubeChild
    #     return None
    
    # async def getNextRedTube(self, statusAdult, statusChild):
    #     if statusAdult == MachineStatus.On:
    #         tubeAdult = await self.getNextRedTubeAdult()
    #     if statusChild == MachineStatus.On:
    #         tubeChild = await self.getNextRedTubeChild()
    #     if self.redIterator == self.redIterator_child or self.redIterator < self.redIterator_child:
    #         if tubeAdult is not None:
    #             return tubeAdult
    #     if tubeChild is None:
    #         return tubeAdult
    #     return tubeChild

    async def getNextGreenTube(self):        
        positions:list=list(range(self.greenIterator,self.gridSize))
        positions.extend(list(range(0,self.greenIterator)))
        for i in positions:
            self.greenIterator=i+1
            if(self.tubes[i].color==Color.GREEN):
                jobslogger.info("{0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.greenIterator))
                return self.tubes[i]
        return None

    async def getNextOrangeTube(self):        
        positions:list=list(range(self.orangeIterator,self.gridSize))
        positions.extend(list(range(0,self.orangeIterator)))
        for i in positions:
            self.orangeIterator=i+1
            if(self.tubes[i].color==Color.ORANGE):
                jobslogger.info("{0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.orangeIterator))
                return self.tubes[i]
        return None
