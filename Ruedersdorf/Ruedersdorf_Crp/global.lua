-- This file is only used to define variables and sub functions.
-- Global variable module is only used to define global variables and module functions. The motion command cannot be called here.
-- Version: Lua 5.3.5
-- 7th Axis Positions -----------------------------------------------------
-- Pos 0 mm - (Cam1,Cam2,Centrifuge Tubes pick/place,decapping,stn14 rack/tube - pick/place, stn7 unloading,
-- stn11 fridge door open/close,fridge tube pick/place, stn9 tube/rack - pick/place)
--  Pos 350 mm -(stn5/6 rack loading/unloading)
-- Pos 1550 mm - (stn15 sliding - basket pick/place,stn2 (1-12 and 26-37) rack pick/place)
-- Pos 1600 mm -(stn7 loading)
-- Pos 1750 mm - (stn3 tube pick/place - rack load/unload,stn17-18 plane,stn17 tube/rack picking, stn18 tube/rack picking)  
-- Pos 1950 mm - (stn16 sliding - basket pick/place,stn2 (13-25 and 38-50) rack pick/place)
-- Pos 2600 mm - (stn8 rack pick/place - basket pick/place )

---// Global Variables /////////----------------------------------------------
IP = "192.168.0.63"
PORT = 9095
isServer = false
speedhigh = 50   
test = false
ping = false
err, socket = nil,nil
coordinateArrSrcDest = {{coordinate={0,0,0,0,0,0}},{coordinate={0,0,0,0,0,0}}}
coordinateArrSrcDestBuf = {{coordinate={0,0,0,0,0,0}},{coordinate={0,0,0,0,0,0}}}
interfaceInBuf = {}
interfaceIn = {0,0,0,0,0,coordinateArrSrcDest,{0,0,0,0,0,0}}  --Recv// {stateOfhandshake=0,tubeType=0,status=0,srcJob=0,destJob=0,srcPos={0,0,0,0,0,0},desPos={0,0,0,0,0,0}, generic={0,0,0,0,0,0}}
interfaceOut = {0,0,0,0,0,0,0,0} --Send// {newConnection=0,stateOfhandshake=0,lockID=0,tubeStatus=0,macID=0,numPos=0,ping=1,Pose1={0,0,0,0,0,0},Pose2={0,0,0,0,0,0}, ..... }
interfaceOutSnd = ""

tubeType = 0
tubeStatus = 0 
tubeAngle  = 0
---/// station 5 racks array
stn5_batch1_poses = {P63, P64, P66, P65}
stn5_batch2_poses = {P67, P68, P70, P69}

---/// Decap start and end

---///All stations z values

stn1_small_tube_z_val = -152.3929 ----// small Tube  pick value at camera 1
stn1_Big_tube_z_val  = -126.8607     -----// big Tube pick value at camera 1 

stn2_rck_diff_pick_z_val = 120   -----//  pick rack value at station2
stn2_rck_diff_plc_z_val = 123   -----//  place rack value at station2

--stn3_rack_z_val = 98.8728  -----// Rack load/ z value
--stn3_rack_unload_y_val = 70  -----// Rack unload/ z value
stn3_rack_load_in_y_val = 153   -----// Rack load y value 
--stn3_rack_unload_in_y_val = 151.4063   -----// Rack load y value old
stn3_rack_unload_in_y_val = 164.8189 -- 163.5288   -----// Rack load y value
--stn3_rack_unload_out_y_val = -7.4323  -----// Rack load y value old
stn3_rack_unload_out_y_val = -2.4691 -- 5.1265  -----// Rack load y value
stn3_tube_plc_z_val = -99.1383     -----// Tube place  value
stn3_tube_pck_z_val = -100.1383     -----// Tube pick  value
stn5_small_tube_pick_z_val = -119.532 -----// small Tube pick  value at centrifuge racks 
stn5_small_tube_plc_z_val = -118.532  -----// small Tube place  value at centrifuge racks  
stn5_Big_tube_pick_z_val =  -95.5320     -----// big Tube pick value  at centrifuge racks      
stn5_Big_tube_plc_z_val = -94.5320    -----// big Tube place value  at centrifuge racks      
stn5_rack_pick_z_val = -96.2       
stn5_rack_plc_val = -95.2

