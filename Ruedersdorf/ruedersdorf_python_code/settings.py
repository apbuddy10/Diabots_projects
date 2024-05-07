from enum import Enum
import logging


class Color(Enum):
    NONE = 0
    GREEN = 1
    ORANGE = 2
    YELLOW = 3
    RED = 4
    BROWN = 7
    CRED = 8
    COUNTERSMALL = -1
    COUNTERBIG = -2

class TubeType(Enum):
    NONE = 0    
    SMALL = 1
    BIG = 2
    ADULT = 3
    CHILD = 4

class BatchStatus(Enum):
    Empty = 0,
    Filled = 1
    Process_Running = 2
    Process_Completed = 3
    # Door_Opened = 4
    # Door_Closed = 5

class HolderStatus(Enum):
    Empty = 0,
    Filled = 1

class RackStatus(Enum):
    Empty = 0,
    Filled = 1

class FridgeRackType(Enum):
    Archive=0,
    Failer=1
    


# Station1Positions = [[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15],[1,16],[1,17],[1,18],[1,19],[1,20],
#                     [2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],[2,11],[2,12],[2,13],[2,14],[2,15],[2,16],[2,17],[2,18],[2,19],[2,20]]

Station1Positions = 90
emergencyPositions = [13, 14, 28, 29, 43, 44, 58, 59, 73, 74, 88, 89]

# Station2Positions =  50       
Station2Positions =  40

Station3Size = 10
Station3MachineGridSize = 3
Station3Positions =  [[1,1],[1,5],[1,9],[1,13],[1,17],[1,21],[1,25],[1,29],[1,33],[1,37],
                     [2,2],[2,6],[2,10],[2,14],[1,18],[1,22],[1,26],[1,30],[1,34],[1,38],
                     [3,3],[3,7],[3,11],[3,15],[1,19],[1,23],[1,27],[1,31],[1,35],[1,39],
                     [4,4],[4,8],[4,12],[4,16],[1,20],[1,24],[1,28],[1,32],[1,36],[1,40]]

#   _______      _______
#  | 7 8 9 |    | 7 8 9 | 
#  | 4 5 6 |    | 4 5 6 | 
#  | 1 2 3 |    | 1 2 3 |  
#   _______      _______
#  | 7 8 9 |    | 7 8 9 | 
#  | 4 5 6 |    | 4 5 6 | 
#  | 1 2 3 |    | 1 2 3 |  
#  ----------------------
#   _______      _______
#  | 7 8 9 |    | 7 8 9 | 
#  | 4 5 6 |    | 4 5 6 | 
#  | 1 2 3 |    | 1 2 3 |    
#   _______      _______    
#  | 7 8 9 |    | 7 8 9 |   
#  | 4 5 6 |    | 4 5 6 | 
#  | 1 2 3 |    | 1 2 3 |  

# Station5Positions =[[1,1],[4,1],[2,1],[3,1],[1,9],[4,9],[2,9],[3,9],[1,3],[4,3],[2,3],[3,3],[1,7],[4,7],[2,7],[3,7],
#                     [1,2],[4,2],[2,2],[3,2],[1,8],[4,8],[2,8],[3,8],[1,4],[4,4],[2,4],[3,4],[1,6],[4,6],[2,6],[3,6],
#                     [5,1],[8,1],[6,1],[7,1],[5,9],[8,9],[6,9],[7,9],[5,3],[8,3],[6,3],[7,3],[5,7],[8,7],[6,7],[7,7],
#                     [5,2],[8,2],[6,2],[7,2],[5,8],[8,8],[6,8],[7,8],[5,4],[8,4],[6,4],[7,4],[5,6],[8,6],[6,6],[7,6]]

Station5Positions =[[1,1],[4,1],[1,9],[4,9],[1,3],[4,3],[1,7],[4,7],[1,2],[4,2],[1,8],[4,8],[1,4],[4,4],[1,6],[4,6],
                    [2,1],[3,1],[2,9],[3,9],[2,3],[3,3],[2,7],[3,7],[2,2],[3,2],[2,8],[3,8],[2,4],[3,4],[2,6],[3,6],
                    [5,1],[8,1],[5,9],[8,9],[5,3],[8,3],[5,7],[8,7],[5,2],[8,2],[5,8],[8,8],[5,4],[8,4],[5,6],[8,6],
                    [6,1],[7,1],[6,9],[7,9],[6,3],[7,3],[6,7],[7,7],[6,2],[7,2],[6,8],[7,8],[6,4],[7,4],[6,6],[7,6]]

Station6Positions =  [[1,1],[1,2],[2,1],[2,2]]

Station7Positions = [[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],
                    [2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10]]

Station9Positions =  [[1,1],[1,5],[1,9],[1,13],[1,17], 
                     [2,2],[2,6],[2,10],[2,14],[2,18],
                     [3,3],[3,7],[3,11],[3,15],[3,19],
                     [4,4],[4,8],[4,12],[4,16],[4,20]]

Station10Size = 25
# Station10Size = 5 # Testing AP

Station11Size = 35

Station14Positions =  [[1,1],[1,2],[1,4],[1,5]]

Station17Positions =  [[1,1],[1,2],[1,4],[1,5],
                       [2,1],[2,2],[2,4],[2,5],
                       [3,1],[3,2],[3,4],[3,5],
                       [4,1],[4,2],[4,4],[4,5],
                       [5,1],[5,2],[5,4],[5,5],
                       [6,1],[6,2],[6,4],[6,5],
                       [7,1],[7,2],[7,4],[7,5],
                       [8,1],[8,2],[8,4],[8,5],
                       [9,1],[9,2],[9,4],[9,5],
                       [10,1],[10,2],[10,4],[10,5]]

