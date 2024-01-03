-- This file is only used to define variables and sub functions.
---/////// Dia Axis 7 positions /////-----------------------------------------

--- Pos = 0 mm (Camera 1)
--- Pos = 700 mm (Centrifuge Tube Place ,Camera 2 , Decap, Counterweight, Open Door Archive,Cobas Pure Rack Holder )
--- Pos = 950 mm ( Centrifuge Rack Pick,Centrifuge Rack Place, Fehler Place and Archive Place,Compact Max)
--- Pos = 2100 mm (Cobas Pure Rack Station )
--- Pos = 2400 mm ( Sysmex)
--- Pos = 2860 mm ( Cobas Pure loading/unloading)
--- Pos = 2950 mm ( Cobas Pure Station )

---// Global Variables /////////----------------------------------------------
IP = "192.168.0.64"
PORT = 9095
PORT_2 = 9097
isServer = false
speedhigh = 50   
test = false
ping = false
readDI = false
pingStatus_g = 1
coordinateArrSrcDest = {{coordinate={0,0,0,0,0,0}},{coordinate={0,0,0,0,0,0}}}
coordinateArrSrcDestBuf = {{coordinate={0,0,0,0,0,0}},{coordinate={0,0,0,0,0,0}}}
interfaceInBuf = {}
interfaceIn = {0,0,0,0,0,0,coordinateArrSrcDest}  --Recv// {stateOfhandshake=0,tubeType=0,status=0,srcJob=0,destJob=0,pingStatus=0,srcPos={0,0,0,0,0,0},desPos={0,0,0,0,0,0}}
interfaceOut = {0,0,0,0,0,0,pingStatus_g,0} --Send// {newConnection=0,stateOfhandshake=0,lockID=0,tubeStatus=0,macID=0,numPos=0,ping=1,Pose1={0,0,0,0,0,0},Pose2={0,0,0,0,0,0}, ..... }
interfaceOutSnd = ""
isCommunicationBroken = false
isNewCommunication = true
tubeStatus = 0 
tubeAngle  = 0

recvBuf = ""

stn5_batch1_poses = {P80, P81, P83, P82}
stn5_batch2_poses = {P84, P85, P87, P86}
startDecap = {joint={11.3997,-22.6038,-89.8270,22.8800,90.7151,284.7332}}
endDecap = {joint={11.4002,-22.5120,-89.6849,22.6460,90.7164,-181.2840}}

--All z values 
captPreCentr_J6_deg = 0
stn1_z_pick_val = -138.6076  --m// stn1 Tube pos z_val 
stn2_z_diff_pick_val = 155 --m// stn2 Rack Pick pos z_val
stn2_z_diff_plc_val = 158 --m// stn2 Rack Place pos z_val
--stn2_z_1_pick_val = -42.6003   --// stn2 Rack pos z_val -- 162.6003
--stn2_z_1_plc_val = -39.6003   --// stn2 Rack pos z_val  
--stn2_z_2_pick_val = 51.3694   --// stn2 Rack pos z_val  -- 213.9697
--stn2_z_2_plc_val = 48.3694   --// stn2 Rack pos z_val
stn3_z_pick_val = -142.692 --m// stn3 Pick Tube pos z_val 
stn3_z_plc_val = -141.692  --m// stn3 Place Tube pos z_val
--stn3_scan_z_val = 128.6029  --// stn3 scan pos z_val
stn3_scan_x_val_1 = -118  --m// stn3 scan pos x_val
stn3_scan_x_val_2 = -57  --m// stn3 scan pos x_val
stn5_z_plc_val = -107.4081  --m// stn5 Place Tube pos z_val 
stn5_z_pick_val = -107.4081 --m// stn5 Pick Tube pos z_val 
stn5_rack_pick_z_val = -92.2417 --m// stn5 Rack pos z_val 
stn5_rack_plc_z_val = -92.2417 --m// stn5 Rack pos z_val 
stn5_cw_pick_z_val = -119.4 --m// stn5 counter weight Pick pos z_val
stn5_cw_plc_z_val = -115.4 --m// stn5 counter weight Place pos z_val 
stn6_plc_z_val = 243 --// stn6 Rack plc in machine z Val 
stn6_pick_z_val = 242
stn9_z_pick_val = -113.2  --m// stn9 Pick Tube pos z_val
stn9_z_plc_val = -110.2  --m// stn9 Place Tube pos z_val
stn9_y_slide_out = -150 --m// 114   
stn9_y_slide_in = 69   --m//
stn9_z_rot_val = -30  --// stn9 Place Tube pos z_val
stn9_rack_z_val = -145.1487 --m// stn9 Rack Holder z_val
stn9_rack_x_out_diff_val = 68.2074 --m//
stn9_rack_x_in_diff_val = 18.2698 --m//
stn10_z_val = -129.8 --m// stn10 Tube pos z_val  
stn11_z_val = -129.8 --m// stn11 Tube pos z_val  
stn14_z_val = -89.0784 --m// stn14 Tube pos z_val
--stn17_holder_z_val = -233.0506 --// stn17 Holder pos z_val
--stn18_holder_z_val = -233.0506 --// stn17 Holder pos z_val
--stn17_z_val = -241.0506 --// stn17 Tube pos z_val
stn17_z_val = 54.9912 --// stn17 Tube pos z_val new
stn18_z_val = -241.0506 --// stn18 Tube pos z_val
--stn17_rack_z_val = -241.775 --// stn17 Tube pos z_val
stn17_rack_z_val = -85.4695 --54.8439 --m// stn17 Tube pos z_val new
--stn17_rack_x_out_diff_val = 55.9285 --m//
stn17_rack_x_in_diff_val = 18 --m//
stn18_rack_z_val = -85.4695 --m// stn18 Tube pos z_val
--stn18_rack_x_out_diff_val = 68.2074 --m//
stn18_rack_x_in_diff_val = 19.6 --m//