small_cw_z_val = -129.4848   -----// Small_Tube cw  value
big_cw_z_val = -105.1159     -----// Big_Tube cw  value



stn8_plc_rck_z_val = 93.326  -----//  place rack value in cobas pure machine

stn9_z_val = -79.7896  -----// Tube pick and place value in Beckman rack
stn9_rack_pck_z_val = -96.6264  -----// Beckman Rack pick and place value at camera 1 
stn9_rack_plc_z_val = -96.0264  -----// Beckman Rack pick and place value at camera 1 


stn10_small_tube_z_val = -129.1004      -----// Small Tube place value in parking fehler Pallete rack 
stn10_big_tube_z_val = -104.8588       -----// Big Tube  place value in parking fehler Pallete rack  

stn11_rck_1_small_z_val = -146.7655
stn11_rck_1_big_z_val = -146.7655
stn11_rck_2_small_z_val = -53.6791
stn11_rck_2_big_z_val = -53.6791




--stn14_plc_rck_p = -194.9     ----// Rack  place value
--stn14_pck_rck_p = -211.1904    -----//  Rack  pick value
stn14_small_z_val = -110.8944    -----// Small_Tube pick and place value
stn14_big_z_val = -84.9736   -----// Big_Tube pick and place value

stn15_bskt_z_val = -120.9994    -----//  pick and place basket value

decap_big_tube_z_val = -21.0952   -----// Tube pick and place value for Decapping
decap_small_tube_z_val = -45.6993   -----// Tube pick and place value for Decapping

stn17_z_val =  -87.8727          -----// Tube pick  value 
stn18_z_val =  -87.8727                       -----// Tube pick  value
---stn17_pck_big_tube_z_val = -140
---stn18_pck_big_tube_z_val = -138

stn17_pck_rck_z_val = -88.8
stn18_pck_rck_z_val = -88.8


--////  Initialization function  ////-----------------------------------------
function InitializePose(macID,numPos,poseArr) 
  local indxCntr = 1  
  local interfaceOutData = {}
  local loopCntr = (numPos * 6)
  local poseArrCntr = 1
  local poseCntr = 1
  interfaceOutData[1] = 0 --// new Connection
  interfaceOutData[2] = 0 --// state of Handshake
  interfaceOutData[3] = 1 --// lock ID
  interfaceOutData[4] = 0 --// tube status 
  interfaceOutData[5] = macID --// initilization ID  
  interfaceOutData[6] = numPos --// numPos
  interfaceOutData[7] = 0 --// ping
    for poseCntr = 1,#poseArr do
      local poseValCntr = 1
      local updateVarCnt = 8
      for indxCntr = (((poseCntr - 1) * 6) + updateVarCnt ),(((poseCntr) * 6) + (updateVarCnt) )  do
        interfaceOutData[indxCntr] = poseArr[poseCntr].coordinate[poseValCntr] --// Pose add
        poseValCntr = poseValCntr + 1
      end
    end
  return interfaceOutData
end

function reset_jobs()
  coordinateArrSrcDest = { {coordinate = {nil,nil,nil,nil,nil,nil}}, {coordinate = {nil,nil,nil,nil,nil,nil} } }
  interfaceIn = {0,0,0,0,0,coordinateArrSrcDest,{0,0,0,0,0,0}}  --Recv// {stateOfhandshake=0,tubeType=0,status=0,srcJob=0,destJob=0,srcPos={0,0,0,0,0,0},desPos={0,0,0,0,0,0},generic={0,0,0,0,0,0}}
  interfaceOut = {0,0,0,0,0,0,0,0}  --Send// {newConnection=0,stateOfhandshake=0,lockID=0,tubeStatus=0,macID=0,numPos=0,ping=1,Pose1={0,0,0,0,0,0},Pose2={0,0,0,0,0,0}, ..... }
