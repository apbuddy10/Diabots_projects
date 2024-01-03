from enum import Enum
from logger import timerlogger
from timer import Timer

class MachineStatus(Enum):
    Off=0,
    On=1,
    Filled=2,
    Running=3
    Completed=4
    ReadyToUnload=5

class Machine:
    def __init__(self,name:str,runTime:int):
        self.name = name
        # self.initTime=initTime
        self.runTime=runTime
        # self.standbyTime=standbyTime
        self.status:MachineStatus=MachineStatus.Off
        # self.initTimer=Timer()        
        # self.standbyTimer=Timer()
        self.runTimeTimer=Timer()

    # async def setInitAlarm(self,callback):
    #     timerlogger.info("{0} initialization started. Time : {1}".format(self.name,self.initTime))
    #     self.initTimer.set_alarm(self.initTime,callback)

    # async def setStandbyAlarm(self,callback):
    #     timerlogger.info("{0} Standby timer started. Time : {1}".format(self.name,self.standbyTime))
    #     self.standbyTimer.set_alarm(self.standbyTime,callback)

    async def setRuntimeAlarm(self,callback):
        timerlogger.info("{0} Runtime timer started. Time : {1}".format(self.name,self.runTime))
        self.runTimeTimer.set_alarm(self.runTime,callback)

    async def setStatus(self,status:MachineStatus):
        self.status=status
    
    async def cancelTimers(self):
        # self.initTimer.cancel_alarm()
        # self.standbyTimer.cancel_alarm()
        self.runTimeTimer.cancel_alarm()
