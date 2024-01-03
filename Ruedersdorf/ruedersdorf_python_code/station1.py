from logger import initlogger,jobslogger
from grids_v2 import Grid
from stations import Station, Tube
from settings import Color, Station1Positions, emergencyPositions
from settings import TubeType
from timer import Timer


class Station1(Station):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.grid:Grid  
        self.emergencyCentrifugeIterator=0
        self.emergencyRedIterator=0
        self.redIterator=0
        self.redIterator_child=0
        self.greenIterator=0
        self.orangeIterator=0
        self.brownIterator=0
        self.gridSize=Station1Positions
        self.tubes=[Tube] * self.gridSize
        self.cam1Counter=0
        self.initTubes()
        self.isRefreshCamera1Results=True
        self.isGreenAvailable=False
        self.isOrangeAvailable=False
        self.isBrownAvailable=False
        self.isYellowAvailable=False
        self.isRedAvailable=False
        self.isCRedAvailable=False
        self.cameraTimer = Timer()

    def initTubes(self):        
        for i in range(self.gridSize):
            self.tubes[i]=Tube(i)

    async def initGrids(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        self.grid=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
        initlogger.info("Grid locations Station:{0}".format(self.name))
        for tube in self.tubes:
            tube.location=self.grid.get_target_x_y(self.tubes.index(tube)+1)
            tube.type=await self.getTubeType(self.tubes.index(tube)+1)
            initlogger.info("Index,location :{0}:{1}".format(self.tubes.index(tube)+1,tube.location))
        await self.startTimer()

    async def getIndex(self,location):
        for tube in self.tubes:
            if tube.location== location:
                return self.tubes.index(tube)
        
    async def getTubeType(self,index):
        if(index >=1 and index <=60):
            return TubeType.SMALL
        elif(index>=61 and index<=90):
            return TubeType.BIG
        else:
            return TubeType.NONE
        
    async def startTimer(self):
        self.cameraTimer.set_alarm(900, self.setRefreshFlag)

    async def setRefreshFlag(self):
        jobslogger.info("Camera1 flag set by timer.")
        self.isRefreshCamera1Results = True
        await self.startTimer()

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
        self.isRedAvailable = any(Color(int(row["color"])) == Color.RED for row in rows)
        self.isCRedAvailable = any(Color(int(row["color"])) == Color.CRED for row in rows)
        if self.isGreenAvailable or self.isOrangeAvailable or self.isBrownAvailable or self.isYellowAvailable or self.isRedAvailable or self.isCRedAvailable:
            self.cam1Counter=0            
        else:
            self.cam1Counter+=1
        if self.cam1Counter == 3:
            self.isRefreshCamera1Results = False
            initlogger.info("Stopped hitting V.Q400 for cam1 results")                

    async def getNextEmergencyGreenTube(self):
        for i in range(len(emergencyPositions)):
            emergencyTube = self.tubes[emergencyPositions[i]]
            if(emergencyTube.color==Color.GREEN):
                jobslogger.info("Emergency {0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.greenIterator))
                self.emergencyCentrifugeIterator=i+1
                emergencyTube.color = Color.NONE
                emergencyTube.type = TubeType.SMALL
                return emergencyTube
        return None
    
    async def getNextEmergencyOrangeYellowTube(self):
        for i in range(len(emergencyPositions)):
            emergencyTube = self.tubes[emergencyPositions[i]]
            if(emergencyTube.color==Color.ORANGE or emergencyTube.color==Color.YELLOW):
                jobslogger.info("Emergency {0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.greenIterator))
                self.emergencyCentrifugeIterator=i+1
                emergencyTube.color = Color.NONE
                emergencyTube.type = TubeType.SMALL
                return emergencyTube
        return None
    
    async def getNextEmergencyBrownTube(self):
        for i in range(len(emergencyPositions)):
            emergencyTube = self.tubes[emergencyPositions[i]]
            if(emergencyTube.color==Color.BROWN):
                jobslogger.info("Emergency {0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.greenIterator))
                self.emergencyCentrifugeIterator=i+1
                emergencyTube.color = Color.NONE
                emergencyTube.type = TubeType.BIG
                return emergencyTube
        return None
    
    async def getNextEmergencyRedTube(self):
        for i in range(len(emergencyPositions)):
            emergencyTube = self.tubes[emergencyPositions[i]]
            if(emergencyTube.color==Color.RED or emergencyTube.color==Color.CRED):
                jobslogger.info("Emergency {0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.greenIterator))
                self.emergencyRedIterator=i+1
                emergencyTube.color = Color.NONE
                emergencyTube.type = TubeType.SMALL
                return emergencyTube
        return None
    
    async def setCentrifugeEmergencyIterator(self, counter):
        self.emergencyCentrifugeIterator=counter

    async def isFilledWithCentrifugeEmergencyTubes(self):
        if self.emergencyCentrifugeIterator > 0:
            return True
        return False
    
    async def setRedEmergencyIterator(self, counter):
        self.emergencyRedIterator=counter

    async def isFilledWithRedEmergencyTubes(self):
        if self.emergencyRedIterator > 0:
            return True
        return False
    
    async def getNextGreenTube(self):        
        # positions:list=list(range(self.greenIterator,self.gridSize))
        # positions.extend(list(range(0,self.greenIterator)))
        for i in range(self.gridSize):
            self.greenIterator=i+1
            if not i in emergencyPositions:
                if(self.tubes[i].color==Color.GREEN):
                    jobslogger.info("{0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.greenIterator))
                    self.tubes[i].color = Color.NONE
                    self.tubes[i].type = TubeType.SMALL
                    return self.tubes[i]
        return None

    async def getNextOrangeYellowTube(self):        
        # positions:list=list(range(self.orangeIterator,self.gridSize))
        # positions.extend(list(range(0,self.orangeIterator)))
        for i in range(self.gridSize):
            self.orangeIterator=i+1
            if not i in emergencyPositions:
                if(self.tubes[i].color==Color.ORANGE):
                    jobslogger.info("{0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.orangeIterator))
                    self.tubes[i].color = Color.NONE
                    self.tubes[i].type = TubeType.SMALL
                    return self.tubes[i]
                if(self.tubes[i].color==Color.YELLOW):
                    jobslogger.info("{0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.orangeIterator))
                    self.tubes[i].color = Color.NONE
                    self.tubes[i].type = TubeType.SMALL
                    return self.tubes[i]
        return None
    
    async def getNextBrownTube(self):        
        # positions:list=list(range(self.brownIterator,self.gridSize))
        # positions.extend(list(range(0,self.brownIterator)))
        for i in range(self.gridSize):
            self.brownIterator=i+1
            if not i in emergencyPositions:
                if(self.tubes[i].color==Color.BROWN):
                    jobslogger.info("{0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.brownIterator))
                    self.tubes[i].color = Color.NONE
                    self.tubes[i].type = TubeType.BIG
                    return self.tubes[i]
        return None
    
    async def getNextRedTube(self):        
        # positions:list=list(range(self.redIterator,self.gridSize))
        # positions.extend(list(range(0,self.redIterator)))
        for i in range(self.gridSize):
            self.redIterator=i+1
            if self.tubes[i].color==Color.RED or self.tubes[i].color==Color.CRED:
                jobslogger.info("{0} tube picked from {1} at index {2} ".format(self.tubes[i].color.name,self.name,self.redIterator))
                self.tubes[i].color = Color.NONE
                self.tubes[i].type = TubeType.SMALL
                return self.tubes[i]
        return None