end

function InitializeMachine(macID)                                  --// Init Val 1 for Camera 1 (macID =1,numPos =3,poseArr={P1,P2,P3})
  if(macID == 1) then
    interfaceOut = InitializePose(macID,3, {P1,P2,P3})          
  elseif(macID == 21) then                                           -- // Init Val 21 for Cobas Pure Racks (1-12) (macID =2,numPos =3,poseArr={P4,P5,P4})
    interfaceOut = InitializePose(macID,3, {P4,P5,P4}) 
  elseif(macID == 22) then                                           -- // Init Val 22 for Cobas Pure Rack(13-25) (macID =2,numPos =3,poseArr={P7,P8,P7})
    interfaceOut = InitializePose(macID,3, {P7,P8,P7})  
  elseif(macID == 23) then                                           -- // Init Val 23 for Cobas Pure Rack(26-37) (macID =2,numPos =3,poseArr={P6,P50,P6})
    interfaceOut = InitializePose(macID,3, {P6,P50,P6})  
  elseif(macID == 24) then                                           -- // Init Val 24 for Cobas Pure Rack(38-50) (macID =2,numPos =3,poseArr={P9,P51,P9})
    interfaceOut = InitializePose(macID,3, {P9,P51,P9})  
  elseif(macID == 31) then                                      -- // Init val 31 place tubes in BCS machine (macID =3,numPos =3,poseArr={P34,P35,P36})
    interfaceOut = InitializePose(macID,3, {P10,P11,P12}) 
  elseif(macID == 32) then                                     -- // Init Val 32 for racks in BCS machine (macID =3,numPos =3,poseArr={P28,P30,28})
    interfaceOut = InitializePose(macID,3, {P13,P14,P13})
  elseif(macID == 4) then
    interfaceOut[1] = 0                                         -- // new Connection
    interfaceOut[5] = macID                                     -- // initilization ID 
  elseif(macID == 5) then
    interfaceOut = InitializePose(macID,5, {P15,P16,P17,P18,P19})   -- // Init Val 6 for Cetrifuge tubes (macID =51,numPos =5,poseArr={P23,P27,P26,P24,P25})
  elseif(macID == 55) then
    interfaceOut = InitializePose(macID,4, {P97,P99,P98,P100})   -- // Init counter weights
  elseif(macID == 61) then
    interfaceOut[1] = 0                                         -- // new Connection
    interfaceOut[5] = macID 
  elseif(macID == 91) then
    interfaceOut = InitializePose(macID,3, {P24,P25,P26}) -- // Init Val 91 for Beckman tubes (macID =91,numPos =3,poseArr={P6,P7,P8})
  elseif(macID == 92) then
    interfaceOut = InitializePose(macID,3, {P27,P28,P27}) -- // Init Val 92 for Beckman Rack (macID =92,numPos =3,poseArr={P12,P13,P12})
  elseif(macID == 10) then
  interfaceOut = InitializePose(macID,3, {P29,P30,P31})  -- // Init Val 101 for Fehler Stand (macID =10,numPos =3,poseArr={P51,P52,P53})
  elseif(macID == 111) then
    interfaceOut = InitializePose(macID,3, {P32,P33,P34}) -- // Init Archiv Rack1  (macID,3,{P100,P101,P102})
  elseif(macID == 112) then
    interfaceOut = InitializePose(macID,3, {P35,P36,P37}) -- // Init Archiv Rack2  (macID,3,{P105,P106,P107}) 
  elseif(macID == 14) then
    interfaceOut = InitializePose(macID,3, {P168,P168,P169})    -- // Init cobas_pure_rack_tubes 
  elseif(macID == 17) then
    interfaceOut = InitializePose(macID,5, {P41,P42,P38,P39,P40}) --/Init Val 17 for Cobas Pure Filled Rack Holder_1 (macID =17,numPos =5,poseArr{P41,P42,P38,P39,P40})
  elseif(macID == 18) then
    interfaceOut = InitializePose(macID,5, {P48,P49,P43,P44,P45}) --//Init Val 18 for Cobas Pure Filled Rack Holder_2 (macID =18,numPos =5,poseArr{P48,P49,P43,P44,P45})
  end  
  statusACK = TCP_snd_rcv()
