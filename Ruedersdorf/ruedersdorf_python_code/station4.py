from stations import Station, Tube
from logger import jobslogger


class Station4(Station):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.tube=Tube(0)

    #to check with camera 2
    async def updateGrid(self,tube):
        jobslogger.info("{0} tube is at {1}".format(tube.color.name,self.name)) 
        self.tube.color=tube.color
        self.tube.type=tube.type
    