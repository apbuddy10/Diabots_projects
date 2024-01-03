from enum import Enum
import logging
class Color(Enum):
    NONE=0
    GREEN=1
    ORANGE=2
    RED=3
    COUNTER=-1

class Color2(Enum):
    NONE=0
    GREEN=4
    ORANGE=5
    RED=6
    
class BatchStatus(Enum):
    Empty=0,
    Filled=1
    Process_Running=2
    Process_Completed=3



Station1Positions= [[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15],[1,16],[1,17],[1,18],[1,19],[1,20],
                    [2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],[2,11],[2,12],[2,13],[2,14],[2,15],[2,16],[2,17],[2,18],[2,19],[2,20]]

Station2Positions=  [[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],
                    [2,1],[2,2],[2,3],[2,4],[2,5],[2,6]]            

Station3Positions=  [1, 2, 4, 6, 7, 8, 9, 10]

Station5Positions =[[1,1],[4,1],[2,1],[3,1],[1,9],[4,9],[2,9],[3,9],[1,3],[4,3],[2,3],[3,3],[1,7],[4,7],[5,1],[8,1],[6,1],
                    [7,1],[5,9],[8,9],[6,9],[7,9],[5,3],[8,3],[6,3],[7,3],[5,7],[8,7]]

Station6Positions=  [[1,1],[1,2],[2,1],[2,2]]

Station7Positions = [[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],
                    [2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10]]

class Settings:   

    # Machine IDs
    macId_all= 0
    macId_coagulation = 3
    macId_centrifuge = 6
    macId_haematology = 7
    macId_chemistry = 8 

    # Machine Initialization times
    coagulation_init_time = 6
    haematology_init_time = 18  
    chemistry_init_time = 6
    centrifuge_init_time=6

    # Machine Running times
    coagulation_run_time = 12
    centrifuge_run_time = 7
    haematology_run_time = 12    
    chemistry_run_time = 12
    centrifuge_run_time_buffer = 6
    
    # Machine Standby times
    coagulation_standby_time = 7
    haematology_standby_time = 4   
    chemistry_standby_time = 6
    centrifuge_standby_time = 7

    # Machine z
    stn8_bottom_z = 125
    stn8_top_z = 170
    stn8_rack_z = 210

    pingInterval=500
    vq400host= "localhost"
    centrifugeComPort="COM4"
   
    logpath="c:\\D\\\QVITEC\\Logs"
    loglevel=logging.INFO
    systemip="localhost"    
    systemport="9095"

    sourcepath="c:\\D\\QVITEC\\Images"
    destpath="\\\\192.168.10.20\\Public\\Naga\\Images"
    resultsPath="\\\\192.168.10.20\\Public\\Naga"
    
    skuser="labo.robot.tb@outlook.de"
    skpswrd="979797Tb!"
    toskypeid="live:.cid.6b5a3a373ca64f8b"

    failtubemsg="Roehrchen in Fehlerstaender."