end
--////  End of Initialization function  ////-----------------------------------

--// Start of utility functions //---------------------
function setCoordinatePos_z(coordArr,z_val)
  local coordinateArr = {coordinate={coordArr.coordinate[1],coordArr.coordinate[2],
    z_val,coordArr.coordinate[4],coordArr.coordinate[5],coordArr.coordinate[6]}}
  return coordinateArr
end

function setCoordinateDiffPos_z(coordArr,z_val)
  local coordinateArr = {coordinate={coordArr.coordinate[1],coordArr.coordinate[2],
    coordArr.coordinate[3] - z_val,coordArr.coordinate[4],coordArr.coordinate[5],coordArr.coordinate[6]}}
  return coordinateArr
end

function setCoordinatePos_y(coordArr,y_val)
  local coordinateArr = {coordinate={coordArr.coordinate[1],y_val,coordArr.coordinate[3],
    coordArr.coordinate[4],coordArr.coordinate[5],coordArr.coordinate[6]}}
  return coordinateArr
end

function setCoordinatePos_x(coordArr,x_val)
  local coordinateArr = {coordinate={x_val,coordArr.coordinate[2],coordArr.coordinate[3],
    coordArr.coordinate[4],coordArr.coordinate[5],coordArr.coordinate[6]}}
  return coordinateArr
end



function addCoordinatePos_x(coordArr,x_val)
  local coordinateArr = {coordinate={coordArr.coordinate[1] + x_val,coordArr.coordinate[2],coordArr.coordinate[3],
    coordArr.coordinate[4],coordArr.coordinate[5],coordArr.coordinate[6]}}
  return coordinateArr
end

function addCoordinatePos_y(coordArr,y_val)
  local coordinateArr = {coordinate={coordArr.coordinate[1],coordArr.coordinate[2] + y_val,
    coordArr.coordinate[3],coordArr.coordinate[4],coordArr.coordinate[5],coordArr.coordinate[6]}}
  return coordinateArr
end

function addCoordinatePos_z(coordArr,z_val)
  local coordinateArr = {coordinate={coordArr.coordinate[1],coordArr.coordinate[2],
    coordArr.coordinate[3] + z_val,coordArr.coordinate[4],coordArr.coordinate[5],coordArr.coordinate[6]}}
  return coordinateArr
end

function addCoordinatePos_z_rz(coordArr,z_val, rz_val)
  local coordinateArr = {coordinate={coordArr.coordinate[1],coordArr.coordinate[2],
    coordArr.coordinate[3] + z_val,coordArr.coordinate[4],coordArr.coordinate[5],coordArr.coordinate[6] + rz_val}}
  return coordinateArr
end

function setBarcodeAngle(jointArr,jointAngle)
  local returnJointArr = {}
  --local offsetArr ={[6]={stn6_offset}}
  if(jointAngle <= 180 ) then  
    returnJointArr= {joint= {jointArr.joint[1],jointArr.joint[2],jointArr.joint[3],jointArr.joint[4],
                      jointArr.joint[5],jointArr.joint[6] + jointAngle }}
  else
    jointAngle = 360 - jointAngle
    returnJointArr= {joint= {jointArr.joint[1],jointArr.joint[2],jointArr.joint[3],jointArr.joint[4],
                                jointArr.joint[5],jointArr.joint[6] - jointAngle }}
  end
  return returnJointArr
