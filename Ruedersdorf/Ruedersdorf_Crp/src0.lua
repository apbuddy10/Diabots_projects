-- Version: Lua 5.3.5
-- This thread is the main thread and can call any commands.
-- Version: Lua 5.3.5

--// Initialization of Variables and Communication
--// Default Values of Motion commands //-----------------
local moveParam = { user   = 0,       --// Default user 0
                    tool   = 1,       --// Default tool 1
                    cp     = 100,     --// Default cp 100==
                    cpl    = 0,       --// Default Move() cp 0
                    speed  = 100,     --// Default speed 100
                    speeds = 100,     --// Default speeds 100
                    accel  = 100,      --// Default accel 50
                    accels = 100,      --// Default accels 50
                    sync   = 1,       --// Default Sync 1
                    pose   = nil}     --// Default pose nil
--// Default parameters of Gripper //-----------------
local gripParam = { g_init        = 0,       --// Default init value is 0
                    g_pos         = nil,     --// Default pos is nil
                    g_speed       = 100,     --// Default speed is 100
                    g_force       = 100,     --// Default force is 100
                    g_exp_status  =   3,     --// Default g_exp_status is 3
                    g_chk_status  = true}   --// Default chk_status is true
--// User Plane Names // ----------------------
local user_base  = 0
local user_cam_1 = 1
local user_stn2_plane = 2
local user_BCS = 3
local user_centri_rck_plane = 4
local user_A_c_9 = 5
local user_arch_d_1 = 6
local user_arch_d_2 = 6
local user_cprt_plane = 8
--// All Pos Command //-----------------------
local MOVE_ARCHIVE_FILLED_P = P259  
--// Stn 1 Pos commands //----------------camera1 
local MOVE_DRIVE_1_P = P54  
local MOVE_STN1_HOME_P = P55 --d
local MOVE_STN1_HELP_1_P = P56  --d
--local MOVE_STN1_HELP_2_P = P6  --d

--// Stn 2 Pos commands //----------------Cobas Pure Rack Station 
local MOVE_STN2_CPR1_HELP_P = P131
local MOVE_STN2_CPR2_HELP_P = P132


--// Stn 3 Pos commands //----------------BCS machine
local MOVE_STN3_HOME_P = P83 --d
--local MOVE_STN3_HELP_P = P84 --
--// Stn 4 Pos commands //----------------camera2 
----local MOVE_STN4_HOME_P = P57 --d
local MOVE_STN4_HELP_P = P58 --d
local MOVE_STN4_CAM2_P = P59 --d
--// Stn 5 Pos commands //----------------Centrifuge racks 
local MOVE_STN5_HOME_P = P61 --d
local MOVE_STN5_HELP_P = P62 --d
--// Stn 6 Pos commands //----------------Centrifuge racks loading/unloading 
--local MOVE_STN6_HELP_P = P81 --nn  
local MOVE_STN6_HELP_1_P = P79  
local MOVE_STN6_HELP_2_P = P80  
local MOVE_STN6_P = P81  
--// Decapping Pos commands //----------------Decapping 
local MOVE_DECAP_HELP_P = P72  --d
local MOVE_DECAP_SMALL_START_P = P75 --d
local MOVE_DECAP_SMALL_END_P = P76   --d
local MOVE_DECAP_BIG_START_P = P73   --d
local MOVE_DECAP_BIG_END_P = P74     --d
local MOVE_DECAP_BIN_P = P77         --d
local MOVE_DECAP_PCK_BIG_P = P197  
local MOVE_DECAP_PCK_SMALL_P = P198 
local MOVE_DECAP_BCS_PCK_P = P200 
--// Counter weight Pos commands //----------------Counter weights 
--local MOVE_CW_HELP_P = P41  --nn
--// Stn 7 Pos commands //----------------Beckman machine
local MOVE_STN7_PCK_HELP_1_P = P101 --d
local MOVE_STN7_PCK_HELP_2_P = P102 --d
local MOVE_STN7_PCK_RACK_P = P103  --d
local MOVE_STN7_SLIDE_P = P104    --d  
local MOVE_STN7_SLIDE_UP_P = P199    --d  
local MOVE_STN7_PLC_HELP_1_P = P106  --d
local MOVE_STN7_PLC_HELP_2_P = P107 --d
local MOVE_STN7_PLC_RACK_P = P108  --d
--// Stn 8 Pos commands //----------------cobas_pure_machine  
----local MOVE_STN8_BSKT_HELP_1_P 
local MOVE_STN8_PLC_RCK_HELP_P = P91
---local MOVE_STN8_PLC_RCK_HELP2_P 
local MOVE_STN8_PLC_RCK_P = P92

---local MOVE_STN8_BSKT_HELP_2_P = P91 
---local MOVE_STN8_PCK_PLC_BSKT_P = P92
local MOVE_STN8_PCK_PLC_BSKT_APP_1 = P181
local MOVE_STN8_PCK_BSKT_HELP1_P = P195
local MOVE_STN8_PCK_BSKT_HELP2_P = P196
local MOVE_STN8_PCK_BSKT_P = P194
local MOVE_STN8_PCK_HELP_1_P = P185
local MOVE_STN8_PCK_HELP_2_P = P184

local MOVE_STN8_PLC_BSKT_P = P183
local MOVE_STN8_PLC_BSKT_HELP_1_P = P182
local MOVE_STN8_PLC_LEAVE_1_P = P202
local MOVE_STN8_PLC_LEAVE_2_P = P203
local MOVE_STN8_BSKT_HOME = P207
--local MOVE_STN16_STN8_BSKT_HLP_1 = P208
local MOVE_STN16_STN8_BSKT_HLP_2 = P209
--local MOVE_STN16_STN8_BSKT_HLP_3 = P210
local MOVE_STN16_STN8_BSKT_HLP_4 = P211
local MOVE_STN16_STN8_BSKT_PLACE = P212
local MOVE_STN16_STN8_BSKT_PLACE_BACK = P213
local MOVE_STN16_STN8_BSKT_PLACE_BACK_UP = P214

--// Stn 9 Pos commands //----------------Beckman racks
local MOVE_STN9_HOME_P = P105  --d
--// Stn 10 Pos commands //----------------Fehler
--local MOVE_STN10_FEHLER_HOME_P = P51  --nn
local MOVE_STN10_FEHLER_HELP_P = P109  --d   
--local MOVE_STN10_FEHLER_PLACE_P = P53 --nn
--// Stn 10 Pos Parking Fehler commands //----------------Parking Fehler  --nn
--[[local MOVE_STN10_HELP_P = P90 
local MOVE_STN10_APPR_P = P91
local MOVE_STN10_APPR_SMALL_P = P92
local MOVE_STN10_APPR_BIG_P = P93]]
--// Stn 11 Pos commands //---------------- Archiv
--local MOVE_STN11_ARCHIV_HELP_P = P18
--local MOVE_STN11_ARCHIV_TUBE_HELP_1_P = P110  --d
--local MOVE_STN11_ARCHIV_TUBE_HELP_2_P = P111  --d
--local MOVE_STN11_ARCHIV_PLACE_P = P19  --nn
--// Stn 11 Pos commands //---------------- Archiv Fridge 1 Commands
local MOVE_STN11_D1_HOME_P = P112  --d
local MOVE_STN11_D1_CLOSE_1_P = P113 --d
local MOVE_STN11_D1_CLOSE_2_P = P114  --d
local MOVE_STN11_D1_HELP_P = P115    --d
local MOVE_STN11_D1_APPR_1_P = P116  --d
local MOVE_STN11_D1_APPR_2_P = P117  --d
local MOVE_STN11_D1_PULL_P = P118  --d
local MOVE_STN11_D1_LEAVE_1_P = P119  --d
local MOVE_STN11_D1_LEAVE_2_P = P129  --d
local MOVE_STN11_D1_PULL_HELP_P = P215  --d
local MOVE_STN11_D1_PULL_HELP1_P = P216  --d
local MOVE_STN11_D1_PULL_HELP2_P = P217  --d

--local MOVE_STN11_RCK1_APPR_P = P98  --nn
--local MOVE_STN11_RCK1_PULL_P = P99  --nn
--local MOVE_STN11_RCK2_APPR_P = P103 --nn 
--local MOVE_STN11_RCK2_PULL_P = P104  --nn
--// Stn 11 Pos commands //---------------- Archiv Fridge 2 Commands
local MOVE_STN11_D2_HOME_P = P120
local MOVE_STN11_D2_CLOSE_1_P = P121 --d
local MOVE_STN11_D2_CLOSE_2_P = P122  --d
local MOVE_STN11_D2_HELP_P = P123
local MOVE_STN11_D2_APPR_1_P = P124  --d
local MOVE_STN11_D2_APPR_2_P = P125  --d
local MOVE_STN11_D2_PULL_P = P126
local MOVE_STN11_D2_LEAVE_1_P = P127  --d
local MOVE_STN11_D2_LEAVE_2_P = P128  --d
local MOVE_STN11_D2_PULL_HELP_P = P218  --d
local MOVE_STN11_D2_PULL_HELP1_P = P219  --d
local MOVE_STN11_D2_PULL_HELP2_P = P220  --d
local MOVE_STN11_D2_PLC_TUBE_HELP_P = P257 --d


--local MOVE_STN11_RCK3_APPR_P = P111  --nn
--local MOVE_STN11_RCK3_PULL_P = P112  --nn
--local MOVE_STN11_RCK4_APPR_P = P116  --nn
--local MOVE_STN11_RCK4_PULL_P = P117  --nn
--// Stn 14 Pos commands //----------------cobas_pure_rack_station  -Done
local MOVE_STN14_RCK_APP_P = P156
--local MOVE_STN14_PUSH_HELP_P = P157
local MOVE_STN14_PUSH_START_P = P158
local MOVE_STN14_PUSH_END_P = P159
local MOVE_STN14_PLC_RCK_HELP_P = P85
local MOVE_STN14_PLC_RCK_APP_P = P86
local MOVE_STN14_PLC_RCK_P = P87
local MOVE_STN14_PCK_RCK_HELP_P = P88
local MOVE_STN14_PCK_RCK_P = P89
local MOVE_STN14_DRIVE_P = P90
local MOVE_STN14_PCK_RCK_PULL_P = P258

--// Stn 15 Pos commands //----------------cobas_pure_Basket_1
local MOVE_STN15_PLC_HELP2_P = P179

local MOVE_STN15_PCK_PLC_BSKT_HELP_P = P133
local MOVE_STN15_BSKT_HELP_1_P= P176
local MOVE_STN15_PCK_BSKT_P = P175



local MOVE_STN15_PLC_HELP2_P = P179
local MOVE_STN15_PLC_P = P178
local MOVE_STN15_PCK_PLC_HELP_P = P177


---//station 15- station 8 new commands--------------
local MOVE_STN15_HOME_P = P180
local MOVE_STN15_8_PCK_HELP1_P = P221
local MOVE_STN15_8_PCK_HELP2_P = P222
local MOVE_STN15_8_PCK_HELP3_P = P223
local MOVE_STN15_8_PCK_SLD_HELP_P = P224
local MOVE_STN15_8_PCK_HELP4_P = P225
--local MOVE_STN_STN8_HOME_P = P226 --nn
local MOVE_STN15_8_HOME_P = P226
local MOVE_STN15_STN8_STN15_BRIDGE_P = P238
local MOVE_STN15_8_PLC_HELP1_P = P227
local MOVE_STN15_8_PLC_HELP2_P = P228
local MOVE_STN15_8_PLC_HELP3_P = P229
local MOVE_STN15_8_PLC_P = P230
local MOVE_STN15_8_PLC_HELP4_P = P231
local MOVE_STN15_8_PLC_HELP5_P = P232
---//station 8- station 15 new commands--------------
local MOVE_STN8_15_PCK_HELP1_P = P233
local MOVE_STN8_15_PCK_HELP2_P = P234
local MOVE_STN8_15_PCK_HELP3_P = P235
local MOVE_STN8_15_PCK_HELP4_P = P236
local MOVE_STN15_STN8_HELP5_P = P237
local MOVE_STN15_STN8_BRIDGE_P = P238
local MOVE_STN8_15_PLC_HELP6_P = P239
local MOVE_STN8_15_PLC_HELP7_P = P240
local MOVE_STN8_15_PLC_HELP8_PUSH_P = P241
local MOVE_STN8_15_PLC_HELP9_P = P242
local MOVE_STN8_15_PLC_HELP10_LEAVE_P = P243

--// Stn 16 Pos commands //----------------cobas_pure_Basket_2
local MOVE_STN16_PCK_PLC_BSKT_HELP_P = P134
local MOVE_STN16_PCK_PLC_BSKT_P = P172
local MOVE_STN16_HOME_P = P186
local MOVE_STN16_BSKT_HELP_1_P  = P188
local MOVE_STN16_PCK_BSKT_P = P187

local MOVE_STN16_PLC_BSKT_P = P190
local MOVE_STN16_PLC_HELP_1_P = P191
local MOVE_STN16_PLC_LEAVE_1_P = P204
local MOVE_STN16_PLC_LEAVE_2_P = P205

local MOVE_DRIVE_STN_15_16_P = P201



---//station 16- station 8 new commands--------------
--[[local MOVE_STN16_8_PCK_HELP1_P = P221
local MOVE_STN16_8_PCK_HELP2_P = P222
local MOVE_STN16_8_PCK_HELP3_P = P223
local MOVE_STN16_8_PCK_SLD_HELP_P = P224
local MOVE_STN16_8_PCK_HELP4_P = P225
local MOVE_STN16_STN8_HOME_P = P237
local MOVE_STN16_STN8_STN16_BRIDGE_P = P238
local MOVE_STN16_8_PLC_HELP1_P = P227
local MOVE_STN16_8_PLC_HELP2_P = P228
local MOVE_STN16_8_PLC_HELP3_P = P229
local MOVE_STN16_8_PLC_P = P230
local MOVE_STN16_8_PLC_HELP4_P = P231
local MOVE_STN16_8_PLC_HELP5_P = P232]]
---//station 8- station 16 new commands--------------
local MOVE_STN16_SLD_HELP_P = P206
local MOVE_STN16_PCK_PLC_HELP_P = P189
local MOVE_STN8_16_PCK_HELP1_P = P244
local MOVE_STN8_16_PCK_HELP2_P = P245
local MOVE_STN8_16_PCK_HELP3_P = P246
local MOVE_STN8_16_PCK_HELP4_P = P247
local MOVE_STN8_16_PCK_HELP5_P = P248
local MOVE_STN16_STN8_BRIDGE_P = P249
local MOVE_STN8_16_PLC_HELP6_P = P250
local MOVE_STN8_16_PLC_HELP7_P = P251
local MOVE_STN8_16_PLC_HELP8_PUSH_P = P252
local MOVE_STN8_16_PLC_HELP9_P = P253
local MOVE_STN8_16_PLC_HELP10_LEAVE_P = P254

