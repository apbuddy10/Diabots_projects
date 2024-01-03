import asyncio
import xmlrpc.client
import main
from datetime import datetime
rows:list=[
    {"row":"row1","color":1,"position":"1","result":"OK"},
    {"row":"row2","color":1,"position":"2","result":"OK"},
    {"row":"row4","color":2,"position":"4","result":"OK"},
    {"row":"row3","color":2,"position":"3","result":"NG"},
    {"row":"row6","color":1,"position":"6","result":"OK"},
    {"row":"row5","color":1,"position":"5","result":"OK"},
    {"row":"row7","color":2,"position":"7","result":"NG"},
    {"row":"row8","color":2,"position":"8","result":"OK"},
    {"row":"row1","color":1,"position":"9","result":"OK"},
    {"row":"row2","color":1,"position":"10","result":"OK"},
    {"row":"row4","color":1,"position":"11","result":"OK"},
    {"row":"row3","color":1,"position":"12","result":"NG"},
    {"row":"row6","color":1,"position":"13","result":"OK"},
    {"row":"row5","color":0,"position":"14","result":"OK"},
    {"row":"row7","color":0,"position":"15","result":"NG"},
    {"row":"row8","color":0,"position":"16","result":"OK"},
    {"row":"row1","color":0,"position":"17","result":"OK"},
    {"row":"row2","color":0,"position":"18","result":"OK"},
    {"row":"row4","color":0,"position":"19","result":"OK"},
    {"row":"row3","color":0,"position":"20","result":"NG"},
    {"row":"row6","color":0,"position":"21","result":"OK"},
    {"row":"row5","color":0,"position":"22","result":"OK"},
    {"row":"row7","color":0,"position":"23","result":"NG"},
    {"row":"row8","color":0,"position":"24","result":"OK"},
    {"row":"row1","color":0,"position":"25","result":"OK"},
    {"row":"row2","color":0,"position":"26","result":"OK"},
    {"row":"row4","color":0,"position":"27","result":"OK"},
    {"row":"row3","color":0,"position":"28","result":"NG"},
    {"row":"row6","color":0,"position":"29","result":"OK"},
    {"row":"row5","color":0,"position":"30","result":"OK"},
    {"row":"row7","color":0,"position":"31","result":"NG"},
    {"row":"row8","color":0,"position":"32","result":"OK"},
    {"row":"row1","color":0,"position":"33","result":"OK"},
    {"row":"row2","color":0,"position":"34","result":"OK"},
    {"row":"row4","color":0,"position":"35","result":"OK"},
    {"row":"row3","color":0,"position":"36","result":"NG"},
    {"row":"row6","color":0,"position":"37","result":"OK"},
    {"row":"row5","color":0,"position":"38","result":"OK"},
    {"row":"row7","color":0,"position":"39","result":"NG"},
    {"row":"row8","color":0,"position":"40","result":"OK"}
]

async def getNextJob(rows:list):
    mainObj=main.MainApp()
    await mainObj.setMachineStatus(0,True)
    mainObj.station3.isInitialized=True
    mainObj.station6.isInitialized=True
    mainObj.station7.isInitialized=True
    mainObj.station8.isInitialized=True
    await mainObj.station1.initGrids([100,100,120,120,150,150],
                                     [240,100,120,120,150,150],
                                     [100,140,120,120,150,150],5,15)
    await mainObj.station2.initGrids([100,100,120,120,150,150],
                                     [340,100,120,120,150,150],
                                     [100,110,140,120,150,150],
                                     [340,110,140,120,150,150],1,25)
    await mainObj.station3.initGrids([100,100,120,120,150,150],
                                     [130,100,120,120,150,150],
                                     [100,110,120,120,150,150],2,4)
    await mainObj.station5.initGrids([100,100,120,120,150,150],
                                     [140,100,120,120,150,150],
                                     [100,150,120,120,150,150],4,2,
                                     [110,100,120,120,150,150],
                                     [100,115,120,120,150,150],3,3)
    await mainObj.station9.initGrids([100,145,120,120,150,150],
                                     [100,100,120,120,150,150],
                                     [100,190,120,120,150,150],
                                     [110,145,120,120,150,150],
                                     [110,100,120,120,150,150],
                                     [110,190,120,120,150,150])
    await mainObj.station10.initGrids([100,100,120,120,150,150],
                                      [130,100,120,120,150,150],
                                      [100,170,120,120,150,150],
                                      [200,100,120,120,150,150],
                                      [230,100,120,120,150,150],
                                      [200,170,120,120,150,150],8,4)
    await mainObj.station11.initGrids_1_2([100,100,120,120,150,150],
                                      [130,100,120,120,150,150],
                                      [100,170,120,120,150,150],
                                      [200,100,120,120,150,150],
                                      [230,100,120,120,150,150],
                                      [200,170,120,120,150,150],8,4)
    await mainObj.station11.initGrids_3_4([300,100,120,120,150,150],
                                      [330,100,120,120,150,150],
                                      [300,170,120,120,150,150],
                                      [400,100,120,120,150,150],
                                      [430,100,120,120,150,150],
                                      [400,170,120,120,150,150],8,4)
    await mainObj.station14.initGrids([100,100,120,120,150,150],
                                      [100,100,120,120,150,150],
                                      [100,140,120,120,150,150],5,1)
    await mainObj.station17.initGrids([100,120,120,120,150,150],
                                      [190,120,120,120,150,150],
                                      [100,120,120,120,150,150],1,10)
    await mainObj.station18.initGrids([100,120,120,120,150,150],
                                      [10,120,120,120,150,150],
                                      [100,120,120,120,150,150],1,10)   
    mainObj.station1.isRefreshCamera1Results=False
    await mainObj.station1.updateGrid(rows)
    for i in range(17):
        await mainObj.getJob()
        await mainObj.getCurrentLocation()

    for row  in rows:
        if(row["color"]== 1 ):
            row["color"]=3
        else:
            row["color"]=0
    await mainObj.station1.updateGrid(rows)

    for i in range(8):
        id=await mainObj.getJob()
        await mainObj.getCurrentLocation()
        if id[0]!=0:
            nextid=await mainObj.getStation4NextJob(True)
            await mainObj.getCurrentLocation()

    await mainObj.getJob()

    for i in range(6):
        id=await mainObj.getJob()
        await mainObj.getCurrentLocation()
        if id[0]!=0:
            nextid=await mainObj.getStation4NextJob(True)
            await mainObj.getCurrentLocation()
            print( nextid)
    await mainObj.getJob()
    await mainObj.getJob()

    for i in range(20):
        id=await mainObj.getJob()
        await mainObj.getCurrentLocation()
        if id[0]!=0:
            nextid=await mainObj.getStation4NextJob(True)
            await mainObj.getCurrentLocation()

    await mainObj.getJob()
    await mainObj.getJob()

asyncio.run(getNextJob(rows))



