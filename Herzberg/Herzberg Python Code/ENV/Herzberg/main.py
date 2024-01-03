from datetime import datetime
import traceback
# from communicationManager import commManager
from filemanager import FileManager
from station10 import Station10
from station2 import Station2
from station3 import Station3
from station4 import Station4
from station5 import Station5
from station6 import Station6
from station8 import Station8
from station11 import Station11
from station14 import Station14
from station15 import Station15
import urlib
from aiohttp import web
from aiohttp_xmlrpc import handler
from machine import MachineStatus
from settings import Settings, Color, BatchStatus, HolderStatus
from station1 import Station1
from station7 import Station7
from stations import CommonError, Job, processQueue, Station, Stn4ColorError
from vq400connector import Vq400Connector
from logger import jobslogger,errorlogger


class MainApp:
    def __init__(self):
        self.machines = {}
        self.conn_Q400=Vq400Connector(Settings.vq400host)
        self.lastPingTime=None
        self.initialize()
        self.fileManager=FileManager()
        print("Service is running... at {0} - {1}".format(Settings.systemip,Settings.systemport))      

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
            await self.station6.resetConnections()            
            self.initialize()
            # await commManager.connectToSkype()
            print("Robot (re)started at : {0}".format(str(datetime.now())))  
        except Exception as e: 
            errorlogger.exception(e)
            raise CommonError("Error occurred during reset")

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
            Job(20,"Initial"),
            Job(21,"pick"),
            Job(22,"place"),
            Job(23,"Door 1 open"),
            Job(24,"Door 1 close"),
            Job(25,"Door 2 open"),
            Job(26,"Door 2 close"),
            Job(27,"Door 3 open"),
            Job(28,"Door 3 close"), 
            Job(29,"3 batches used")          
        ])
        self.station3=Station3("coagulation machine",
        [
            Job(30,"Initial"),
            Job(31,"pick"),
            Job(32,"place"),
            Job(33,"start Machine"),
            Job(34,"close popup"),
            Job(35,"refresh standby")
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
        self.station7=Station7("haematology machine",
        [
            Job(70,"Initial"),
            Job(71,"pick"),
            Job(72,"place"),
            Job(73,"start"),
            Job(74,"open door"),
            Job(75,"close door"),
        ])
        self.station8=Station8("Chemistry machine",
        [
            Job(0,"Initial"),
            Job(0,"pick"),
            Job(82,"place")
        ])
        self.station9=Station11("electric gripper",
        [
            Job(90,"Initial"),
            Job(91,"pick"),
            Job(92,"place")
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
            Job(113,"show bin filled")
        ])
        self.station12=Station("Haematology bin",
        [
            Job(120,"Initial"),
            Job(121,"pick"),
            Job(122,"place")
        ])
        self.station13=Station("Decap bin",
        [
            Job(130,"Initial"),
            Job(131,"pick"),
            Job(132,"place")
        ])
        self.station14=Station14("Cobas pure rack holder ",
        [
            Job(140,"Initial"),
            Job(141,"pick rack"),
            Job(142,"place rack"),
            Job(143,"place tube")
        ])
        self.station15=Station15("Sysmex parking station ",
        [
            Job(150,"Initial"),
            Job(151,"pick tube"),
            Job(152,"place tube")
        ])
    
    async def setMachineStatus(self,machineId,isOn):
        try:
            match machineId: 
                case Settings.macId_all:
                    await self.station7.prepareInitJobWithStatus(isOn)
                    await self.station3.prepareInitJobWithStatus(isOn)
                    await self.station8.prepareInitJobWithStatus(isOn)
                    await self.station6.prepareInitJobWithStatus(isOn)
                    await self.station7.setTogetherTubesMax(isOn)
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
                    await self.station7.setTogetherTubesMax(isOn)
                # case Settings.maxId_haematology_both:
                #     await self.station7.setTogetherTubesMax(isOn)
                # case Settings.maxId_haematology_one:
                #     await self.station7.setIndividualTubesMax(isOn)
        except Exception as e: 
            errorlogger.exception(e)
            raise CommonError("Error occurred during set machine status")

    async def getResultsFromCamera1(self):
        await self.conn_Q400.q400_execute_cam1(22)
        rows=await self.conn_Q400.q400_execute_cam1(21)
        self.lastPingTime=None
        return rows

    async def modifyRefreshFlag(self):
        if (((self.station3.isInitialized or await self.station3.getStatus() == MachineStatus.On) and self.station1.isGreenAvailable and await self.station5.isAvailableForGreen()) or ((await self.station8.getStatus() == MachineStatus.On) and self.station1.isOrangeAvailable and await self.station5.isAvailableForOrange()) or (self.station7.isInitialized and self.station1.isRedAvailable and (await self.station7.isAvailableAdult() or await self.station7.isAvailableChild()))):
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
        
    async def getCurrentLocation(self):
        location=processQueue.destLocation
        processQueue.destLocation=[]
        jobslogger.info("Sent locations Source,Destination: {0}".format(location))
        return location

    async def getStation5GridLocations(self):
        locations=processQueue.stn5GridLocations
        processQueue.stn5GridLocations=[]
        jobslogger.info("Sent locations Source,Destination: {0}".format(locations))
        return locations
    
    async def getTestJob(self):
        location={'x': -0.038528583303603446, 'y': 0.06588481789436851, 'z': 0.2099640039926176, 'rx': 3.14139940436524, 'ry': -0.015477257807032949, 'rz': 0.0002312832234047768}
        location1={'x': -0.038528583303603446, 'y': 0.06588481789436851, 'z': 0.2099640039926176, 'rx': 3.14139940436524, 'ry': -0.015477257807032949, 'rz': 0.0002312832234047768}
        processQueue.destLocation.extend([location,location1])
        return [103,103]
    
    async def getJob(self):
        try:            
            if not(await processQueue.isEmpty()) or await self.checkAndPrepareForJobs():            
                dest= await processQueue.dequeue()
                if dest is not None:
                    # Whenever there are tubes in Sysmex machine, especially 1, if refresh standby alarm comes after picking the tube from camera 1
                    # and placing it in Sysmex, then job 70 comes which closes and start the machine, so when there are tubes, we check the counter and start the machine.
                    if dest[0] == 70:
                        if await self.station7.areTubesFilledInMachine():
                            jobslogger.info("Sent Jobs Source,Destination: [0, 0] instead of [70, 70] as there are tubes in machine")
                            processQueue.destLocation=[]
                            return [0,0]
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
        if await self.station3.getStation3Jobs():
            return True
        if await self.getStation14_8_Job():
            return True
        if await self.station7.getStation7Jobs():
            return True 
        if await self.getStation7_To_12_Job():
            return True
        if await self.getStation3_To_11_Job():
            return True
        if await self.getStation5_To_4_3_Job():
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
        if await self.getStation1_To_4_2_Job():
            return True       
        if await self.getStation15_To_7_Jod():
            return True
        if await self.getStation1_To_4_7_Job():
            return True               
        return False
    
    #from haematology machine to bin
    async def getStation7_To_12_Job(self):
        if not(self.station7.isInitialized):
            return False
        if await self.station7.getStatus() == MachineStatus.Completed:
            await self.station7.closeDoors()         
            tube = await self.station7.getNextTubeToBin()
            if tube is not None:
                srcJobId=self.station7.jobs[1].jobId 
                destJobId=self.station12.jobs[2].jobId 
                processQueue.destLocation.extend([tube.location,tube.location])            
                await processQueue.enqueue([srcJobId,destJobId])
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station7.name,self.station12.name)) 
                return True
        return False
    
    #from coagulation machine to archive
    async def getStation3_To_11_Job(self):
        if not(self.station3.isInitialized):
            return False
        if await self.station3.getStatus() == MachineStatus.Completed:
            stn3_status = await self.getCamera3Results(3)
            if not stn3_status:
                return False
            tube=await self.station3.getNextTube()
            if tube is None:    
                if await self.station3.currentBatchEmpty():
                    return await self.getStation5_To_4_3_Job()
            if tube is not None:
                srcJobId=self.station3.jobs[1].jobId 
                destJobId=self.station11.jobs[2].jobId 
                location=await self.station11.getNextLocation()
                processQueue.destLocation.extend([tube.location,location])            
                await processQueue.enqueue([srcJobId,destJobId])                       
                await self.station11.updateGrid(tube.color)
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station3.name,self.station11.name)) 
                await self.station3.close_check_popup()
                return True
        return False
    
    # centrifuge racks to camera2 only Green tubes
    async def getStation5_To_4_3_Job(self):
        if not(self.station3.isInitialized):
            return False
        tube=None
        if await self.station3.isAvailable():
            tube=await self.station5.getNextGreenTube()
            if tube is None:
                    if await self.station3.setMachineFilled():
                        return await self.station3.getStation3Jobs()
            else:
                srcJobId=self.station5.jobs[1].jobId 
                destJobId=self.station4.jobs[1].jobId 
                processQueue.destLocation.extend([tube.location,tube.location])            
                await processQueue.enqueue([srcJobId,destJobId])                       
                await self.station4.updateGrid(tube)
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station5.name,self.station4.name))
                return True        
        return False
    
    # from cobas pure rack holder to cobas pure machine
    async def getStation14_8_Job(self):
        # if not(self.station8.isInitialized):
        #     return False
        if await self.station8.getStatus() == MachineStatus.On:
            return await self.station14.placeRackInMachine()       
        return False
    
    # from cobas pure racks to cobas pure rack holder
    async def getStation2_14_Job(self):
        # if not(self.station8.isInitialized):
        #     return False
        if await self.station8.getStatus() == MachineStatus.On:            
            if await self.station14.getHolderStatus() == HolderStatus.Empty:
                await self.station2.isCurrentBatchEmpty()              
                await self.station2.getCurrentBatchOpenDoorJobID()
                location = await self.station2.getNextLocation()
                if location is not None:        
                    srcJobId = self.station2.jobs[1].jobId
                    destJobId = self.station14.jobs[2].jobId                    
                    await processQueue.enqueue([srcJobId,destJobId])
                    processQueue.destLocation.extend([location,location])
                    await self.station2.updateGrid()
                    # await self.station14.fillHolder()
                    jobslogger.info("Cobas pure rack moved from {0} to {1}".format(self.station2.name,self.station14.name))
                    return True        
        return False

    # centrifuge racks to camera2 only orange tubes
    async def getStation5_To_4_14_Job(self):
        tube=None        
        if await self.station14.isAvailable():
            tube = await self.station5.getNextOrangeTube()
            if tube is None:    
                # if await self.station14.fillTubesGrid():
                #     return await self.getStation2_14_Job()
                if await self.station14.fillTubesGrid():
                    return await self.getStation14_8_Job()
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
                processQueue.stn5GridLocations.extend(locations)             
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
                processQueue.stn5GridLocations.extend(locations)              
                await processQueue.enqueue([srcJobId,destJobId])                       
                await self.station6.setStatus(MachineStatus.Filled)
                jobslogger.info("batch moved from {0} to {1}".format(self.station5.name,self.station6.name))
                return True
        return False
    
    # Camera 1 to Camera 2, only Green Tubes
    async def getStation1_To_4_3_Job(self):     
        if self.station3.isInitialized or await self.station3.getStatus() == MachineStatus.On:
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

    # Camera 1 to Camera 2, only orange tubes
    async def getStation1_To_4_2_Job(self):
        if await self.station8.getStatus() == MachineStatus.On:
            tube=None       
            if await self.station5.isAvailableForOrange():
                await self.refreshCamera1Results()
                tube=await self.station1.getNextOrangeTube()
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

    # Sysmex parking station to Sysmex machine
    async def getStation15_To_7_Jod(self):
        if not(self.station7.isInitialized):
            return False
        if await self.station7.isAvailableAdult() or await self.station7.isAvailableChild():
            tube = await self.station15.getNextFilledTube()
            if tube is not None:
                if not self.station7.isDoorOpened:
                    jobId=self.station7.jobs[4].jobId
                    await processQueue.enqueue([jobId,jobId])
                    self.station7.isDoorOpened=True
                if tube.color == Color.RED and await self.station7.isAvailableAdult():
                    srcJobId=self.station15.jobs[1].jobId 
                    destJobId=self.station7.jobs[2].jobId 
                    destLocation = await self.station7.getNextLocationAdult()
                    processQueue.destLocation.extend([tube.location,destLocation])                        
                    await processQueue.enqueue([srcJobId,destJobId])  
                    await self.station15.updateFilledTube(tube)                     
                    await self.station7.updateGridAdult(tube.color)
                    jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station15.name,self.station7.name))
                    return True
                if tube.color == Color.CRED and await self.station7.isAvailableChild():
                    srcJobId=self.station15.jobs[1].jobId 
                    destJobId=self.station7.jobs[2].jobId 
                    destLocation = await self.station7.getNextLocationChild()
                    processQueue.destLocation.extend([tube.location,destLocation])                        
                    await processQueue.enqueue([srcJobId,destJobId])
                    await self.station15.updateFilledTube(tube)                   
                    await self.station7.updateGridChild(tube.color)
                    jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station15.name,self.station7.name))
                    return True
        return False

    # red tubes from camera1 to camera2 
    async def getStation1_To_4_7_Job(self): 
        if not(self.station7.isInitialized):
            return False
        if await self.station7.isAvailableAdult() or await self.station7.isAvailableChild():            
            await self.refreshCamera1Results()  
            tube = None
            if self.station7.statusAdult == MachineStatus.On and await self.station7.isAvailableAdult():
                tube = await self.station1.getNextRedTubeAdult() 
            if tube is None and self.station7.statusChild == MachineStatus.On and await self.station7.isAvailableChild():
                tube = await self.station1.getNextRedTubeChild()
            # tube=await self.station1.getNextRedTube()
            if tube is None:
                if await self.station7.setMachineFilled():
                    return await self.station7.getStation7Jobs()
            if tube is not None:
                if not self.station7.isDoorOpened:
                    jobId=self.station7.jobs[4].jobId
                    await processQueue.enqueue([jobId,jobId])
                    self.station7.isDoorOpened=True
                srcJobId=self.station1.jobs[1].jobId 
                destJobId=self.station4.jobs[1].jobId 
                processQueue.destLocation.extend([tube.location,tube.location])                        
                await processQueue.enqueue([srcJobId,destJobId])                       
                await self.station4.updateGrid(tube)
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station1.name,self.station4.name))
                return True
        return False

    #from camera 2 to coagulation machine, cobas pure rack and haematology machine
    async def getStation4NextJob(self,isSuccess:bool):
        res=self.conn_Q400.getCurrentTubeResults()
        try:
            tube=self.station4.tube
            tube.color = res.color
            if isSuccess:   
                if tube is not None:                    
                    if tube.color == Color.GREEN:
                        location=await self.station5.getNextLocation()
                        processQueue.destLocation.extend([location,location]) 
                        await self.station5.updateGrid(tube.color)
                        # res.color=tube.color
                        jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                        jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station5.name))
                        await self.fileManager.deleteFiles()
                        # await self.fileManager.processFiles(res)
                        self.conn_Q400.resetCurrentTubeResults()
                        return self.station5.jobs[2].jobId                  
                    if tube.color == Color.ORANGE:
                        location=await self.station5.getNextLocation()
                        processQueue.destLocation.extend([location,location]) 
                        await self.station5.updateGrid(tube.color)
                        # res.color=tube.color  
                        jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                        jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station5.name))
                        await self.fileManager.deleteFiles()
                        # await self.fileManager.processFiles(res) 
                        self.conn_Q400.resetCurrentTubeResults() 
                        return self.station5.jobs[2].jobId
                    if tube.color == Color.RED:
                        if self.station7.statusAdult == MachineStatus.On: 
                            if await self.station7.isAvailableAdult():
                                location=await self.station7.getNextLocationAdult()
                                processQueue.destLocation.extend([location,location]) 
                                await self.station7.updateGridAdult(tube.color)  
                                # res.color=tube.color                     
                                jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station7.name))
                                await self.fileManager.deleteFiles()
                                # await self.fileManager.processFiles(res)
                                self.conn_Q400.resetCurrentTubeResults()                    
                                return self.station7.jobs[2].jobId
                            else:                                               
                                return await self.getStation15PlaceJob(tube, res)
                        else:   
                            return await self.getStation10PlaceJob(tube, res)
                    if tube.color == Color.CRED:
                        if self.station7.statusChild == MachineStatus.On:
                            if await self.station7.isAvailableChild():
                                location=await self.station7.getNextLocationChild()
                                processQueue.destLocation.extend([location,location]) 
                                await self.station7.updateGridChild(tube.color)  
                                # res.color=tube.color                     
                                jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station7.name))
                                await self.fileManager.deleteFiles()
                                # await self.fileManager.processFiles(res)
                                self.conn_Q400.resetCurrentTubeResults()                    
                                return self.station7.jobs[2].jobId   
                            else:                                               
                                return await self.getStation15PlaceJob(tube, res)   
                        else:   
                            return await self.getStation10PlaceJob(tube, res)
            else: 
                return await self.getStation10PlaceJob(tube, res)
        except Exception as e: 
            traceback.print_exc()
            errorlogger.exception(e)
            processQueue.destLocation=[]
            raise CommonError("Unexpected error occurred. Please check logs!")

    async def getStation15PlaceJob(self, tube, res):
        location=await self.station15.getNextEmptyLocation()
        processQueue.destLocation.extend([location,location])
        await self.station15.updateGrid(tube.color)
        jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
        jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station15.name))
        await self.fileManager.deleteFiles()
        # await self.fileManager.processFiles(res)
        self.conn_Q400.resetCurrentTubeResults()                    
        return self.station15.jobs[2].jobId
    
    async def getStation10PlaceJob(self, tube, res):
        location=await self.station10.getNextLocation()           
        processQueue.destLocation.extend([location,location]) 
        await self.station10.updateGrid(tube.color)
        # res.color=tube.color
        jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
        jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station10.name)) 
        await self.fileManager.processFailedFiles(res)
        # await self.fileManager.deleteFiles()
        self.conn_Q400.resetCurrentTubeResults()
        # await commManager.sendMessage(Settings.failtubemsg)
        return self.station10.jobs[2].jobId

    async def getStation4NextJob_afterCentrifugation(self,isSucess:bool):
        res=self.conn_Q400.getCurrentTubeResults()
        try:
            tube=self.station4.tube
            if isSucess:   
                if tube is not None:
                    if tube.color == Color.GREEN:
                        location=await self.station3.getNextLocation()
                        processQueue.destLocation.extend([location,location]) 
                        await self.station3.updateGrid(tube.color)
                        res.color=tube.color
                        jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                        jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station3.name))
                        await self.fileManager.deleteFiles()
                        self.conn_Q400.resetCurrentTubeResults()
                        return self.station3.jobs[2].jobId                  
                    if tube.color == Color.ORANGE:
                        location=await self.station14.getNextLocation()
                        processQueue.destLocation.extend([location,location]) 
                        await self.station14.updateGrid(tube.color)
                        res.color=tube.color  
                        jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                        jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station14.name))
                        await self.fileManager.deleteFiles()
                        self.conn_Q400.resetCurrentTubeResults() 
                        return self.station14.jobs[3].jobId            
            else:
                location=await self.station10.getNextLocation()           
                processQueue.destLocation.extend([location,location]) 
                await self.station10.updateGrid(tube.color)
                res.color=tube.color
                jobslogger.info("Camera 2 results: Color-{0},Barcode-{1},Blood level-{2},Plasma level-{3}".format(res.color.name,res.barCode,res.bloodLevel,res.plasmaLevel))
                jobslogger.info("{0} tube moved from {1} to {2}".format(tube.color.name,self.station4.name,self.station10.name)) 
                await self.fileManager.processFailedFilesAfterCentrifugation(res)
                self.conn_Q400.resetCurrentTubeResults()
                # await commManager.sendMessage(Settings.failtubemsg)
                return self.station10.jobs[2].jobId
        except Exception as e: 
            traceback.print_exc()
            errorlogger.exception(e)
            processQueue.destLocation=[]
            raise CommonError("Unexpected error occurred. Please check logs!")
        
    async def getStation4NextJobColor(self):        
        try:
            tube = self.station4.tube
            if tube is None:
                raise Stn4ColorError("Station4 got wrong color, it is not either GREEN or ORANGE, Color: " + str(color.name))
            color = tube.color
            jobslogger.info("Robot asked for tube color and returned {0}".format(color.name))
            if color == Color.GREEN:
                return 1
            elif color == Color.ORANGE:
                return 2
            else:
                errorlogger.info("Station4 got wrong color, it is not either GREEN or ORANGE, Color: " + str(color.name))
                raise Stn4ColorError("Station4 got wrong color, it is not either GREEN or ORANGE, Color: " + str(color.name))
        except Exception as e: 
            traceback.print_exc()
            errorlogger.exception(e)
            raise Stn4ColorError("Station4 got wrong color, it is not either GREEN or ORANGE, Color: " + str(color.name))
    
    async def setInitAlarm(self,macId):
        try:
            match macId:
                case Settings.macId_coagulation:
                    await self.station3.startInitTimer()
                case Settings.macId_centrifuge:
                    await self.station6.initCentrifuge()
                case Settings.macId_haematology:
                    await self.station7.startInitTimer()
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
        except Exception as e:
            errorlogger.exception(e)
            processQueue.destLocation=[]
            raise CommonError("Unexpected error occured. Please check logs!")
    
    async def isStation1Good(self):
        try:
            if not self.stn1_good:
                self.stn1_good = True
                return False
            return True
        except Exception as e: 
            errorlogger.exception(e)
            # raise CommonError("Error occured during ping. please check logs") 
            return False

    async def ping(self):
        try:
            currentTime=datetime.now()
            if self.lastPingTime == None:
                self.lastPingTime=currentTime
            diffTime=currentTime - self.lastPingTime 
            self.lastPingTime=currentTime
            diff=diffTime.total_seconds()*1000
            if diff > Settings.pingInterval:
                jobslogger.info("ping interrupted for:{0} milli seconds ".format(diff)) 
                self.station1.isRefreshCamera1Results=True
                self.stn1_good = False
        except Exception as e: 
            errorlogger.exception(e)
            raise CommonError("Error occured during ping. please check logs")  

    async def getCamera2Results(self,group:int):
        res = await self.conn_Q400.q400_execute_cam2(group)
        return res

    async def getCamera3Results(self,group:int):
        res = await self.conn_Q400.q400_execute_cam3(group)
        return res

    # need to be removed later
    async def setInitialized(self):
        self.station6.isInitialized=True
    
    async def setCamera1Flag(self,isOn:bool):
        self.station1.isRefreshCamera1Results=isOn
    
    async def stn7_start_machine(self):
        self.station7.counter=2
        self.station7.machine.status=MachineStatus.Filled
        return await self.station7.startMachine()

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
        return  res

    async def send_skype_message(self, msg):
        # res = await commManager.sendMessage(msg)
        print(msg)
        return True
   