Station18Positions =  [[1,1],[1,2],[1,4],[1,5],
                       [2,1],[2,2],[2,4],[2,5],
                       [3,1],[3,2],[3,4],[3,5],
                       [4,1],[4,2],[4,4],[4,5],
                       [5,1],[5,2],[5,4],[5,5],
                       [6,1],[6,2],[6,4],[6,5],
                       [7,1],[7,2],[7,4],[7,5],
                       [8,1],[8,2],[8,4],[8,5],
                       [9,1],[9,2],[9,4],[9,5],
                       [10,1],[10,2],[10,4],[10,5]]

Station17_18Positions = [1,11,31,41,
                      2,12,32,42,
                      3,13,33,43,
                      4,14,34,44,
                      5,15,35,45,
                      6,16,36,46,
                      7,17,37,47,
                      8,18,38,48,
                      9,19,39,49,
                      10,20,40,50]

dummyLocation=[[0,0,0,0,0,0],[0,0,0,0,0,0]]


class Settings:    
    # Machine IDs
    macId_all= 0
    macId_coagulation = 3
    macId_centrifuge = 6
    macId_haematology = 7
    maxId_haematology_both = 71
    maxId_haematology_one = 72
    macId_chemistry = 8 

    # Machine Running times
    coagulation_run_time = 100
    centrifuge_run_time = 600
    haematology_run_time = 300    
    chemistry_run_time = 500
    centrifuge_run_time_buffer = 6
    extra_run_time = 240

    # Maximum tubes
    green_max = 10
    orangeYellow_max = 6
    brown_max = 16
    Station8UnloadingAfter = 0

    pingInterval=1
    vq400host= "localhost"
    centrifugeComPort="COM6"

    redPostFix = "1"
    greenPostFix = "2"
    orangePostFix = "3"
    
    logpath="C:\\Diabots\\ruedersdorf\\Logs"
    # logpath="Logs"
    loglevel=logging.INFO
    systemip="192.168.0.63"
    systemport="9095"
    Axis7Host="192.168.0.64"
    Axis7Port="9060"



    # HOME_POS_CAM_1=[0000,1100]  #ch
    # HOME_POS_CENTRIFUGE=[310000,1100]
    # HOME_POS_BECKMANN_LOAD=[1600000,1100]
    # HOME_POS_COBAS_SLIDE_15=[1510000,1100]
    # HOME_POS_BCS_MACHINE=[1750000,1100]
    # HOME_POS_COBAS_SLIDE_16=[1910000,1100]
    # HOME_POS_COBAS_MACHINE=[2360000,1100]   # ch
   
    HOME_POS_CAM_1=[0,2000,500,500]    #ch
    HOME_POS_FRIDGE_2=[770000,2000,2000,2000]
    HOME_POS_CENTRIFUGE=[310000,2000,2000,2000] #ch
    HOME_POS_BECKMANN_LOAD=[1560000,2000,2000,2000] #ch
    HOME_POS_COBAS_SLIDE_15=[1510000,2000,2000,2000] #ch
    HOME_POS_BCS_MACHINE=[1710000,2000,2000,2000] #ch
    HOME_POS_COBAS_SLIDE_16=[1910000,2000,2000,2000] #ch
    HOME_POS_COBAS_MACHINE=[2360000,2000,2000,2000]     # ch
    HOME_POS_COBAS_BASKET_15=[2280000,2000,2000,2000]     # ch
   
    # HOME_POS_CAM_1=[1,500,1000,1000]    #ch
    # HOME_POS_FRIDGE_2=[770000,500,1000,1000]
    # HOME_POS_CENTRIFUGE=[311000,500,1000,1000] #ch
    # HOME_POS_BECKMANN_LOAD=[1560000,500,1000,1000] #ch
    # HOME_POS_COBAS_SLIDE_15=[1510000,500,1000,1000] #ch
    # HOME_POS_BCS_MACHINE=[1710000,500,1000,1000] #ch
    # HOME_POS_COBAS_SLIDE_16=[1910000,500,1000,1000] #ch
    # HOME_POS_COBAS_MACHINE=[2360000,500,1000,1000]     # ch
    # HOME_POS_COBAS_BASKET_15=[2280000,500,1000,1000]     # ch


    # sourcepath="D:\\QVITEC\\Images"
    # destpath="\\\\192.168.140.34\\robo\\QVITEC\\Images"
    # resultsPath="\\\\192.168.140.34\\robo"

    
    # hostname = 'SRH001MO007.ad.itksp.net'
    hostname = 'sftp1.itksp.net'
    username = 'SVC-GS-007ROBO01@ad.itksp.net'
    password = 'E2T[3/m$m9/\K0F.'

    sourcepath="C:\\Diabots\\ruedersdorf\\Images"
    destpath="C:\\Diabots\\ruedersdorf\\OrganizedImages"
    resultsPath="C:\\Diabots\\ruedersdorf\\CSV"
    
    skuser="labo.robot.tb@outlook.de"
    skpswrd="979797Tb!"
    toskypeid="live:.cid.6b5a3a373ca64f8b"

    failtubemsg="Röhrchen in Fehlerständer."