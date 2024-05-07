from enum import Enum
import logging

class Color(Enum):
    NONE = 0
    GREEN = 1
    ORANGE = 2
    YELLOW = 3
    RED = 4
    YELLOW_2 = 5
    YELLOW_3 = 6
    BROWN = 7
    COUNTER = -1

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


# Station1Positions = [[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15],[1,16],[1,17],[1,18],[1,19],[1,20],
#                     [2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],[2,11],[2,12],[2,13],[2,14],[2,15],[2,16],[2,17],[2,18],[2,19],[2,20]]

Station1Positions = 75

Station2Positions =  50        

Station3Size = 8

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

# Station5Positions =[[1,1],[4,1],[2,1],[3,1],[1,9],[4,9],[2,9],[3,9],[1,3],[4,3],[2,3],[3,3],[1,7],[4,7],[5,1],[8,1],[6,1],
#                     [7,1],[5,9],[8,9],[6,9],[7,9],[5,3],[8,3],[6,3],[7,3],[5,7],[8,7]]

Station5Positions =[[1,1],[4,1],[2,1],[3,1],[1,9],[4,9],[2,9],[3,9],[1,3],[4,3],[2,3],[3,3],[1,7],[4,7],[2,7],[3,7],
                    [1,2],[4,2],[2,2],[3,2],[1,8],[4,8],[2,8],[3,8],[1,4],[4,4],[2,4],[3,4],[1,6],[4,6],[2,6],[3,6],
                    [5,1],[8,1],[6,1],[7,1],[5,9],[8,9],[6,9],[7,9],[5,3],[8,3],[6,3],[7,3],[5,7],[8,7],[6,7],[7,7],
                    [5,2],[8,2],[6,2],[7,2],[5,8],[8,8],[6,8],[7,8],[5,4],[8,4],[6,4],[7,4],[5,6],[8,6],[6,6],[7,6]]

Station6Positions =  [[1,1],[1,2],[2,1],[2,2]]

Station7Positions = [[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],
                    [2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10]]

Station9Positions =  [[1,1],[1,2],[1,3],[1,4],[1,7],[1,8],[1,9],[1,10], 
                     [2,1],[2,2],[2,3],[2,4],[2,7],[2,8],[2,9],[2,10]]

Station10Size = 64

Station11Size = 128

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
    chemistry_run_time = 3995
    centrifuge_run_time_buffer = 60

    # Maximum tubes
    green_max = 8
    orange_max = 24
    Station8UnloadingAfter = 1000

    pingInterval=600
    vq400host= "localhost"
    centrifugeComPort="COM20"

    redPostFix = "1"
    greenPostFix = "2"
    orangePostFix = "3"
    
    # logpath="C:\\Users\\arunk\\OneDrive - Diabots\\Diabots\\Development\\Python_Programs\\QVITEC Work\\Soltau\\Soltau_Final_12_07_2023\\ENV\\Soltau Onsite\\Logs"
    logpath="C:\\Diabots\\Soltau Onsite\\Logs"
    loglevel=logging.INFO
    # systemip="127.0.0.1"
    systemip="192.168.0.64"
    systemport="9095"
    Axis7Host="192.168.0.61"
    Axis7Port="9060"
    PacketLimit = 1000  
    RetryCounter = 100
    sftpTimeout = 600 #sec

    # sourcepath="D:\\QVITEC\\Images"
    # destpath="\\\\192.168.140.34\\robo\\QVITEC\\Images"
    # resultsPath="\\\\192.168.140.34\\robo"

    hostname = 'sftp1.itksp.net'
    username = 'SVC-GS-052ROBO01@ad.itksp.net'
    password = '<RAR,L&3WPG6-Q#b17'

    sourcepath="C:\\Diabots\\Soltau Onsite\\Images"
    destpath="C:\\Diabots\\Soltau Onsite\\OrganizedImages"
    resultsPath="C:\\Diabots\\Soltau Onsite\\CSV"
    
    skuser="labo.robot.tb@outlook.de"
    skpswrd="979797Tb!"
    toskypeid="live:.cid.6b5a3a373ca64f8b"

    failtubemsg="Röhrchen in Fehlerständer."


    HOME_POS_CAM_1=[0,2000,3000,3000]
    HOME_POS_CAM_2=[700000,2000,3000,3000]
    HOME_POS_CENTRIFUGE=[950000,2000,3000,3000]
    HOME_POS_COBAS_PURE_RCK=[2100000,2000,3000,3000]
    HOME_POS_COBAS_PURE_RCK_SLOW=[2100000,200,50,50]
    HOME_POS_SYSMEX=[2400000,2000,3000,3000]
    HOME_POS_COBASPURE=[2950000,2000,3000,3000]
    HOME_POS_COBASPURE_SLOW =[2950000,200,50,50]
    HOME_POS_COBASPURE_LOAD_UNLOAD =[2860000,2000,3000,3000]