mainObj=MainApp()


class XMLRPCHandler(handler.XMLRPCView):
    async def rpc_init_q400(self):
        return await mainObj.conn_Q400.initVQ400()
    async def rpc_q400_execute_cam2(self, group):
        return await mainObj.getCamera2Results(group)
    async def rpc_reset(self):
        await mainObj.reset()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    # async def rpc_fritzbox(self, address, user, password, number):
    #     return await mainObj.connect_to_fritzbox(address, user, password, number)
    async def rpc_set_machine_status(self, machineID, status):
        return await mainObj.setMachineStatus(machineID, status)
    async def rpc_set_stn1_grid(self, id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):        
        return await mainObj.station1.initGrids(id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
    async def rpc_set_stn2_grid(self, id, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5, ref_pose_6):
        return await mainObj.station2.initGrids(id, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5, ref_pose_6)
    async def rpc_set_stn3_grid(self, id, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5,ref_pose_6, ref_pose_7, ref_pose_8):
        return await mainObj.station3.initGrids(id, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5,ref_pose_6, ref_pose_7, ref_pose_8)   
    async def rpc_set_stn5_grid(self, id, ref_pose_1, ref_pose_2, ref_pose_3, p_rows, p_columns, ref_pose_4, ref_pose_5, ch_rows, ch_columns):
        return await mainObj.station5.initGrids(id, ref_pose_1, ref_pose_2, ref_pose_3, p_rows, p_columns, ref_pose_4, ref_pose_5, ch_rows, ch_columns)
    async def rpc_set_stn5_counter_grid(self, ref_pose_1, ref_pose_2):
        return await mainObj.station5.initCounterGrids(ref_pose_1, ref_pose_2)
    async def rpc_set_stn5_batch_grid(self, id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        return await mainObj.station5.initBatchGrids(id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
    async def rpc_set_stn7_grid(self, id, ref_pose_1, ref_pose_2, ref_pose_3, p_rows, p_columns, ref_pose_4, ref_pose_5, ch_rows, ch_columns):
        return await mainObj.station7.initGrids(id, ref_pose_1, ref_pose_2, ref_pose_3, p_rows, p_columns, ref_pose_4, ref_pose_5, ch_rows, ch_columns)
    async def rpc_set_stn10_grid(self,  id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        return await mainObj.station10.initGrids(id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
    async def rpc_set_stn11_grid(self,  id, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5,ref_pose_6, ref_pose_7, ref_pose_8, ref_pose_9, ref_pose_10, ref_pose_11, ref_pose_12, rows, columns):
        return await mainObj.station11.initGrids(id, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5,ref_pose_6, ref_pose_7, ref_pose_8, ref_pose_9, ref_pose_10, ref_pose_11, ref_pose_12, rows, columns)
    async def rpc_set_stn14_grid(self,  id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        return await mainObj.station14.initGrids(id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
    async def rpc_set_stn15_grid(self,  id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        return await mainObj.station15.initGrids(id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns)
    async def rpc_get_job(self):
        return await mainObj.getJob()
    async def rpc_get_loc(self):
        return await mainObj.getCurrentLocation()
    async def rpc_add_z(self, pose_received, z):
        return await mainObj.add_z(pose_received, z)
    async def rpc_stn4_get_next(self,isSuccess):
        return await mainObj.getStation4NextJob(isSuccess)
    async def rpc_stn4_get_next_after(self,isSuccess):
        return await mainObj.getStation4NextJob_afterCentrifugation(isSuccess)
    async def rpc_stn4_get_color(self): 
        return await mainObj.getStation4NextJobColor()
    async def rpc_stn3_get_angle(self):
        return await mainObj.station3.getAngle()
    async def rpc_stn5_get_loc(self):
        return await mainObj.getStation5GridLocations()
    async def rpc_set_init_alarm(self,macId):
        return await mainObj.setInitAlarm(macId)
    async def rpc_set_runtime_alarm(self,macId):
        return await mainObj.startRuntimeAlarm(macId)
    async def rpc_stn6_hatch_open(self):
        return await mainObj.stn6_hatch_open()
    async def rpc_stn6_hatch_close(self):
        return await mainObj.stn6_hatch_close()
    async def rpc_stn6_is_runnning(self):
        return await mainObj.stn6_is_runnning()
    async def rpc_stn6_check_lock(self):
        return await mainObj.stn6_check_lock()
    async def rpc_stn6_set_rotor_position(self,position):
        return await mainObj.stn6_set_rotor_position(position)
    async def rpc_stn6_start_centrifuge(self):
        return await mainObj.stn6_start_centrifuge()  
    async def rpc_check_z(self, pose_received):
        return await mainObj.station8.check_z(pose_received)
    async def rpc_add_x_y(self, pose_received, x, y):
        return await mainObj.station8.add_x_y(pose_received, x, y)
    async def rpc_ping(self):
        return await mainObj.ping()
    async def rpc_is_stn1_good(self):
        return await mainObj.isStation1Good()
    # async def rpc_register_ids(self,commaNumbers):
    #     return await commManager.registerIds(commaNumbers)
    async def rpc_send_msg(self,msg:str):
        return await mainObj.send_skype_message(msg)
    async def rpc_set_initialized(self):
        return await mainObj.setInitialized()
    async def rpc_set_camera1_flag(self,status:bool=False):
        return await mainObj.setCamera1Flag(status)
    async def rpc_stn1_update_grid(self,rows):
        return await mainObj.station1.updateGrid(rows)
    async def rpc_stn7_start_machine(self):
        return await mainObj.stn7_start_machine()
    async def rpc_stn14_fill_holder(self):
        return await mainObj.station14.fillHolder()

app = web.Application()
app.router.add_route("*", "/", XMLRPCHandler)
web.run_app(app, host=Settings.systemip, port=Settings.systemport)
    
        