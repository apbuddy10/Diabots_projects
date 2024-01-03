import asyncio
import math
import random
import xmlrpc.client
from machine import MachineStatus
import main
from datetime import datetime
from settings import Color
from stations import processQueue
import matplotlib.pyplot as plt

class PlotJob():
    def __init__(self,isActive):
        self.isActive = isActive
        self.plot_counter= 0
        self.txt_height = 3
        self.plot_counter=0
        # plt.axis([0,50,0,1000])
        self.plt = plt
        self.initPlot()

    def initPlot(self):
        if (self.isActive):
            self.fig = self.plt.figure()
            self.ax = self.fig.add_subplot(111)   
            self.plt.ion()
            self.plt.isinteractive()
            self.plt.show()

    async def plotJob(self,jobID):
        if (self.isActive):
            if jobID is not None:
                self.plt.plot(self.plot_counter,jobID,'-o',markerfacecolor="green")
                self.ax.text(self.plot_counter, jobID + self.txt_height, "%d" %jobID, ha="center")
                self.plot_counter+=1
                self.plt.draw()
                self.plt.pause(0.1)

    async def plotgetNextJob(self,jobID):
        if (self.isActive):
            if jobID is not None:
                self.plt.plot(self.plot_counter,jobID,'-o',markerfacecolor="blue")
                self.ax.text(self.plot_counter, jobID + self.txt_height, "%d" %jobID, ha="center")
                self.plot_counter+=1
                self.plt.draw()
                self.plt.pause(0.1)

rows:list=[]
for i in range(20):
    rows.append({"row":"row1","color":random.choice([0,1,2,3,4,8]),"position":str(i+1),"result":"OK"})

for i in range(20,75):
    rows.append({"row":"row1","color":random.choice([0]),"position":str(i+1),"result":"OK"})

for i in range(75,90):
    rows.append({"row":"row1","color":random.choice([0,7]),"position":str(i+1),"result":"OK"})

