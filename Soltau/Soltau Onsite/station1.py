from logger import initlogger,jobslogger
from grids_v2 import Grid
from stations import Station, Tube
from settings import Color, Station1Positions


class Station1(Station):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.grid:Grid  
        self.redIterator=0
        self.redIterator_child=0
        self.greenIterator=0
        self.orangeIterator=0
        self.gridSize=Station1Positions
        self.tubes=[Tube] * self.gridSize
        self.cam1Counter=0
        self.initTubes()
        self.isRefreshCamera1Results=True
        self.isGreenAvailable=False
        self.isOrangeAvailable=False
        self.isBrownAvailable=False
        self.isYellowAvailable=False
        self.isYellow2Available=False
        self.isYellow3Available=False
        self.isRedAvailable=False

    def initTubes(self):        
        for i in range(self.gridSize):
            self.tubes[i]=Tube(i)

    async def initGrids(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        self.grid=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
        initlogger.info("Grid locations Station:{0}".format(self.name))
        for tube in self.tubes:
            tube.location=self.grid.get_target_x_y(self.tubes.index(tube)+1)
            initlogger.info("Index,location :{0}:{1}".format(self.tubes.index(tube)+1,tube.location))

    async def updateGrid(self,rows):          
        rows.sort(key=lambda x: int(x.get('position')))
        for row in rows:
            position=int(row["position"])-1
            color=Color(int(row["color"]))
            if position < Station1Positions:
                self.tubes[position].color=color
        jobslogger.info("Q400 results Cam 1: {0}".format(rows))
        self.updateRefreshCounter(rows)

    def updateRefreshCounter(self,rows):
        self.isGreenAvailable = any(Color(int(row["color"])) == Color.GREEN for row in rows)
        self.isOrangeAvailable = any(Color(int(row["color"])) == Color.ORANGE for row in rows)  
        self.isBrownAvailable = any(Color(int(row["color"])) == Color.BROWN for row in rows)
        self.isYellowAvailable = any(Color(int(row["color"])) == Color.YELLOW for row in rows)  
        self.isYellow2Available = any(Color(int(row["color"])) == Color.YELLOW_2 for row in rows) 
        self.isYellow3Available = any(Color(int(row["color"])) == Color.YELLOW_3 for row in rows)                
        self.isRedAvailable = any(Color(int(row["color"])) == Color.RED for row in rows)
        if self.isGreenAvailable or self.isOrangeAvailable or self.isBrownAvailable or self.isYellowAvailable or self.isYellow2Available or self.isYellow3Available or self.isRedAvailable:
            self.cam1Counter=0            
        else:
            self.cam1Counter+=1
        if self.cam1Counter == 3:
            self.isRefreshCamera1Results = False
            initlogger.info("Stopped hitting V.Q400 for cam1 results")                

    async def getNextGreenTube(self):        
        positions:list=list(range(self.greenIterator,self.gridSize))
        positions.extend(list(range(0,self.greenIterator)))
        for i in positions:
            self.greenIterator=i+1
            if(self.tubes[i].color==Color.GREEN):
                jobslogger.info("{0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.greenIterator))
                self.tubes[i].color = Color.NONE
                return self.tubes[i]
        return None

    async def getNextOrangeBrownYellowTube(self):        
        positions:list=list(range(self.orangeIterator,self.gridSize))
        positions.extend(list(range(0,self.orangeIterator)))
        for i in positions:
            self.orangeIterator=i+1
            if(self.tubes[i].color==Color.ORANGE):
                jobslogger.info("{0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.orangeIterator))
                self.tubes[i].color = Color.NONE
                return self.tubes[i]
            if(self.tubes[i].color==Color.BROWN):
                jobslogger.info("{0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.orangeIterator))
                self.tubes[i].color = Color.NONE
                return self.tubes[i]
            if(self.tubes[i].color==Color.YELLOW or self.tubes[i].color==Color.YELLOW_2 or self.tubes[i].color==Color.YELLOW_3):
                jobslogger.info("{0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.orangeIterator))
                self.tubes[i].color = Color.NONE
                return self.tubes[i]
        return None
    
    async def getNextRedTube(self):        
        positions:list=list(range(self.redIterator,self.gridSize))
        positions.extend(list(range(0,self.redIterator)))
        for i in positions:
            self.redIterator=i+1
            if(self.tubes[i].color==Color.RED):
                jobslogger.info("{0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.redIterator))
                self.tubes[i].color = Color.NONE
                return self.tubes[i]
        return None