--// Stn 17 Pos commands //----------------Sliding_racks_into_stn17
--local MOVE_STN17_PCK_RCK_HELP_P = P74
--local MOVE_STN17_PCK_RCK_P = P86
--local MOVE_STN17_sld_RCK_P = P74
--local MOVE_STN17_sld = P88
local MOVE_STN17_SLD_HELP_P = P160
local MOVE_STN17_SLD_START_P = P162
local MOVE_STN17_SLD_MIDDLE_HELP_P= P255
local MOVE_STN17_SLD_END_P = P163
local MOVE_STN17_HELP_P = P192
local MOVE_STN17_RCK_SLD_OUT_P = P170
local MOVE_STN17_RCK_SLD_OUT_HELP_P = P171


--// Stn 18 Pos commands //----------------Sliding_racks_into_stn18
--local MOVE_STN18_PCK_RCK_HELP_P = P75
---local MOVE_STN18_PCK_RCK_P = P87
---local MOVE_STN18_sld_RCK_P = P71
---local MOVE_STN18_sld = P89
local MOVE_STN18_SLD_HELP_P = P164
--local MOVE_STN18_SLD_APP_P = P165
local MOVE_STN18_SLD_START_P = P166
local MOVE_STN18_SLD_MIDDLE_HELP_P= P256
local MOVE_STN18_SLD_END_P = P167
local MOVE_STN18_HELP_P = P193
local MOVE_STN18_RCK_SLD_OUT_P = P173
local MOVE_STN18_RCK_SLD_OUT_HELP_P = P174
--// End of All Pos Command //---------------

--AXIS 7 POS COMMANDS 
local AXIS_HOME_POS_CAM_1 = 701             -- Pos 0 mm
local AXIS_HOME_POS_CENTRIFUGE = 705        --  Pos 310 mm
local AXIS_HOME_POS_FRIDGE2 = 711             -- Pos 770 mm
local AXIS_HOME_POS_COBAS_PURE_RCK_1 = 717  -- Pos 1510 mm
local AXIS_HOME_POS_BECKMAN_LOAD = 707      -- Pos 1560 mm
local AXIS_HOME_POS_BCS = 703               -- Pos 1710 mm
local AXIS_HOME_POS_COBAS_PURE_RCK_2 = 718 -- Pos 1910 mm
local AXIS_HOME_POS_COBAS_BASKET_15 = 715   -- Pos 2280 mm
local AXIS_HOME_POS_COBAS_PURE = 708        -- Pos 2360 mm
--//utility functions//------------------

gripperStatus = 0