--stn9_rack_y_val = -286.3673  --// stn9 Rack Holder y_val
--stn6_offset = 90
--// End of Global Variables ////////-----------------------------------------

--////  Initialization function  ////-----------------------------------------

function reset_jobs()
  coordinateArrSrcDest = {{coordinate={nil,nil,nil,nil,nil,nil}},{coordinate={nil,nil,nil,nil,nil,nil}}}
  interfaceIn = {0,0,0,0,0,0,coordinateArrSrcDest}
  interfaceOut = {0,0,0,0,0,0,pingStatus_g,0}
end

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
  interfaceOutData[7] = pingStatus_g --// ping
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

function InitializeMachine(macID)
  if(macID == 1) then
    interfaceOut = InitializePose(macID,3,{P1,P2,P3})           --// Init Val 1 for Camera 1 (macID =1,numPos =3,poseArr={P1,P2,P3})
  elseif(macID == 2) then
    interfaceOut = InitializePose(macID,3,{P55,P56,P57,P191})        -- // Init Val 2 for Cobas Pure Rack (macID =2,numPos =3,poseArr={P55,P56,P57})
  elseif(macID == 3) then
    interfaceOut = InitializePose(macID,3,{P12,P13,P14})           -- // Init Val 3 for Compact Max (macID =3,numPos =3,poseArr={P12,P13,P14})
  elseif(macID == 4) then
    interfaceOut[1] = 0                                         -- // new Connection
    interfaceOut[5] = macID                                     -- // initilization ID  
  elseif(macID == 61) then
    interfaceOut[1] = 0                                         -- // new Connection
    interfaceOut[5] = macID
  elseif(macID == 9) then
    interfaceOut = InitializePose(macID,6,{P15,P17,P18,P16,P19,P20}) -- // Init Val 9 for Symex Rack (macID =9,numPos =6,poseArr={P15,P17,P18,P16,P19,P20})
  elseif(macID == 5) then
    interfaceOut = InitializePose(macID,5,{P7,P8,P9,P11,P10})   -- // Init Val 6 for Cetrifuge tubes (macID =51,numPos =5,poseArr={P7,P8,P9,P11,P10})
  elseif(macID == 55) then
    interfaceOut = InitializePose(macID,2,{P35,P36})   -- // Init counter weights
  elseif(macID == 10) then
    interfaceOut = InitializePose(macID,6,{P21,P22,P23,P140,P141,P142})        -- // Init Val 101 for Fehler Stand (macID =10,numPos =3,poseArr={P21,P22,P23})
  elseif(macID == 111) then
    interfaceOut = InitializePose(macID,6,{P24,P25,P26,P143,P144,P145})        -- // Init Val 111 for Archive (macID =11,numPos =3,poseArr={P24,P25,P26})
  elseif(macID == 112) then
    interfaceOut = InitializePose(macID,6,{P146,P147,P148,P149,P150,P151})        -- // Init Val 112 for Archive (macID =11,numPos =3,poseArr={P24,P25,P26})
  elseif(macID == 14) then
    interfaceOut = InitializePose(macID,3,{P53,P53,P54})            -- // Init Val 14 for Cobas Pure Rack Holder (macID =14,numPos =2,poseArr={P53,P54})
  elseif(macID == 17) then
    --interfaceOut = InitializePose(macID,4,{P185,P186,P187,P188})
    interfaceOut = InitializePose(macID,4,{P185,P186,P185})
  elseif(macID == 18) then
    interfaceOut = InitializePose(macID,4,{P62,P63,P62}) -- // Init Val 18 for Cobas Pure Filled Rack Holder_2 (macID =18,numPos =4,poseArr={P62,P63,P64,P65})
  end  
  statusACK = send_UDP_ACK_2()