async def getNextJob(rows:list):
    mainObj=main.MainApp()
    await mainObj.setMachineStatus(0,True)
    mainObj.station3.isInitialized=True
    mainObj.station6.isInitialized=True
    mainObj.station7.isInitialized=True
    mainObj.station8.isInitialized=True
    await mainObj.station1.initGrids([100,100,120,120,150,150],
                                     [240,100,120,120,150,150],
                                     [100,150,120,120,150,150],6,15)
    await mainObj.station2.initGrids_1([100,100,120,120,150,150],
                                       [210,100,120,120,150,150],
                                       [100,100,120,120,150,150],1,12)
    await mainObj.station2.initGrids_2([220,100,120,120,150,150],
                                       [340,100,120,120,150,150],
                                       [220,100,120,120,150,150],1,13)
    await mainObj.station2.initGrids_3([100,110,140,120,150,150],
                                       [210,110,140,120,150,150],
                                       [100,110,140,120,150,150],1,12)
    await mainObj.station2.initGrids_4([220,110,140,120,150,150],
                                       [340,110,140,120,150,150],
                                       [220,110,140,120,150,150],1,13)
    await mainObj.station5.initGrids([100,100,120,120,150,150],
                                     [140,100,120,120,150,150],
                                     [100,150,120,120,150,150],4,2,
                                     [110,100,120,120,150,150],
                                     [100,115,120,120,150,150],3,3)
    await mainObj.station9.initGrids([100,100,120,120,150,150],
                                     [130,100,120,120,150,150],
                                     [100,140,120,120,150,150],5,4)
    await mainObj.station9.initRackGrid([100,100,120,120,150,150],
                                        [130,100,120,120,150,150],
                                        [100,100,120,120,150,150],1,4)
    await mainObj.station10.initGrids([100,100,120,120,150,150],
                                      [160,100,120,120,150,150],
                                      [100,140,120,120,150,150],5,7)
    await mainObj.station11.initGrids([100,100,120,120,150,150],
                                      [160,100,120,120,150,150],
                                      [100,140,120,120,150,150],5,7,1)
    await mainObj.station11.initGrids([100,100,150,120,150,150],
                                      [160,100,150,120,150,150],
                                      [100,140,150,120,150,150],5,7,2)
    await mainObj.station14.initGrids([100,100,120,120,150,150],
                                      [100,100,120,120,150,150],
                                      [100,140,120,120,150,150],5,1)
    await mainObj.station17.initGrids([100,120,120,120,150,150],
                                      [190,120,120,120,150,150],1,10,
                                      [100,100,120,120,150,150],
                                      [100,140,120,120,150,150],
                                      [190,100,120,120,150,150],10,5)
    await mainObj.station18.initGrids([100,120,120,120,150,150],
                                      [10,120,120,120,150,150],1,10,
                                      [100,100,120,120,150,150],
                                      [100,140,120,120,150,150],
                                      [ 10,100,120,120,150,150],10,5)
    mainObj.station1.isRefreshCamera1Results=False

    # await mainObj.getJob() # Place Cobas Pure Rack inside the rack
    # await mainObj.getCurrentLocation()
    # await mainObj.getJob()
    # await mainObj.getCurrentLocation()

    await mainObj.station1.updateGrid(rows)
    iter = 0
    plotJob = PlotJob(isActive=False)
    plotList = []
    srcJob = None
    destJob = None
    tubeType = None
    index = None
    for iter_val in range(400):
        if len(list(filter(lambda row: row["color"]!=0 ,rows)))== 0:        
            for i in range(75):
                rows[i]["color"]=random.choice([0,1,2,3,4,8])
            for i in range(75,90):
                rows[i]["color"]= random.choice([0,7])
        await mainObj.station1.updateGrid(rows)
        jobArray = await mainObj.getJob()
        await plotJob.plotJob(srcJob)
        await plotJob.plotJob(destJob)
        if jobArray.__len__() == 2:
            [srcJob,destJob]= jobArray
        elif jobArray.__len__() == 3:
            [srcJob,destJob,tubeType]= jobArray    
        elif jobArray.__len__() >= 4:
            [srcJob,destJob,tubeType,index]= jobArray 
        # print("tubeType:",tubeType)
        # print("index:",index)
        plotList.append(srcJob)
        plotList.append(destJob)
        if(srcJob != 0 and destJob != 0 ):
            location=await mainObj.getCurrentLocation()
            print("tubeType:",tubeType)
            print("index:",index)
        print("srcJob:{0} and destJob:{1}".format(srcJob,destJob))
        if srcJob == 11:          
            mainObj.conn_Q400.tubeResults.color=mainObj.station4.tube.color
            mainObj.station4.tube.color=Color.NONE
            getNextJobID = await mainObj.getStation4NextJob(True)
            await mainObj.getCurrentLocation()    
            index=await mainObj.station1.getIndex(location[0])        
            rows[index]["color"]= 0 
            print("Get next job before centrifugation srcJob:{0} and destJob:{1} ".format(getNextJobID,getNextJobID))
            await plotJob.plotgetNextJob(getNextJobID)
            plotList.append(getNextJobID)
        elif srcJob == 51 and destJob == 41:            
            mainObj.conn_Q400.tubeResults.color=mainObj.station4.tube.color
            getNextJobID = await mainObj.getStation4NextJob_afterCentrifugation(True)
            await mainObj.getCurrentLocation()
            print("Get next job after centrifugation srcJob:{0} and destJob:{1}".format(getNextJobID,getNextJobID))
            await plotJob.plotgetNextJob(getNextJobID)
            plotList.append(getNextJobID)
        elif srcJob == 51 and destJob == 62:
            await mainObj.station6.setStatus(MachineStatus.Completed)           
        
        elif srcJob == 0 and destJob == 0:
            await asyncio.sleep(1)        

asyncio.run(getNextJob(rows))



