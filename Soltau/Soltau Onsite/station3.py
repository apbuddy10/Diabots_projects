from logger import initlogger,jobslogger,timerlogger
from machine import Machine, MachineStatus
from grids_v2 import  Grid
from stations import processQueue, StationMachine, Tube
from settings import Color, Settings, Station3Size
from interface_board import Board, Mouse, board_by_id, Keyboard
from vq400connector import conn_Q400
import asyncio


class Station3(StationMachine):
    def __init__(self,name,jobs): 
        super().__init__(name,jobs)
        self.name = name
        self.status:MachineStatus=MachineStatus.Off
        self.grid:Grid
        self.counter:int=0
        self.gridSize:int=Station3Size
        self.tubes:list[Tube]=[None] * self.gridSize
        self.machine:Machine=Machine("Compact Max ",Settings.coagulation_run_time)
        self.initTubes()
        self.iterator:int=0
        self.isDoorOpened=False
        self.stn3_status_window = False
        self.keyboard = board_by_id(8)
        self.mouse = board_by_id(8)
        
    def initTubes(self):        
        for i in range(self.gridSize):
            self.tubes[i]=Tube(i)

    async def initGrids(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        await self.keyboard.check_connection()
        self.grid=Grid(ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)        
        initlogger.info("Grid locations Station3:{0}".format(self.name))
        for tube in self.tubes:
            tube.location=self.grid.get_target_x_y(self.tubes.index(tube)+1)
            initlogger.info("Index,location :{0}:{1}".format(self.tubes.index(tube)+1,tube.location))

    async def resetTubes(self):
        await self.setStatus(MachineStatus.On)
        self.iterator=0
        self.counter=0
        for tube in self.tubes:
            tube.color=Color.NONE      

    #this station as target
    async def updateGrid(self,color):
        self.tubes[self.counter].color=color
        self.counter+=1
        jobslogger.info("{0} tube placed in {1} at index {2} ".format(color.name,self.name,self.counter))
        if self.counter == self.gridSize:
            await self.setMachineFilled()

    async def setMachineFilled(self):
        if self.counter > 0:
            await self.setStatus(MachineStatus.Filled)
            jobslogger.info("{0} machine is filled with tubes".format(self.name)) 
            return True
        return False

    #this station as target
    async def getNextLocation(self):
        if self.counter < self.gridSize:            
            tube=self.tubes[self.counter]
            return tube.location
        return None
    
    async def isAvailable(self):
        if self.counter < self.gridSize and await self.getStatus() == MachineStatus.On:
            return True
        return False    
        
    async def isFirstTube(self):
        return self.counter == 0

    #this station as source
    async def getNextTubeToArchiv(self):
        if self.iterator < self.counter :
            if self.iterator==0 and not self.isDoorOpened:
                await self.openDoor()
            if self.isDoorOpened:
                tube=self.tubes[self.iterator]
                self.iterator+=1
                jobslogger.info("{0} tube picked from {1} at index {2} ".format(tube.color.name,self.name,self.iterator))                  
                return tube      
        return None
    
    async def getIterator(self):
        return self.iterator
    
    async def currentBatchEmpty(self):
        if self.machine.status == MachineStatus.Completed and self.iterator == self.counter:
            jobslogger.info("{0} made empty".format(self.name)) 
            await self.resetTubes()            
            return True
        return False

    def getRuntime(self,tubeCount:int):       
        runTime:str=""
        match tubeCount:
            case 1|2:
                runTime= "14:00"
            case 3|4:
                runTime= "16:00"
            case 5|6:
                runTime= "18:00"
            case 7|8:
                runTime= "20:00"
        if tubeCount > 8:
            runTime= "30:00"
        # runTime= "2:00"
        if runTime!="":
            #convert to seconds
            mm, ss = runTime.split(':')
            return int(mm) * 60 + int(ss)     
        return self.machine.runTime

    async def startMachine(self):
        self.setRuntime(self.getRuntime(self.counter))    
        # jobId=self.jobs[3].jobId
        # await processQueue.enqueue([jobId,jobId])
        # processQueue.destLocation.extend([[0,0,0,0,0,0],[0,0,0,0,0,0]])
        # close door
        await self.closeDoor()
        # await asyncio.sleep(1)
        # Close door new
        # await self.mouse.mouse.moveAbs(250,330)
        # await self.mouse.mouse.click()
        # await asyncio.sleep(1)
        # await self.mouse.mouse.moveAbs(560,330)
        # await self.mouse.mouse.click()
        # await asyncio.sleep(1)
        # await self.keyboard.keyboard.down(Keyboard.KEY_CODES.KEY_ENTER)
        # await self.keyboard.keyboard.up(Keyboard.KEY_CODES.KEY_ENTER)
        
        jobslogger.info("{0} machine started".format(self.name)) 
        await self.setStatus(MachineStatus.Running)
        self.isDoorOpened=False
        await self.startRuntimeAlarm()
        return True
    
    #to start and stop couglation machine
    async def getStation3StartMachineJob(self):
        # if not self.isInitialized:
        #     return False
        if await self.getStatus() == MachineStatus.Filled:            
            return await self.startMachine()       
        return False
    
    async def checkStatusWindow(self):
        if not self.stn3_status_window:
            # Commands here
            jobslogger.info("Compact Max status window opened") 
            self.stn3_status_window = True
    
    async def closeDoor(self):
        if self.isDoorOpened:
            count = 0
            while (count < 3):
                await self.keyboard.keyboard.down(Keyboard.KEY_CODES.KEY_ESCAPE)
                await self.keyboard.keyboard.up(Keyboard.KEY_CODES.KEY_ESCAPE)
                jobslogger.info("Compact Max key pressed in close: KEY_ESCAPE")
                await asyncio.sleep(10)
                await self.keyboard.keyboard.down(Keyboard.KEY_CODES.KEY_ENTER)
                await self.keyboard.keyboard.up(Keyboard.KEY_CODES.KEY_ENTER)
                jobslogger.info("Compact Max key pressed in close: KEY_ENTER")
                close_status = await conn_Q400.q400_execute_cam2(24)
                jobslogger.info("Compact Max close, close_status: {0}".format(close_status))
                if close_status == 1:
                    jobslogger.info("{0} door closed".format(self.name))
                    self.isDoorOpened=False
                    self.stn3_status_window = False
                    break
                else:
                    jobslogger.info("{0} door closing failed".format(self.name))
                    count = count + 1
            jobslogger.info("{0} door closed forcibly".format(self.name))
            self.isDoorOpened=False
            self.stn3_status_window = False

    async def openDoor(self):
        if not self.isDoorOpened:
            count = 0
            while (count < 3):
                special_status = await conn_Q400.q400_execute_cam2(26)
                jobslogger.info("Compact Max special_status: {0}".format(special_status))
                if special_status == 0:
                    close_status = await conn_Q400.q400_execute_cam2(24)
                    jobslogger.info("Compact Max close_status: {0}".format(close_status))
                    if close_status == 1:
                        await self.keyboard.keyboard.down(Keyboard.KEY_CODES.KEY_ESCAPE)
                        await self.keyboard.keyboard.up(Keyboard.KEY_CODES.KEY_ESCAPE)
                        jobslogger.info("Compact Max key pressed after close success: KEY_ESCAPE")
                        await asyncio.sleep(10)
                    dd_status = await conn_Q400.q400_execute_cam2(25)
                    jobslogger.info("Compact Max dd_status: {0}".format(dd_status))
                    if dd_status == 2 or dd_status == 1:
                        await self.keyboard.keyboard.down(Keyboard.KEY_CODES.KEY_ESCAPE)
                        await self.keyboard.keyboard.up(Keyboard.KEY_CODES.KEY_ESCAPE)
                        jobslogger.info("Compact Max key pressed after dd success: KEY_ESCAPE")
                        await asyncio.sleep(10)
                        await self.keyboard.keyboard.down(Keyboard.KEY_CODES.KEY_F1)
                        await self.keyboard.keyboard.up(Keyboard.KEY_CODES.KEY_F1)
                        jobslogger.info("Compact Max key pressed after dd success: KEY_F1")
                        await asyncio.sleep(10)
                    else:
                        await self.keyboard.keyboard.down(Keyboard.KEY_CODES.KEY_F1)
                        await self.keyboard.keyboard.up(Keyboard.KEY_CODES.KEY_F1)
                        jobslogger.info("Compact Max key pressed after dd failed: KEY_ESCAPE")
                        await asyncio.sleep(10)
                    open_status = await conn_Q400.q400_execute_cam2(23)
                    jobslogger.info("Compact Max open_status: {0}".format(open_status))
                    if open_status == 1:
                        jobslogger.info("{0} door opened".format(self.name))
                        jobId=self.jobs[4].jobId
                        await processQueue.enqueue([jobId,jobId])   
                        processQueue.destLocation.extend([[0,0,0,0,0,0],[0,0,0,0,0,0]])
                        self.isDoorOpened=True
                        break
                count = count + 1


# async def main():
#     keyboard = board_by_id(8)
#     mouse = board_by_id(8)
#     # await keyboard.check_connection()
#     # await mouse.check_connection()

#     for i in range(20):
#         # await mouse.mouse.moveAbs(250,330)
#         # await mouse.mouse.click()
#         # await asyncio.sleep(1)
#         # await mouse.mouse.moveAbs(560,330)
#         # await mouse.mouse.click()
#         # await asyncio.sleep(1)
#         # await mouse.mouse.moveAbs(560,130)
#         # await mouse.mouse.click()
#         # await asyncio.sleep(1)

#         await keyboard.keyboard.down(Keyboard.KEY_CODES.KEY_ESCAPE)
#         await keyboard.keyboard.up(Keyboard.KEY_CODES.KEY_ESCAPE)
#         await asyncio.sleep(1)
#         await keyboard.keyboard.down(Keyboard.KEY_CODES.KEY_F1)
#         await keyboard.keyboard.up(Keyboard.KEY_CODES.KEY_F1)
#         print("Door Open")
#         await asyncio.sleep(10)

#         # await mouse.mouse.moveAbs(250,330)
#         # await mouse.mouse.click()
#         # await asyncio.sleep(1)
#         # await mouse.mouse.moveAbs(560,330)
#         # await mouse.mouse.click()
#         # await asyncio.sleep(10)
#         # # await mouse.mouse.moveAbs(310,217)
#         # # await mouse.mouse.click()
#         # await keyboard.keyboard.down(Keyboard.KEY_CODES.KEY_ENTER)
#         # await keyboard.keyboard.up(Keyboard.KEY_CODES.KEY_ENTER)
        
#         await keyboard.keyboard.down(Keyboard.KEY_CODES.KEY_ESCAPE)
#         await keyboard.keyboard.up(Keyboard.KEY_CODES.KEY_ESCAPE)
#         await asyncio.sleep(1)
#         await keyboard.keyboard.down(Keyboard.KEY_CODES.KEY_ENTER)
#         await keyboard.keyboard.up(Keyboard.KEY_CODES.KEY_ENTER)


#         print("Enter clicked")
#         print("Door Close")
#         await asyncio.sleep(10)

#     # await mouse.mouse.moveAbs(310,217)
#     # await mouse.mouse.click()

# asyncio.run(main())