function getGripperStatus()
  local crc2,crc1 = CRC16({9,0x03,0x07,0xD0,0x00,0x03})
  Sync() 
  Sleep(50)
  GWrite(0x01,{9,0x03,0x07,0xD0,0x00,0x03,crc1,crc2})
  local value = GRead(0x01)
  local retPosition = nil
  if value ~= nil and value.size == 11 then
    retPosition = math.floor((255-value.buf[8])*100/255)
    local objectStatus = value.buf[4]
    local t = {}
	for i=7,0,-1 do
	  t[#t+1] = math.floor(objectStatus / 2^i)
	  objectStatus = objectStatus % 2^i
    end
    return retPosition, tonumber(tostring(t[1])..tostring(t[2]),2)
  end
  return -1, -1
end

function setGripperWithoutCheck(position, speed, force)
  RiqSet(position, speed, force)
  Sync()
  Sleep(500)
end

function setGripper(position, speed, force)
  local commandCount = 0
  local count = 0
  local success = false
  local openbuff = 5
  while(true) do
    count = 0
    Sync()
    RiqSet(position, speed, force)
    Sync()
    commandCount = commandCount + 1
    while(true) do
      local reponsePosition = -1
      local responseObjStatus = -1
      reponsePosition, responseObjStatus = getGripperStatus()
      gripperStatus = responseObjStatus
      Sync()
      count = count + 1
      if (reponsePosition ~= nil) then
        if ((reponsePosition >= position-openbuff and reponsePosition <= position+openbuff) or responseObjStatus == 2) then
          success = true   
          break
        end
      end
      if(count >= 10) then
        break
      end
    end
    if (commandCount <= 100) then
      if (success == true) then
        break
      end
    else
      Pause()
      break
    end
  end
  Sync()
end

function initializeComm()
  --setGripperCheck( {g_init=1,g_exp_status=3})  --// Init Gripper 
  RiqEPickInit()
  Sync()
  RiqInit()
  Sync()
  --setGripperCheck( {g_pos=0,g_exp_status=3})  --// Close the Gripper 
  setGripper(0,50,50) --// Close the Gripper 
  --Go(P91,"User=0 Tool=1 CP=100 Speed=50 Accel=10 SYNC=1")
  err, socket = TCPCreate(isServer, IP, PORT)
  local err = TCPStart(socket, 0)
  return err
end

--// Start of Modified Motion commmands //-----------------------------------
function  Go_(param)
  local user = param.user or moveParam.user     --// Default user 0
  local tool = param.tool or moveParam.tool     --// Default tool 1
  local cp = param.cp or moveParam.cp       --// Default cp 100
  local speed = param.speed or moveParam.speed --// Default speed 100
  local accel = param.accel or moveParam.accel  --// Default accel 50
  local sync = param.sync or moveParam.sync     --// Default Sync 1
  
  local paramStr = "User=" .. tostring(user) .. " " .. "Tool=" .. tostring(tool) .. " " ..
              "CP=" .. tostring(cp) .. " " .. "Speed=" .. tostring(speed) .. " " .. 
              "Accel=" .. tostring(accel) .. " " .. "SYNC=" .. tostring(sync)
  Go(param.pose, paramStr)
end

function  Move_(param)
  local user = param.user or moveParam.user     --// Default user 0
  local tool = param.tool or moveParam.tool     --// Default tool 1
  local cpl = param.cpl or moveParam.cpl           --// Default cp 0
  local speeds = param.speeds or moveParam.speeds --// Default speeds 100
  local accels = param.accels or moveParam.accels  --// Default accels 50
  local sync = param.sync or moveParam.sync     --// Default Sync 1
  
  local paramStr = "User=" .. tostring(user) .. " " .. "Tool=" .. tostring(tool) .. " " ..
              "CP=" .. tostring(cpl) .. " " .. "SpeedS=" .. tostring(speeds) .. " " .. 
              "AccelS=" .. tostring(accels) .. " " .. "SYNC=" .. tostring(sync)
  Move(param.pose, paramStr)
end

function  MoveJ_(param)
  local cp = param.cp or moveParam.cp       --// Default cp 100
  local speed = param.speed or moveParam.speed --// Default speed 100
  local accel = param.accel or moveParam.accel  --// Default accel 50
  local sync = param.sync or moveParam.sync     --// Default Sync 1
  
  local paramStr = "CP=" .. tostring(cp) .. " " .. "Speed=" .. tostring(speed) .. " " .. 
              "Accel=" .. tostring(accel) .. " " .. "SYNC=" .. tostring(sync)
  MoveJ(param.pose, paramStr)
end

function setBarcodeOnly(robot_pose, plane, z_val, angle, diffAngle)
  Go_( {pose=robot_pose, user=plane} )
  local jointArrStartPos = GetAngle()      --// start pos
  local updatedJointPos = setBarcodeAngle(jointArrStartPos,angle+diffAngle)
  MoveJ_({pose=updatedJointPos, sync=1})
  local updatedPos = GetPose()
  coordinateArr = setCoordinatePos_z({coordinate=updatedPos.coordinate}, z_val)
  Move_( {pose=coordinateArr, user=plane,speeds=3, accels=2, cpl=0, sync=1} )
  setGripper(30,50,50) --// Open the Gripper
  local updatedPos = GetPose()
  coordinateArr = addCoordinatePos_z({coordinate=updatedPos.coordinate}, 100)
  Move_( {pose=coordinateArr, user=plane,speeds=10, accels=5, cpl=0} )
  Go_( {pose=robot_pose, user=plane} )  
end

--// End of Modified Motion commmands //-----------------------------------

--//End of utility functions//------------------

--//Start of Program//------------------
MoveJ_( {pose=MOVE_DRIVE_1_P, speed=10,accel=10,sync=1} )
DOExecute(3, OFF)
DOExecute(5, OFF) 
DOExecute(6, OFF) 
DOExecute(7, OFF)
DOExecute(14, OFF)
DOExecute(15, OFF) 
DOExecute(16, OFF)
local errRetVal = initializeComm()
if (errRetVal == 0) then  
  --RiqInit()  --// Init Gripper 
  interfaceOut[1] = 1   --//new Connection
  statusACK = TCP_snd_rcv()
  interfaceOut[1] = 0   --//new Connection
  InitializeMachine(1)  --// Init Camera 1
  InitializeMachine(21)  --// Init Cobas Pure Rack
  InitializeMachine(22)  --// Init Cobas Pure Rack
  InitializeMachine(23)  --// Init Cobas Pure Rack
  InitializeMachine(24)  --// Init Cobas Pure Rack
  InitializeMachine(31)  --// Init BCS tubes
  InitializeMachine(32)  --// Init BCS racks 
  InitializeMachine(4)  --// Init Q00 and reset
  InitializeMachine(5)  --// Init Centrifuge Tube Points
  InitializeMachine(55)  --// Init Counter Weight
  InitializeMachine(61) --// Init centrifuge
  InitializeMachine(91)  --// Init Beckman Tubes
  InitializeMachine(92)  --// Init Beckman Racks
  InitializeMachine(10)  --// Init Fehler
  InitializeMachine(111)  --// Init Archive fridge1 rack1
  InitializeMachine(112)  --// Init Archive fridge2 rack2
  InitializeMachine(14) --// Init Cobas Pure Rack Holder
  InitializeMachine(17) --// Init Cobas Pure Filled Rack Holder_1
  InitializeMachine(18) --// Init Cobas Pure Filled Rack Holder_2
  
  if (DI(27))== ON then            ---- BCS Status
    interfaceOut[5] = 3
    statusACK = TCP_snd_rcv()
    interfaceOut[5] = 0
  end
  if (DI(28))== ON then            ---- COBAS Status
    interfaceOut[5] = 8
    statusACK = TCP_snd_rcv()
    interfaceOut[5] = 0
  end
  if (DI(29))== ON then            ---- Beckman Status
    interfaceOut[5] = 7
    statusACK = TCP_snd_rcv()
    interfaceOut[5] = 0
  end
  --setGripperCheck( {g_init=1,g_exp_status=3})  --// Init Gripper 
  --checkGripperStatus(3,{pos=0,init=1})
  RiqEPickInit()
  Sync()
  RiqInit()
  Sync()
  setGripper(0,50,50) --// Close the Gripper 
  --setGripperCheck( {g_pos=0,g_exp_status=3})  --// Close the Gripper 
  --checkGripperStatus(3,{pos=0})
  --Go(P5,"User=2 Tool=1 CP=100 Speed=50 Accel=20 SYNC=1")
  while true do 
    Sync()
    reset_jobs()
    resetLockStatus()
    if (DI(24))== ON then            ---- Archiv Reset
      interfaceOut[5] = 11
      statusACK = TCP_snd_rcv()
      interfaceOut[5] = 0
      DOExecute(8, OFF)
      Sync()
    end
    if (DI(26))== ON then            ---- Fehler Reset
      interfaceOut[5]= 100
      statusACK = TCP_snd_rcv()
      interfaceOut[5] = 0
      DOExecute(10, OFF)
      Sync()
    end
    if (DI(21)) == ON then
      interfaceOut[7] = 1
      DOExecute(5, OFF)
      Sync()
    else
      interfaceOut[7] = 0
    end
    statusACK = TCP_snd_rcv()
    if(statusACK == true) then
      local srcJob = interfaceIn[4]  
      local destJob = interfaceIn[5]
      local tubeType = interfaceIn[2]
      local z_small_big_val = nil
      local cw_z_small_big_val = nil
      local decap_z_small_big_val= nil
      local stn14_small_big_z_val = nil
      local generic = interfaceIn[18]
      interfaceOut[7] = 0
      print("srcJob:",srcJob)
      print("destJob:",destJob)
      print("tubeType:",tubeType)
      print("generic:",generic)
      if(srcJob == 0) then
        Sleep(50)
      elseif(srcJob == 11) then   --// Stn1 Pick camera 1
        setGripper(60,50,50)
        --[[if (DI(21))== ON then
          srcJob = 0
          destJob = 0
          reset_jobs()
          resetLockStatus()
        end]]
        if(tubeType == 1)then
          z_small_big_val = stn1_small_tube_z_val
        elseif(tubeType == 2) then
          z_small_big_val = stn1_Big_tube_z_val
        end
        --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        interfaceOut[5] = AXIS_HOME_POS_CAM_1 ----- axis 7 cam1 home
        statusACK = TCP_snd_rcv()
        Sync()
        interfaceOut[5] = 0
        DOExecute(6, ON)
        Go_( {pose=MOVE_STN1_HOME_P, user=user_cam_1} )
        Go_( {pose=MOVE_STN1_HELP_1_P, user=user_cam_1,sync=0} )
        Go_( {pose=coordinateArrSrcDest[1], user=user_cam_1, sync=0} )   --// Src Pose
        coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],z_small_big_val)
        Move_( {pose=coordinateArr, user=user_cam_1, speeds=10, accels=5} )  --// Pick the test tube
        setGripper(0,50,50) --// Close the Gripper 
        Move_( {pose=coordinateArrSrcDest[1], user=user_cam_1, cp=100, sync=0} )
        -- Go_( {pose=MOVE_STN1_HELP_2_P, user=user_cam_1,sync=0} )
        Go_( {pose=MOVE_STN1_HELP_1_P, user=user_cam_1,sync=0} )
        Go_( {pose=MOVE_STN1_HOME_P, user=user_cam_1, sync=1} )       
        DOExecute(6, OFF)
        -- local gripperStatus = RiqGetStatus()
        Sync()
        if (gripperStatus ~= 2) then
          Go_( {pose=MOVE_STN1_HOME_P, user=user_cam_1, sync=0} )  
          Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane, sync=0} )
          Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1 , sync=1} ) 
          srcJob = 0
          destJob = 0
          reset_jobs()
          DOExecute(5, ON)
        end
        if(destJob == 41) then   --// Stn4 Pick or Place
          --interfaceOut[5] = AXIS_HOME_POS_CAM_1 ----- axis 7 cam2 home
          --statusACK = TCP_snd_rcv()
          --interfaceOut[5] = 0
            --[[if (test == true) then
            DO(1, ON)
            DO(1, OFF)
            tubeStatus = 1
            setLockStatus(2) --// Set the Lock Status to 2 to get next job
            statusACK = TCP_snd_rcv()]]
          --Go_( {pose=MOVE_STN4_HOME_P, user=user_base, accel=50} )
          Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane, sync=0} )
          Go_( {pose=MOVE_STN4_HELP_P, user=user_centri_rck_plane, sync=0} )
          Move_( {pose=MOVE_STN4_CAM2_P, user=user_centri_rck_plane} )
          DO(1, ON)
          local colorOfTube = 0
          tubeStatus = 0
          local levelStatus = 0
          tubeAngle = 0
          --Check the color of the tube
          interfaceOut[5] = 41  --// mac ID 
          interfaceOut[3] = 13  --// execution group 
          statusACK = TCP_snd_rcv()
          if(statusACK == true) then
            colorOfTube = interfaceIn[3]  --// color value
            print("colorOfTube:",colorOfTube)
          end
          if(colorOfTube ~= 0) then 
            local jointArr = GetAngle()
            local jointArrInitPos = GetAngle()   
            while(tubeAngle < 340) do
              if(tubeType == 1)then
                interfaceOut[5] = 41  --// mac ID 
                interfaceOut[3] = 14  --// lock ID , barcode 1 
              elseif(tubeType == 2) then
                interfaceOut[5] = 41  --// mac ID 
                interfaceOut[3] = 14  --// lock ID , barcode 1 
              end
              statusACK = TCP_snd_rcv() 
              if(statusACK == true) then
                tubeStatus = interfaceIn[3]  --// tube status
              end
              if(tubeStatus == 1) then    
                --[[if(tubeStatus == 1 and colorOfTube == 15) then --// only for red tube
                  local jointArr180 = GetAngle()
                  local rot180_p = {joint={jointArr180.joint[1],jointArr180.joint[2],jointArr180.joint[3],
                      jointArr180.joint[4],jointArr180.joint[5],jointArr180.joint[6] - 180}}
                  MoveJ_({pose=rot180_p,speed=100,accel=100})
                  interfaceOut[5] = 41
                  if(colorOfTube == 11)then    
                    interfaceOut[3] = 16      --// lock ID , green level check
                  elseif(colorOfTube == 12)then
                    interfaceOut[3] = 16
                  elseif(colorOfTube == 13)then  -- // brown level check
                    interfaceOut[3] = 17
                  elseif(colorOfTube == 14)then
                    interfaceOut[3] = 16
                  elseif(colorOfTube == 15)then
                    interfaceOut[3] = 18
                  elseif(colorOfTube == 16)then
                    interfaceOut[3] = 16
                  end
                  statusACK = TCP_snd_rcv() 
                  if(statusACK == true) then
                    -- levelStatus = 1
                    levelStatus = interfaceIn[3]  --// tube status
                    tubeStatus = levelStatus  --// tube status
                  end
                  break               
                end]]
                break
              end
              jointArr = GetAngle()
              local rot_p = {joint={jointArr.joint[1],jointArr.joint[2],jointArr.joint[3],jointArr.joint[4],
                                      jointArr.joint[5],jointArr.joint[6] + 15}}
              MoveJ_({pose=rot_p,speed=100,accel=100})
              tubeAngle = tubeAngle + 15
              print("tubeAngle:",tubeAngle)
            end
            MoveJ_({pose=jointArrInitPos,speed=100,accel=100})
          end
          DO(1, OFF)
          Move_( {pose=MOVE_STN4_HELP_P, user=user_centri_rck_plane, sync=1} )
          --Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane, sync=1} )
          setLockStatus(2) --// Set the Lock Status to 2 to get next job
          statusACK = TCP_snd_rcv()
          if(statusACK == true) then
            srcJob = interfaceIn[4]
            destJob = interfaceIn[5]
            print("srcJob:",srcJob)
            print("destJob:",destJob)
            if(srcJob == 52) then   --// Place Tube in Centrifuge Racks
              if(tubeType == 1)then
                z_small_big_val = stn5_small_tube_plc_z_val
              elseif(tubeType == 2) then
                z_small_big_val = stn5_Big_tube_plc_z_val
              end  
              --Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane, sync=1} )
              --Go_( {pose=MOVE_STN5_HELP_P, user=user_centri_rck_plane} )
              Move_( {pose=MOVE_STN4_HELP_P, user=user_centri_rck_plane, sync=1} )
              Move_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane, cpl=100,sync=0} )
              coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],z_small_big_val)
              Move_( {pose=coordinateArr, user=user_centri_rck_plane,speeds=30} )
              setGripper(60,50,50) --// open the Gripper
              Move_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane, speeds=50,cpl=100,sync=0} )
              --Go_( {pose=MOVE_STN5_HELP_P, user=user_centri_rck_plane,sync=0} )
              Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane,sync=1} )
              --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
              setGripper(0,50,50) --// close the Gripper
              resetLockStatus()
              reset_jobs()
            elseif(srcJob == 94) then   --// Place Tube in Beckmen Racks
              Go_( {pose=MOVE_STN9_HOME_P, user=user_A_c_9} )
              setBarcodeOnly(coordinateArrSrcDest[1], user_A_c_9, stn9_z_val, tubeAngle, -90)
              Go_( {pose=MOVE_STN9_HOME_P, user=user_A_c_9} )
              --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
              setGripper(0,50,50) --// Close the Gripper 
              reset_jobs()
            elseif(srcJob == 102) then      --// Place in Fehler Stand
              --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
              interfaceOut[5] = AXIS_HOME_POS_CAM_1 ----- axis 7 cam1 home
              statusACK = TCP_snd_rcv()
              interfaceOut[5] = 0
              --Go_( {pose=MOVE_STN10_FEHLER_HELP_P, user=user_centri_rck_plane} ) 
              if(tubeType == 1) then --// small tube
                Go_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane, sync=0} )
                coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn10_small_tube_z_val)
                Move_( {pose=coordinateArr, user=user_centri_rck_plane,speeds=5,accels=5} )
                setGripper(50,50,50) --// Open the Gripper
                Move_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane,sync=0} )
                setGripper(0,50,50) --// close the Gripper
              elseif(tubeType == 2) then  --// big tube
                Go_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane, sync=0} )
                coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn10_big_tube_z_val)
                Move_( {pose=coordinateArr, user=user_centri_rck_plane,speeds=5,accels=5} )
                setGripper(50,50,50) --// Open the Gripper
                Move_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane,sync=0} )
                setGripper(0,50,50) --// close the Gripper`
              end
              --Go_( {pose=MOVE_STN10_FEHLER_HELP_P, user=user_centri_rck_plane,sync=0} ) 
              Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane, sync=1} )
              --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
              resetLockStatus()  --// Reset the Lock Status
              reset_jobs()
            end
          end
        end
      elseif(srcJob == 91) then   --// Stn9 Pick Rack from Beckmen Rack Holder
        --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        setGripper(100,50,50) --// open the Gripper 
        interfaceOut[5] = AXIS_HOME_POS_CAM_1 ----- axis 7 cam1 home
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        --Go_( {pose=MOVE_STN1_HOME_P, user=user_cam_1,sync=0} )
        --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        Go_( {pose=MOVE_STN9_HOME_P, user=user_A_c_9} )
        Go_( {pose=coordinateArrSrcDest[1], user=user_A_c_9,sync=0} )
        coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn9_rack_pck_z_val)
        Move_( {pose=coordinateArr, user=user_A_c_9} )
        setGripper(0,50,100) --// Close the Gripper 
        Move_( {pose=coordinateArrSrcDest[1], user=user_A_c_9,cpl=100,sync=0} )
        Go_( {pose=MOVE_STN9_HOME_P, user=user_A_c_9,sync=0} )
        --Go_( {pose=MOVE_STN1_HOME_P, user=user_cam_1,sync=0} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        interfaceOut[5] = AXIS_HOME_POS_BECKMAN_LOAD   ----- axis 7 beckman load
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        --Go_( {pose=MOVE_STN7_PLC_HELP_1_P, user=user_base,sync=0} )
        Go_( {pose=MOVE_STN7_PLC_HELP_2_P, user=user_base,sync=1} )
        DOExecute(7, ON)
        Move_( {pose=MOVE_STN7_PLC_RACK_P, user=user_base,speeds=50} )
        setGripper(100,50,50) --// open the Gripper
        Move_( {pose=MOVE_STN7_PLC_HELP_2_P, user=user_base,sync=1} )
        DOExecute(7, OFF)
        --Go_( {pose=MOVE_STN7_PLC_HELP_1_P, user=user_base,sync=0} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        setGripper(0,50,100) --// Close the Gripper 
        reset_jobs()
      elseif(srcJob == 71) then   --// Pick Rack from Beckmen Machine
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        setGripper(100,50,50) --// open the Gripper
        interfaceOut[5] = AXIS_HOME_POS_CAM_1 ----- axis 7 cam1 home
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        Go_( {pose=MOVE_STN7_PCK_HELP_1_P, user=user_base,sync=0} )
        Go_( {pose=MOVE_STN7_PCK_HELP_2_P, user=user_base,speed=50,sync=0} )
        Move_( {pose=MOVE_STN7_PCK_RACK_P, user=user_base,speeds=50} )
        setGripper(0,50,50) --// Close the Gripper 
        -- local gripperStatus = RiqGetStatus()
        if (gripperStatus == 2) then
          tubeStatus = 1
        else
          tubeStatus = 0
        end
        Move_( {pose=MOVE_STN7_SLIDE_P, user=user_base,speeds=5} )
        Move_( {pose=MOVE_STN7_SLIDE_UP_P, user=user_base,cpl=100,sync=0} )
        Go_( {pose=MOVE_STN7_PCK_HELP_1_P, user=user_base,sync=0} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        setLockStatus(5) --// Set the Lock Status to 5 
        statusACK = TCP_snd_rcv()
        if(statusACK == true) then
          srcJob = interfaceIn[4]
          destJob = interfaceIn[5]
          print("srcJob:",srcJob)
          print("destJob:",destJob)
          if(srcJob == 92) then   
            --Go_( {pose=MOVE_STN1_HOME_P, user=user_cam_1,sync=0} )
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
            Go_( {pose=MOVE_STN9_HOME_P, user=user_A_c_9,sync=0} )
            Go_( {pose=coordinateArrSrcDest[1], user=user_A_c_9,sync=0} )
            coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn9_rack_plc_z_val)
            Move_( {pose=coordinateArr, user=user_A_c_9,speeds=10, accels=10} )
            setGripper(100,50,50) --// open the Gripper
            Move_( {pose=coordinateArrSrcDest[1], user=user_A_c_9,cpl=100,sync=0} )
            Go_( {pose=MOVE_STN9_HOME_P, user=user_A_c_9} )
            --Go_( {pose=MOVE_STN1_HOME_P, user=user_cam_1,sync=0} )
            --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
            setGripper(0,50,50) --// Close the Gripper 
          end
        end
        reset_jobs()
      elseif(srcJob == 141) then   --// Pick Rack from Cobas Pure Rack Holder
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        interfaceOut[5] = AXIS_HOME_POS_CAM_1 ----- axis 7 cam1 home
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        Go_( {pose=MOVE_STN14_PCK_RCK_HELP_P, user=user_centri_rck_plane,sync=0})
        --Go_( {pose=MOVE_STN14_PUSH_HELP_P, user=user_centri_rck_plane,speed=100, accel=50} )
        setGripper(0,100,100) --// Close the Gripper 
        Go_( {pose=MOVE_STN14_PUSH_START_P, user=user_centri_rck_plane,sync=0} )
        Go_( {pose=MOVE_STN14_PUSH_END_P, user=user_centri_rck_plane,speed=2, accel=1} )
        Go_( {pose=MOVE_STN14_PUSH_START_P, user=user_centri_rck_plane,sync=0} )
        setGripper(100,50,50) --// open the Gripper
        --Go_( {pose=MOVE_STN14_RCK_APP_P, user=user_centri_rck_plane,speed=50, accel=50} )
        Move_( {pose=MOVE_STN14_PCK_RCK_P, user=user_centri_rck_plane} )
        setGripper(0,10,100) --// Close the Gripper 
        Sleep(1000)
        Move_( {pose=MOVE_STN14_PCK_RCK_PULL_P, user=user_centri_rck_plane,speeds=2, accels=2} )
        Move_( {pose=MOVE_STN14_RCK_APP_P, user=user_centri_rck_plane,cpl=100,sync=0} )
        --Go_( {pose=MOVE_STN14_PCK_RCK_HELP_P, user=user_centri_rck_plane,speed=10, accel=5} )
        Go_( {pose=MOVE_STN14_DRIVE_P, user=user_centri_rck_plane} )
        interfaceOut[5] = AXIS_HOME_POS_COBAS_PURE ----- axis 7 cobas pure machine 
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        Go_( {pose=MOVE_STN14_DRIVE_P, user=user_centri_rck_plane} )
        Go_( {pose=MOVE_STN8_PLC_RCK_HELP_P, user=user_base,sync=0} )
        --Go_( {pose=MOVE_STN8_PLC_RCK_HELP2_P, user=user_base,speed=10, accel=5} )
        DOExecute(7, ON)
        Move_( {pose=MOVE_STN8_PLC_RCK_P, user=user_base,speeds=5, accels=5} )
        setGripper(80,20,20) --// open the Gripper
        --Move_( {pose=MOVE_STN8_PLC_RCK_HELP2_P, user=user_base,speeds=100, accels=50} )
        Move_( {pose=MOVE_STN8_PLC_RCK_HELP_P, user=user_base,cpl=100,sync=0} )
        setGripper(0,50,50) --// Close the Gripper 
        DOExecute(7, OFF)
        Go_( {pose=MOVE_STN14_DRIVE_P, user=user_centri_rck_plane,sync=0} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        --interfaceOut[5] = 704 ----- axis 7 cam 2 home
        --statusACK = send_UDP_ACK_2()
        --interfaceOut[5] = 0
        reset_jobs()
      elseif(srcJob == 93) then   --// Pick tube from Beckmen Rack Holder
        setGripper(60,50,50) --// open the Gripper
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        interfaceOut[5] = AXIS_HOME_POS_CAM_1 ----- axis 7 cam1 home
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        Go_( {pose=MOVE_STN9_HOME_P, user=user_A_c_9,sync=0} )
        Go_( {pose=coordinateArrSrcDest[1], user=user_A_c_9,sync=0} )
        coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn9_z_val)
        Move_( {pose=coordinateArr, user=user_A_c_9,speeds=100, accels=50} )
        setGripper(0,100,50) --// Close the Gripper
        Move_( {pose=coordinateArrSrcDest[1], user=user_A_c_9,cpl=100,sync=0} )
        Go_( {pose=MOVE_STN9_HOME_P, user=user_A_c_9,sync=0} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        if(destJob == 112) then   --// Place in Archive
          local generic = interfaceIn[18]
          Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
          local rackNum = generic
          if (rackNum == 1 ) then  --// Fridge 1
            interfaceOut[5] = AXIS_HOME_POS_CAM_1	
            statusACK = TCP_snd_rcv()
            interfaceOut[5] = 0
            if( tubeType == 1 )then
                z_small_big_val = stn11_rck_1_small_z_val
            elseif( tubeType == 2 ) then
              z_small_big_val = stn11_rck_1_big_z_val
            end
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
            Go_( {pose=MOVE_STN11_D1_HOME_P, user=user_arch_d_1,sync=0} ) 
            Go_( {pose=coordinateArrSrcDest[2], user=user_arch_d_1, sync=0} )   --// Src Pose
            coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],z_small_big_val)
            Move_( {pose=coordinateArr, user=user_arch_d_1, cp=0, speeds=10, accels=5} )
            setGripper(50,50,50) --// open the Gripper
            Move_( {pose=coordinateArrSrcDest[2], user=user_arch_d_1,cpl=100,sync=0} )   --// Src Pose
            --setGripper(0,50,50) --// Close the Gripper
            Go_( {pose=MOVE_STN11_D1_HOME_P, user=user_arch_d_1, sync=0} )
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
          elseif(rackNum == 2 ) then --// Fridge 2
            interfaceOut[5] = AXIS_HOME_POS_BCS ----- axis 7 bcs machine
            statusACK = TCP_snd_rcv()
            interfaceOut[5] = 0
            if( tubeType == 1 )then
              z_small_big_val = stn11_rck_2_small_z_val
            elseif( tubeType == 2 ) then
              z_small_big_val = stn11_rck_2_big_z_val
            end
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
            Go_( {pose=MOVE_STN11_D2_PLC_TUBE_HELP_P, user=user_arch_d_2, sync=0} ) 
            Go_( {pose=coordinateArrSrcDest[2], user=user_arch_d_2, accel=50, sync=0} )   --// Src Pose
            coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],z_small_big_val)
            Move_( {pose=coordinateArr, user=user_arch_d_2, cp=0, speeds=10, accels=5} )
            setGripper(50,50,50) --// open the Gripper
            Move_( {pose=coordinateArrSrcDest[2], user=user_arch_d_2, cpl=100,sync=0} )   --// Src Pose
            Go_( {pose=MOVE_STN11_D2_PLC_TUBE_HELP_P, user=user_arch_d_2, sync=0} ) 
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
          else
            print("Unexpected error in Placing Archive")
            Pause()
          end
          Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
          setGripper(0,50,50) --// Close the Gripper
        end
        reset_jobs()
      elseif(srcJob == 51) then    --// Pick tube from Centrifuge Racks
        if(destJob == 41) then   --// Stn4 Pick or Place 
          --interfaceOut[5] = 704 ----- axis 7 cam2 home
          -- statusACK = TCP_snd_rcv()
          --interfaceOut[5] = 0
          setGripper(50,50,50) --// open the Gripper
          if(tubeType == 1)then
            z_small_big_val = stn5_small_tube_pick_z_val
          elseif(tubeType == 2) then
            z_small_big_val = stn5_Big_tube_pick_z_val
          end
          --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,sync=1} )
          interfaceOut[5] = AXIS_HOME_POS_CAM_1 ----- axis 7 cam1 home
          statusACK = TCP_snd_rcv()
          interfaceOut[5] = 0
          Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane} )
          --Go_( {pose=MOVE_STN5_HELP_P, user=user_centri_rck_plane,sync=0} )          
          Go_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane,sync=0} )
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],z_small_big_val)
          Move_( {pose=coordinateArr, user=user_centri_rck_plane} )   --// Pick the tube from centrifuge racks
          setGripper(0,50,50) --// Close the Gripper
          Move_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane, cpl=100,sync=0} )
          --Go_( {pose=MOVE_STN5_HELP_P, user=user_centri_rck_plane,sync=0} )
          --Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane,sync=0} )
          Go_( {pose=MOVE_STN4_HELP_P, user=user_centri_rck_plane, sync=0} )
          DOExecute(1, ON)
          Move_( {pose=MOVE_STN4_CAM2_P, user=user_centri_rck_plane,sync=1} )
          local colorOfTube = 0
          tubeStatus = 0
          tubeAngle = 0 
          interfaceOut[5] = 41  --// mac ID 
          interfaceOut[3] = 13  --// color eg
          statusACK = TCP_snd_rcv()
          if(statusACK == true) then
            colorOfTube = interfaceIn[3]  --// color value
            print("colorOfTube:",colorOfTube)
          end
          local jointArr = GetAngle()
          local jointArrInitPos = GetAngle()
          while(tubeAngle < 340) do
            interfaceOut[5] = 41  --// mac ID 
            interfaceOut[3] = 14  --// lock ID , barcode 1 
            statusACK = TCP_snd_rcv()
            if(statusACK == true) then
              tubeStatus = interfaceIn[3]  --// tube status
            end
            if(tubeStatus == 1) then 
              if(tubeStatus == 1 and colorOfTube~= 14) then --// no check for yellow
                local jointArr180 = GetAngle()
                local rot180_p = {joint={jointArr180.joint[1],jointArr180.joint[2],jointArr180.joint[3],
                    jointArr180.joint[4],jointArr180.joint[5],jointArr180.joint[6] - 180}}
                MoveJ_({pose=rot180_p,speed=100,accel=100})
                interfaceOut[5] = 41
                if(colorOfTube == 11)then    
                  interfaceOut[3] = 16      --// lock ID , green level check
                elseif(colorOfTube == 12)then  -- // orange
                  interfaceOut[3] = 19
                elseif(colorOfTube == 13)then --// brown level check
                  interfaceOut[3] = 17
                elseif(colorOfTube == 14)then --// yellow  
                  interfaceOut[3] = 16
                elseif(colorOfTube == 15)then
                  interfaceOut[3] = 16
                elseif(colorOfTube == 16)then
                  interfaceOut[3] = 16
                end
                statusACK = TCP_snd_rcv() 
                if(statusACK == true) then
                  levelStatus = interfaceIn[3]  --// tube status
                  --levelStatus = 1
                  tubeStatus = levelStatus  --// tube status
                end
                break
                --[[if(tubeStatus == 1) then
                break
                else
                jointArr = GetAngle()
                local rot_p = {joint={jointArr.joint[1],jointArr.joint[2],jointArr.joint[3],
                jointArr.joint[4],jointArr.joint[5],jointArr.joint[6] - 180}}
                MoveJ(rot_p,"CP=0 Speed =100 Accel=100 SYNC=1")      
                end    ]]                  
              end
              break
            end
            jointArr = GetAngle()
            local rot180_p = {joint={jointArr.joint[1],jointArr.joint[2],jointArr.joint[3],jointArr.joint[4],
                                    jointArr.joint[5],jointArr.joint[6] + 15}}
            MoveJ_( {pose=rot180_p,speed=100,accel=100} )
            tubeAngle = tubeAngle + 15
            print("tubeAngle:",tubeAngle)
          end
          MoveJ_( {pose=jointArrInitPos,speed=100,accel=100} )
          DOExecute(1, OFF)
          Move_( {pose=MOVE_STN4_HELP_P, user=user_centri_rck_plane,sync=1} )
          --Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane} )
          setLockStatus(3) --// Set the Lock Status to 2 to get next job
          statusACK = TCP_snd_rcv() 
          if(statusACK == true) then
            srcJob = interfaceIn[4]
            destJob = interfaceIn[5]
            decap_z_small_big_val = nil
            decap_small_big_pck_p = nil
            print("srcJob:",srcJob)
            print("destJob:",destJob)
            if(srcJob == 32) then     --// Place tube in BCS machine
              if(tubeType == 1)then
                decap_z_small_big_val = decap_small_tube_z_val
                decap_small_big_pck_p = P200
              elseif(tubeType == 2) then
                decap_z_small_big_val = decap_big_tube_z_val
                decap_small_big_pck_p = P200
              end
              DOExecute(2, ON)
              Go_( {pose=MOVE_DECAP_HELP_P, user=user_centri_rck_plane} )
              updatedPos = GetPose()
              coordinateArr = setCoordinatePos_z({coordinate=updatedPos.coordinate},decap_z_small_big_val)
              Move_( {pose=coordinateArr, user=user_centri_rck_plane, speeds=50} )
              jointArr = GetAngle()
              local jointArrStartPos = GetAngle()      --// start pos
              local updatedJointPos = setBarcodeAngle(jointArrStartPos,tubeAngle)
              MoveJ_( {pose=updatedJointPos,speed=100,accel=100} )
              DOExecute(2, OFF)
              setGripper(80,50,50) --// open the Gripper 
              DOExecute(2, ON)
              DOExecute(2, OFF)
              Go_( {pose=MOVE_DECAP_SMALL_START_P, user=user_centri_rck_plane} )
              setGripper(0,30,30) --// Close the Gripper
              Go_( {pose=MOVE_DECAP_SMALL_END_P, user=user_centri_rck_plane} )
              Go_( {pose=MOVE_DECAP_HELP_P, user=user_centri_rck_plane,sync=0} )
              Go_( {pose=MOVE_DECAP_BIN_P, user=user_centri_rck_plane} )
              setGripper(80,50,50) --// open the Gripper
              setGripper(0,50,50) --// Close the Gripper
              setGripper(80,50,50) --// open the Gripper
              setGripper(0,50,50) --// Close the Gripper
              setGripper(80,50,50) --// open the Gripper
              --Go_( {pose=MOVE_DECAP_HELP_P, user=user_centri_rck_plane,speed=50, accel=50} )
              MoveJ_( {pose=jointArr,speed=100,accel=100} )
              Move_( {pose=decap_small_big_pck_p , user=user_centri_rck_plane,speeds=50, accels=50} )
              setGripper(0,50,5) --// Close the Gripper
              DOExecute(2, ON)
              Move_( {pose=MOVE_DECAP_HELP_P, user=user_centri_rck_plane,cpl=100,sync=0} )
              Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane,sync=0} )
              Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
              interfaceOut[5] = AXIS_HOME_POS_BCS ----- axis 7 cam1 home
              statusACK = TCP_snd_rcv()
              interfaceOut[5] = 0
              Go_( {pose=MOVE_STN3_HOME_P, user=user_BCS} )
              Go_( {pose=coordinateArrSrcDest[2], user=user_BCS,sync=0} )
              coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],stn3_tube_plc_z_val)
              Move_( {pose=coordinateArr, user=user_BCS,speeds=10, accels=5} )   
              setGripper(60,50,50) --// open the Gripper
              Move_( {pose=coordinateArrSrcDest[2], user=user_BCS,cpl=100,sync=0} )
              Go_( {pose=MOVE_STN3_HOME_P, user=user_BCS,sync=0} )
              Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
              setGripper(100,100,100) --// Close the Gripper
              resetLockStatus()  --// Reset the Lock Status
              reset_jobs()
            elseif(srcJob == 143) then   --// Place tube in Cobas Pure Rack Holder
              if(tubeType == 1)then
                decap_z_small_big_val = decap_small_tube_z_val
                stn14_small_big_z_val = stn14_small_z_val
                decap_small_big_pck_p = P198
                DOExecute(2, ON)
                Go_( {pose=MOVE_DECAP_HELP_P, user=user_centri_rck_plane} )
                updatedPos = GetPose()
                coordinateArr = setCoordinatePos_z({coordinate=updatedPos.coordinate},decap_z_small_big_val)
                Move_( {pose=coordinateArr, user=user_centri_rck_plane, speeds=10, accels=5} )
                jointArr = GetAngle()
                local jointArrStartPos = GetAngle()      --// start pos
                local updatedJointPos = setBarcodeAngle(jointArrStartPos,tubeAngle)
                MoveJ_( {pose=updatedJointPos,speed=100,accel=100} )
                DOExecute(2, OFF)
                setGripper(80,50,50) --// open the Gripper 
                DOExecute(2, ON)
                DOExecute(2, OFF)
                Go_( {pose=MOVE_DECAP_SMALL_START_P, user=user_centri_rck_plane} )
                setGripper(0,30,30) --// Close the Gripper
                Go_( {pose=MOVE_DECAP_SMALL_END_P, user=user_centri_rck_plane} )
                Go_( {pose=MOVE_DECAP_HELP_P, user=user_centri_rck_plane,sync=0} )
                Go_( {pose=MOVE_DECAP_BIN_P, user=user_centri_rck_plane} )
                setGripper(80,50,50) --// open the Gripper
                setGripper(0,50,50) --// Close the Gripper
                setGripper(80,50,50) --// open the Gripper
                setGripper(0,50,50) --// Close the Gripper
                setGripper(80,50,50) --// open the Gripper
                --Go_( {pose=MOVE_DECAP_HELP_P, user=user_centri_rck_plane,speed=50, accel=50} )
                MoveJ_( {pose=jointArr,speed=100,accel=100} )
                Move_( {pose=decap_small_big_pck_p, user=user_centri_rck_plane} )
                setGripper(0,50,10) --// Close the Gripper
                DOExecute(2, ON)
                Move_( {pose=MOVE_DECAP_HELP_P, user=user_centri_rck_plane,cpl=100,sync=0} )
                Go_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane,sync=0} )
                coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn14_small_big_z_val)
                Move_( {pose=coordinateArr, user=user_centri_rck_plane,speeds=5, accels=2} )   
                setGripper(50,50,50) --// open the Gripper
                Move_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane ,cpl=100,sync=0} )
                Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane} )
                --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
                setGripper(0,50,50) --// close  the Gripper 
              elseif(tubeType == 2) then
                decap_z_small_big_val = decap_big_tube_z_val
                stn14_small_big_z_val = stn14_big_z_val
                decap_small_big_pck_p = P197
                DOExecute(2, ON)
                Go_( {pose=MOVE_DECAP_HELP_P, user=user_centri_rck_plane} )
                updatedPos = GetPose()
                coordinateArr = setCoordinatePos_z({coordinate=updatedPos.coordinate},decap_z_small_big_val)
                Move_( {pose=coordinateArr, user=user_centri_rck_plane, speeds=10, accels=5} )
                jointArr = GetAngle()
                local jointArrStartPos = GetAngle()      --// start pos
                local updatedJointPos = setBarcodeAngle(jointArrStartPos,tubeAngle)
                MoveJ_( {pose=updatedJointPos,speed=100,accel=100} )
                DOExecute(2, OFF)
                setGripper(80,50,50) --// open the Gripper 
                DOExecute(2, ON)
                DOExecute(2, OFF)
                Go_( {pose=MOVE_DECAP_BIG_START_P, user=user_centri_rck_plane} )
                setGripper(0,30,30) --// Close the Gripper
                Go_( {pose=MOVE_DECAP_BIG_END_P, user=user_centri_rck_plane} )
                Go_( {pose=MOVE_DECAP_HELP_P, user=user_centri_rck_plane} )
                Go_( {pose=MOVE_DECAP_BIN_P, user=user_centri_rck_plane} )
                setGripper(80,50,50) --// open the Gripper
                setGripper(0,50,50) --// Close the Gripper
                setGripper(80,50,50) --// open the Gripper
                setGripper(0,50,50) --// Close the Gripper
                setGripper(80,50,50) --// open the Gripper
                --Go_( {pose=MOVE_DECAP_HELP_P, user=user_centri_rck_plane,speed=50, accel=50} )
                MoveJ_( {pose=jointArr,speed=100,accel=100} )
                Move_( {pose=decap_small_big_pck_p, user=user_centri_rck_plane} )
                setGripper(0,50,5) --// Close the Gripper
                DOExecute(2, ON)
                Move_( {pose=MOVE_DECAP_HELP_P, user=user_centri_rck_plane} )
                Go_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane} )
                coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn14_small_big_z_val)
                Move_( {pose=coordinateArr, user=user_centri_rck_plane} )   
                setGripper(50,50,50) --// open the Gripper
                Move_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane,sync=0} )
                Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane} )
                --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
                setGripper(0,50,50) --// close  the Gripper 
              end 
              --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
              Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane} )
              resetLockStatus()  --// Reset the Lock Status
              reset_jobs()
            elseif(srcJob == 102) then   --// Place in Fehler Stand
              --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
              interfaceOut[5] = AXIS_HOME_POS_CAM_1 ----- axis 7 cam1 home
              statusACK = TCP_snd_rcv()
              interfaceOut[5] = 0
              --Go_( {pose=MOVE_STN10_FEHLER_HELP_P, user=user_centri_rck_plane} ) 
              Go_( {pose=MOVE_STN4_HELP_P, user=user_centri_rck_plane,sync=1} )
              if(tubeType == 1) then --// small tube
                Go_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane, sync=0} )
                coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn10_small_tube_z_val)
                Move_( {pose=coordinateArr, user=user_centri_rck_plane,speeds=50} )
                setGripper(50,50,50) --// Open the Gripper
                Move_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane,cpl=100,sync=0} )
                setGripper(0,50,50) --// close the Gripper
              elseif(tubeType == 2) then  --// big tube
                Go_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane, sync=0} )
                coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn10_big_tube_z_val)
                Move_( {pose=coordinateArr, user=user_centri_rck_plane,speeds=50} )
                setGripper(50,50,50) --// Open the Gripper
                Move_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane,cpl=100,sync=0} )
                setGripper(0,50,50) --// close the Gripper`
              end
              --Go_( {pose=MOVE_STN10_FEHLER_HELP_P, user=user_centri_rck_plane,sync=0} ) 
              --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
              Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane} )
              resetLockStatus()  --// Reset the Lock Status
              reset_jobs()
            end
          end 
        elseif(destJob == 62) then    --// Place Racks in Centrifuge Machine    
          if (test == true) then
            print("Centrifuge skipped")
            interfaceOut[5] = 68  --// mac ID 
            statusACK = TCP_snd_rcv()
            Sync()
          else 
            setGripper(50,50,50) --// Open the Gripper
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
            interfaceOut[5] = AXIS_HOME_POS_CENTRIFUGE ----- axis 7 centrifuge
            statusACK = TCP_snd_rcv()
            Sync() -- for 7th axis
            interfaceOut[5] = 0
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
            Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane,sync=0} )
            Go_( {pose=MOVE_STN6_HELP_1_P, user=user_centri_rck_plane} )
            local rack_poses = {}
            local batch_num = coordinateArrSrcDest[1].coordinate[1]
            if (batch_num == 1) then 
              rack_poses = stn5_batch1_poses
            elseif (batch_num == 2) then
              rack_poses = stn5_batch2_poses
            else
              Pause()
            end
            interfaceOut[5] = 62  --// mac ID 
            statusACK = TCP_snd_rcv()
            Sync()
            local loop_count = 0
            while true do
              loop_count = loop_count + 1
              if (loop_count == 1) then
                interfaceOut[5] = 63 
              elseif(loop_count == 2) then
                interfaceOut[5] = 64 
              elseif(loop_count == 3) then
                interfaceOut[5] = 65  
              elseif(loop_count == 4) then
                interfaceOut[5] = 66 
              end            
              statusACK = TCP_snd_rcv()
              --Sync()
              ----write here picking from centrifuge machine-------------------------------------------
              Go_( {pose=MOVE_STN6_HELP_1_P, user=user_centri_rck_plane} )
              Go_( {pose=rack_poses[loop_count], user=user_centri_rck_plane,sync=0} )
              --setGripper(50,100,0)
              local coordinateArr = setCoordinatePos_z(rack_poses[loop_count],stn5_rack_pick_z_val)
              Move_( {pose=coordinateArr, user=user_centri_rck_plane} )
              --setGripper(0,50,50)
              setGripper(0,50,50) --// Close the Gripper
              Move_( {pose=rack_poses[loop_count], user=user_centri_rck_plane,cpl=100,sync=0} )
              Go_( {pose=MOVE_STN6_HELP_1_P, user=user_centri_rck_plane,sync=0} )
              Go_( {pose=MOVE_STN6_HELP_2_P, user=user_centri_rck_plane,sync=0} )              
              Move_( {pose=MOVE_STN6_P, user=user_centri_rck_plane, speeds=2, accels=2} )
              --setGripper(50,100,0)
              setGripper(50,100,0) --// Open the Gripper
              Move_( {pose=MOVE_STN6_HELP_2_P, user=user_centri_rck_plane,cpl=100,sync=0} )
              Go_( {pose=MOVE_STN6_HELP_1_P, user=user_centri_rck_plane,sync=1} )       
              if(loop_count >= 4) then
                break
              end
            end
            interfaceOut[5] = 67  --// mac ID 
            statusACK = TCP_snd_rcv()
            Sync()
            interfaceOut[5] = 68  --// mac ID 
            statusACK = TCP_snd_rcv()
            Sync()
            Go_( {pose=MOVE_STN6_HELP_1_P, user=user_centri_rck_plane,sync=1} )   
            Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane,sync=0} )
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
          end
          reset_jobs()
        elseif(destJob == 55) then   --// Pick from racks and place tube in Counter Weight Pos
          if(tubeType == 1)then
            z_small_big_val = stn5_small_tube_pick_z_val
          elseif(tubeType == 2) then
            z_small_big_val = stn5_Big_tube_pick_z_val
          end 
          setGripper(50,50,50) --// open the Gripper
          --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,sync=1} )
          interfaceOut[5] = AXIS_HOME_POS_CAM_1 ----- axis 7 cam1 home
          statusACK = TCP_snd_rcv()
          interfaceOut[5] = 0
          --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,sync=1} )
          Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane} )
          --Go_( {pose=MOVE_STN5_HELP_P, user=user_centri_rck_plane} )
          Go_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane,sync=0} )
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],z_small_big_val)
          Move_( {pose=coordinateArr, user=user_centri_rck_plane} )   --// Pick the tube from centrifuge racks
          setGripper(0,50,50) --// Close the Gripper
          Move_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane,cpl=100,sync=0} )
          --Go_( {pose=MOVE_STN5_HELP_P, user=user_centri_rck_plane,sync=0} )
          if(tubeType == 1)then
            cw_z_small_big_val = small_cw_z_val
          elseif(tubeType == 2) then
            cw_z_small_big_val = big_cw_z_val
          end
          Go_( {pose=coordinateArrSrcDest[2], user=user_centri_rck_plane,sync=0} )
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],cw_z_small_big_val)
          Move_( {pose=coordinateArr, user=user_centri_rck_plane,speeds=20} )
          setGripper(50,50,50) --// open the Gripper 
          Move_( {pose=coordinateArrSrcDest[2], user=user_centri_rck_plane,cpl=100,sync=0} )  ------ cw_pick
          Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane} )
          --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
          setGripper(0,50,50) --// Close the Gripper
          reset_jobs()
        end
      elseif(srcJob == 61) then   --// Pick Racks from Centrifuge Machine
        if (test == true) then 
          print("Centrifuge skipped")
        else
          setGripper(50,50,50) --// Open the Gripper
          Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,sync=1} )  
          interfaceOut[5] = AXIS_HOME_POS_CENTRIFUGE ----- axis 7 centrifuge home
          statusACK = TCP_snd_rcv()
          Sync()
          interfaceOut[5] = 0       
          Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )  
          Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane,sync=0} )  
          Go_( {pose=MOVE_STN6_HELP_1_P, user=user_centri_rck_plane} )
          local rack_poses = {}
          local batch_num = coordinateArrSrcDest[1].coordinate[1]
          if (batch_num == 1) then 
            rack_poses = stn5_batch1_poses
          elseif (batch_num == 2) then
            rack_poses = stn5_batch2_poses
          else
            Pause()
          end
          interfaceOut[5] = 62  --// mac ID 
          statusACK = TCP_snd_rcv()
          Sync()
          local loop_count = 0
          while true do
            loop_count = loop_count + 1
            if (loop_count == 1) then
              interfaceOut[5] = 63 
            elseif(loop_count == 2) then
              interfaceOut[5] = 64 
            elseif(loop_count == 3) then
              interfaceOut[5] = 65  
            elseif(loop_count == 4) then
              interfaceOut[5] = 66 
            end
            statusACK = TCP_snd_rcv()
            Go_( {pose=MOVE_STN6_HELP_1_P, user=user_centri_rck_plane} )
            Go_( {pose=MOVE_STN6_HELP_2_P, user=user_centri_rck_plane,sync=0} ) 
            Move_( {pose=MOVE_STN6_P, user=user_centri_rck_plane} )
            setGripper(0,50,50) --// Close the Gripper
            Move_( {pose=MOVE_STN6_HELP_2_P, user=user_centri_rck_plane,cpl=100,sync=0} ) 
            Go_( {pose=MOVE_STN6_HELP_1_P, user=user_centri_rck_plane,sync=0} )
            Go_( {pose=rack_poses[loop_count], user=user_centri_rck_plane, sync=0} )
            local coordinateArr = setCoordinatePos_z(rack_poses[loop_count],stn5_rack_plc_val)
            Move_( {pose=coordinateArr, user=user_centri_rck_plane, speeds=20, accels=10} )
            setGripper(50,50,50) --// Open the Gripper
            Move_( {pose=rack_poses[loop_count], user=user_centri_rck_plane,sync=0} )
            Go_( {pose=MOVE_STN6_HELP_1_P, user=user_centri_rck_plane} )
            if(loop_count >= 4) then
              break
            end
          end
          Go_( {pose=MOVE_STN6_HELP_1_P, user=user_centri_rck_plane} )
          Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane,sync=0} )
          Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        end
        reset_jobs()
      elseif(srcJob == 54) then   --// Pick Counter Weight 
        if(tubeType == 1)then
          cw_z_small_big_val = small_cw_z_val
        elseif(tubeType == 2) then
          cw_z_small_big_val = big_cw_z_val
        end
        interfaceOut[5] = AXIS_HOME_POS_CAM_1 ----- axis 7 cam2 home
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1, speed=50,sync=0} )
        Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane} )
        Go_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane,sync=0} )
        setGripper(50,50,50) --// open the Gripper 
        coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],cw_z_small_big_val)
        Move_( {pose=coordinateArr, user=user_centri_rck_plane} )
        setGripper(0,50,50) --// Close the Gripper
        Move_( {pose=coordinateArrSrcDest[1], user=user_centri_rck_plane,cpl=100,sync=0} )
        --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,speed=50, accel=5} )  
        if(destJob == 52) then     --// Place Counter Weight in Centrifuge Racks
          if(tubeType == 1)then
            z_small_big_val = stn5_small_tube_plc_z_val
          elseif(tubeType == 2) then
            z_small_big_val = stn5_Big_tube_plc_z_val
          end 
          --Go_( {pose=MOVE_STN5_HELP_P, user=user_centri_rck_plane,sync=0} )
          Go_( {pose=coordinateArrSrcDest[2], user=user_centri_rck_plane,sync=0} )
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],z_small_big_val)
          Move_( {pose=coordinateArr, user=user_centri_rck_plane} )   --// Place cw in centrifuge racks
          setGripper(50,50,50) --// open the Gripper
          Move_( {pose=coordinateArrSrcDest[2], user=user_centri_rck_plane,cpl=100,sync=0} )
          --Go_( {pose=MOVE_STN5_HELP_P, user=user_centri_rck_plane,sync=0} )
          Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane,sync=1} )
        end
        Go_( {pose=MOVE_STN5_HOME_P, user=user_centri_rck_plane,sync=1} )
        --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1, sync=1} )
        setGripper(0,50,50) --// Close the Gripper
        reset_jobs()
      elseif(srcJob == 33) then    --// load Rack in BCS machine 
        setGripper(0,50,50) --// Close the Gripper
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        interfaceOut[5] = AXIS_HOME_POS_BCS ----- axis 7 bcs machine
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        Go_( {pose=MOVE_STN3_HOME_P, user=user_BCS,sync=0} )
        Go_( {pose=coordinateArrSrcDest[1], user=user_BCS} )
        --coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn3_rack_z_val)
        --Move_( {pose=coordinateArr, user=user_BCS,speeds=10, accels=5} )
        local updatedPos = GetPose()
        coordinateArr = setCoordinatePos_y({coordinate=updatedPos.coordinate},stn3_rack_load_in_y_val)
        Move_( {pose=coordinateArr, user=user_BCS,speeds=2, accels=2} )
        Move_( {pose=coordinateArrSrcDest[1], user=user_BCS,cpl=100,sync=0} )
        Go_( {pose=MOVE_STN3_HOME_P, user=user_BCS,sync=0} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        reset_jobs()
      elseif(srcJob == 34) then    --// unload Rack  from BCS machine 
        setGripper(50,50,50) --// open the Gripper
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        interfaceOut[5] = AXIS_HOME_POS_BCS ----- axis 7 bcs machine
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        Go_( {pose=MOVE_STN3_HOME_P, user=user_BCS,sync=0} )
        Go_( {pose=coordinateArrSrcDest[1], user=user_BCS} )
        coordinateArr = setCoordinatePos_y(coordinateArrSrcDest[1],stn3_rack_unload_in_y_val)
        Move_( {pose=coordinateArr, user=user_BCS,speeds=2, accels=2} )    
        setGripper(10,0,50) --// Close the Gripper ---- BCS gripper pos 10 is important
        -- local gripperStatus = RiqGetStatus()
        if (gripperStatus == 2) then
          tubeStatus = 1
        else
          tubeStatus = 0
        end
        coordinateArr = setCoordinatePos_y(coordinateArrSrcDest[1],stn3_rack_unload_out_y_val)
        Move_( {pose=coordinateArr, user=user_BCS,speeds=1, accels=1} )    
        setGripper(40,50,50) --// open the Gripper
        Go_( {pose=coordinateArrSrcDest[1], user=user_BCS,sync=0} )
        Go_( {pose=MOVE_STN3_HOME_P, user=user_BCS, sync=0} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        setGripper(0,50,50) 
        setLockStatus(4) --// Set the Lock Status to 4 
        statusACK = TCP_snd_rcv()
        reset_jobs()
      elseif(srcJob == 31) then   --// Pick tube from BCS RACK
        setGripper(60,50,50) --// open the Gripper
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        interfaceOut[5] = AXIS_HOME_POS_BCS ----- axis 7 bcs machine
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        Go_( {pose=MOVE_STN3_HOME_P, user=user_BCS,sync=0} )
        Go_( {pose=coordinateArrSrcDest[1], user=user_BCS,sync=0} )
        coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn3_tube_pck_z_val)
        Move_( {pose=coordinateArr, user=user_BCS,speeds=10, accels=10} )
        setGripper(0,50,20) --// Close the Gripper
        Move_( {pose=coordinateArrSrcDest[1], user=user_BCS,speeds=10, accels=10,cpl=100,sync=0} )
        Go_( {pose=MOVE_STN3_HOME_P, user=user_BCS,sync=0} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
        if(destJob == 112) then   --// Place in Archive
          local generic = interfaceIn[18]
          local rackNum = generic
          if (rackNum == 1 ) then  --// Fridge 1
            interfaceOut[5] = AXIS_HOME_POS_CAM_1	
            statusACK = TCP_snd_rcv()
            interfaceOut[5] = 0
            if( tubeType == 1 )then
                z_small_big_val = stn11_rck_1_small_z_val
            elseif( tubeType == 2 ) then
              z_small_big_val = stn11_rck_1_big_z_val
            end
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
            Go_( {pose=MOVE_STN11_D1_HOME_P, user=user_arch_d_1,sync=0} ) 
            Go_( {pose=coordinateArrSrcDest[2], user=user_arch_d_1, accel=50, sync=0} )   --// Src Pose
            coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],z_small_big_val)
            Move_( {pose=coordinateArr, user=user_arch_d_1, cpl=0, speeds=10, accels=5} )
            setGripper(50,50,50) --// open the Gripper
            Move_( {pose=coordinateArrSrcDest[2], user=user_arch_d_1,cpl=100, sync=0} )   --// Src Pose
            --setGripper(0,50,50) --// Close the Gripper
            Go_( {pose=MOVE_STN11_D1_HOME_P, user=user_arch_d_1, sync=0} ) 
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
          elseif(rackNum == 2 ) then --// Fridge 2
            if( tubeType == 1 )then
              z_small_big_val = stn11_rck_2_small_z_val
            elseif( tubeType == 2 ) then
              z_small_big_val = stn11_rck_2_big_z_val
            end
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
            Go_( {pose=MOVE_STN11_D1_HOME_P, user=user_arch_d_1,sync=0} ) 
            Go_( {pose=MOVE_STN11_D2_PLC_TUBE_HELP_P, user=user_arch_d_2, sync=0} ) 
            Go_( {pose=coordinateArrSrcDest[2], user=user_arch_d_2,sync=0} )   --// Src Pose
            coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],z_small_big_val)
            Move_( {pose=coordinateArr, user=user_arch_d_2, cpl=0, speeds=10, accels=5} )
            setGripper(50,50,50) --// open the Gripper
            Move_( {pose=coordinateArrSrcDest[2], user=user_arch_d_2,cpl=100,sync=0} )   --// Src Pose
            Go_( {pose=MOVE_STN11_D2_PLC_TUBE_HELP_P, user=user_arch_d_2, sync=0} ) 
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
          else
            print("Unexpected error in Placing Archive")
            Pause()
          end
          Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
          setGripper(0,50,50) --// Close the Gripper
        end
        reset_jobs()
      elseif(srcJob == 21) then   ----//Pick Rack from Cobas Pure station and place in (cobas pure rack holder station 14) 
        if ( test == true ) then
          print("Pick Cobas Pure Rack skipped")
        else
          local generic = interfaceIn[18]
          local rckIndx = generic
          if ( (rckIndx >= 1  and rckIndx <= 10) or (rckIndx >= 21 and rckIndx <= 30) ) then 
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1, sync=1} )
            setGripper(70,50,50)
            interfaceOut[5] = AXIS_HOME_POS_COBAS_PURE_RCK_1 ----- axis 7 cobas pure rack 1
            statusACK = TCP_snd_rcv()
            interfaceOut[5] = 0
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1, sync=1} )
            --Go_( {pose=MOVE_STN2_CPR1_HELP_P, user=user_stn2_plane,sync=0} )
            Go_( {pose=coordinateArrSrcDest[1], user=user_stn2_plane, sync=0} )   --// Src Pose
            coordinateArr = setCoordinateDiffPos_z(coordinateArrSrcDest[1],stn2_rck_diff_pick_z_val)
            --Move_( {pose=coordinateArr, user=user_stn2_plane, cp=0, speeds=10, accels=5} )
            Move_( {pose=coordinateArr, user=user_stn2_plane, cpl=0} )
            setGripper(0,50,100)
            Move_( {pose=coordinateArrSrcDest[1], user=user_stn2_plane,cpl=100, sync=0} )
            --Go_( {pose=MOVE_STN2_CPR1_HELP_P, user=user_stn2_plane,sync=0} )
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1, sync=1} )
            interfaceOut[5] = AXIS_HOME_POS_CAM_1 ----- axis 7 cam 1
            statusACK = TCP_snd_rcv()
            interfaceOut[5] = 0
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1, sync=1} )
            --Go_( {pose=MOVE_STN14_PLC_RCK_HELP_P, user=user_centri_rck_plane,sync=0} )
            Go_( {pose=MOVE_STN14_PLC_RCK_APP_P, user=user_centri_rck_plane,sync=0} )
            Move_( {pose=MOVE_STN14_PLC_RCK_P, user=user_centri_rck_plane,sync=0} )
            setGripper(70,50,50) --// open the Gripper
            Move_( {pose=MOVE_STN14_PLC_RCK_APP_P, user=user_centri_rck_plane,cpl=100, sync=0} )
            --Go_( {pose=MOVE_STN14_PLC_RCK_HELP_P, user=user_centri_rck_plane, sync=0} )
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,sync=1} )
            setGripper(0,50,50) --// Close the Gripper
            reset_jobs()
          elseif((rckIndx >= 11  and rckIndx <= 20) or (rckIndx >= 31 and rckIndx <= 40)) then 
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1, sync=1} )
            setGripper(70,50,50)
            interfaceOut[5] = AXIS_HOME_POS_COBAS_PURE_RCK_2 ----- axis 7 cobas pure rack 2
            statusACK = TCP_snd_rcv()
            interfaceOut[5] = 0
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1, sync=1} )
            --Go_( {pose=MOVE_STN2_CPR2_HELP_P, user=user_stn2_plane,sync=0} )
            Go_( {pose=coordinateArrSrcDest[1], user=user_stn2_plane, sync=0} )   --// Src Pose
            coordinateArr = setCoordinateDiffPos_z(coordinateArrSrcDest[1],stn2_rck_diff_pick_z_val)
            Move_( {pose=coordinateArr, user=user_stn2_plane, cp=0} )
            setGripper(0,50,100)
            Move_( {pose=coordinateArrSrcDest[1], user=user_stn2_plane,cpl=100, sync=0} )
            --Go_( {pose=MOVE_STN2_CPR2_HELP_P, user=user_stn2_plane, sync=0} )
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1, sync=1} )
            interfaceOut[5] = AXIS_HOME_POS_CAM_1 ----- axis 7 cam 1
            statusACK = TCP_snd_rcv()
            interfaceOut[5] = 0
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1, sync=1} )
            --Go_( {pose=MOVE_STN14_PLC_RCK_HELP_P, user=user_centri_rck_plane,sync=0} )
            Go_( {pose=MOVE_STN14_PLC_RCK_APP_P, user=user_centri_rck_plane, sync=0} )
            Move_( {pose=MOVE_STN14_PLC_RCK_P, user=user_centri_rck_plane,sync=0} )
            setGripper(70,50,50) --// open the Gripper
            Move_( {pose=MOVE_STN14_PLC_RCK_APP_P, user=user_centri_rck_plane,cpl=100, sync=0} )
            --Go_( {pose=MOVE_STN14_PLC_RCK_HELP_P, user=user_centri_rck_plane, sync=0} )
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,sync=1} )
            setGripper(0,50,50) --// Close the Gripper
            reset_jobs()
          else
            print("Some Error occured while passing index of stn2 ")
            Pause()
          end
        end
        reset_jobs()
      elseif(srcJob == 152) then   --// Place Basket in Cobas Pure station 15
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,sync=1} )
        interfaceOut[5] = AXIS_HOME_POS_COBAS_BASKET_15----- axis 7 cobas pure machine
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        setGripper(80,100,100)
        Go_( {pose=MOVE_STN8_15_PCK_HELP1_P, user=user_base} )
        Move_( {pose=MOVE_STN8_15_PCK_HELP2_P, user=user_base,speeds= 10, accels = 5,cpl=0 } )
        setGripper(50,100,100)
        Move_( {pose=MOVE_STN8_15_PCK_HELP3_P, user=user_base,speeds= 10, accels = 5,cpl=0 } )
        setGripper(0,20,100)
        Sleep(500)
        Move_( {pose=MOVE_STN8_15_PCK_HELP4_P, user=user_base,speeds= 2, accels = 5,cpl=0 } )
        Go_( {pose=MOVE_STN15_STN8_HELP5_P, user=user_base,speed=5,accel=5,sync=1} )
        Go_( {pose=MOVE_STN15_STN8_BRIDGE_P, user=user_cprt_plane,speed=5,accel=5,sync=0} )
        Go_( {pose=MOVE_STN8_15_PLC_HELP6_P, user=user_cprt_plane,speed=5,accel=5,sync=1} )
        Sleep(1000)
        Move_( {pose=MOVE_STN8_15_PLC_HELP7_P, user=user_cprt_plane,speeds= 3, accels = 3,cpl=0 } )
        Move_( {pose=MOVE_STN8_15_PLC_HELP8_PUSH_P, user=user_cprt_plane,speeds= 2, accels = 2,cpl=0 } )
        setGripper(50,100,100)
        Move_( {pose=MOVE_STN8_15_PLC_HELP9_P, user=user_cprt_plane,speeds= 2, accels = 2,cpl=0 } )
        Move_( {pose=MOVE_STN8_15_PLC_HELP10_LEAVE_P, user=user_cprt_plane,sync=0} )
        Go_( {pose=MOVE_STN15_STN8_BRIDGE_P, user=user_cprt_plane,sync=0} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        setGripper(0,100,10)
        reset_jobs()
      elseif(srcJob == 162) then   --// Place Basket in Cobas Pure station 16
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,sync=1} )
        interfaceOut[5] = AXIS_HOME_POS_COBAS_PURE ----- axis 7 cobas pure machine
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        setGripper(80,100,100)
        Go_( {pose=MOVE_STN8_16_PCK_HELP1_P, user=user_base} )
        Move_( {pose=MOVE_STN8_16_PCK_HELP2_P, user=user_base,speeds= 10, accels = 5,cpl=0 } )
        setGripper(50,100,100)
        Move_( {pose=MOVE_STN8_16_PCK_HELP3_P, user=user_base,speeds= 10, accels = 5,cpl=0 } )
        setGripper(0,20,100)
        Sleep(500)
        Move_( {pose=MOVE_STN8_16_PCK_HELP4_P, user=user_base,speeds= 2, accels = 5,cpl=0 } )
        Go_( {pose=MOVE_STN8_16_PCK_HELP5_P, user=user_base,speed=5,accel=5,sync=1} )
        Go_( {pose=MOVE_STN16_STN8_BRIDGE_P, user=user_cprt_plane,speed=5,accel=5,sync=0} )
        Go_( {pose=MOVE_STN8_16_PLC_HELP6_P, user=user_cprt_plane,speed=5,accel=5,sync=1} )
        Sleep(1000)
        Move_( {pose=MOVE_STN8_16_PLC_HELP7_P, user=user_cprt_plane,speeds= 3, accels = 3,cpl=0 } )
        Move_( {pose=MOVE_STN8_16_PLC_HELP8_PUSH_P, user=user_cprt_plane,speeds= 2, accels = 2,cpl=0 } )
        setGripper(50,100,100)
        Move_( {pose=MOVE_STN8_16_PLC_HELP9_P, user=user_cprt_plane,speeds= 2, accels = 2,cpl=0 } )
        Move_( {pose=MOVE_STN8_16_PLC_HELP10_LEAVE_P, user=user_cprt_plane,sync=0} )
        Go_( {pose=MOVE_STN16_STN8_BRIDGE_P, user=user_cprt_plane,sync=0} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        setGripper(0,100,10)
        reset_jobs()
      elseif(srcJob == 151) then   --// Pick Basket from Cobas Pure Rack 1
        if ( test == true ) then
          print("Pick Cobas Pure Basket 1 skipped")
        else
          Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,sync=1} )
          interfaceOut[5] = AXIS_HOME_POS_COBAS_BASKET_15
          statusACK = TCP_snd_rcv()
          interfaceOut[5] = 0
          setGripper(100,100,100)
          Go_( {pose=MOVE_STN15_HOME_P, user=user_cprt_plane, sync=1} )
          Go_( {pose=MOVE_STN15_8_PCK_HELP1_P, user=user_cprt_plane, sync=0} )
          Move_( {pose=MOVE_STN15_8_PCK_HELP2_P, user=user_cprt_plane, sync=1} )
          setGripper(50,100,100)
          Move_( {pose=MOVE_STN15_8_PCK_HELP3_P, user=user_cprt_plane, speeds=2, accels=2, cpl=0} )
          setGripper(0,50,100)
          Move_( {pose=MOVE_STN15_8_PCK_SLD_HELP_P, user=user_cprt_plane, speeds=2, accels=2, cpl=0} )
          Move_( {pose=MOVE_STN15_8_PCK_HELP4_P, user=user_cprt_plane, speeds= 10, accels=10} )
          Go_( {pose=MOVE_STN15_STN8_STN15_BRIDGE_P, user=user_cprt_plane,speed=10, accel=10, sync=1} )
          Go_( {pose=MOVE_STN15_8_HOME_P, user=user_base,speed=10, accel=10, sync=1} )
          Go_( {pose=MOVE_STN15_8_PLC_HELP2_P, user=user_base,speed=10, accel=10, sync=1} )
          -- Move_( {pose=MOVE_STN15_8_PLC_HELP2_P, user=user_base,speeds=10, accels=10, sync=1} )
          Sleep(2000)
          Move_( {pose=MOVE_STN15_8_PLC_HELP3_P, user=user_base, speeds=2, accels=2, cpl=0} )
          Move_( {pose=MOVE_STN15_8_PLC_P, user=user_base, speeds=2, accels=2, cpl=0} )
          setGripper(100,100,100)
          Move_( {pose=MOVE_STN15_8_PLC_HELP4_P, user=user_base, speeds=2, accels=2, cpl=0} )
          Go_( {pose=MOVE_STN15_8_PLC_HELP5_P, user=user_base} )
          Go_( {pose=MOVE_STN15_8_HOME_P, user=user_base} )
          Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
          setGripper(0,50,100)
        end
        reset_jobs()
        --[[Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,accel=50,sync=1} )
        interfaceOut[5] = AXIS_HOME_POS_COBAS_BASKET_15
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        Go_( {pose=MOVE_STN15_HOME_P, user=user_cprt_plane, accel=50} )
        setGripper(100,100,100)
        Go_( {pose=MOVE_STN15_BSKT_HELP_1_P, user=user_cprt_plane} )
        Go_( {pose=MOVE_STN15_PCK_BSKT_P, user=user_cprt_plane} )
        setGripper(0,50,10)
        Move_( {pose=MOVE_STN15_PCK_PLC_HELP_P, user=user_cprt_plane, speeds= 50, accels=50} )
        ---Go_( {pose=MOVE_STN16_HOME_P, user=user_cprt_plane} )
        Go_( {pose=MOVE_DRIVE_STN_15_16_P, user=user_cam_1} )
        interfaceOut[5] = AXIS_HOME_POS_COBAS_PURE 
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        Go_( {pose=MOVE_STN8_PLC_BSKT_HELP_1_P, user=user_base, accel=50, sync=0} )
        Go_( {pose=MOVE_STN8_PLC_BSKT_P, user=user_base, accel=50, sync=0} )
        setGripper(100,100,100)
        Go_( {pose=MOVE_STN8_PLC_LEAVE_1_P, user=user_base} )
        Go_( {pose=MOVE_STN8_PLC_LEAVE_2_P, user=user_base} )
        Go_( {pose=MOVE_DRIVE_STN_15_16_P, user=user_cam_1} ) 
        setGripper(0,50,100)
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,accel=50,sync=0} )
        reset_jobs()]]
        
      elseif(srcJob == 161) then   --// Pick Basket from Cobas Pure Rack 2
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,sync=1} )
        interfaceOut[5] = AXIS_HOME_POS_COBAS_PURE
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        setGripper(100,100,100)
        Go_( {pose=MOVE_STN16_HOME_P, user=user_cprt_plane, sync=1} )
        Move_( {pose=MOVE_STN16_BSKT_HELP_1_P, user=user_cprt_plane, sync=1} )
        setGripper(50,100,100)
        Move_( {pose=MOVE_STN16_PCK_BSKT_P, user=user_cprt_plane, speeds=10, accels=10, cpl=0} )
        setGripper(0,50,100)
        Move_( {pose=MOVE_STN16_SLD_HELP_P, user=user_cprt_plane, speeds=2, accels=2, cpl=0} )
        Move_( {pose=MOVE_STN16_PCK_PLC_HELP_P, user=user_cprt_plane, speeds= 10, accels=10} )
        Go_( {pose=MOVE_STN8_BSKT_HOME, user=user_base,speed=10, accel=10, sync=1} )
        --Go_( {pose=MOVE_STN16_STN8_BSKT_HLP_1, user=user_base,speed=10, accel=10, sync=1} )
        Go_( {pose=MOVE_STN16_STN8_BSKT_HLP_2, user=user_base,speed=10, accel=10, sync=1} )
        Sleep(2000)
        --Move_( {pose=MOVE_STN16_STN8_BSKT_HLP_3, user=user_base, speeds=2, accels=2, cpl=0} )
        Move_( {pose=MOVE_STN16_STN8_BSKT_HLP_4, user=user_base, speeds=2, accels=2, cpl=0} )
        Move_( {pose=MOVE_STN16_STN8_BSKT_PLACE, user=user_base, speeds=2, accels=2, cpl=0} )
        setGripper(100,100,100)
        Move_( {pose=MOVE_STN16_STN8_BSKT_PLACE_BACK, user=user_base, speeds=2, accels=2, cpl=0} )
        Move_( {pose=MOVE_STN16_STN8_BSKT_PLACE_BACK_UP, user=user_base, speeds=20, accels=20, cpl=100} )
        Go_( {pose=MOVE_STN8_BSKT_HOME, user=user_base} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        setGripper(0,50,100)
        reset_jobs()
      elseif(srcJob == 171) then   --// Pick Rack  from Cobas Pure Basket Holder 1 
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1, sync=1} )
        interfaceOut[5] = AXIS_HOME_POS_COBAS_PURE_RCK_1 
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        local generic = interfaceIn[18]
        local rckIndx = generic
        setGripper(60,100,100)
        Go_( {pose=MOVE_STN17_HELP_P, user=user_cprt_plane,sync=0} )
        Go_( {pose=coordinateArrSrcDest[1], user=user_cprt_plane, sync=1} )
        if ( rckIndx == 1  or rckIndx == 11 or rckIndx == 21 or rckIndx == 31) then 
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_x({coordinate=updatedPos.coordinate},-25)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} ) 
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_z({coordinate=updatedPos.coordinate},-159)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} ) 
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_x({coordinate=updatedPos.coordinate},5)
          Move_( {pose=coordinateArr, user=user_cprt_plane, speeds=1, accels=1, cpl=0, sync=1} )
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_x({coordinate=updatedPos.coordinate},-5)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} )
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_z({coordinate=updatedPos.coordinate},159)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} ) 
        else
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_x({coordinate=updatedPos.coordinate},-45)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} ) 
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_z({coordinate=updatedPos.coordinate},-159)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} ) 
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_x({coordinate=updatedPos.coordinate},25)
          Move_( {pose=coordinateArr, user=user_cprt_plane, speeds=1, accels=1, cpl=0, sync=1} )
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_x({coordinate=updatedPos.coordinate},-25)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} )
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_z({coordinate=updatedPos.coordinate},159)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} ) 
        end
        Go_( {pose=coordinateArrSrcDest[1], user=user_cprt_plane} )        
        setGripper(80,100,100)
        coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn17_pck_rck_z_val)
        Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, speeds=10, accels=3, sync=1} )   --// Pick rack in station17
        setGripper(0,10,100)
        --Sleep(1000)
        Move_( {pose=MOVE_STN17_RCK_SLD_OUT_P, user=user_cprt_plane, cpl=0, speeds=2, accels=1, sync=1} )
        setGripper(35,100,100)
        setGripper(0,10,100)
        --Sleep(1000)
        Move_( {pose=MOVE_STN17_RCK_SLD_OUT_HELP_P, user=user_cprt_plane, cpl=0} )
        if ( (rckIndx >= 1  and rckIndx <= 10) or (rckIndx >= 21 and rckIndx <= 30) ) then 
          interfaceOut[5] = 0
        elseif((rckIndx >= 11  and rckIndx <= 20) or (rckIndx >= 31 and rckIndx <= 40)) then 
          Go_( {pose=MOVE_STN17_HELP_P, user=user_cprt_plane, sync=1} )
          interfaceOut[5] = AXIS_HOME_POS_COBAS_PURE_RCK_2
          statusACK = TCP_snd_rcv()
          interfaceOut[5] = 0
        else
          print("Some Error occured while passing index of stn2 ")
          Pause()
        end
        Go_( {pose=coordinateArrSrcDest[2], user=user_stn2_plane} )
        coordinateArr = addCoordinatePos_z(coordinateArrSrcDest[2],-stn2_rck_diff_plc_z_val)
        Move_( {pose=coordinateArr, user=user_stn2_plane, cpl=0, speeds=2, accels=1, sync=1} )   --// Place rack in station 2
        setGripper(100,100,100)
        Move_( {pose=coordinateArrSrcDest[2], user=user_stn2_plane, cpl=100, sync=0} )        
        Go_( {pose=MOVE_STN17_RCK_SLD_OUT_HELP_P, user=user_cprt_plane,cp=100,sync=0} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1, sync=1} )
        setGripper(0,100,100)
        reset_jobs()
      elseif(srcJob == 181) then   --// Pick Rack  from Cobas Pure Basket Holder 2 
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1, sync=1} )
        interfaceOut[5] = AXIS_HOME_POS_COBAS_PURE_RCK_2 
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        local generic = interfaceIn[18]
        local rckIndx = generic
        setGripper(60,100,100)
        Go_( {pose=MOVE_STN18_HELP_P, user=user_cprt_plane,sync=0} )
        Go_( {pose=coordinateArrSrcDest[1], user=user_cprt_plane, sync=1} )
        if ( rckIndx == 1  or rckIndx == 11 or rckIndx == 21 or rckIndx == 31) then 
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_x({coordinate=updatedPos.coordinate},25)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} ) 
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_z({coordinate=updatedPos.coordinate},-159)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} ) 
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_x({coordinate=updatedPos.coordinate},-5)
          Move_( {pose=coordinateArr, user=user_cprt_plane, speeds=1, accels=1, cpl=0, sync=1} )
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_x({coordinate=updatedPos.coordinate},5)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} )
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_z({coordinate=updatedPos.coordinate},159)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} ) 
        else
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_x({coordinate=updatedPos.coordinate},45)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} ) 
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_z({coordinate=updatedPos.coordinate},-159)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} ) 
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_x({coordinate=updatedPos.coordinate},-25)
          Move_( {pose=coordinateArr, user=user_cprt_plane, speeds=1, accels=1, cpl=0, sync=1} )
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_x({coordinate=updatedPos.coordinate},25)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} )
          local updatedPos = GetPose()
          coordinateArr = addCoordinatePos_z({coordinate=updatedPos.coordinate},159)
          Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, sync=1} ) 
        end
        Go_( {pose=coordinateArrSrcDest[1], user=user_cprt_plane} )        
        setGripper(80,100,100)
        coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn18_pck_rck_z_val)
        Move_( {pose=coordinateArr, user=user_cprt_plane, cpl=0, speeds=10, accels=3, sync=1} )   --// Pick rack in station18
        setGripper(0,10,100)
        --Sleep(1000)
        Move_( {pose=MOVE_STN18_RCK_SLD_OUT_P, user=user_cprt_plane, cpl=0, speeds=2, accels=1, sync=1} )
        setGripper(35,100,100)
        setGripper(0,10,100)
        --Sleep(1000)
        Move_( {pose=MOVE_STN18_RCK_SLD_OUT_HELP_P, user=user_cprt_plane, cpl=0} )
        if ( (rckIndx >= 1  and rckIndx <= 10) or (rckIndx >= 21 and rckIndx <= 30) ) then
          Go_( {pose=MOVE_STN18_HELP_P, user=user_cprt_plane, sync=1} )
          interfaceOut[5] = AXIS_HOME_POS_COBAS_PURE_RCK_1
          statusACK = TCP_snd_rcv()
          interfaceOut[5] = 0
        elseif((rckIndx >= 11  and rckIndx <= 20) or (rckIndx >= 31 and rckIndx <= 40)) then 
          interfaceOut[5] = 0
        else
          print("Some Error occured while passing index of stn2 ")
          Pause()
        end
        Go_( {pose=coordinateArrSrcDest[2], user=user_stn2_plane} )
        coordinateArr = addCoordinatePos_z(coordinateArrSrcDest[2],-stn2_rck_diff_plc_z_val)
        Move_( {pose=coordinateArr, user=user_stn2_plane, cpl=0, speeds=2, accels=1, sync=1} )   --// Place rack in station 2
        setGripper(100,100,100)
        Move_( {pose=coordinateArrSrcDest[2], user=user_stn2_plane, cpl=100, sync=0} )        
        Go_( {pose=MOVE_STN18_RCK_SLD_OUT_HELP_P, user=user_cprt_plane,cp=100,sync=0} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1, sync=1} )
        setGripper(0,100,100)
        --[[Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,accel=50,sync=0} )
        Go_( {pose=MOVE_STN18_PCK_RCK_HELP_P, user=user_base,accel=50,sync=0} )
        setGripper(50,100,100)
        Go_( {pose=MOVE_STN18_PCK_RCK_P, user=user_base,accel=50,sync=0} )
        setGripper(0,50,100)
        Go_( {pose=MOVE_STN18_PCK_RCK_HELP_P, user=user_base,accel=50,sync=0} )
        Go_( {pose=MOVE_STN2_HOME_P, user=user_stn2_plane,accel=50,sync=0} )
        Go_( {pose=MOVE_STN2_CPR2_HELP_P, user=user_stn2_plane,accel=50,sync=0} )
        Go_( {pose=coordinateArrSrcDest[2], user=user_stn2_plane, accel=10, sync=0} )   --// Src Pose
        coordinateArr = setCoordinateDiffPos_z(coordinateArrSrcDest[2],stn2_rck_diff_plc_z_val)
        Move_( {pose=coordinateArr, user=user_stn2_plane, cp=0, speeds=10, accels=5} )
        setGripper(50,100,100)
        Move_( {pose=coordinateArrSrcDest[2], user=user_stn2_plane, cp=0, speeds=10, accels=5} )
        setGripper(0,50,100)
        Go_( {pose=MOVE_STN2_CPR2_HELP_P, user=user_stn2_plane,accel=50,sync=0} )
        Go_( {pose=MOVE_STN2_HOME_P, user=user_stn2_plane,accel=50,sync=0} )]]
        reset_jobs()
      elseif(srcJob == 172) then   --// Pick Tube  from Cobas Pure Basket Holder 1 
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,accel=50,sync=1} )
        interfaceOut[5] = AXIS_HOME_POS_BCS
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        Go_( {pose=MOVE_STN17_HELP_P, user=user_cprt_plane, sync=1} )
        Go_( {pose=coordinateArrSrcDest[1], user=user_cprt_plane} )   --// Src Pose
        setGripper(40,50,50)
        coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn17_z_val)
        Move_( {pose=coordinateArr, user=user_cprt_plane, cp=0, speeds=10, accels=5} )
        setGripper(0,50,20)
        -- local gripperStatus = RiqGetStatus()
        if (gripperStatus == 2) then
          tubeStatus = 1
        else
          tubeStatus = 0
        end
        Move_( {pose=coordinateArrSrcDest[1], user=user_cprt_plane, cp=0, speeds=10, accels=5, sync=0} )
        Go_( {pose=MOVE_STN17_HELP_P, user=user_cprt_plane,speed=30, accel=30, sync=0} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        setLockStatus(6) --// Set the Lock Status to 6
        statusACK = TCP_snd_rcv()
        if(statusACK == true) then
          srcJob = interfaceIn[4]
          destJob = interfaceIn[5]
          print("srcJob:",srcJob)
          print("destJob:",destJob)
          if(srcJob == 112) then   --// Place in Archive
            local generic = interfaceIn[18]
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
            local rackNum = generic
            if (rackNum == 1 ) then  --// Fridge 1
              interfaceOut[5] = AXIS_HOME_POS_CAM_1		
              statusACK = TCP_snd_rcv()
              interfaceOut[5] = 0
              if( tubeType == 1 )then
                  z_small_big_val = stn11_rck_1_small_z_val
              elseif( tubeType == 2 ) then
                z_small_big_val = stn11_rck_1_big_z_val
              end
              Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
              Go_( {pose=MOVE_STN11_D1_HOME_P, user=user_arch_d_1,sync=0} ) 
              Go_( {pose=coordinateArrSrcDest[2], user=user_arch_d_1, sync=0} )   --// Src Pose
              coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],z_small_big_val)
              Move_( {pose=coordinateArr, user=user_arch_d_1, cp=0, speeds=10, accels=5} )
              setGripper(50,50,50) --// open the Gripper
              Move_( {pose=coordinateArrSrcDest[2], user=user_arch_d_1,cpl=100, sync=0} )   --// Src Pose
              --setGripper(0,50,50) --// Close the Gripper
              Go_( {pose=MOVE_STN11_D1_HOME_P, user=user_arch_d_1, sync=0} ) 
              Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
            elseif(rackNum == 2 ) then --// Fridge 2
              if( tubeType == 1 )then
                z_small_big_val = stn11_rck_2_small_z_val
              elseif( tubeType == 2 ) then
                z_small_big_val = stn11_rck_2_big_z_val
              end
              Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
              Go_( {pose=MOVE_STN11_D2_PLC_TUBE_HELP_P, user=user_arch_d_2, sync=0} ) 
              Go_( {pose=coordinateArrSrcDest[2], user=user_arch_d_2, sync=0} )   --// Src Pose
              coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],z_small_big_val)
              Move_( {pose=coordinateArr, user=user_arch_d_2, cp=0, speeds=10, accels=5} )
              setGripper(50,50,50) --// open the Gripper
              Move_( {pose=coordinateArrSrcDest[2], user=user_arch_d_2,cpl=100,sync=0} )   --// Src Pose
              Go_( {pose=MOVE_STN11_D2_PLC_TUBE_HELP_P, user=user_arch_d_2, sync=0} ) 
              Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
            else
              print("Unexpected error in Placing Archive")
              Pause()
            end
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
            setGripper(0,50,50) --// Close the Gripper
          end
        end
        reset_jobs()
      elseif(srcJob == 182) then   --// Pick Tube  from Cobas Pure Basket Holder 2 
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,sync=1} )
        interfaceOut[5] = AXIS_HOME_POS_BCS ----- axis 7 BCS
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        Go_( {pose=MOVE_STN18_HELP_P, user=user_cprt_plane} )
        Go_( {pose=coordinateArrSrcDest[1], user=user_cprt_plane} )   --// Src Pose
        setGripper(40,50,50)
        coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn18_z_val)
        Move_( {pose=coordinateArr, user=user_cprt_plane, speeds=5, accels=2, sync=1} )
        setGripper(0,50,20)
        -- local gripperStatus = RiqGetStatus()
        if (gripperStatus == 2) then
          tubeStatus = 1
        else
          tubeStatus = 0
        end
        Move_( {pose=coordinateArrSrcDest[1], user=user_cprt_plane, speeds=3, accels=2} )
        Go_( {pose=MOVE_STN18_HELP_P, user=user_cprt_plane,accel=50,sync=1} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,accel=50,sync=1} )
        setLockStatus(7) --// Set the Lock Status to 7
        statusACK = TCP_snd_rcv()
        if(statusACK == true) then
          srcJob = interfaceIn[4]
          destJob = interfaceIn[5]
          print("srcJob:",srcJob)
          print("destJob:",destJob)
          if(srcJob == 112) then   --// Place in 
            local generic = interfaceIn[18]
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
            local rackNum = generic
            if (rackNum == 1 ) then  --// Fridge 1
              interfaceOut[5] = AXIS_HOME_POS_CAM_1	
              statusACK = TCP_snd_rcv()
              interfaceOut[5] = 0
              if( tubeType == 1 )then
                z_small_big_val = stn11_rck_1_small_z_val
              elseif( tubeType == 2 ) then
                z_small_big_val = stn11_rck_1_big_z_val
              end
              Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
              Go_( {pose=MOVE_STN11_D1_HOME_P, user=user_arch_d_1,sync=0} ) 
              Go_( {pose=coordinateArrSrcDest[2], user=user_arch_d_1,sync=0} )   --// Src Pose
              coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],z_small_big_val)
              Move_( {pose=coordinateArr, user=user_arch_d_1, cp=0, speeds=10, accels=5} )
              setGripper(50,50,50) --// open the Gripper
              Move_( {pose=coordinateArrSrcDest[2], user=user_arch_d_1,cpl=100,sync=0} )   --// Src Pose
              --setGripper(0,50,50) --// Close the Gripper
              Go_( {pose=MOVE_STN11_D1_HOME_P, user=user_arch_d_1, sync=0} ) 
              Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
            elseif(rackNum == 2 ) then --// Fridge 2
              if( tubeType == 1 )then
                z_small_big_val = stn11_rck_2_small_z_val
              elseif( tubeType == 2 ) then
                z_small_big_val = stn11_rck_2_big_z_val
              end
              Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
              Go_( {pose=MOVE_STN11_D2_PLC_TUBE_HELP_P, user=user_arch_d_2, sync=0} ) 
              Go_( {pose=coordinateArrSrcDest[2], user=user_arch_d_2,sync=0} )   --// Src Pose
              coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],z_small_big_val)
              Move_( {pose=coordinateArr, user=user_arch_d_2, cp=0, speeds=10, accels=5} )
              setGripper(50,50,50) --// open the Gripper
              Move_( {pose=coordinateArrSrcDest[2], user=user_arch_d_2,cpl=100,sync=0} )   --// Src Pose
              Go_( {pose=MOVE_STN11_D2_PLC_TUBE_HELP_P, user=user_arch_d_2, sync=0} ) 
              Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
            else
              print("Unexpected error in Placing Archive")
              Pause()
            end
            Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
            setGripper(0,50,50) --// Close the Gripper
          end
        end
        reset_jobs()
      elseif(srcJob == 153) then   --// Slide Racks from Basket 1 
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        interfaceOut[5] = AXIS_HOME_POS_BCS ----- axis 7 cobas pure rack1
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        Go_( {pose=MOVE_STN15_PCK_PLC_BSKT_HELP_P, user=user_cprt_plane} )
        Go_( {pose=MOVE_STN17_SLD_HELP_P, user=user_cprt_plane} )
        setGripper(50,50,50) --// open the Gripper
        Move_( {pose=MOVE_STN17_SLD_START_P, user=user_cprt_plane,speeds=5, accels=2} )
        Move_( {pose=MOVE_STN17_SLD_MIDDLE_HELP_P,user=user_cprt_plane,speeds=10, accels=10} )
        Move_( {pose=MOVE_STN17_SLD_END_P, user=user_cprt_plane,speeds=2, accels=2} )
        Go_( {pose=MOVE_STN17_SLD_HELP_P, user=user_cprt_plane} )
        Go_( {pose=MOVE_STN15_PCK_PLC_BSKT_HELP_P, user=user_cprt_plane} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        reset_jobs()
      elseif(srcJob == 163) then   --// Slide Racks from Basket 2 
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        interfaceOut[5] = AXIS_HOME_POS_BCS ----- axis 7 cobas pure rack 2
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        Go_( {pose=MOVE_STN16_PCK_PLC_BSKT_HELP_P, user=user_cprt_plane} )
        Go_( {pose=MOVE_STN18_SLD_HELP_P, user=user_cprt_plane} )
        setGripper(100,50,50) --// open the Gripper
        --Move_( {pose=MOVE_STN18_SLD_APP_P, user=user_cprt_plane,speeds=5, accels=2} )
        Move_( {pose=MOVE_STN18_SLD_START_P, user=user_cprt_plane,speeds=5, accels=2} )
        Move_( {pose=MOVE_STN18_SLD_MIDDLE_HELP_P, user=user_cprt_plane,speeds=10, accels=10} )
        Move_( {pose=MOVE_STN18_SLD_END_P, user=user_cprt_plane,speeds=2, accel=2} )
        --Move_( {pose=MOVE_STN18_SLD_APP_P, user=user_cprt_plane,speeds=5, accels=2} )
        Go_( {pose=MOVE_STN18_SLD_HELP_P, user=user_cprt_plane} )
        Go_( {pose=MOVE_STN16_PCK_PLC_BSKT_HELP_P, user=user_cprt_plane} )
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
        setGripper(0,50,50) --// Close the Gripper
        reset_jobs()
      elseif(srcJob == 113) then   --// Close door of Archive 
        setGripper(0,50,50) --// Close the Gripper
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
        local fridgeNum = coordinateArrSrcDest[2].coordinate[1]
        if ( fridgeNum == 1 ) then
          interfaceOut[5] = AXIS_HOME_POS_CAM_1 ----- axis 7 cam1 home
          statusACK = TCP_snd_rcv()
          interfaceOut[5] = 0
          Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
          Go_( {pose=MOVE_STN11_D1_HOME_P, user=user_arch_d_1,sync=0} ) 
          Go_( {pose=MOVE_STN11_D1_CLOSE_1_P, user=user_arch_d_1,sync=0} ) 
          Move_( {pose=MOVE_STN11_D1_CLOSE_2_P, user=user_arch_d_1,speeds=3,accels=3} ) 
          Sleep(1000)
          Go_( {pose=MOVE_STN11_D1_HELP_P, user=user_arch_d_1,sync=0} ) 
          Go_( {pose=MOVE_STN11_D1_HOME_P, user=user_arch_d_1,sync=0} ) 
        elseif( fridgeNum == 2 ) then
          interfaceOut[5] = AXIS_HOME_POS_FRIDGE2 ----- axis 7 fridge 2
          statusACK = TCP_snd_rcv()
          interfaceOut[5] = 0
          Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
          Go_( {pose=MOVE_STN11_D2_HOME_P, user=user_arch_d_2,sync=0} ) 
          Go_( {pose=MOVE_STN11_D2_CLOSE_1_P, user=user_arch_d_2,sync=0} ) 
          Move_( {pose=MOVE_STN11_D2_CLOSE_2_P, user=user_arch_d_2,speeds=3,accels=3} ) 
          Sleep(1000)
          Go_( {pose=MOVE_STN11_D2_HELP_P, user=user_arch_d_2,sync=0} ) 
          Go_( {pose=MOVE_STN11_D2_HOME_P, user=user_arch_d_2,sync=0} ) 
        else
          print("Unexpected error in Fridge Door Closing")
          Pause()
        end
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
        DOExecute(3, OFF)  --// Reset Archive and Reset Fehler enabled in GUI
        reset_jobs()
      elseif(srcJob == 114) then   --// Open door of Archive
        DOExecute(3, ON)  --// Reset Archive and Reset Fehler disabled in GUI
        setGripper(0,50,50) --// Close the Gripper
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
        local fridgeNum = coordinateArrSrcDest[2].coordinate[1]
        if ( fridgeNum == 1 ) then
          interfaceOut[5] = AXIS_HOME_POS_CAM_1 ----- axis 7 cam1 home
          statusACK = TCP_snd_rcv()
          interfaceOut[5] = 0
          Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
          Go_( {pose=MOVE_STN11_D1_HOME_P, user=user_arch_d_1,sync=0} ) 
          Go_( {pose=MOVE_STN11_D1_CLOSE_1_P, user=user_arch_d_1,sync=0} ) 
          Move_( {pose=MOVE_STN11_D1_CLOSE_2_P, user=user_arch_d_1,speeds=3,accels=3} ) 
          Sleep(1000)
          Go_( {pose=MOVE_STN11_D1_HELP_P, user=user_arch_d_1,sync=0} ) 
          setGripper(70,50,50) --// open the Gripper
          Move_( {pose=MOVE_STN11_D1_APPR_1_P, user=user_arch_d_1} ) 
          setGripper(0,50,50) --// Close the Gripper
          Move_( {pose=MOVE_STN11_D1_APPR_2_P, user=user_arch_d_1,speeds=10,accels=5} ) 
          Move_( {pose=MOVE_STN11_D1_PULL_P, user=user_arch_d_1,speeds=10,accels=5} ) 
          Move_( {pose=MOVE_STN11_D1_LEAVE_1_P, user=user_arch_d_1,speeds=10,accels=5} ) 
          setGripper(70,50,50) --// open the Gripper
          setGripper(0,50,50) --// Close the Gripper
          setGripper(70,50,50) --// open the Gripper
          Go_( {pose=MOVE_STN11_D1_LEAVE_2_P, user=user_arch_d_1,sync=0} ) 
          Go_( {pose=MOVE_STN11_D1_HOME_P, user=user_arch_d_1,sync=0} ) 
          setGripper(0,50,50) --// Close the Gripper
          Go_( {pose=MOVE_STN11_D1_PULL_HELP_P, user=user_arch_d_1,sync=0} )  
          Go_( {pose=MOVE_STN11_D1_PULL_HELP1_P, user=user_arch_d_1,sync=0} ) 
          Move_( {pose=MOVE_STN11_D1_PULL_HELP2_P, user=user_arch_d_1,speeds=10,accels=5} )
          Go_( {pose=MOVE_STN11_D1_PULL_HELP1_P, user=user_arch_d_1,sync=0} ) 
          Go_( {pose=MOVE_STN11_D1_PULL_HELP_P, user=user_arch_d_1,sync=0} )
          Go_( {pose=MOVE_STN11_D1_HOME_P, user=user_arch_d_1,sync=0} )
        elseif( fridgeNum == 2 ) then
          --Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1,accel=50} ) 
          interfaceOut[5] = AXIS_HOME_POS_FRIDGE2 ----- axis 7 fridge 2
          statusACK = TCP_snd_rcv()
          interfaceOut[5] = 0
          Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} )
          Go_( {pose=MOVE_STN11_D2_HOME_P, user=user_arch_d_2,sync=0} ) 
          Go_( {pose=MOVE_STN11_D2_CLOSE_1_P, user=user_arch_d_2,sync=0} ) 
          Move_( {pose=MOVE_STN11_D2_CLOSE_2_P, user=user_arch_d_2,speeds=3,accels=3} ) 
          Sleep(1000)
          Go_( {pose=MOVE_STN11_D2_HELP_P, user=user_arch_d_2,sync=0} ) 
          setGripper(70,50,50) --// open the Gripper
          Move_( {pose=MOVE_STN11_D2_APPR_1_P, user=user_arch_d_2} ) 
          setGripper(0,50,50) --// Close the Gripper
          Move_( {pose=MOVE_STN11_D2_APPR_2_P, user=user_arch_d_2,speeds=10,accels=5} ) 
          Move_( {pose=MOVE_STN11_D2_PULL_P, user=user_arch_d_2,speeds=10,accels=5} ) 
          Move_( {pose=MOVE_STN11_D2_LEAVE_1_P, user=user_arch_d_2,speeds=10,accels=5} ) 
          setGripper(70,50,50) --// open the Gripper
          setGripper(0,50,50) --// Close the Gripper
          setGripper(70,50,50) --// open the Gripper
          Go_( {pose=MOVE_STN11_D2_LEAVE_2_P, user=user_arch_d_2,sync=0} ) 
          Go_( {pose=MOVE_STN11_D2_HOME_P, user=user_arch_d_2,sync=0} ) 
          setGripper(0,50,50) --// Close the Gripper
          Go_( {pose=MOVE_STN11_D2_PULL_HELP_P, user=user_arch_d_2,sync=0} )  
          Go_( {pose=MOVE_STN11_D2_PULL_HELP1_P, user=user_arch_d_2,sync=0} ) 
          Move_( {pose=MOVE_STN11_D2_PULL_HELP2_P, user=user_arch_d_2,speeds=10,accels=5} )
          Go_( {pose=MOVE_STN11_D2_PULL_HELP1_P, user=user_arch_d_2,sync=0} ) 
          Go_( {pose=MOVE_STN11_D2_PULL_HELP_P, user=user_arch_d_2,sync=0} )
          Go_( {pose=MOVE_STN11_D2_HOME_P, user=user_arch_d_2,sync=0} )
        else
          print("Unexpected error in Fridge Door Opening")
          Pause()
        end
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
        reset_jobs()
      elseif(srcJob == 117) then   --// All tubes Filled in Archive
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
        interfaceOut[5] = AXIS_HOME_POS_CAM_1  ----- axis 7 cam 1
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        print("All tubes Filled in Archive")
        DOExecute(14, ON)
        Go_( {pose=MOVE_ARCHIVE_FILLED_P, user=user_base} ) 
        reset_jobs()
        Pause()
      elseif(srcJob == 103) then   --// All tubes Filled in Fehler
        Go_( {pose=MOVE_DRIVE_1_P, user=user_cam_1} ) 
        interfaceOut[5] = AXIS_HOME_POS_CAM_1  ----- axis 7 cam 1
        statusACK = TCP_snd_rcv()
        interfaceOut[5] = 0
        print("All tubes Filled in Fehler")
        DOExecute(16, ON)
        Go_( {pose=MOVE_ARCHIVE_FILLED_P, user=user_base} ) 
        reset_jobs()
        Pause()
      end
    end
  end 
end


