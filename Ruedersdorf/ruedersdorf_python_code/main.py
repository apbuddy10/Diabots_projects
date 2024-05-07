import asyncio
import socket
import traceback
from datetime import datetime

import interface_buffer
from axis7 import AxisConn_7
from filemanager import FileManager
from logger import errorlogger, jobslogger
from machine import MachineStatus
from settings import (Color, FridgeRackType, HolderStatus, Settings, TubeType,
                      dummyLocation)
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
from stations import CommonError, Job, processQueue
from vq400connector import Vq400Connector

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

    def  initialize(self):     
        self.initStations()
        self.isCameraClicked=False
        self.stn1_good = True
        self.ping_bad = False
        self.testCounter = 0
        processQueue.reset()

    async def reset(self):
        try:
            await self.station3.cancelTimers()
            await self.station6.cancelTimers()
            await self.station7.cancelTimers()
            await self.station6.resetConnections()                     
            self.initialize()
            # await commManager.connectToSkype()
            await self.setMachineStatus(Settings.macId_centrifuge, True)
            # await self.test8Unloading()
            await mainObj.axis7.reset(True)
            print("Robot (re)started at : {0}".format(str(datetime.now())))  
        except Exception as e: 
            errorlogger.exception(e)
            raise CommonError("Error occurred during reset")
    
    async def test_fillGreensIn5(self,color:Color):
        for i in range(2):
            self.conn_Q400.setCurrentTubeResults(color)
            await mainObj.getStation4NextJob(int(1))

        await self.station5.testFillBatch()
        #await self.getStation5_To_6_Job()
        #await self.getStation6_To_5_Job()
        await self.getStation5_To_4_3_Job()
        

    async def test8Unloading(self):
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
        self.station3=Station3("BCS ",
        [
            Job(30,"Initial"),
            Job(31,"pick"),
            Job(32,"place"),
            Job(33,"load rack"),
            Job(34,"unload rack")
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
        self.station7=Station7("Beckman machine",
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
        self.station9=Station9("Beckman rack holders",
        [
            Job(90,"Initial"),
            Job(91,"pick rack"),
            Job(92,"place rack"),
            Job(93,"pick tube"),
            Job(94,"place tube")
        ])
        self.station10=Station10("Fehler Pallette",
        [
            Job(100,"Initial"),
            Job(101,"pick"),
            Job(102,"place"),
            Job(103,"filled")
        ])
        self.station11=Station11("Archive Palette",
        [
            Job(110,"Initial"),
            Job(111,"pick"),
            Job(112,"place"),
            Job(113,"close"),
            Job(114,"open"),
            Job(115,"closerack"),
            Job(116,"openrack"),
            Job(117,"filled")
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
                    await self.station3.setStatus(MachineStatus.On)
                    await self.station8.prepareInitJobWithStatus(isOn)
                    if isOn:
                        await self.station8.setStatus(MachineStatus.Filled)
                        self.station15.holderStatus=HolderStatus.Empty
                    await self.station6.prepareInitJobWithStatus(isOn)
                case Settings.macId_coagulation:
                    await self.station3.prepareInitJobWithStatus(isOn)      
                    await self.station3.setStatus(MachineStatus.On) 
                case Settings.macId_chemistry:
                    await self.station8.prepareInitJobWithStatus(isOn)
                    if isOn:
                        await self.station8.setStatus(MachineStatus.Filled)
                        self.station15.holderStatus=HolderStatus.Empty
                case Settings.macId_centrifuge:
                    await self.station6.prepareInitJobWithStatus(isOn)
                    if not isOn:
                        await self.station8.prepareInitJobWithStatus(isOn)
                        await self.station3.setStatus(MachineStatus.On)
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
        if (((await self.station3.getStatusLoad() == MachineStatus.On) and self.station1.isGreenAvailable and await self.station5.isAvailableForGreen()) or 
            ((await self.station8.getStatus() != MachineStatus.Off) and (self.station1.isOrangeAvailable or self.station1.isBrownAvailable or
            self.station1.isYellowAvailable or self.station1.isYellow2Available or self.station1.isYellow3Available) and (await self.station5.isAvailableForOrangeYellow() or await self.station5.isAvailableForBrown())) or 
            (self.station1.isRedAvailable and await self.station9.isAvailable(TubeType.ADULT) and await self.station9.isAvailable(TubeType.CHILD))):
            self.station1.isRefreshCamera1Results=True
        else:
            self.station1.isRefreshCamera1Results=False

    async def refreshCamera1Results(self):
        self.stn1_good = True
        if self.station1.isRefreshCamera1Results: # and not self.isCameraClicked:            
            results=await self.getResultsFromCamera1()
            await self.station1.updateGrid(results)    
            self.station1.isRefreshCamera1Results=False        
            self.isCameraClicked=True
        # await self.modifyRefreshFlag()

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
        if await self.station10.isFehlerFilled():
            await self.station11.closeDoor()
            await self.station10.getFehlerFilledJob()
            return True
        if await self.station11.getArchiveFilledJob():
            return True
        if await self.station3.startMachine():
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
        if await self.getStation14_To_8_Job():
            return True
        if await self.getStation2_14_Job():
            return True 
        if await self.getStation5_To_4_14_Orange_Job():
            return True
        # if await self.getStation5_To_4_14_Yellow_Job():
        #     return True
        if await self.getStation5_To_4_14_Brown_Job():
            return True
        if await self.getStation5_To_4_3_Job():
            return True
        if await self.station5.getNextCounterTube():
            return True
        if await self.getStation6_To_5_Job():
            return True
        if await self.getStation5_To_6_Job():
            return True
        if await self.getStation7_To_9_Job():
             return True
        if await self.getStation9_To_7_Job():
             return True
        if await self.getStation1_To_4_3_Emergency_Job():
            return True
        if await self.getStation1_To_4_14_Emergency_Job():
            return True
        if await self.getStation1_To_4_9_Emergency_Job():
             return True
        if await self.getStation1_To_4_3_Job():
            return True
        if await self.getStation1_To_4_14_Job():
            return True
        if await self.getStation1_To_4_9_Job():
             return True
        if await self.station3.stopMachine():
            return True
        if await self.getStation9_To_11_Job():
            return True
        if await self.getStation3_To_11_Job():
            return True
        if await self.getStation17_To_2_Job():
            return True
        if await self.getStation18_To_2_Job():
            return True
        if await self.getStation17_To_11_Job():
            return True
        if await self.getStation18_To_11_Job():
            return True
        if await self.station11.closeDoor():
            return True
        return False
    
    # from cobas pure racks storage to cobas pure rack holder
    async def getStation2_14_Job(self):
        if await self.station8.getStatus() == MachineStatus.Filled and await self.station14.getHolderStatus() == HolderStatus.Empty:
            if not await self.station2.getPickRackStatus():
                return False
            index,location = await self.station2.getNextLocationToPick()
            srcJobId = self.station2.jobs[1].jobId
            destJobId = self.station14.jobs[2].jobId                    
            await processQueue.enqueue([srcJobId,destJobId,TubeType.SMALL,index])
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
                    if await self.station15.getHolderStatus() == HolderStatus.Empty and await self.station17.getHolderStatus() == HolderStatus.Empty and self.station8.updateRacks():
                        await self.station17.setTubesCountInBatches(await self.station8.getFilledBatches())
                    if await self.station16.getHolderStatus() == HolderStatus.Empty and await self.station18.getHolderStatus() == HolderStatus.Empty and self.station8.updateRacks():
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
                if not await self.station2.getPlaceRackStatus():
                    return False
                if await self.station17.currentRackEmpty():
                    index,destLoc = await self.station2.getNextLocationToPlace()
                    # if destLoc is None:
                    #     return False
                    srcJobId=self.station17.jobs[0].jobId
                    destJobId=self.station2.jobs[2].jobId
                    await processQueue.enqueue([srcJobId,destJobId,TubeType.SMALL,index])
                    srcLoc = await self.station17.getNextRackLocation()                    
                    processQueue.destLocation.extend([srcLoc,destLoc])
                    jobslogger.info("Picked the rack from first filled rack holder: loc {0} and placed in Racks storage at {1}".format(srcLoc,destLoc)) 
                    return True
        return False

    # from Cobas pure second filled rack holder to racks storage
    async def getStation18_To_2_Job(self):
        if await self.station8.getStatus() == MachineStatus.Filled or await self.station8.getStatus() == MachineStatus.Running:
            if await self.station18.getHolderStatus() == HolderStatus.Filled:
                if not await self.station2.getPlaceRackStatus():
                    return False
                if await self.station18.currentRackEmpty():
                    index,destLoc = await self.station2.getNextLocationToPlace()
                    # if destLoc is None:
                    #     return False
                    srcJobId=self.station18.jobs[0].jobId
                    destJobId=self.station2.jobs[2].jobId
                    await processQueue.enqueue([srcJobId,destJobId,TubeType.SMALL,index])
                    srcLoc = await self.station18.getNextRackLocation()
                    processQueue.destLocation.extend([srcLoc,destLoc])
                    jobslogger.info("Picked the rack from second filled rack holder: loc {0} and placed in Racks storage at {1}".format(srcLoc,destLoc)) 
                    return True
        return False

    #from Sysmex racks to archive
    async def getStation9_To_11_Job(self):
        if await self.station7.getStatus() == MachineStatus.Off:
            return False
        if await self.station11.isAvailable():
            tube=await self.station9.getNextTubeToArchiv()
            if tube is None:    
                if await self.station9.currentBatchEmpty():
                    # await self.station11.closeDoor()
                    return await self.getStation1_To_4_9_Job()
            if tube is not None:
                await self.station11.openDoor()
                srcJobId=self.station9.jobs[3].jobId 
                destJobId=self.station11.jobs[2].jobId 
                fridgeNo=await self.station11.getNextAvailableFridgeNo()
                await processQueue.enqueue([srcJobId,destJobId,tube.type,fridgeNo]) 
                location=await self.station11.getNextLocation()
                processQueue.destLocation.extend([tube.location,location])
                await self.station11.updateGrid(tube.color)
                jobslogger.info("{0} tube moved from {1} to {2},fridge:{3}".format(tube.color.name,self.station9.name,self.station11.name,fridgeNo)) 
                return True
        return False
    
    #from coagulation machine to archive
    async def getStation3_To_11_Job(self):
        if await self.station3.getStatus() == MachineStatus.Off:
            return False
        if await self.station11.isAvailable():
            if await self.station3.getStatusUnload() == MachineStatus.ReadyToUnload:
                tube=await self.station3.getNextTubeToArchiv()
                if tube is None:    
                    if await self.station3.currentBatchEmpty():
                        # await self.station11.closeDoor()
                        return await self.getStation5_To_4_3_Job()
                if tube is not None:
                    await self.station11.openDoor()
                    srcJobId=self.station3.jobs[1].jobId 
                    destJobId=self.station11.jobs[2].jobId 
                    fridgeNo=await self.station11.getNextAvailableFridgeNo()
                    await processQueue.enqueue([srcJobId,destJobId,tube.type,fridgeNo])
                    location=await self.station11.getNextLocation()
                    processQueue.destLocation.extend([tube.location,location])     
                    await self.station11.updateGrid(tube.color)
                    jobslogger.info("{0} tube moved from {1} to {2}, fridgeNo: {3}".format(tube.color.name,self.station3.name,self.station11.name,fridgeNo)) 
                    return True
        return False
    
    # from Cobas pure first filled rack holder to Archiv
    async def getStation17_To_11_Job(self):   
        if await self.station8.getStatus() == MachineStatus.Off:
            return False 
        if await self.station11.isAvailable():     
            if await self.station8.getStatus() == MachineStatus.Filled or await self.station8.getStatus() == MachineStatus.Running:
                if await self.station17.getHolderStatus() == HolderStatus.Filled:
                    if not await self.station17.currentRackEmpty():
                        await self.station11.openDoor()
                        srcJobId = self.station17.jobs[1].jobId
                        await processQueue.enqueue([srcJobId,srcJobId,TubeType.SMALL])
                        srcLoc = await self.station17.getNextTubeLocation()                        
                        processQueue.destLocation.extend([srcLoc,srcLoc])
                        jobslogger.info("Picked the tube from first filled rack holder: loc {0}".format(srcLoc)) 
                        return True
                    # return await self.station11.closeDoor()
        return False
    
    # from Cobas pure second filled rack holder to Archiv
    async def getStation18_To_11_Job(self):   
        if await self.station8.getStatus() == MachineStatus.Off:
            return False
        if await self.station11.isAvailable():      
            if await self.station8.getStatus() == MachineStatus.Filled or await self.station8.getStatus() == MachineStatus.Running:
                if await self.station18.getHolderStatus() == HolderStatus.Filled:
                    if not await self.station18.currentRackEmpty():
                        await self.station11.openDoor()
                        srcJobId = self.station18.jobs[1].jobId
                        await processQueue.enqueue([srcJobId,srcJobId,TubeType.SMALL])
                        srcLoc = await self.station18.getNextTubeLocation()
                        processQueue.destLocation.extend([srcLoc,srcLoc])
                        jobslogger.info("Picked the tube from second filled rack holder: loc {0}".format(srcLoc)) 
                        return True
                    # return await self.station11.closeDoor()
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
        return False
    
    # centrifuge racks to camera2 only Green tubes
    async def getStation5_To_4_3_Job(self):        
        if await self.station3.getStatus() == MachineStatus.Off:
            return False
        tube=None
        if await self.station3.isAvailable():
            tube=await self.station5.getNextGreenTube()
        if tube is None:
            if await self.station3.setMachineFilled():                    
                return await self.station3.startMachine()
        else:
            srcJobId=self.station5.jobs[1].jobId 
            destJobId=self.station4.jobs[1].jobId 
            processQueue.destLocation.extend([tube.location,tube.location])            
            await processQueue.enqueue([srcJobId,destJobId,tube.type])                       
            await self.station4.updateGrid(tube)
            jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station5.name,self.station4.name))
            return True        
        return False

    # centrifuge racks to camera2 only orange tubes
    async def getStation5_To_4_14_Orange_Job(self):
        if await self.station8.getStatus() == MachineStatus.Off:
            return False
        tube=None        
        if await self.station14.isAvailable():
            tube = await self.station5.getNextOrangeTube()
            if tube is None:
                tubesCount = await self.station14.fillTubesGrid(Color.ORANGE)
                if tubesCount != -1:
                    await self.station8.updateGrid(tubesCount)
                    return await self.getStation14_To_8_Job()
            else:
                srcJobId=self.station5.jobs[1].jobId 
                destJobId=self.station4.jobs[1].jobId 
                processQueue.destLocation.extend([tube.location,tube.location])            
                await processQueue.enqueue([srcJobId,destJobId,tube.type])                       
                await self.station4.updateGrid(tube)
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station5.name,self.station4.name))
                return True        
        return False
    
    # centrifuge racks to camera2 only brown tubes
    async def getStation5_To_4_14_Brown_Job(self):
        if await self.station8.getStatus() == MachineStatus.Off:
            return False
        tube=None        
        if await self.station14.isAvailable():
            tube = await self.station5.getNextBrownTube()
            if tube is None:
                tubesCount = await self.station14.fillTubesGrid(Color.BROWN)
                if tubesCount != -1:
                    await self.station8.updateGrid(tubesCount)
                    return await self.getStation14_To_8_Job()
            else:
                srcJobId=self.station5.jobs[1].jobId 
                destJobId=self.station4.jobs[1].jobId 
                processQueue.destLocation.extend([tube.location,tube.location])            
                await processQueue.enqueue([srcJobId,destJobId,tube.type])                       
                await self.station4.updateGrid(tube)
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station5.name,self.station4.name))
                return True        
        return False
    
    # centrifuge racks to camera2 only yellow tubes
    async def getStation5_To_4_14_Yellow_Job(self):
        if await self.station8.getStatus() == MachineStatus.Off:
            return False
        tube=None
        if await self.station14.isAvailable():
            tube = await self.station5.getNextYellowTube()
            if tube is None:
                tubesCount = await self.station14.fillTubesGrid(Color.YELLOW)
                if tubesCount != -1:
                    await self.station8.updateGrid(tubesCount)
                    return await self.getStation14_To_8_Job()
            else:
                srcJobId=self.station5.jobs[1].jobId 
                destJobId=self.station4.jobs[1].jobId 
                processQueue.destLocation.extend([tube.location,tube.location])            
                await processQueue.enqueue([srcJobId,destJobId,tube.type])                       
                await self.station4.updateGrid(tube)
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station5.name,self.station4.name))
                return True        
        return False
    
    # centrifuge racks to centrifuge machine
    async def getStation6_To_5_Job(self):
        if await self.station3.getStatus() == MachineStatus.Off and await self.station8.getStatus() == MachineStatus.Off:
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
        if await self.station3.getStatus() == MachineStatus.Off and await self.station8.getStatus() == MachineStatus.Off:
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
                # await self.station6.startRuntimeAlarm()
                return True
        return False
    
    async def set_1_To_4_Job(self, tube):
        srcJobId=self.station1.jobs[1].jobId 
        destJobId=self.station4.jobs[1].jobId                            
        await processQueue.enqueue([srcJobId,destJobId,tube.type])
        processQueue.destLocation.extend([tube.location,tube.location])                      
        await self.station4.updateGrid(tube)
        jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station1.name,self.station4.name))

    # Camera 1 to Camera 2, only Emergency Green Tubes
    async def getStation1_To_4_3_Emergency_Job(self):
        if await self.station3.getStatus() == MachineStatus.Off:
            return False
        if await self.station3.getStatusLoad() == MachineStatus.On:
            tube=None
            if await self.station5.isAvailableForGreen():
                await self.refreshCamera1Results()                
                tube=await self.station1.getNextEmergencyGreenTube()        
            if tube is not None:
                await self.set_1_To_4_Job(tube)
                return True      
        return False
    
    # Camera 1 to Camera 2, only Green Tubes
    async def getStation1_To_4_3_Job(self):
        if await self.station3.getStatus() == MachineStatus.Off:
            return False
        if await self.station3.getStatusLoad() == MachineStatus.On:
            tube=None
            if await self.station5.isAvailableForGreen():
                await self.refreshCamera1Results()                
                tube=await self.station1.getNextGreenTube()        
            if tube is not None:
                await self.set_1_To_4_Job(tube)
                return True      
        return False

    # Camera 1 to Camera 2, only emergency orange brown and yellow tubes
    async def getStation1_To_4_14_Emergency_Job(self):
        if await self.station8.getStatus() == MachineStatus.Filled:
            tube=None       
            if await self.station5.isAvailableForOrangeYellow():
                await self.refreshCamera1Results()
                tube=await self.station1.getNextEmergencyOrangeYellowTube()
            if tube is None:
                if await self.station5.isAvailableForBrown():
                    await self.refreshCamera1Results()
                    tube=await self.station1.getNextEmergencyBrownTube()
            if tube is not None:
                await self.set_1_To_4_Job(tube)
                return True        
        if await self.station6.isAvailable():
            if await self.station1.isFilledWithCentrifugeEmergencyTubes():
                await self.station5.prepareCounterWeightJobs()
                if await self.station5.currentBatchFilled():
                    await self.station1.setCentrifugeEmergencyIterator(0)
                    return await self.getStation5_To_6_Job()
        return False 
    
    # Camera 1 to Camera 2, only orange brown and yellow tubes
    async def getStation1_To_4_14_Job(self):
        if await self.station8.getStatus() == MachineStatus.Filled:
            tube=None       
            if await self.station5.isAvailableForOrangeYellow():
                await self.refreshCamera1Results()
                tube=await self.station1.getNextOrangeYellowTube()
            if tube is None:
                if await self.station5.isAvailableForBrown():
                    await self.refreshCamera1Results()
                    tube=await self.station1.getNextBrownTube()
            if tube is not None:
                await self.set_1_To_4_Job(tube)
                return True
        if await self.station6.isAvailable():
            await self.station5.prepareCounterWeightJobs()
            if await self.station5.currentBatchFilled():
                return await self.getStation5_To_6_Job()
        return False  
    
    # red tubes from camera1 to camera2 emergency
    async def getStation1_To_4_9_Emergency_Job(self):
        if await self.station7.getStatus() == MachineStatus.Off:
            return False
        tube = None
        if await self.station9.isAvailable(TubeType.ADULT) and await self.station9.isAvailable(TubeType.CHILD):            
            await self.refreshCamera1Results()
            tube=await self.station1.getNextEmergencyRedTube()
            if tube is not None:
                await self.set_1_To_4_Job(tube)
                return True
        if tube is None:
            if await self.station1.isFilledWithRedEmergencyTubes():
                if await self.station9.currentBatchFilled():
                    await self.station1.setRedEmergencyIterator(0)
                    return await self.getStation9_To_7_Job()
        return False
    
    # red tubes from camera1 to camera2 
    async def getStation1_To_4_9_Job(self):
        if await self.station7.getStatus() == MachineStatus.Off:
            return False
        tube = None
        if await self.station9.isAvailable(TubeType.ADULT) and await self.station9.isAvailable(TubeType.CHILD):            
            await self.refreshCamera1Results()
            tube=await self.station1.getNextRedTube()
            if tube is not None:
                await self.set_1_To_4_Job(tube)
                return True
        if tube is None:
            if await self.station9.currentBatchFilled():
                return await self.getStation9_To_7_Job()
        return False

    async def getStation7StartMachineJob(self):
        if await self.station7.getStatus() == MachineStatus.Filled:
            tubeCount=await self.station9.getFilledBatchCount()
            await self.station7.startMachine(tubeCount)            
            return True
        return False
    
    async def getStation7_To_9_Job(self):
        if await self.station7.getStatus() == MachineStatus.Completed:
            srcJobId=self.station7.jobs[1].jobId
            # destJobId=self.station9.jobs[2].jobId
            await processQueue.enqueue([srcJobId,srcJobId])
            processQueue.destLocation.extend(dummyLocation)
            # location=await self.station9.getLocationOfRunningJob()
            # processQueue.destLocation.extend([location,location])          
            # jobslogger.info("rack moved from {0} to {1}".format(self.station7.name,self.station9.name)) 
            # await self.station7.setStatus(MachineStatus.On)
            # await self.station9.moveBatchFromFilledToCompleted()
            return True
        return False

    #from camera 2 to coagulation machine, cobas pure rack and haematology machine
    async def getStation4NextJob(self,isSuccess):
        res=self.conn_Q400.getCurrentTubeResults()
        try:
            tube=self.station4.tube
            if res.color != Color.NONE:
                tube.color = res.color
            if int(isSuccess) == 1 and tube is not None:                   
                if tube.color == Color.GREEN:
                    location=await self.station5.getNextLocationSmall()
                    processQueue.destLocation.extend([location,location]) 
                    await self.station5.updateGrid(tube.color,tube.type)
                    jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                    jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station5.name))
                    await self.fileManager.processFiles(res) 
                    sftpCommunication.moveCSVToSFTPServer()
                    self.conn_Q400.resetCurrentTubeResults()
                    return self.station5.jobs[2].jobId         
                elif tube.color == Color.ORANGE or tube.color == Color.BROWN or tube.color == Color.YELLOW:
                    location = None
                    if tube.color == Color.BROWN:
                        location=await self.station5.getNextLocationBig()
                    else:
                        location=await self.station5.getNextLocationSmall()
                    processQueue.destLocation.extend([location,location])
                    await self.station5.updateGrid(tube.color,tube.type)
                    jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                    jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station5.name))
                    await self.fileManager.processFiles(res) 
                    sftpCommunication.moveCSVToSFTPServer()
                    self.conn_Q400.resetCurrentTubeResults() 
                    return self.station5.jobs[2].jobId                    
                elif tube.color == Color.RED or tube.color == Color.CRED:
                    if tube.color == Color.RED:
                        location=await self.station9.getNextLocation(TubeType.ADULT)
                    elif tube.color == Color.CRED:
                        location=await self.station9.getNextLocation(TubeType.CHILD)
                    processQueue.destLocation.extend([location,location])
                    await self.station9.updateGrid(tube.color)
                    jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                    jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station9.name))
                    await self.fileManager.processFiles(res) 
                    sftpCommunication.moveCSVToSFTPServer()
                    self.conn_Q400.resetCurrentTubeResults()
                    return self.station9.jobs[4].jobId
            # tube to move to fehler pallette 
            location=await self.station10.getNextLocation() 
            processQueue.destLocation.extend([location,location]) 
            await self.station10.updateGrid(tube.type)
            jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
            jobslogger.info("{0} tube moved from {1} to {2} ".format(tube.color.name,self.station4.name,self.station10.name)) 
            #await self.fileManager.processFailedFilesAfterCentrifugation(res)
            self.conn_Q400.resetCurrentTubeResults()
            # await commManager.sendMessage(Settings.failtubemsg)
            # return [self.station10.jobs[2].jobId,self.station10.jobs[2].jobId,tube.type]
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
            if int(isSucess) == 1 and tube is not None:
                if tube.color == Color.GREEN and await self.station3.getStatus() != MachineStatus.Off:
                    location=await self.station3.getNextLocation()
                    processQueue.destLocation.extend([location,location]) 
                    await self.station3.updateGrid(tube.color)     # Calling from Robot
                    res.color=tube.color
                    jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                    jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station3.name))
                    #await self.fileManager.processFilesAfterCentrifugation(res) 
                    self.conn_Q400.resetCurrentTubeResults()
                    return self.station3.jobs[2].jobId
                elif (tube.color == Color.ORANGE or tube.color == Color.BROWN or tube.color == Color.YELLOW) and await self.station8.getStatus() != MachineStatus.Off:
                    location=await self.station14.getNextLocation()
                    processQueue.destLocation.extend([location,location]) 
                    await self.station14.updateGrid(tube.color)
                    tubesCount = await self.station14.fillTubesGridMax(tube.color)
                    if tubesCount != -1:
                        await self.station8.updateGrid(tubesCount)
                    res.color=tube.color  
                    jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                    jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station14.name))
                    #await self.fileManager.processFilesAfterCentrifugation(res) 
                    self.conn_Q400.resetCurrentTubeResults() 
                    return self.station14.jobs[3].jobId      
             # tube to move to fehler pallette 
            location=await self.station10.getNextLocation() 
            processQueue.destLocation.extend([location,location]) 
            await self.station10.updateGrid(tube.type)
            jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
            jobslogger.info("{0} tube moved from {1} to {2} ".format(tube.color.name,self.station4.name,self.station10.name)) 
            #await self.fileManager.processFailedFilesAfterCentrifugation(res)
            self.conn_Q400.resetCurrentTubeResults()
            # await commManager.sendMessage(Settings.failtubemsg)
            # return [self.station10.jobs[2].jobId,self.station10.jobs[2].jobId,tube.type]
            return self.station10.jobs[2].jobId
        except Exception as e: 
            traceback.print_exc()
            errorlogger.exception(e)
            processQueue.destLocation=[]
            raise CommonError("Unexpected error occurred. Please check logs!")
    
    async def getStation3NextJob(self,isSuccess):
        jobId = await self.station3.stopMachineSuccess(int(isSuccess))
        if jobId != 0:
            processQueue.destLocation.extend(dummyLocation)  
        return jobId
    
    async def getStation7NextJob(self,isSuccess):
        if int(isSuccess) == 1:
            destJobId=self.station9.jobs[2].jobId
            # await processQueue.enqueue([destJobId,destJobId])
            location=await self.station9.getLocationOfRunningJob()
            processQueue.destLocation.extend([location,location])            
            jobslogger.info("rack moved from {0} to {1}".format(self.station7.name,self.station9.name)) 
            await self.station7.setStatus(MachineStatus.On)
            await self.station9.moveBatchFromFilledToCompleted()
            return destJobId
        else:
            await self.station7.startMachineAgain()
            # processQueue.destLocation.extend(dummyLocation) 
        return 0
    
    #from 17 to 11
    async def getStation17NextJob(self,isSuccess):
        try:
            if int(isSuccess) == 1:
                destJobId = self.station11.jobs[2].jobId
                fridgeNo=await self.station11.getNextAvailableFridgeNo()
                # await processQueue.enqueue([destJobId,destJobId,TubeType.SMALL,fridgeNo])
                destLoc = await self.station11.getNextLocation()
                processQueue.destLocation.extend([destLoc,destLoc])
                await self.station11.updateGrid(Color.ORANGE)
                jobslogger.info("Placed the tube in Archiv at {0}".format(destLoc)) 
                return destJobId, fridgeNo
            return 0, 0
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

    async def ping(self):
        try:
            currentTime=datetime.now()
            if self.lastPingTime == None:
                self.lastPingTime=currentTime
            diffTime=currentTime - self.lastPingTime 
            self.lastPingTime=currentTime
            diff=diffTime.total_seconds()*1000
            if diff > Settings.pingInterval:
                # jobslogger.info("ping interrupted for:{0} milli seconds ".format(diff)) 
                # print("ping interrupted for: ",diff)
                self.station1.isRefreshCamera1Results=True
                self.stn1_good = False
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
        self.station1.isRefreshCamera1Results = isOn
        jobslogger.info("Robot paused and resumed, Set the camera flag to {0}".format(isOn)) 

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
        res = True
        await self.station6.startRuntimeAlarm()
        return res

    async def send_skype_message(self, msg):
        # res = await commManager.sendMessage(msg)
        print(msg)
        return True

    async def getTestJob(self):
        # srcLoc = self.station18.testRacksArray[self.testCounter % 10]
        # self.testCounter += 1
        # index, destLoc = await self.station2.getNextLocationToPlace()
        # processQueue.destLocation.extend([srcLoc, destLoc])        
        # return [181, 22, TubeType.SMALL, index]
        """ index, location = await self.station2.getNextLocationToPick()
        processQueue.destLocation.extend([location, location])
        return [21, 142, TubeType.SMALL, index] """
        # processQueue.destLocation.extend([[0,0,0,0,0,0], [2,0,0,0,0,0]])  
        # return [114, 114, TubeType.SMALL,1]
        # processQueue.destLocation.extend([[2, 20.60693422222228, 0.0, -180.0, 0.0001, -90.0], [2, 150.0, 180.0, 0.0, 90.0]])  
        # return [114, 114, TubeType.SMALL,1]
        srcLoc = self.station3.machines[self.testCounter].location
        self.testCounter += 1
        #index, destLoc = await self.station2.getNextLocationToPlace()
        # processQueue.destLocation.extend([srcLoc, srcLoc])        
        # return [34, 34, TubeType.SMALL]
        processQueue.destLocation.extend([[2,0,0,0,0,0], [2,0,0,0,0,0]])  
        return [51, 62, TubeType.SMALL,1]
   
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
    
    async def setJobsLocations(self,jobArray):
        if jobArray[0] != 0:
            self.interfaceOut.srcJob = jobArray[0]
            self.interfaceOut.destJob = jobArray[1]
            locations = await mainObj.getCurrentLocation()
            self.interfaceOut.srcPos = locations[0]
            self.interfaceOut.destPos = locations[1]
            if jobArray.__len__() >= 3:
                if jobArray[2] == TubeType.BIG:
                    self.interfaceOut.tubeType=TubeType.BIG.value
                if jobArray[2] == TubeType.SMALL:
                    self.interfaceOut.tubeType=TubeType.SMALL.value
            else:
                self.interfaceOut.tubeType=TubeType.SMALL.value
            if jobArray.__len__() == 4:
                self.interfaceOut.generic[0]=jobArray[3]

    async def handling_buffer(self,data):    
        # await mainObj.ping()    
        data = data.decode('utf-8')
        self.interfaceIn.setData(data)  
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
                    if self.interfaceIn.dataFromRobot[6] == 1:
                        await mainObj.setCamera1Flag(True)
                    jobArray = await mainObj.getJob()
                    #jobArray = await mainObj.getTestJob()
                    await self.setJobsLocations(jobArray) 
                elif(self.interfaceIn.dataFromRobot[2] == 2 or self.interfaceIn.dataFromRobot[2] == 3):   # Stn4 Next Job ID, lockID
                    if self.interfaceIn.dataFromRobot[2] == 2:         # Stn4 Next Job ID before centrifugation, lockID
                        stn4_get_next_jobId = await mainObj.getStation4NextJob(int(self.interfaceIn.dataFromRobot[3]))
                    else:                                              # Stn4 Next Job ID after centrifugation, lockID
                        stn4_get_next_jobId = await mainObj.getStation4NextJob_afterCentrifugation(int(self.interfaceIn.dataFromRobot[3]))
                    await self.setJobsLocations([stn4_get_next_jobId,stn4_get_next_jobId]) 
                elif(self.interfaceIn.dataFromRobot[2] == 4):                    # BCS Next Job
                    stn3_get_next_jobId = await mainObj.getStation3NextJob(int(self.interfaceIn.dataFromRobot[3]))
                    await self.setJobsLocations([stn3_get_next_jobId,stn3_get_next_jobId])
                elif(self.interfaceIn.dataFromRobot[2] == 5):                    # Beckmann next job
                    stn7_get_next_jobId = await mainObj.getStation7NextJob(int(self.interfaceIn.dataFromRobot[3]))
                    await self.setJobsLocations([stn7_get_next_jobId,stn7_get_next_jobId])
                elif(self.interfaceIn.dataFromRobot[2] == 6):
                    stn17_get_next_jobId, fridgeNum = await mainObj.getStation17NextJob(int(self.interfaceIn.dataFromRobot[3]))
                    await self.setJobsLocations([stn17_get_next_jobId,stn17_get_next_jobId,TubeType.SMALL,fridgeNum])
                elif(self.interfaceIn.dataFromRobot[2] == 7):
                    stn18_get_next_jobId, fridgeNum = await mainObj.getStation17NextJob(int(self.interfaceIn.dataFromRobot[3]))
                    await self.setJobsLocations([stn18_get_next_jobId,stn18_get_next_jobId,TubeType.SMALL,fridgeNum])
            elif(self.interfaceIn.dataFromRobot[4] == 41):
                self.interfaceOut.status = await mainObj.conn_Q400.q400_execute_cam2(int(self.interfaceIn.dataFromRobot[2]))
            elif(self.interfaceIn.dataFromRobot[4] == 61):  # centrifuge check lock
                await mainObj.station6.initCentrifuge()
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
                await mainObj.station1.initGrids(pose[0], pose[1], pose[2], 6, 15)  
            elif(self.interfaceIn.dataFromRobot[4] == 21):  # Cobas Pure Racks Storage (1 to 12)
                pose = self.getPose(3)
                await mainObj.station2.initGrids_1(pose[0], pose[1], pose[2], 1, 10)
            elif(self.interfaceIn.dataFromRobot[4] == 22):  # Cobas Pure Racks Storage (13 to 25)
                pose = self.getPose(3)
                await mainObj.station2.initGrids_2(pose[0], pose[1], pose[2], 1, 10)
            elif(self.interfaceIn.dataFromRobot[4] == 23):  # Cobas Pure Racks Storage (26 to 37)
                pose = self.getPose(3)
                await mainObj.station2.initGrids_3(pose[0], pose[1], pose[2], 1, 10)
            elif(self.interfaceIn.dataFromRobot[4] == 24):  # Cobas Pure Racks Storage  (38 to 50)
                pose = self.getPose(3)
                await mainObj.station2.initGrids_4(pose[0], pose[1], pose[2], 1, 10)
            elif(self.interfaceIn.dataFromRobot[4] == 31):  # BCS tubes
                pose = self.getPose(3)
                await mainObj.station3.initGrids(pose[0], pose[1], pose[2], 10, 4)
            elif(self.interfaceIn.dataFromRobot[4] == 32):  # BCS racks
                pose = self.getPose(3)
                await mainObj.station3.initMachinesGrid(pose[0], pose[1], pose[2], 1, 4)
            elif(self.interfaceIn.dataFromRobot[4] == 4):  # Q400
                await mainObj.conn_Q400.initVQ400()                 
            elif(self.interfaceIn.dataFromRobot[4] == 91):  # Beckman Tube initialization
                pose = self.getPose(3)
                await mainObj.station9.initGrids(pose[0], pose[1], pose[2],5,4) 
            elif(self.interfaceIn.dataFromRobot[4] == 92):  # Beckman Rack initialization
                pose = self.getPose(3)
                await mainObj.station9.initRackGrid(pose[0], pose[1], pose[2],1,4) 
            elif(self.interfaceIn.dataFromRobot[4] == 5):  # Centrifuge racks TubePos initialization
                pose = self.getPose(5)
                await mainObj.station5.initGrids(pose[0], pose[1], pose[2], 4, 2, pose[3],pose[4], 3, 3)
            elif(self.interfaceIn.dataFromRobot[4] == 55):  # Centrifuge counter weights initialization
                pose = self.getPose(4)
                await mainObj.station5.initCounterGrids(pose[0], pose[1], pose[2], pose[3]) 
            elif(self.interfaceIn.dataFromRobot[4] == 10):  # Fehler initialization    
                pose = self.getPose(3)
                await mainObj.station10.initGrids(pose[0], pose[1], pose[2], 5, 5)
            elif(self.interfaceIn.dataFromRobot[4] == 111):  # Archive initialization fridge 1   
                pose = self.getPose(3)
                await mainObj.station11.initGrids(pose[0], pose[1], pose[2], 5, 7, 1)  
            elif(self.interfaceIn.dataFromRobot[4] == 112):  # Archive initialization  fridge 2             
                pose = self.getPose(3)
                await mainObj.station11.initGrids(pose[0], pose[1], pose[2], 5, 7, 2)            
            elif(self.interfaceIn.dataFromRobot[4] == 14):  # Cobas Pure Rack Holder            
                pose = self.getPose(3)
                await mainObj.station14.initGrids(pose[0], pose[1], pose[2], 5, 1)            
            elif (self.interfaceIn.dataFromRobot[4] == 17):  # Cobas Pure Filled Rack Holder 1
                pose = self.getPose(5)
                await mainObj.station17.initGrids(pose[0], pose[1], 1, 10, pose[2], pose[3], pose[4], 5, 10)
            elif (self.interfaceIn.dataFromRobot[4] == 18):  # Cobas Pure Filled Rack Holder 2
                pose = self.getPose(5)
                await mainObj.station18.initGrids(pose[0], pose[1], 1, 10, pose[2], pose[3], pose[4], 5, 10)
            elif (self.interfaceIn.dataFromRobot[4] == 701):
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_CAM_1))
            elif (self.interfaceIn.dataFromRobot[4] == 703):
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_BCS_MACHINE))    
            elif (self.interfaceIn.dataFromRobot[4] == 705):
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_CENTRIFUGE))
            elif (self.interfaceIn.dataFromRobot[4] == 707):
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_BECKMANN_LOAD))
            elif (self.interfaceIn.dataFromRobot[4] == 708):
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_COBAS_MACHINE))  
            elif (self.interfaceIn.dataFromRobot[4] == 711):
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_FRIDGE_2)) 
            elif (self.interfaceIn.dataFromRobot[4] == 715):
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_COBAS_BASKET_15))
            elif (self.interfaceIn.dataFromRobot[4] == 717):
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_COBAS_SLIDE_15))
            elif (self.interfaceIn.dataFromRobot[4] == 718):
                await mainObj.axis7.sendMessage(mainObj.axis7.posStr(Settings.HOME_POS_COBAS_SLIDE_16))
            elif(self.interfaceIn.dataFromRobot[4] == 100):  # Fehler reset
                await mainObj.station10.resetFehler(True)
            elif(self.interfaceIn.dataFromRobot[4] == 11):  # Archiv Reset
                await mainObj.station11.resetArchive(True)
            elif(self.interfaceIn.dataFromRobot[4] == 3):  # Status of BCS
                await mainObj.setMachineStatus(Settings.macId_coagulation, True)
            elif(self.interfaceIn.dataFromRobot[4] == 7):  # Status of Beckmann
                await mainObj.setMachineStatus(Settings.macId_haematology, True)
            elif(self.interfaceIn.dataFromRobot[4] == 8):  # Status of Cobas Pure
                await mainObj.setMachineStatus(Settings.macId_chemistry, True)
            self.interfaceOut.stateOfHandshake = 1       # State of Handshake          
            self.isBusy = False
        if(self.interfaceIn.dataFromRobot[1] == 0 and self.interfaceOut.stateOfHandshake == 1 and not self.isBusy):
            self.interfaceOut.stateOfHandshake = 0
        self.transport.write(self.interfaceOut.getData().encode())    


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
            print("Retrying Service ... at {0} - {1}".format(Settings.systemip,Settings.systemport))
            errorlogger.exception("Retrying attempt: {0}".format(retry_count+1))

   
if __name__ == '__main__':
    # loop = asyncio.get_running_loop()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.run_forever()
    asyncio.run(main())