end
--////  End of Initialization function  ////-----------------------------------


function send_UDP_ACK_2()
  --interfaceOut[2] = 1   --// state of Handshake 
  local ackFlag_1 = false
  local ackFlag_2 = false
  interfaceOut[7] = pingStatus_g --// ping
  local interfaceOutSnd = convertToString(interfaceOut)
  TCPWrite(socket,interfaceOutSnd) --interfaceOutSnd// Send back One
  --print("interfaceOutSnd:",interfaceOutSnd)
  Sleep(100)
  err, recvBuf = TCPRead(socket,0,"string")
  if (err == 0) then 
    local recvBuf_1 = recvBuf.buf    
    local indx = 1
    local recvBufCntr = 1
    local updateVarCnt = 6
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

--/// All util functions ////--------------------------------------------------
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

function setScanAngle(jointArr,jointAngle)
  local returnJointArr = {}
  returnJointArr= {joint= {jointArr.joint[1],jointArr.joint[2],jointArr.joint[3],jointArr.joint[4],jointArr.joint[5],jointArr.joint[6] - jointAngle }}
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

function convertToString(varToString) 
  msgSendStr = ''
  for key,value in ipairs(varToString) do 
    msgSendStr =  msgSendStr .. tostring(value) .. "," 
  end
  return msgSendStr
end
-----------------------------------------------------------------------
function colisionFreePath() 
  local u = {}
  u = CalcUser(6,0,{10,10,0,0,0,0})
  SetUser(0,u)
  pose = GetPose()
  print("Pose:",pose)
  user = pose.user
  if user == 1 then
    if(pose.coordinate[1] <= 409 and pose.coordinate[1] >= -70 and
      pose.coordinate[2] <= 236 and pose.coordinate[2] >= -23 and
      pose.coordinate[3] <= 357 and pose.coordinate[3] >= 0) then
      coordinateArr = {coordinate={(-70 + 409)/2,(-23 + 236)/2,(0 + 357)/2,pose.coordinate[4],pose.coordinate[5],pose.coordinate[6]}}
      print("coordinateArr:",coordinateArr)
      local status = CheckGo(coordinateArr,"User=1 CP=0 SYNC=1")
      if(status == 0) then
        Go(coordinateArr,"User=1 CP=0 SYNC=1")
      end
      Go(P27,"User=0 CP=0 SYNC=1")  --// Stn1 Home Pos
    end
  end
end

function send_UDP_ACK()
  interfaceOut[2] = 1   --// state of Handshake 
  --Go(InitialPose, "CP=1 Speed=50 Accel=50 SYNC=1")
  local ackFlag_1 = false
  local ackFlag_2 = false
  local ackLoop = 0
  for ackLoop = 1,2 do
    local interfaceOutSnd = convertToString(interfaceOut)
    UDPWrite(socket,interfaceOutSnd) --interfaceOutSnd// Send back One
    local err, recvBuf = UDPRead(socket, 0,"string")
    local recvBuf_1 = recvBuf.buf    
    local indx = 1
    local recvBufCntr = 1
    local updateVarCnt = 6
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
          coordinateArrSrcDest[1].coordinate[recvBufCntr - updateVarCnt] = tonumber(sub) --// Src Pos 
      end
      if (recvBufCntr > (updateVarCnt + 12) and recvBufCntr <= (updateVarCnt + 12)) then
        --// getting the dest pose coordinate
        coordinateArrSrcDest[2].coordinate[recvBufCntr - (updateVarCnt + 6)] = tonumber(sub) --// Dest Pos 
      end
      interfaceIn[recvBufCntr] = tonumber(sub)
      recvBuf_1 = string.format("%q",string.sub(recvBuf_1,(indx + 1),string.len(recvBuf_1)))
    end
    --print("print ", ackLoop, "   ", interfaceOut[5], "    ", interfaceOut, "     ", interfaceIn)
    if interfaceOut[2] == 1 and interfaceIn[1] == 1  then
      interfaceOut[2] = 0 --// Send back state of Handshake  = 0
      ackFlag_1 = true
    elseif interfaceOut[2] == 0 and interfaceIn[1] == 0 then
      interfaceOut[2] = 1 --// Send back state of Handshake  = 1
      ackFlag_2 = true
    end
  end
  if(ackFlag_1 == true and ackFlag_2 == true) then
    return true
  else 
    return false
  end
end  
--/// End of All util functions ////----------------------------------------------