end

function setLockStatus(lockID)
  interfaceOut[3] = lockID  --// Lock ID 
  interfaceOut[4] = tubeStatus  --// tubeStatus to 1
  interfaceOut[5] = 0  --// mac ID 
end

function resetLockStatus()
  interfaceOut[3] = 1  --// Lock ID to 1
  interfaceOut[4] = 0  --// tubeStatus to 0
  interfaceOut[5] = 0  --// mac ID 
end

function checkBarcode(param)  
  -- pass "before" if before centrifugation
  -- pass "after" if after centrifugation
  param = param or "before"
end

function convertToString(varToString) 
  msgSendStr = ''
  for key,value in ipairs(varToString) do 
    msgSendStr =  msgSendStr .. tostring(value) .. "," 
  end
  return msgSendStr
end

function TCP_snd_rcv()
  --interfaceOut[2] = 1   --// state of Handshake 
  local ackFlag_1 = false
  local ackFlag_2 = false
  local interfaceOutSnd = convertToString(interfaceOut)
  TCPWrite(socket,interfaceOutSnd) --interfaceOutSnd// Send back One
  Sleep(100)
  err, recvBuf = TCPRead(socket,0,"string")
  if (err == 0) then 
    local recvBuf_1 = recvBuf.buf    
    local indx = 1
    local recvBufCntr = 1
    local updateVarCnt = 5
    local totalBufSize = 18
    for recvBufCntr=1,totalBufSize do
      local indx = string.find(recvBuf_1,",")
      local sub = ""
      --print("recvBuf_1:",recvBuf_1)
      --print("indx:",indx)
      if (recvBufCntr == 1) then
        sub = string.sub(recvBuf_1,1,(indx - 1)) 
      else
        sub = string.sub(recvBuf_1,2,(indx - 1)) 
      end
      --print("sub:",sub)
      if (recvBufCntr > updateVarCnt and recvBufCntr <= (updateVarCnt + 6)) then
        --// getting the src pose coordinate
        coordinateArrSrcDestBuf[1].coordinate[recvBufCntr - updateVarCnt] = tonumber(sub) --// Src Pos 
      end
      if (recvBufCntr > (updateVarCnt + 6) and recvBufCntr <= (updateVarCnt + 12)) then
        --// getting the dest pose coordinate
        coordinateArrSrcDestBuf[2].coordinate[recvBufCntr - (updateVarCnt + 6)] = tonumber(sub) --// Dest Pos 
      end
      interfaceInBuf[recvBufCntr] = tonumber(sub)
      recvBuf_1 = string.format("%q",string.sub(recvBuf_1,(indx + 1),string.len(recvBuf_1)))
    end
    interfaceIn = interfaceInBuf
    coordinateArrSrcDest = coordinateArrSrcDestBuf
    return true
  end
  --until(ackFlag_1 == true and ackFlag_2 == true)
  --interfaceOut[2] = 0   --// state of Handshake = 0
  reset_jobs()
  return true
end  

--// End of utility functions  //-----------------------------------

--[[
SetToolBaudRate(115200)
local crc2,crc1 = CRC16({9,0x10,0x03,0xE8,0x00,0x03,0x06,0x00,0x00,0x00,0x00,0x00,0x00})
print("crc2:",crc2,"crc1:",crc1)
GWrite(0x01,{9,0x10,0x03,0xE8,0x00,0x03,0x06,0x00,0x00,0x00,0x00,0x00,0x00,115,48})
Sleep(300)
local crc4,crc3 = CRC16({9,0x10,0x03,0xE8,0x00,0x03,0x06,0x09,0x00,0x00,0x00,0x00,0x00})
print("crc3:",crc3,"crc4:",crc4)
GWrite(0x01,{9,0x10,0x03,0xE8,0x00,0x03,0x06,0x09,0x00,0x00,0x00,0x00,0x00,115,169})
Sleep(3000)]]