from settings import Settings
from machine import Machine, MachineStatus
from stations import StationMachine, processQueue
from logger import jobslogger


class Stn8Batch:
    def __init__(self):
        self.counter = 0
    
    async def updateGrid(self, tubesCount):
        self.counter = tubesCount
        jobslogger.info("Cobas Pure, Tubes in batch: {0}".format(tubesCount))
    
    # to move to Archive
    async def getTubesCount(self):
        return self.counter
    

class Station8(StationMachine):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.machine:Machine=Machine("Cobas Pure Machine ",Settings.chemistry_run_time) 
        self.status:MachineStatus=MachineStatus.Off
        self.batchCount = 10
        self.totalRacksCounter = 0
        self.batchCounter = 0
        self.batches = []
        self.initBatches()
    
    def initBatches(self):        
        for i in range(self.batchCount):
            batch=Stn8Batch()
            self.batches.append(batch)

    #this station as destination
    async def updateGrid(self, tubesCount):
        self.totalRacksCounter+=1
        if self.totalRacksCounter > Settings.Station8UnloadingAfter:
            batch=self.batches[self.batchCounter]
            jobslogger.info("{0} batch {1} filling".format(self.name,self.batchCounter+1))
            await batch.updateGrid(tubesCount)    

    async def incrementCounter(self):
        self.batchCounter = (self.batchCounter + 1) % self.batchCount

    def getRuntime(self):       
        runTime:str=""
        # match tubeCount:
        #     case 1:
        #         runTime= "1:00"
        #     case 2:
        #         runTime= "2:00"
        #     case 3:
        #         runTime= "2:00"
        #     case 4:
        #         runTime= "2:00"
        runTime= "20:00"
        if runTime!="":
            #convert to seconds
            mm, ss = runTime.split(':')
            return int(mm) * 60 + int(ss)     
        return self.machine.runTime
    
    async def startMachine(self):
        if self.batchCounter == self.batchCount-1:
            self.setRuntime(self.getRuntime())
            # jobId=self.jobs[4].jobId
            # await processQueue.enqueue([jobId,jobId])
            # processQueue.destLocation.extend([[0,0,0,0,0,0],[0,0,0,0,0,0]])
            jobslogger.info("{0} machine started".format(self.name)) 
            await self.setStatus(MachineStatus.Running)
            await self.startRuntimeAlarm()
            return True
        return False
    
    async def counterEqualsBatchCount(self):
        if self.batchCounter == self.batchCount-1:
            return True
        return False

    async def getFilledBatches(self):
        return self.batches