import asyncio
import interface_buffer
import socket
from datetime import datetime
import traceback

from station1 import Station1
from station2 import Station2
from station3 import Station3
from station4 import Station4
from station5 import Station5
from station6 import Station6
from station7 import Station7
from station8 import Station8
from station9 import Station9
from station10 import Station10
from station11 import Station11
from station14 import Station14
from station15 import Station15
from station16 import Station16
from station17 import Station17
from station18 import Station18

from filemanager import FileManager
from machine import MachineStatus
from settings import Settings, Color, HolderStatus
from stations import CommonError, Job, processQueue
from vq400connector import Vq400Connector
from logger import jobslogger,errorlogger
from axis7 import AxisConn_7
# from communicationManager import commManager
from sftpClass import sftpCommunication


class MainApp:
    def __init__(self):
        self.machines = {}
        self.conn_Q400=Vq400Connector(Settings.vq400host)
        self.lastPingTime=None
        self.initialize()
        self.fileManager=FileManager()
        self.axis7 = AxisConn_7(Settings.Axis7Host,Settings.Axis7Port)
        
        # print("Service is running... at {0} - {1}".format(Settings.systemip,Settings.systemport))      

    def  initialize(self):     
        self.initStations()
        self.isCameraClicked=False
        self.stn1_good = True
        self.ping_bad = False
        processQueue.reset()

    async def reset(self):
        try:
            await self.station3.cancelTimers()
            await self.station6.cancelTimers()
            await self.station7.cancelTimers()
            # await self.station6.resetConnections()                     
            self.initialize()
            # await commManager.connectToSkype()
            await self.setMachineStatus(0, True)
            # await self.testUnloading()
            await mainObj.axis7.reset(True)
            print("Robot (re)started at : {0}".format(str(datetime.now())))  
        except Exception as e: 
            errorlogger.exception(e)
            raise CommonError("Error occurred during reset")
    
    async def testUnloading(self):
        await self.station8.setStatus(MachineStatus.Running)
        # stn8batches = await self.station8.getFilledBatches()
        # tubesCount = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        # for i in range(10):  
        #     batch = stn8batches[i]          
        #     await batch.updateGrid(tubesCount[i])
        #     await self.station2.getNextLocationToPick()
        # await self.station17.setTubesCountInBatches(await self.station8.getFilledBatches())
        await self.station15.fillHolder()
        await self.station15.emptyBasket()
        # await self.station17.fillHolder()

        stn8batches = await self.station8.getFilledBatches()
        tubesCount = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        for i in range(10):
            await self.station2.getNextLocationToPick()
            await self.station2.getNextLocationToPlace()
        for i in range(10):  
            batch = stn8batches[i]          
            await batch.updateGrid(tubesCount[i])
            await self.station2.getNextLocationToPick()
        await self.station18.setTubesCountInBatches(await self.station8.getFilledBatches())
        await self.station16.fillHolder()
        await self.station16.emptyBasket()
        await self.station18.fillHolder()

    #station names with priorities
    def initStations(self):
        self.station1=Station1("camera1",
        [
            Job(10,"Initial"),
            Job(11,"pick"),
            Job(12,"place")
        ])
        self.station2=Station2("Cobas Pure racks",
        [
            Job(20,"initial"),
            Job(21,"pick"),
            Job(22,"place")  
        ])
        self.station3=Station3("Compact Max ",
        [
            Job(30,"Initial"),
            Job(31,"pick"),
            Job(32,"place"),
            Job(33,"close door and start"),
            Job(34,"open door")
        ])
        self.station4=Station4("camera2",
        [
            Job(40,"Initial"),
            Job(41,"pick or place")
        ])
        self.station5=Station5("centrifuge racks",
        [
            Job(50,"Initial"),            
            Job(51,"pick"),
            Job(52,"place"),
            Job(53,"start"),
            Job(54,"pick counter"),
            Job(55,"none"),
        ])
        self.station6=Station6("centrifuge machine",
        [
            Job(60,"Initial"),
            Job(61,"pick"),
            Job(62,"place"),
            Job(63,"start"),
            Job(64,"stop"),
            Job(65,"refresh standby"),
        ])
        self.station7=Station7("Sysmex machine",
        [
            Job(70,"Initial"),
            Job(71,"pick rack"),
            Job(72,"place rack")            
        ])
        self.station8=Station8("Cobas pure machine",
        [
            Job(80,"Initial"),
            Job(81,"pick basket"),
            Job(82,"place basket"),
            Job(83,"place rack"),
            Job(84, "Start Machine, run timer")
        ])
        self.station9=Station9("Sysmex rack holders",
        [
            Job(90,"Initial"),
            Job(91,"pick rack"),
            Job(92,"place rack"),
            Job(93,"pick tube"),
            Job(94,"place tube")
        ])
        self.station10=Station10("Failed plate",
        [
            Job(100,"Initial"),
            Job(101,"pick"),
            Job(102,"place"),
            Job(103,"show bin filled")
        ])
        self.station11=Station11("Archive",
        [
            Job(110,"Initial"),
            Job(111,"pick"),
            Job(112,"place"),
            Job(113,"show Archiv filled")
        ])
        self.station14=Station14("Cobas pure rack holder ",
        [
            Job(140,"Initial"),
            Job(141,"pick rack"),
            Job(142,"place rack"),
            Job(143,"place tube")
        ])
        self.station15=Station15("Cobas pure first basket holder ",
        [
            Job(151,"pick basket"),
            Job(152,"place basket"),
            Job(153,"slide racks"),
        ])
        self.station16=Station16("Cobas pure second basket holder ",
        [
            Job(161,"pick basket"),
            Job(162,"place basket"),
            Job(163,"slide racks"),
        ])
        self.station17=Station17("Cobas pure first filled rack holder ",
        [
            Job(171,"pick rack"),
            Job(172,"pick tube"),
        ])
        self.station18=Station18("Cobas pure second filled rack holder ",
        [
            Job(181,"pick rack"),
            Job(182,"pick tube"),
        ])
    
    async def setMachineStatus(self,machineId,isOn):
        try:
            match machineId: 
                case Settings.macId_all:                    
                    await self.station7.prepareInitJobWithStatus(isOn)        
                    await self.station3.prepareInitJobWithStatus(isOn)
                    await self.station8.prepareInitJobWithStatus(isOn)
                    await self.station6.prepareInitJobWithStatus(isOn)
                case Settings.macId_coagulation:
                    await self.station3.prepareInitJobWithStatus(isOn)       
                case Settings.macId_chemistry:
                    await self.station8.prepareInitJobWithStatus(isOn)
                case Settings.macId_centrifuge:
                    await self.station6.prepareInitJobWithStatus(isOn)
                    if not isOn:
                        await self.station8.prepareInitJobWithStatus(isOn)
                        await self.station3.prepareInitJobWithStatus(isOn)
                case Settings.macId_haematology:
                    await self.station7.prepareInitJobWithStatus(isOn)
        except Exception as e:
            errorlogger.exception(e)
            raise CommonError("Error occurred during set machine status")

    async def getResultsFromCamera1(self):
        rows=await self.conn_Q400.q400_execute_cam1(1)
        self.lastPingTime=None
        return rows

    async def modifyRefreshFlag(self):
        if (((await self.station3.getStatus() == MachineStatus.On) and self.station1.isGreenAvailable and await self.station5.isAvailableForGreen()) or 
            ((await self.station8.getStatus() != MachineStatus.Off) and (self.station1.isOrangeAvailable or self.station1.isBrownAvailable or
            self.station1.isYellowAvailable or self.station1.isYellow2Available or self.station1.isYellow3Available) and await self.station5.isAvailableForOrange()) or 
            (self.station1.isRedAvailable and await self.station9.isAvailable())):
            self.station1.isRefreshCamera1Results=True
        else:
            self.station1.isRefreshCamera1Results=False

    async def refreshCamera1Results(self):
        self.stn1_good = True
        if self.station1.isRefreshCamera1Results and not self.isCameraClicked:            
            results=await self.getResultsFromCamera1()
            await self.station1.updateGrid(results)            
            self.isCameraClicked=True
        await self.modifyRefreshFlag()

    async def getStation5GridLocations(self):
        locations=processQueue.stn5GridLocations
        processQueue.stn5GridLocations=[]
        jobslogger.info("Sent locations Source,Destination: {0}".format(locations))
        return locations
    
    async def getCurrentLocation(self):
        # print(processQueue.destLocation)
        srcLoc=processQueue.destLocation.pop(0)
        destLoc=processQueue.destLocation.pop(0)
        location = [srcLoc, destLoc]
        # print(location)
        # processQueue.destLocation=[]
        jobslogger.info("Sent locations Source,Destination: {0}".format(location))
        return location

    async def getJob(self):
        try:            
            if not(await processQueue.isEmpty()) or await self.checkAndPrepareForJobs():            
                dest= await processQueue.dequeue()
                if dest is not None:
                    jobslogger.info("Sent Jobs Source,Destination: {0}".format(dest))
                    return dest
        except Exception as e: 
            traceback.print_exc()
            errorlogger.exception(e)
            processQueue.destLocation=[]
            raise CommonError("Unexpected error occured. Please check logs!")
        return [0,0]

    async def checkAndPrepareForJobs(self):
        self.isCameraClicked = False
        if await self.station3.getStation3StartMachineJob():
            return True
        if await self.getStation8_To_15_Job():
            return True
        if await self.getStation8_To_16_Job():
            return True
        if await self.getStation15_To_8_Job():
            return True
        if await self.getStation16_To_8_Job():
            return True
        if await self.getStation15_To_17_Job():
            return True
        if await self.getStation16_To_18_Job():
            return True
        if await self.getStation7_To_9_Job():
            return True
        if await self.getStation9_To_7_Job():
            return True      
        if await self.getStation1_To_4_9_Job():
            return True
        if await self.getStation3_To_11_Job():
            return True
        if await self.getStation5_To_4_3_Job():
            return True
        if await self.getStation14_To_8_Job():
            return True
        if await self.getStation2_14_Job():
            return True        
        if await self.getStation5_To_4_14_Job():
            return True
        if await self.station5.getNextCounterTube():
            return True
        if await self.getStation6_To_5_Job():
            return True
        if await self.getStation5_To_6_Job():
            return True
        if await self.getStation1_To_4_3_Job():
            return True
        if await self.getStation1_To_4_14_Job():
            return True
        if await self.getStation9_To_11_Job():
            return True
        if await self.getStation17_To_2_Job():
            return True
        if await self.getStation18_To_2_Job():
            return True
        if await self.getStation17_To_11_Job():
            return True
        if await self.getStation18_To_11_Job():
            return True
        return False
    
    # from cobas pure racks storage to cobas pure rack holder
    async def getStation2_14_Job(self):        
        if await self.station8.getStatus() == MachineStatus.Filled and await self.station14.getHolderStatus() == HolderStatus.Empty:
            location = await self.station2.getNextLocationToPick()
            if location is None:
                return False
            srcJobId = self.station2.jobs[1].jobId
            destJobId = self.station14.jobs[2].jobId                    
            await processQueue.enqueue([srcJobId,destJobId])
            processQueue.destLocation.extend([location,location])
            await self.station14.fillHolder()
            jobslogger.info("Cobas pure rack moved from {0} to {1}".format(self.station2.name,self.station14.name))
            return True
        return False
    
    # from cobas pure rack holder to cobas pure machine
    async def getStation14_To_8_Job(self):
        if await self.station8.getStatus() == MachineStatus.Filled:
            res = await self.station14.placeRackInMachine()
            if res:
                if await self.station8.counterEqualsBatchCount():
                    await self.station8.startMachine()
                    if await self.station15.getHolderStatus() == HolderStatus.Empty and await self.station17.getHolderStatus() == HolderStatus.Empty:
                        await self.station17.setTubesCountInBatches(await self.station8.getFilledBatches())
                    if await self.station16.getHolderStatus() == HolderStatus.Empty and await self.station18.getHolderStatus() == HolderStatus.Empty:
                        await self.station18.setTubesCountInBatches(await self.station8.getFilledBatches())                    
                await self.station8.incrementCounter()
            return res
        return False
    
    # from cobas pure machine to basket holder
    async def getStation8_To_15_Job(self):
        if await self.station8.getStatus() == MachineStatus.Completed:            
            if await self.station15.placeBasket():
                await self.station8.setStatus(MachineStatus.On)
                return True
        return False
    
    # from cobas pure machine to basket holder 2
    async def getStation8_To_16_Job(self):
        if await self.station8.getStatus() == MachineStatus.Completed:            
            if await self.station16.placeBasket():
                await self.station8.setStatus(MachineStatus.On)
                return True
        return False
    
    # from basket holder 1 to cobas pure machine
    async def getStation15_To_8_Job(self):
        if await self.station8.getStatus() == MachineStatus.On:            
            if await self.station15.pickBasket():
                srcJob=self.station15.jobs[0].jobId
                destJob=self.station8.jobs[2].jobId
                await processQueue.enqueue([srcJob,destJob])  
                processQueue.destLocation.extend([[0,0,0,0,0,0],[0,0,0,0,0,0]])   
                await self.station8.setStatus(MachineStatus.Filled)
                return True
        return False
    
    # from basket holder 2 to cobas pure machine
    async def getStation16_To_8_Job(self):
        if await self.station8.getStatus() == MachineStatus.On:            
            if await self.station16.pickBasket():
                srcJob=self.station16.jobs[0].jobId
                destJob=self.station8.jobs[2].jobId
                await processQueue.enqueue([srcJob,destJob])  
                processQueue.destLocation.extend([[0,0,0,0,0,0],[0,0,0,0,0,0]])   
                await self.station8.setStatus(MachineStatus.Filled)
                return True
        return False
    
    # sliding racks from basket holder 1
    async def getStation15_To_17_Job(self):
        if (await self.station8.getStatus() == MachineStatus.Filled or await self.station8.getStatus() == MachineStatus.Running) and await self.station17.getHolderStatus() == HolderStatus.Empty:            
            if await self.station15.slideRacks():
                await self.station17.fillHolder()
                return True
        return False
    
    # sliding racks from basket holder 2
    async def getStation16_To_18_Job(self):
        if (await self.station8.getStatus() == MachineStatus.Filled or await self.station8.getStatus() == MachineStatus.Running) and await self.station18.getHolderStatus() == HolderStatus.Empty:            
            if await self.station16.slideRacks():
                await self.station18.fillHolder()
                return True
        return False

    # from Cobas pure first filled rack holder to racks storage
    async def getStation17_To_2_Job(self):
        if await self.station8.getStatus() == MachineStatus.Filled or await self.station8.getStatus() == MachineStatus.Running:
            if await self.station17.getHolderStatus() == HolderStatus.Filled:
                if await self.station17.currentRackEmpty():
                    destLoc = await self.station2.getNextLocationToPlace()
                    if destLoc is None:
                        return False
                    srcJobId=self.station17.jobs[0].jobId
                    destJobId=self.station2.jobs[2].jobId
                    await processQueue.enqueue([srcJobId,destJobId])  
                    srcLoc = await self.station17.getNextRackLocation()                    
                    processQueue.destLocation.extend([srcLoc,destLoc])
                    jobslogger.info("Picked the rack from first filled rack holder: loc {0} and placed in Racks storage at {1}".format(srcLoc,destLoc)) 
                    return True
        return False
    
    # from Cobas pure second filled rack holder to racks storage
    async def getStation18_To_2_Job(self):
        if await self.station8.getStatus() == MachineStatus.Filled or await self.station8.getStatus() == MachineStatus.Running:
            if await self.station18.getHolderStatus() == HolderStatus.Filled:
                if await self.station18.currentRackEmpty():
                    destLoc = await self.station2.getNextLocationToPlace()
                    if destLoc is None:
                        return False
                    srcJobId=self.station18.jobs[0].jobId
                    destJobId=self.station2.jobs[2].jobId
                    await processQueue.enqueue([srcJobId,destJobId])  
                    srcLoc = await self.station18.getNextRackLocation()
                    processQueue.destLocation.extend([srcLoc,destLoc])
                    jobslogger.info("Picked the rack from second filled rack holder: loc {0} and placed in Racks storage at {1}".format(srcLoc,destLoc)) 
                    return True
        return False

    # from Cobas pure first filled rack holder to Archiv
    async def getStation17_To_11_Job(self):         
        if await self.station8.getStatus() == MachineStatus.Filled or await self.station8.getStatus() == MachineStatus.Running:
            if await self.station17.getHolderStatus() == HolderStatus.Filled:
                if not await self.station17.currentRackEmpty():
                    srcJobId = self.station17.jobs[1].jobId
                    destJobId = self.station11.jobs[2].jobId
                    await processQueue.enqueue([srcJobId,destJobId])  
                    srcLoc = await self.station17.getNextTubeLocation()
                    destLoc = await self.station11.getNextLocation()
                    processQueue.destLocation.extend([srcLoc,destLoc])
                    await self.station11.updateGrid(Color.ORANGE)
                    jobslogger.info("Picked the tube from first filled rack holder: loc {0} and placed in Archiv at {1}".format(srcLoc,destLoc)) 
                    return True
        return False
    
    # from Cobas pure second filled rack holder to Archiv
    async def getStation18_To_11_Job(self):         
        if await self.station8.getStatus() == MachineStatus.Filled or await self.station8.getStatus() == MachineStatus.Running:
            if await self.station18.getHolderStatus() == HolderStatus.Filled:
                if not await self.station18.currentRackEmpty():
                    srcJobId = self.station18.jobs[1].jobId
                    destJobId = self.station11.jobs[2].jobId
                    await processQueue.enqueue([srcJobId,destJobId])  
                    srcLoc = await self.station18.getNextTubeLocation()
                    destLoc = await self.station11.getNextLocation()
                    processQueue.destLocation.extend([srcLoc,destLoc])
                    await self.station11.updateGrid(Color.ORANGE)
                    jobslogger.info("Picked the tube from second filled rack holder: loc {0} and placed in Archiv at {1}".format(srcLoc,destLoc)) 
                    return True
        return False

    # from Sysmex racks to Sysmex machine
    async def getStation9_To_7_Job(self):
        if await self.station7.getStatus() == MachineStatus.On:
            location=await self.station9.getLocationOfFilledJob()
            if location is not None:        
                srcJobId=self.station9.jobs[1].jobId
                destJobId=self.station7.jobs[2].jobId
                await processQueue.enqueue([srcJobId,destJobId])
                processQueue.destLocation.extend([location,location])                
                jobslogger.info("rack moved from {0} to {1}".format(self.station9.name,self.station7.name)) 
                await self.station7.setStatus(MachineStatus.Filled)
                return await self.getStation7StartMachineJob()
                return True        
        return False
    
    # red tubes from camera1 to camera2 
    async def getStation1_To_4_9_Job(self):
        if await self.station9.isAvailable():            
            await self.refreshCamera1Results()
            tube=await self.station1.getNextRedTube()
            # if tube is None:
            if tube is None and await self.station7.isAvailable():
                if await self.station9.currentBatchFilled():
                    return await self.getStation9_To_7_Job()
            if tube is not None:
                srcJobId=self.station1.jobs[1].jobId 
                destJobId=self.station4.jobs[1].jobId 
                await processQueue.enqueue([srcJobId,destJobId]) 
                processQueue.destLocation.extend([tube.location,tube.location])
                await self.station4.updateGrid(tube)
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station1.name,self.station4.name))
                return True
        else:
            if await self.station9.currentBatchFilled():
                return await self.getStation9_To_7_Job()
        return False
    
    #from Sysmex racks to archive
    async def getStation9_To_11_Job(self):
        tube=await self.station9.getNextTubeToArchiv()
        if tube is None:    
            if await self.station9.currentBatchEmpty():
                return await self.getStation1_To_4_9_Job()
        if tube is not None:
            srcJobId=self.station9.jobs[3].jobId 
            destJobId=self.station11.jobs[2].jobId 
            await processQueue.enqueue([srcJobId,destJobId]) 
            location=await self.station11.getNextLocation()
            processQueue.destLocation.extend([tube.location,location])
            await self.station11.updateGrid(tube.color)
            jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station9.name,self.station11.name)) 
            return True
        return False
    
    # from coagulation machine to archive
    async def getStation3_To_11_Job(self):
        if await self.station3.getStatus() == MachineStatus.Completed:
            # await self.station3.checkStatusWindow()
            if await self.station3.getIterator() == 0:
                stn3_status = await self.getCompactMaxStatus(22)
                jobslogger.info("Compact Max Process Execution Status : {0}".format(stn3_status)) 
                if not stn3_status:
                    return False
            tube=await self.station3.getNextTubeToArchiv()
            if tube is None:    
                if await self.station3.currentBatchEmpty():
                    await self.station3.closeDoor()
                    return await self.getStation5_To_4_3_Job()
            if tube is not None:
                srcJobId=self.station3.jobs[1].jobId 
                destJobId=self.station11.jobs[2].jobId 
                await processQueue.enqueue([srcJobId,destJobId])
                location=await self.station11.getNextLocation()
                processQueue.destLocation.extend([tube.location,location])     
                await self.station11.updateGrid(tube.color)
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station3.name,self.station11.name)) 
                return True
        return False
    
    async def getCompactMaxStatus(self,group:int):
        res = await self.conn_Q400.q400_execute_cam2(group)
        return res
    
    # centrifuge racks to camera2 only Green tubes
    async def getStation5_To_4_3_Job(self):
        # if not(self.station3.isInitialized):
        #     return False
        tube=None
        if await self.station3.isAvailable():
            tube=await self.station5.getNextGreenTube()
            if tube is None:
                if await self.station3.setMachineFilled():                    
                    return await self.station3.getStation3StartMachineJob()
            else:
                if not self.station3.isDoorOpened:
                    await self.station3.openDoor()
                srcJobId=self.station5.jobs[1].jobId 
                destJobId=self.station4.jobs[1].jobId 
                processQueue.destLocation.extend([tube.location,tube.location])            
                await processQueue.enqueue([srcJobId,destJobId])                       
                await self.station4.updateGrid(tube)
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station5.name,self.station4.name))
                return True        
        return False

    # centrifuge racks to camera2 only orange tubes
    async def getStation5_To_4_14_Job(self):
        tube=None        
        if await self.station14.isAvailable():
            tube = await self.station5.getNextOrangeTube()
            if tube is None:
                tubesCount = await self.station14.fillTubesGrid()
                if tubesCount != -1:
                    await self.station8.updateGrid(tubesCount)
                    # if await self.station8.startMachine(tubesCount):
                    # if await self.station8.counterEqualsBatchCount():
                    #     if await self.station17.getHolderStatus() == HolderStatus.Empty:
                    #         await self.station17.setTubesCountInBatches(await self.station8.getFilledBatches())
                    #     if await self.station18.getHolderStatus() == HolderStatus.Empty:
                    #         await self.station18.setTubesCountInBatches(await self.station8.getFilledBatches())
                    return await self.getStation14_To_8_Job()
            else:
                srcJobId=self.station5.jobs[1].jobId 
                destJobId=self.station4.jobs[1].jobId 
                processQueue.destLocation.extend([tube.location,tube.location])            
                await processQueue.enqueue([srcJobId,destJobId])                       
                await self.station4.updateGrid(tube)
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station5.name,self.station4.name))
                return True        
        return False
    
    #centrifuge racks to centrifuge machine
    async def getStation6_To_5_Job(self):
        if not(self.station6.isInitialized):
            return False
        if await self.station6.isCompleted():
            locations=await self.station5.getRunningBatchLocations()
            if locations is not None:
                srcJobId=self.station6.jobs[1].jobId 
                destJobId=self.station5.jobs[2].jobId 
                # processQueue.stn5GridLocations.extend(locations)   
                processQueue.destLocation.extend([locations, locations])            
                await processQueue.enqueue([srcJobId,destJobId])                       
                await self.station6.setStatus(MachineStatus.On)
                jobslogger.info("batch moved from {0} to {1}".format(self.station6.name,self.station5.name))
                return True
        return False
    
    #centrifuge racks to centrifuge machine
    async def getStation5_To_6_Job(self):
        if not(self.station6.isInitialized):
            return False
        if await self.station6.isAvailable():
            locations=await self.station5.getFilledBatchLocations()
            if locations is not None:
                srcJobId=self.station5.jobs[1].jobId 
                destJobId=self.station6.jobs[2].jobId 
                # processQueue.stn5GridLocations.extend(locations)      
                processQueue.destLocation.extend([locations, locations])        
                await processQueue.enqueue([srcJobId,destJobId])                       
                await self.station6.setStatus(MachineStatus.Filled)
                jobslogger.info("batch moved from {0} to {1}".format(self.station5.name,self.station6.name))
                return True
        return False
    
    # Camera 1 to Camera 2, only Green Tubes
    async def getStation1_To_4_3_Job(self):
        if await self.station3.getStatus() == MachineStatus.On or  await self.station3.getStatus() == MachineStatus.Running:
            tube=None
            if await self.station5.isAvailableForGreen():
                await self.refreshCamera1Results()                
                tube=await self.station1.getNextGreenTube()        
            if tube is not None:
                srcJobId=self.station1.jobs[1].jobId 
                destJobId=self.station4.jobs[1].jobId                            
                await processQueue.enqueue([srcJobId,destJobId])
                processQueue.destLocation.extend([tube.location,tube.location])                      
                await self.station4.updateGrid(tube)
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station1.name,self.station4.name))
                return True       
        return False

    # Camera 1 to Camera 2, only orange brown and yellow tubes
    async def getStation1_To_4_14_Job(self):
        if await self.station8.getStatus() == MachineStatus.Filled:
            tube=None       
            if await self.station5.isAvailableForOrange():
                await self.refreshCamera1Results()
                tube=await self.station1.getNextOrangeBrownYellowTube()
            if tube is not None:
                srcJobId=self.station1.jobs[1].jobId 
                destJobId=self.station4.jobs[1].jobId                            
                await processQueue.enqueue([srcJobId,destJobId])
                processQueue.destLocation.extend([tube.location, tube.location])                      
                await self.station4.updateGrid(tube)
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station1.name,self.station4.name))
                return True        
        if await self.station6.isAvailable():
            await self.station5.prepareCounterWeightJobs()
            if await self.station5.currentBatchFilled():
                return await self.getStation5_To_6_Job()
        return False  

    async def getStation7StartMachineJob(self):
        if await self.station7.getStatus() == MachineStatus.Filled:
            tubeCount=await self.station9.getFilledBatchCount()
            await self.station7.startMachine(tubeCount)
            await self.station7.startRuntimeAlarm()
            return True
        return False
    
    async def getStation7_To_9_Job(self):
        if await self.station7.getStatus() == MachineStatus.Completed:
            srcJobId=self.station7.jobs[1].jobId
            destJobId=self.station9.jobs[2].jobId
            await processQueue.enqueue([srcJobId,destJobId])
            location=await self.station9.getLocationOfRunningJob()
            processQueue.destLocation.extend([location,location])            
            jobslogger.info("rack moved from {0} to {1}".format(self.station7.name,self.station9.name)) 
            await self.station7.setStatus(MachineStatus.On)
            return True
        return False

    #from camera 2 to coagulation machine, cobas pure rack and haematology machine
    async def getStation4NextJob(self,isSuccess):
        res=self.conn_Q400.getCurrentTubeResults()
        try:
            tube=self.station4.tube
            tube.color = res.color
            if int(isSuccess) == 1 and tube is not None:                   
                if tube.color == Color.GREEN:
                    location=await self.station5.getNextLocation()
                    processQueue.destLocation.extend([location,location]) 
                    await self.station5.updateGrid(tube.color)
                    jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                    jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station5.name))
                    await self.fileManager.processFiles(res) 
                    await sftpCommunication.moveCSVToSFTPServer()
                    self.conn_Q400.resetCurrentTubeResults()
                    return self.station5.jobs[2].jobId                  
                elif tube.color == Color.ORANGE or tube.color == Color.BROWN or tube.color == Color.YELLOW:
                    location=await self.station5.getNextLocation()
                    processQueue.destLocation.extend([location,location])
                    await self.station5.updateGrid(Color.ORANGE)
                    jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                    jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station5.name))
                    await self.fileManager.processFiles(res) 
                    await sftpCommunication.moveCSVToSFTPServer()
                    self.conn_Q400.resetCurrentTubeResults() 
                    return self.station5.jobs[2].jobId
                elif tube.color == Color.RED:
                    location=await self.station9.getNextLocation()
                    processQueue.destLocation.extend([location,location])
                    await self.station9.updateGrid(tube.color)
                    jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                    jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station9.name))
                    await self.fileManager.processFiles(res) 
                    await sftpCommunication.moveCSVToSFTPServer()
                    self.conn_Q400.resetCurrentTubeResults()                    
                    return self.station9.jobs[4].jobId
                else:
                    location=await self.station10.getNextLocation()           
                    processQueue.destLocation.extend([location,location]) 
                    await self.station10.updateGrid(tube.color)
                    jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                    jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station10.name)) 
                    #await self.fileManager.processFailedFiles(res)
                    self.conn_Q400.resetCurrentTubeResults()
                    # await commManager.sendMessage(Settings.failtubemsg)
                    return self.station10.jobs[2].jobId
            else: 
                location=await self.station10.getNextLocation()           
                processQueue.destLocation.extend([location,location]) 
                await self.station10.updateGrid(tube.color)
                jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station10.name)) 
                #await self.fileManager.processFailedFiles(res)
                self.conn_Q400.resetCurrentTubeResults()
                # await commManager.sendMessage(Settings.failtubemsg)
                return self.station10.jobs[2].jobId
        except Exception as e: 
            traceback.print_exc()
            errorlogger.exception(e)
            processQueue.destLocation=[]
            raise CommonError("Unexpected error occurred. Please check logs!")

    async def getStation4NextJob_afterCentrifugation(self,isSucess):
        res=self.conn_Q400.getCurrentTubeResults()
        try:
            tube=self.station4.tube
            tube.color = res.color
            if int(isSucess) == 1 and tube is not None:
                if tube.color == Color.GREEN:
                    location=await self.station3.getNextLocation()
                    processQueue.destLocation.extend([location,location]) 
                    # await self.station3.updateGrid(tube.color)     # Calling from Robot
                    # res.color=tube.color
                    jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                    jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station3.name))
                    #await self.fileManager.processFilesAfterCentrifugation(res) 
                    self.conn_Q400.resetCurrentTubeResults()
                    return self.station3.jobs[2].jobId
                elif tube.color == Color.ORANGE or tube.color == Color.BROWN or tube.color == Color.YELLOW:
                    location=await self.station14.getNextLocation()
                    processQueue.destLocation.extend([location,location]) 
                    await self.station14.updateGrid(Color.ORANGE)
                    tubesCount = await self.station14.fillTubesGridMax()
                    if tubesCount != -1:
                        await self.station8.updateGrid(tubesCount)
                        # if await self.station8.startMachine(tubesCount):
                        #     if await self.station17.getHolderStatus() == HolderStatus.Empty:
                        #         await self.station17.setTubesCountInBatches(await self.station8.getFilledBatches())
                        #     if await self.station18.getHolderStatus() == HolderStatus.Empty:
                        #         await self.station18.setTubesCountInBatches(await self.station8.getFilledBatches())
                    # res.color=tube.color  
                    jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                    jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station14.name))
                    #await self.fileManager.processFilesAfterCentrifugation(res) 
                    self.conn_Q400.resetCurrentTubeResults() 
                    return self.station14.jobs[3].jobId  
                else:  
                    location=await self.station10.getNextLocation()           
                    processQueue.destLocation.extend([location,location]) 
                    await self.station10.updateGrid(tube.color)
                    res.color=tube.color
                    jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                    jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station10.name)) 
                    #await self.fileManager.processFailedFilesAfterCentrifugation(res)
                    self.conn_Q400.resetCurrentTubeResults()
                    # await commManager.sendMessage(Settings.failtubemsg)
                    return self.station10.jobs[2].jobId        
            else:
                location=await self.station10.getNextLocation()           
                processQueue.destLocation.extend([location,location]) 
                await self.station10.updateGrid(tube.color)
                res.color=tube.color
                jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station10.name)) 
                #await self.fileManager.processFailedFilesAfterCentrifugation(res)
                self.conn_Q400.resetCurrentTubeResults()
                # await commManager.sendMessage(Settings.failtubemsg)
                return self.station10.jobs[2].jobId
        except Exception as e: 
            traceback.print_exc()
            errorlogger.exception(e)
            processQueue.destLocation=[]
            raise CommonError("Unexpected error occurred. Please check logs!")
    
    async def setInitAlarm(self,macId):
        try:
            match macId:
                case Settings.macId_centrifuge:
                    await self.station6.initCentrifuge()
        except Exception as e:
            errorlogger.exception(e)
            processQueue.destLocation=[]
            raise CommonError("Unexpected error occured. Please check logs!")
    
    async def startRuntimeAlarm(self,macId):
        try:
            match macId:
                case Settings.macId_coagulation:
                    await self.station3.startRuntimeAlarm()
                case Settings.macId_centrifuge:
                    await self.station6.startRuntimeAlarm()
                case Settings.macId_haematology:
                    await self.station7.startRuntimeAlarm()
                case Settings.macId_chemistry:
                    await self.station8.startRuntimeAlarm()
        except Exception as e:
            errorlogger.exception(e)
            processQueue.destLocation=[]
            raise CommonError("Unexpected error occured. Please check logs!")
    
    async def isStation1Good(self):
        try:
            if not self.stn1_good:
                self.stn1_good = True
                jobslogger.info("Station 1 status : 0") 
                return 0
            jobslogger.info("Station 1 status : 1")
            return 1
        except Exception as e: 
            errorlogger.exception(e)
            # raise CommonError("Error occured during ping. please check logs") 
            return 0

    # async def ping(self):
    #     try:
    #         currentTime=datetime.now()
    #         if self.lastPingTime == None:
    #             self.lastPingTime=currentTime
    #         diffTime=currentTime - self.lastPingTime 
    #         self.lastPingTime=currentTime
    #         diff=diffTime.total_seconds()*1000
    #         if diff > Settings.pingInterval:
    #             # jobslogger.info("ping interrupted for:{0} milli seconds ".format(diff)) 
    #             # print("ping interrupted for: ",diff)
    #             self.station1.isRefreshCamera1Results=True
    #             self.stn1_good = False
    #     except Exception as e: 
    #         errorlogger.exception(e)
    #         raise CommonError("Error occured during ping. please check logs")  

    async def ping(self,pingStatus):
        try:
            if(pingStatus == 0):  # there is ping
                self.station1.isRefreshCamera1Results=True
                self.stn1_good = False
                return 1
            else:
                return 0
        except Exception as e: 
            errorlogger.exception(e)
            raise CommonError("Error occured during ping. please check logs")  

    async def getCamera2Results(self,group:int):
        res = await self.conn_Q400.q400_execute_cam2(group)
        return res

    # need to be removed later
    async def setInitialized(self):
        self.station6.isInitialized=True
    
    async def setCamera1Flag(self,isOn:bool):
        self.station1.isRefreshCamera1Results=isOn

    async def stn6_hatch_open(self):        
        res = await self.station6.hatchOpen()
        return res

    async def stn6_hatch_close(self):
        res = await self.station6.hatchClose()
        return res

    async def stn6_is_runnning(self):
        res = await self.station6.centrifugeClient.is_running()
        return res

    async def stn6_check_lock(self):
        res = await self.station6.checkLock()
        return res

    async def stn6_set_rotor_position(self,position):
        res = await self.station6.setRotorPosition(position)
        return res

    async def stn6_start_centrifuge(self):
        res = await self.station6.startCentrifuge()
        await self.station6.startRuntimeAlarm()
        return  res

    async def send_skype_message(self, msg):
        # res = await commManager.sendMessage(msg)
        print(msg)
        return True

    async def getTestJob(self):      
        # src=self.station17.rackLocations.pop(0)
        # # src=self.station2.rackLocations.pop(0)
        # dest=self.station2.rackLocations.pop(0)
        src = [0,0,0,0,0,0]
        dest= [0,0,0,0,0,0]
        processQueue.destLocation.extend([src, dest])
        return [152,152]
   
