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
    await mainObj.station1.initGrids(1,{'x':100,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':110,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':100,'y':120,'z':120,'rx':120,'ry':150,'rz':150},3,3)
    await mainObj.station7.initGrids(1,{'x':100,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':200,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':100,'y':300,'z':120,'rx':120,'ry':150,'rz':150},1,2,{'x':110,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':100,'y':115,'z':120,'rx':120,'ry':150,'rz':150},2,5)
    await mainObj.station5.initGrids(1,{'x':100,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':200,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':100,'y':300,'z':120,'rx':120,'ry':150,'rz':150},4,2,{'x':110,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':100,'y':115,'z':120,'rx':120,'ry':150,'rz':150},3,3) 
    await mainObj.station2.initGrids(1,{'x':100,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':110,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':100,'y':100,'z':100,'rx':120,'ry':150,'rz':150},{'x':110,'y':100,'z':100,'rx':120,'ry':150,'rz':150},
            {'x':100,'y':100,'z':80,'rx':120,'ry':150,'rz':150},{'x':110,'y':100,'z':80,'rx':120,'ry':150,'rz':150})   
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



