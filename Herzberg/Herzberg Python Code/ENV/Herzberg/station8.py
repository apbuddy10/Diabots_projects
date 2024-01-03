from settings import Settings
from machine import Machine, MachineStatus
from stations import processQueue, StationMachine, Station
from logger import jobslogger
import urlib


class Station8(Station):

    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.machine:Machine=Machine("Cobas Pure Machine",Settings.chemistry_init_time,Settings.chemistry_run_time,Settings.chemistry_standby_time)  
        self.status:MachineStatus=MachineStatus.Off
        self.gridLocation:int=1
    
    async def setDestLocation(self,location):
        self.gridLocation=location

    async def prepareInitJobWithStatus(self,isOn):
        await self.setStatus(MachineStatus.On if isOn else MachineStatus.Off)

    async def setStatus(self,status:MachineStatus):
        self.status=status
    
    async def getStatus(self):
        return self.status
    
    # async def refreshStandbyAlarm(self):
    #     if await self.getStatus()==MachineStatus.Filled:
    #         await self.startMachine(6)
    #     else:
    #         await super().refreshStandbyAlarm()

    # def getRuntime(self,tubeCount:int):       
    #     runTime:str=""
    #     match tubeCount:
    #         case 1:
    #             runTime= "20:40"
    #         case 2|3:
    #             runTime= "23:00"
    #         case 4|5:
    #             runTime= "26:00"
    #         case 6|7:
    #             runTime= "48:00"
    #         case 8|9|10:
    #             runTime= "66:35"
    #     if tubeCount > 10:
    #         runTime= "66:35"
    #     if runTime!="":
    #         #convert to seconds
    #         mm, ss = runTime.split(':')
    #         return int(mm) * 60 + int(ss)     
    #     return self.machine.runTime

    # async def startMachine(self,tubeCount:int):
    #     self.setRuntime(self.getRuntime(tubeCount))
    #     jobId=self.jobs[3].jobId
    #     await processQueue.enqueue([jobId,jobId])
    #     jobslogger.info("{0} machine started".format(self.name)) 
    #     await self.setStatus(MachineStatus.Running)
    #     return True 
    
    # async def check_z(self, pose_received):
    #     assert type(pose_received) is dict
    #     pose = urlib.poseToList(pose_received)
    #     if pose[2]*1000 - 20 < -25 and pose[2]*1000 + 30 > -25:
    #         return 1
    #     elif pose[2]*1000 - 50 < 45 and pose[2]*1000 + 50 > 45:
    #         return 2
    #     return 0

    # async def add_x_y(self, pose_received, x, y):
    #     assert type(pose_received) is dict
    #     pose = urlib.poseToList(pose_received)
    #     pose_sent = [pose[0]+(x/1000), pose[1]+(y/1000),pose[2], pose[3], pose[4], pose[5]]
    #     return urlib.listToPose(pose_sent)