from grids_v2 import Grid
from stations import  processQueue,Station
from settings import BatchStatus, HolderStatus
from logger import jobslogger


class Station15(Station):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.holderStatus=HolderStatus.Filled 
        self.basketStatus=BatchStatus.Empty

    async def pickBasket(self):
        if self.holderStatus == HolderStatus.Filled and self.basketStatus == BatchStatus.Empty:
            jobslogger.info("Placed the basket in cobas pure machine, from first basket holder, station 15")
            await self.emptyHolder()
            jobslogger.info("First basket holder, station 15, is empty")
            return True
        return False
    
    async def placeBasket(self):
        if self.holderStatus == HolderStatus.Empty and self.basketStatus == BatchStatus.Empty:
            jobId=self.jobs[1].jobId
            await processQueue.enqueue([jobId,jobId])   
            processQueue.destLocation.extend([[0,0,0,0,0,0],[0,0,0,0,0,0]])      
            jobslogger.info("Picked the basket from cobas pure machine, and placed in first basket holder, station 15")
            await self.fillHolder()
            await self.fillBasket()
            jobslogger.info("First basket holder, station 15, is filled with basket and racks")
            return True
        return False
    
    async def slideRacks(self):
        if self.holderStatus == HolderStatus.Filled and self.basketStatus == BatchStatus.Filled:
            jobId=self.jobs[2].jobId
            await processQueue.enqueue([jobId,jobId]) 
            processQueue.destLocation.extend([[0,0,0,0,0,0],[0,0,0,0,0,0]])         
            jobslogger.info("Racks sliding from first basket holder, station 15, to first rack filled holder, station 17")
            await self.emptyBasket()
            jobslogger.info("First basket holder, station 15, is filled with basket and with no racks")
            return True
        return False
    
    async def fillHolder(self):
        if self.holderStatus == HolderStatus.Empty:
            self.holderStatus = HolderStatus.Filled

    async def emptyHolder(self):
        if self.holderStatus == HolderStatus.Filled:
            self.holderStatus = HolderStatus.Empty

    async def emptyBasket(self):
        if self.basketStatus == BatchStatus.Filled:
            self.basketStatus = BatchStatus.Empty
    
    async def fillBasket(self):
        if self.basketStatus == BatchStatus.Empty:
            self.basketStatus = BatchStatus.Filled
    
    async def getHolderStatus(self):
        return self.holderStatus

    
    

    