mainObj=MainApp()

    
class TCPServer(asyncio.Protocol):
    def __init__(self):
        self.taskID = 0 
        self.isBusy = False
        self.interfaceIn = interface_buffer.InterfaceIn()
        self.interfaceOut = interface_buffer.InterfaceOut()

    def connection_made(self, transport):
        self.transport = transport
        
    def data_received(self, data):
        loop = asyncio.get_event_loop()
        loop.create_task(self.handle_incoming_packet(data))
        
    async def handle_incoming_packet(self,data):
        await self.handling_buffer(data)

    def getPose(self, count):
        pose =[]
        for cnt in range(count):
            pose.append(self.interfaceIn.dataFromRobot[(cnt * 6 + 7 ): ((cnt + 2) * 6) + 1])
        return pose

    async def handling_buffer(self,data):    
        data = data.decode('utf-8')
        self.interfaceIn.setData(data)
        self.interfaceOut.pingStatus = await mainObj.ping(self.interfaceIn.dataFromRobot[6])    
        self.interfaceIn.dataFromRobot[1] = 1
        self.interfaceOut.stateOfHandshake = 0
        if(self.interfaceIn.dataFromRobot[1] == 1 and self.interfaceOut.stateOfHandshake == 0):             
            self.isBusy = True      
            if(self.interfaceIn.dataFromRobot[0] == 1): # new connection
                self.isBusy = False
                #self.interfaceOut.stateOfHandshake = 0
                self.interfaceOut.srcJob    = 0
                self.interfaceOut.destJob   = 0
                self.interfaceOut.srcPos    = [0,0,0,0,0,0]
                self.interfaceOut.destPos   = [0,0,0,0,0,0]
                await mainObj.reset()     
            if(self.interfaceIn.dataFromRobot[4] == 0):  # Starting of Job Id
                if(self.interfaceIn.dataFromRobot[2] == 1):                    
                    self.interfaceOut.srcJob    = 0
                    self.interfaceOut.destJob   = 0
                    self.interfaceOut.srcPos    = [0,0,0,0,0,0]
                    self.interfaceOut.destPos   = [0,0,0,0,0,0]
                    jobArray = await mainObj.getJob()
                    # jobArray = await mainObj.getTestJob()
                    if jobArray[0] != 0:
                        self.interfaceOut.srcJob    = jobArray[0]
                        self.interfaceOut.destJob   = jobArray[1]
                        location = await mainObj.getCurrentLocation()
                        self.interfaceOut.srcPos = location[0]
                        self.interfaceOut.destPos = location[1]  
                elif(self.interfaceIn.dataFromRobot[2] == 2 or self.interfaceIn.dataFromRobot[2] == 3):   # Stn4 Next Job ID, lockID
                    if self.interfaceIn.dataFromRobot[2] == 2:         # Stn4 Next Job ID before centrifugation, lockID
                        stn4_get_next_jobId = await mainObj.getStation4NextJob(int(self.interfaceIn.dataFromRobot[3]))
                    else:                                              # Stn4 Next Job ID after centrifugation, lockID
                        stn4_get_next_jobId = await mainObj.getStation4NextJob_afterCentrifugation(int(self.interfaceIn.dataFromRobot[3]))
                    self.interfaceOut.srcJob = stn4_get_next_jobId
                    self.interfaceOut.destJob = stn4_get_next_jobId
                    location = await mainObj.getCurrentLocation()
                    self.interfaceOut.srcPos = location[0]
                    self.interfaceOut.destPos = location[1]            
            elif(self.interfaceIn.dataFromRobot[4] == 41):
                self.interfaceOut.status = await mainObj.conn_Q400.q400_execute_cam2(int(self.interfaceIn.dataFromRobot[2]))
            elif(self.interfaceIn.dataFromRobot[4] == 302):               
                await mainObj.station3.updateGrid(Color.GREEN)
            elif(self.interfaceIn.dataFromRobot[4] == 61):  # centrifuge check lock
                await mainObj.station6.initCentrifuge()
                await mainObj.stn6_check_lock()
            elif(self.interfaceIn.dataFromRobot[4] == 62):  # centrifuge hatch open
                await mainObj.stn6_hatch_open()
            elif(self.interfaceIn.dataFromRobot[4] == 63):  # centrifuge set rotar 1
                await mainObj.stn6_set_rotor_position(1)
            elif(self.interfaceIn.dataFromRobot[4] == 64):  # centrifuge set rotar 2
                await mainObj.stn6_set_rotor_position(2)
            elif(self.interfaceIn.dataFromRobot[4] == 65):  # centrifuge set rotar 3
                await mainObj.stn6_set_rotor_position(3)
            elif(self.interfaceIn.dataFromRobot[4] == 66):  # centrifuge set rotar 4
                await mainObj.stn6_set_rotor_position(4)                
            elif(self.interfaceIn.dataFromRobot[4] == 67):  # centrifuge hatch close
                await mainObj.stn6_hatch_close()
            elif(self.interfaceIn.dataFromRobot[4] == 68):  # centrifuge start
                await mainObj.stn6_start_centrifuge()
            elif(self.interfaceIn.dataFromRobot[4] == 1):  # Initialization of camera 1 (mac ID)
                pose = self.getPose(3)
                await mainObj.station1.initGrids(pose[0], pose[1], pose[2], 5, 15)
            elif(self.interfaceIn.dataFromRobot[4] == 2):  # Cobas Pure Racks Storage
                pose = self.getPose(4)
                await mainObj.station2.initGrids(pose[0], pose[1], pose[2], pose[3], 1, 25)
            elif(self.interfaceIn.dataFromRobot[4] == 3):  # Compact Max initialization
                pose = self.getPose(3)
                await mainObj.station3.initGrids(pose[0], pose[1], pose[2], 2, 4)
            elif(self.interfaceIn.dataFromRobot[4] == 4):  # Q400
                await mainObj.conn_Q400.initVQ400()                 
            elif(self.interfaceIn.dataFromRobot[4] == 9):  # Sysmex Rack initialization
                pose = self.getPose(6)
                await mainObj.station9.initGrids(pose[0], pose[1], pose[2], pose[3], pose[4], pose[5]) 
            elif(self.interfaceIn.dataFromRobot[4] == 5):  # Centrifuge racks TubePos initialization
                pose = self.getPose(5)
                await mainObj.station5.initGrids(pose[0], pose[1], pose[2], 4, 2, pose[3],pose[4], 3, 3)
            elif(self.interfaceIn.dataFromRobot[4] == 55):  # Centrifuge counter weights initialization
                pose = self.getPose(2)
                await mainObj.station5.initCounterGrids(pose[0], pose[1])
            elif(self.interfaceIn.dataFromRobot[4] == 10):  # Fehler stand initialization                
                pose = self.getPose(6)
                await mainObj.station10.initGrids(pose[0], pose[1], pose[2], pose[3], pose[4], pose[5], 8, 4)
            elif(self.interfaceIn.dataFromRobot[4] == 111):  # Archive initialization  1             
                pose = self.getPose(6)
                await mainObj.station11.initGrids_1_2(pose[0], pose[1], pose[2], pose[3], pose[4], pose[5], 8, 4)
            elif(self.interfaceIn.dataFromRobot[4] == 112):  # Archive initialization  2             
                pose = self.getPose(6)
                await mainObj.station11.initGrids_3_4(pose[0], pose[1], pose[2], pose[3], pose[4], pose[5], 8, 4)
            elif(self.interfaceIn.dataFromRobot[4] == 14):  # Cobas Pure Rack Holder            
                pose = self.getPose(3)
                await mainObj.station14.initGrids(pose[0], pose[1], pose[2], 5, 1)
            elif(self.interfaceIn.dataFromRobot[4] == 17):  # Cobas Pure Filled Rack Holder 1             
                pose = self.getPose(3)
                await mainObj.station17.initGrids(pose[0], pose[1], pose[2], 1, 10)
            elif(self.interfaceIn.dataFromRobot[4] == 18):  # Cobas Pure Filled Rack Holder 2             
                pose = self.getPose(5) 
                await mainObj.station18.initGrids(pose[0], pose[1], pose[2], 1, 10)  # This is in negative direction of the axis
            elif(self.interfaceIn.dataFromRobot[4] == 701):      
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_CAM_1))
            elif(self.interfaceIn.dataFromRobot[4] == 702):     
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_COBAS_PURE_RCK))         
            elif(self.interfaceIn.dataFromRobot[4] == 703):    
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_COBAS_PURE_RCK_SLOW))         
            elif(self.interfaceIn.dataFromRobot[4] == 704):    
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_CAM_2))         
            elif(self.interfaceIn.dataFromRobot[4] == 706):    
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_CENTRIFUGE))         
            elif(self.interfaceIn.dataFromRobot[4] == 707):     
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_SYSMEX))          
            elif(self.interfaceIn.dataFromRobot[4] == 708):  
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_COBASPURE))          
            elif(self.interfaceIn.dataFromRobot[4] == 709):  
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_COBASPURE_SLOW))       
            elif(self.interfaceIn.dataFromRobot[4] == 710):  
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_COBASPURE_LOAD_UNLOAD))     
            self.interfaceOut.stateOfHandshake = 1       # State of Handshake          
            self.isBusy = False
        if(self.interfaceIn.dataFromRobot[1] == 0 and self.interfaceOut.stateOfHandshake == 1 and not self.isBusy):
            self.interfaceOut.stateOfHandshake = 0
        self.transport.write(self.interfaceOut.getData().encode())    
        # print("isRecv")


