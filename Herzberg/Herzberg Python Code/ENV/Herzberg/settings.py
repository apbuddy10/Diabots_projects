from enum import Enum
import logging

class Color(Enum):
    NONE = 0
    GREEN = 1
    ORANGE = 2
    RED = 3
    CRED = 4
    COUNTER = -1

class BatchStatus(Enum):
    Empty = 0,
    Filled = 1
    Process_Running = 2
    Process_Completed = 3
    Door_Opened = 4
    Door_Closed = 5

class HolderStatus(Enum):
    Empty = 0,
    Filled = 1


Station1Positions = [[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15],[1,16],[1,17],[1,18],[1,19],[1,20],
                    [2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],[2,11],[2,12],[2,13],[2,14],[2,15],[2,16],[2,17],[2,18],[2,19],[2,20]]

Station2Positions =  [[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10], 
                     [2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],
                     [3,1],[3,2],[3,3],[3,4],[3,5],[3,6],[3,7],[3,8],[3,9],[3,10]]        

Station3Positions =  [1, 2, 4, 6, 7, 8, 9, 10]

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

Station14Positions =  [[1,1],[1,2],[1,3],[1,4],[1,5]]

class Settings:    
    # Machine IDs
    macId_all= 0
    macId_coagulation = 3
    macId_centrifuge = 6
    macId_haematology = 7
    maxId_haematology_both = 71
    maxId_haematology_one = 72
    macId_chemistry = 8 

    # Machine Initialization times
    coagulation_init_time = 60
    haematology_init_time = 180    
    chemistry_init_time = 60
    centrifuge_init_time = 60

    # Machine Running times
    coagulation_run_time = 3420
    centrifuge_run_time = 600
    haematology_run_time = 1600    
    chemistry_run_time = 3995
    centrifuge_run_time_buffer = 60
    
    # Machine Standby times
    coagulation_standby_time = 1800
    haematology_standby_time = 4800    
    chemistry_standby_time = 1800
    centrifuge_standby_time = 700

    # Maximum tubes
    green_max = 8
    orange_max = 24

    # Machine z
    stn8_bottom_z = 125
    stn8_top_z = 170
    stn8_rack_z = 210

    pingInterval=200
    vq400host= "localhost"
    centrifugeComPort="COM18"

    redPostFix = "1"
    greenPostFix = "2"
    orangePostFix = "3"
    
    logpath="C:\\Diabots\\Herzberg\\Logs"
    loglevel=logging.INFO
    systemip="192.168.20.222"
    systemport="9095"

    # sourcepath="D:\\QVITEC\\Images"
    # destpath="\\\\192.168.140.34\\robo\\QVITEC\\Images"
    # resultsPath="\\\\192.168.140.34\\robo"

    sourcepath="C:\\Diabots\\Herzberg\\Images"
    destpath="\\\\192.168.92.110\\Diabots"
    # destpath="C:\\Diabots\\Herzberg\\OrganizedImages"
    resultsPath="C:\\Diabots\\Herzberg\\CSV"
    resultsPath="C:\\Diabots\\Herzberg\\CSV"
    
    skuser="labo.robot.tb@outlook.de"
    skpswrd="979797Tb!"
    toskypeid="live:.cid.6b5a3a373ca64f8b"

    failtubemsg="Röhrchen in Fehlerständer."