# async def main():
#     loop = asyncio.get_running_loop()
#     # loop = asyncio.get_event_loop()
#     try:
#         server = await loop.create_server(lambda: TCPServer(), Settings.systemip, Settings.systemport)
#         print("Service is running... at {0} - {1}".format(Settings.systemip,Settings.systemport))
#         async with server:
#             await server.serve_forever()        
#     except Exception as e: 
#         errorlogger.exception(e)
#         raise CommonError("Unexpected error occurred with TCP server. Please check logs!")
#     finally:
#         server.close()

async def main():
    loop = asyncio.get_running_loop()
    # loop = asyncio.get_event_loop()
    retry_delay = 5  # Delay in seconds between retries
    max_retries = 3  # Maximum number of retries
    for retry_count in range(max_retries):
        try:
            server = await loop.create_server(lambda: TCPServer(), Settings.systemip, Settings.systemport)
            print("Service is running... at {0} - {1}".format(Settings.systemip,Settings.systemport))
            async with server:
                await server.serve_forever()    
        except Exception as e: 
            errorlogger.exception(e)
            await asyncio.sleep(retry_delay)
            errorlogger.exception("Retrying attempt: {0}".format(retry_count+1))

   
if __name__ == '__main__':
    # loop = asyncio.get_running_loop()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.run_forever()
    asyncio.run(main())
