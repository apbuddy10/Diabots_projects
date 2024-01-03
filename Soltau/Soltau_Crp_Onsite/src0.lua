--- Movements Function commands-------------------

function setGripper(position, speed, force)
  RiqSet(position, speed, force)
  Sync()
  Sleep(500)
end

function setGripperCheck(gripper,expectedStatus)
  local gripInit = gripper.init or 0     --// Default value 0
  local pos = gripper.pos or 0     --// Default value 0
  local speed = gripper.speed or 100     --// Default value 0
  local force = gripper.force or 100     --// Default value 0
  local count = 0
  if(gripInit == 1) then 
    Sync()
    RiqInit()
    Sync()
  else 
    Sync()
    RiqSet(pos,speed,force)
    Sync()
  end
  while(count < 5) do
    Sleep((gripInit + 1)*1100) -- // Init needs a 2 sec sleep
    status = RiqGetStatus()
    print(status)
    if (status == expectedStatus ) then  -- at rest
      return 0
    else
      if(expectedStatus ~= 3 and gripInit == 1) then 
        Sync()
        RiqInit()
        Sync()
      elseif(expectedStatus ~= 2 or expectedStatus ~= 3) then 
        Sync()
        RiqSet(pos,speed,force)
        Sync()
      end
    end
    count = count + 1
    if(count >= 3) then
      Pause()
    end
  end
end

function openDoorArchive()
  setGripper(0,50,50)
  Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=0") --// Drive end
  interfaceOut[5] = 704 ----- axis 7 cam2 home
  statusACK = send_UDP_ACK_2()
  interfaceOut[5] = 0
  Go(P176,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
  Move(P177,"User=3 Tool=1 CP=0 SpeedS=5 AccelS=100 SYNC=1")
  Go(P125,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
  Go(P126,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
  Move(P127,"User=3 Tool=1 SpeedS=5 AccelS=2 CP=100 SYNC=0")
  Move(P128,"User=3 Tool=1 SpeedS=5 AccelS=4 CP=100 SYNC=1")
  Move(P129,"User=3 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")
  Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1") --// Drive end
end

function checkBarcode()
  Go(P28,"User=0 CP=100 Speed=100 Accel=100 SYNC=0")  --// Stn4 Ref Pose
  Go(P32,"User=3 CP=0 Speed=100 Accel=100 SYNC=1")  --// Stn4 appr Pose
  Move(P33,"User=3 CP=0 SpeedS=100 AccelS=100 SYNC=1")  --// Stn4 down Pose
  local jointArrInitPos = GetAngle()
  local tubeAngle = 0
  tubeStatus = 0
  while(tubeAngle <= 370) do
    interfaceOut[5] = 41  --// mac ID
    interfaceOut[3] = 13  --// lock ID , barcode  
    statusACK = send_UDP_ACK_2() 
    if(statusACK == true) then
      tubeStatus = interfaceIn[3]  --// tube status
      print("tubeStatus:",tubeStatus)
    end
    if(tubeStatus == 1) then
      break
    end
    --tubeStatus = interfaceIn[3]  --// tube status
    print("tubeStatus:",tubeStatus)
    jointArr = GetAngle()
    local rot_p = {joint={jointArr.joint[1],jointArr.joint[2],jointArr.joint[3],jointArr.joint[4],jointArr.joint[5],jointArr.joint[6] + 10}}
    MoveJ(rot_p,"CP=0 SYNC=1")     
    --statusACK = send_UDP_ACK() 
    tubeAngle = tubeAngle + 10
  end
  MoveJ(jointArrInitPos,"CP=0 Speed=100 Accel=100 SYNC=1")  --// Stn4 down Pose but using MoveJ
  Go(P32,"User=3 CP=0 Speed=100 Accel=100 SYNC=1")  --// Stn4 appr Pose
  Go(P28,"User=0 CP=100 Speed=100 Accel=100 SYNC=0")  --// Stn4 Ref Pose
  Go(P29,"User=0 CP=0 Speed=100 Accel=100 SYNC=1")  --// Stn6 Home Pose
  return tubeAngle
end
-- End of Movements Function commands-------------

--// Initialization of Variables and Communication
setGripperCheck( {init=1},3)  --// Init Gripper ,status 3
Sync()
setGripperCheck( {pos=0},3)  --// Close the Gripper ,status 3
MoveJ(P91,"CP=100 Speed=50 Accel=10 SYNC=1")
err, socket = TCPCreate(isServer, IP, PORT)
err = TCPStart(socket, 0)
DOExecute(3, ON) --// Turn on Button 1 Light
DOExecute(4, ON) --// Turn on Button 2 Light
DOExecute(9, OFF) --// Turn off process indicator compact max
DOExecute(10, OFF) --// Initialize ping
DOExecute(5, ON)     ------ Signal to Safety
Sleep(1000)
DOExecute(5, OFF)

function setPingStatus()
  local pingStatus = interfaceIn[6]
  print("interfaceIn:",interfaceIn)
  if (pingStatus == 1 ) then
    DOExecute(10, OFF) --// Turn off Ping
  end
  if (DI(26)) == ON then
    pingStatus_g = 0
    interfaceOut[7] = 0   --//ping status interrupted
    ping = true
  else
    pingStatus_g = 1
    interfaceOut[7] = 1   --//ping status not interrupted
    ping = false
  end
end

if (err == 0)
  then
    interfaceOut[1] = 1   --//new Connection
    --local interfaceOutSnd = convertToString(interfaceOut)
    --UDPWrite(socket,interfaceOutSnd) --interfaceOutSnd// Send back One
    setPingStatus()  --// check ping status
    isNewCommunication  = false
    statusACK = send_UDP_ACK_2()
    interfaceOut[1] = 0   --//new Connection
    InitializeMachine(4)  --// Init Q00 and reset
    InitializeMachine(1)  --// Init Camera 1
    InitializeMachine(2)  --// Init Cobas Pure Rack
    InitializeMachine(3)  --// Init Compact max
    InitializeMachine(9)  --// Init Sysmex Rack
    InitializeMachine(5)  --// Init Centrifuge Tube Points
    InitializeMachine(55)  --// Init Counter weights
    InitializeMachine(10) --// Init Fehler stand 1
    InitializeMachine(111) --// Init Archive 1
    InitializeMachine(112) --// Init Archive 2
    InitializeMachine(61) --// Init centrifuge
    InitializeMachine(14) --// Init Cobas Pure Rack Holder
    InitializeMachine(17) --// Init Cobas Pure Filled Rack Holder_1
    InitializeMachine(18) --// Init Cobas Pure Filled Rack Holder_2
    
    setGripperCheck( {init=1},3 )  --// Init Gripper ,status 3
    Sync()
    setGripperCheck( {pos=0},3 )  --// Close the Gripper ,status 3
    openDoorArchive() --Open the Door of Archive 
    --[[while true do
      interfaceOut[5] = 701 ----- axis 7 sysmex home
      statusACK = send_UDP_ACK_2()
      interfaceOut[5] = 0
      interfaceOut[5] = 704 ----- axis 7 sysmex home
      statusACK = send_UDP_ACK_2()
      interfaceOut[5] = 0
      interfaceOut[5] = 706 ----- axis 7 sysmex home
      statusACK = send_UDP_ACK_2()
      interfaceOut[5] = 0
      interfaceOut[5] = 707 ----- axis 7 sysmex home
      statusACK = send_UDP_ACK_2()
      interfaceOut[5] = 0
      interfaceOut[5] = 708 ----- axis 7 sysmex home
      statusACK = send_UDP_ACK_2()
      interfaceOut[5] = 0     
    end]]
    while true do 
      Sync()
      reset_jobs()
      resetLockStatus()
      readDI = false
      ping = false
      statusACK = send_UDP_ACK_2()
      setPingStatus()  --// check ping status
      if(statusACK == true) then
        local srcJob = interfaceIn[4]
        local destJob = interfaceIn[5]
        print("srcJob:",srcJob)
        print("destJob:",destJob)
        print("coordinateArrSrcDest:",coordinateArrSrcDest)
        local coordinateArr = {}
        if(srcJob == 0) then
          Sleep(50)
        elseif(srcJob == 11) then   --// Stn1 Pick
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          interfaceOut[5] = 701 ----- axis 7 cam1 home
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P27,"User=1 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")  --// Stn1 Home Pos
          Go(P88,"User=1 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P89,"User=1 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(coordinateArrSrcDest[1],"User=1 Tool=1 CP=100 Speed=50 Accel=100 SYNC=0")  --// Src Pose
          setGripper(50,50,50)
          --setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Close the Gripper ,status 3
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn1_z_pick_val)
          Move(coordinateArr,"User=1 Tool=1 SpeedS=10 AccelS=5 CP=0 SYNC=1")  --// Pick the test tube
          setGripper(0,50,50) --// --// Close the Gripper 
          Move(coordinateArrSrcDest[1],"User=1 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0") 
          Go(P89,"User=1 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P88,"User=1 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P27,"User=1 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")  --// Stn1 Home Pos
          --local gripperStatus = RiqGetStatus()
          --if (gripperStatus ~= 2) then
            --srcJob = 0
            --destJob = 0
            --reset_jobs()
            --resetLockStatus()
          --end
          if(destJob == 41) then   --// Stn4 Pick or Place
            interfaceOut[5] = 704 ----- axis 7 cam2 home
            statusACK = send_UDP_ACK_2()
            interfaceOut[5] = 0
            Go(P28,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
            DO(1, ON)
            Move(P32,"User=3 Tool=1 CP=100 SpeedS=100 AccelS=100 SYNC=1")
            local colorOfTube = 0
            tubeStatus = 0
            local levelStatus = 0
            tubeAngle = 0
            --Check the color of the tube
            interfaceOut[5] = 41  --// mac ID 
            interfaceOut[3] = 13  --// lock ID to
            statusACK = send_UDP_ACK_2() 
            if(statusACK == true) then
              colorOfTube = interfaceIn[3]  --// color value
              print("colorOfTube:",colorOfTube)
            end
            local jointArr = GetAngle()
            local jointArrInitPos = GetAngle()            
            while(tubeAngle <= 370) do
              interfaceOut[5] = 41  --// mac ID 
              interfaceOut[3] = 14  --// lock ID , barcode 1 
              statusACK = send_UDP_ACK_2() 
              if(statusACK == true) then
                tubeStatus = interfaceIn[3]  --// tube status
              end
              if(tubeStatus == 1) then    
                --[[ tubeStatus = 0
                jointArr = GetAngle()
                local rot_p = {joint={jointArr.joint[1],jointArr.joint[2],jointArr.joint[3],jointArr.joint[4],
                                  jointArr.joint[5],jointArr.joint[6] + 0.5}}
                MoveJ(rot_p,"CP=0 Speed=100 Accel=100 SYNC=1")
                interfaceOut[5] = 41
                interfaceOut[3] = 15  --// lock ID , barcode 2
                statusACK = send_UDP_ACK_2() 
                if(statusACK == true) then
                  tubeStatus = interfaceIn[3]  --// tube status 
                end]]
                if(tubeStatus == 1) then
                  local jointArr180 = GetAngle()
                  local rot180_p = {joint={jointArr180.joint[1],jointArr180.joint[2],jointArr180.joint[3],
                                            jointArr180.joint[4],jointArr180.joint[5],jointArr180.joint[6] + 180}}
                  MoveJ(rot180_p,"CP=0 Speed =100 Accel=100 SYNC=1")
                  interfaceOut[5] = 41
                  if(colorOfTube == 11)then    
                    interfaceOut[3] = 17      --// lock ID , green level check
                  elseif(colorOfTube == 12)then
                    interfaceOut[3] = 16
                  elseif(colorOfTube == 13)then
                    interfaceOut[3] = 16
                  elseif(colorOfTube == 14)then
                    interfaceOut[3] = 16
                  elseif(colorOfTube == 18)then
                    interfaceOut[3] = 16
                  end
                  statusACK = send_UDP_ACK_2() 
                  if(statusACK == true) then
                    -- levelStatus = 1
                    levelStatus = interfaceIn[3]  --// tube status
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
              end
              jointArr = GetAngle()
              local rot_p = {joint={jointArr.joint[1],jointArr.joint[2],jointArr.joint[3],jointArr.joint[4],
                                      jointArr.joint[5],jointArr.joint[6] + 15}}
              MoveJ(rot_p,"CP=0 Speed =100 Accel=100 SYNC=1")
              tubeAngle = tubeAngle + 15
              print("tubeAngle:",tubeAngle)
            end
            --[[if(levelStatus == 0 and colorOfTube ~= 0) then
              while (tubeAngle <= 370) do              
                jointArr = GetAngle()
                local rot_p = {joint={jointArr.joint[1],jointArr.joint[2],jointArr.joint[3],jointArr.joint[4],
                                        jointArr.joint[5],jointArr.joint[6] + 15}}
                MoveJ(rot_p,"CP=0 Speed =100 Accel=100 SYNC=1")     
                interfaceOut[5] = 41
                interfaceOut[3] = 21  --// lock ID , level NG
                statusACK = send_UDP_ACK_2() 
                tubeAngle = tubeAngle + 15
              end
            end]]
            MoveJ(jointArrInitPos,"CP=0 Speed =100 Accel=100 SYNC=1")
            Move(P28,"User=3 Tool=1 CP=100 SpeedS=100 AccelS=100 SYNC=0")  --// Stn4 appr Pose
            DO(1, OFF)
            Go(P90,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
            setLockStatus(2) --// Set the Lock Status to 2 to get next job
            statusACK = send_UDP_ACK_2() 
            if(statusACK == true) then
              srcJob = interfaceIn[4]
              destJob = interfaceIn[5]
              print("srcJob:",srcJob)
              print("destJob:",destJob)
              if(srcJob == 52) then   --// Place Tube in Centrifuge Racks
                Go(P92,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
                Go(coordinateArrSrcDest[1],"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")  --// Src Pose
                -- local jointArr = GetAngle()
                -- local updatedJointPos = setBarcodeAngle(jointArr,tubeAngle)
                -- MoveJ(updatedJointPos,"CP=0 Speed =100 Accel=100 SYNC=1")
                -- updatedPos = GetPose()
                -- coordinateArr = setCoordinatePos_z({coordinate=updatedPos.coordinate},stn5_z_plc_val)
                coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn5_z_plc_val)
                Move(coordinateArr,"User=3 SpeedS=50 AccelS=100 CP=0 SYNC=1")
                --setGripper(50,50,50)
                setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
                Move(coordinateArrSrcDest[1],"User=3 SpeedS=100 AccelS=100 CP=0 SYNC=1")
                setGripper(0,50,50) --// --// Close the Gripper 
                --setGripperCheck( {pos=0,speed=50,force=50},3 )  --// Close the Gripper ,status 3
                Go(P92,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
                Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
                Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
                resetLockStatus()  --// Reset the Lock Status 
                reset_jobs()
              elseif(srcJob == 94) then       --// Place Tube in Sysmex Racks
                Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
                interfaceOut[5] = 707 ----- axis 7 sysmex home
                statusACK = send_UDP_ACK_2()
                interfaceOut[5] = 0
                Go(P30,"User=4 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")        
                Go(coordinateArrSrcDest[1],"User=4 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")  --// Src Pose
                -- coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn9_z_rot_val)
                -- Move(coordinateArr,"User=4 SpeedS=5 AccelS=3 CP=0 SYNC=1")
                -- local jointArr = GetAngle()
                -- local updatedJointPos = setBarcodeAngle(jointArr,tubeAngle)
                -- MoveJ(updatedJointPos,"CP=0 Speed=100 Accel=50 SYNC=1")
                --local updatedPos = GetPose()
                coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn9_z_plc_val)
                Move(coordinateArr,"User=4 SpeedS=20 AccelS=100 CP=0 SYNC=1")
                --setGripper(50,50,50)
                setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
                Move(coordinateArrSrcDest[1],"User=4 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")  --// Src Pose
                Go(P30,"User=4 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")
                Go(P91,"User=0 Tool=1 Speed=100 Accel=100 CP=0 SYNC=1")
                setGripper(0,50,50)
                --setGripperCheck( {pos=0,speed=50,force=50},3 )  --// Close the Gripper ,status 3
                resetLockStatus()  --// Reset the Lock Status
                reset_jobs()              
              elseif(srcJob == 102) then      --// Place in Fehler Stand
                Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
                interfaceOut[5] = 706 ----- axis 7 centifuge home
                statusACK = send_UDP_ACK_2()
                interfaceOut[5] = 0
                Go(P93,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")
                Go(coordinateArrSrcDest[1],"User=5 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")  --// Src Pose
                coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn10_z_val)
                Move(coordinateArr,"User=5 Tool=1 SpeedS=50 AccelS=100 CP=0 SYNC=1")  
                --setGripper(50,50,50)
                setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
                Move(coordinateArrSrcDest[1],"User=5 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")  
                Go(P93,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")
                Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
                Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
                setGripper(0,50,50)
                --setGripperCheck( {pos=0,speed=50,force=50},3 )  --// Close the Gripper ,status 3
                resetLockStatus()  --// Reset the Lock Status
                reset_jobs()  
              end
            end
          end
        elseif(srcJob == 51) then    --// Pick Rack/tube from Centrifuge Racks 
          if(destJob == 41) then   --// Stn4 Pick or Place 
            setGripper(50,50,50)
            --setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
            Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
            interfaceOut[5] = 704 ----- axis 7 cam2 home
            statusACK = send_UDP_ACK_2()
            interfaceOut[5] = 0
            Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
            Go(P92,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
            Go(coordinateArrSrcDest[1],"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")  --// Src Pose
            coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn5_z_pick_val)
            Move(coordinateArr,"User=3 Tool=1 SpeedS=50 AccelS=100 CP=0 SYNC=1")
            --setGripper(0,50,50) --// --// Close the Gripper
            setGripperCheck( {pos=0,speed=50,force=50},2 )  --// Close the Gripper ,status 2
            Move(coordinateArrSrcDest[1],"User=3 SpeedS=100 AccelS=100 CP=100 SYNC=0")
            Go(P92,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
            Go(P28,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
            DO(1, ON)
            Move(P32,"User=3 Tool=1 CP=100 SpeedS=100 AccelS=100 SYNC=1")
            tubeStatus = 0
            tubeAngle = 0 
            interfaceOut[5] = 41  --// mac ID 
            interfaceOut[3] = 13  --// color eg
            statusACK = send_UDP_ACK_2()
            local jointArr = GetAngle()
            local jointArrInitPos = GetAngle()
            while(tubeAngle <= 370) do
              interfaceOut[5] = 41  --// mac ID 
              interfaceOut[3] = 14  --// lock ID , barcode 1 
              statusACK = send_UDP_ACK_2() 
              if(statusACK == true) then
                tubeStatus = interfaceIn[3]  --// tube status
              end
              if(tubeStatus == 1) then 
                break
              end
              jointArr = GetAngle()
              local rot_p = {joint={jointArr.joint[1],jointArr.joint[2],jointArr.joint[3],jointArr.joint[4],
                                      jointArr.joint[5],jointArr.joint[6] + 15}}
              MoveJ(rot_p,"CP=0 Speed =100 Accel=100 SYNC=1")
              tubeAngle = tubeAngle + 15
              print("tubeAngle:",tubeAngle)
            end
            MoveJ(jointArrInitPos,"CP=0 Speed =100 Accel=100 SYNC=1")
            Move(P28,"User=3 Tool=1 CP=100 SpeedS=100 AccelS=100 SYNC=0")  --// Stn4 appr Pose
            DO(1, OFF)
            Go(P90,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
            setLockStatus(3) --// Set the Lock Status to 2 to get next job
            statusACK = send_UDP_ACK_2() 
            if(statusACK == true) then
              srcJob = interfaceIn[4]
              destJob = interfaceIn[5]
              print("srcJob:",srcJob)
              print("destJob:",destJob)
              if(srcJob == 32) then     --// Place in Compact Max
                DO(2, ON)
                Go(P101,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
                Move(P100,"User=3 Tool=1 SpeedS=20 AccelS=100 CP=0 SYNC=1")
                jointArr = GetAngle()
                local jointArrStartPos = GetAngle()      --// start pos
                local updatedJointPos = setBarcodeAngle(jointArrStartPos,tubeAngle)
                MoveJ(updatedJointPos,"CP=0 Speed =100 Accel=100 SYNC=1")
                DO(2, OFF)
                setGripper(100,100,100)
                --setGripperCheck( {pos=100},3 )  --// Open the Gripper ,status 3
                DO(2, ON)
                DO(2, OFF)
                MoveJ(jointArr,"CP=0 Speed=100 Accel=100 SYNC=1")
                Move(P100,"User=3 Tool=1 SpeedS=100 AccelS=100 CP=0 SYNC=1")
                setGripperCheck( {pos=0,speed=50,force=10},2 )  --// Close the Gripper ,status 2
                DOExecute(2, ON)
                Sleep(1)
                Move(P101,"User=3 Tool=1 CP=100 SpeedS=100 AccelS=100 SYNC=0")
                Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
                Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
                interfaceOut[5] = 706 ----- axis 7 centrifuge home
                statusACK = send_UDP_ACK_2()
                interfaceOut[5] = 0
                Go(P34,"User=2 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
                --local jointArrStartPos = GetAngle()      --// start pos
                --local updatedJointPos = setBarcodeAngle(jointArrStartPos,tubeAngle)
                --MoveJ(updatedJointPos,"CP=0 Speed =100 Accel=100 SYNC=1")
                local scan_count = 0
                local scanStatus = 0
                DOExecute(9, ON) --// Turn on process indicator compact max
                while true do
                  local updatedPos = GetPose()
                  local coordinateArr = setCoordinatePos_x({coordinate=updatedPos.coordinate},stn3_scan_x_val_2)
                  Move(coordinateArr,"User=2 Tool=1 SpeedS=5 AccelS=100 CP=0 SYNC=1")
                  scan_count = scan_count + 1
                  interfaceOut[5] = 41  --// mac ID 
                  interfaceOut[3] = 3  --// compact max barcode
                  statusACK = send_UDP_ACK_2() 
                  print("scanStatus:",interfaceIn[3])
                  if(statusACK == true) then
                    scanStatus = interfaceIn[3]  --// tube status
                  end
                  if(scanStatus == 1) then 
                    break
                  end
                  local updatedPos = GetPose()
                  local coordinateArr = setCoordinatePos_x({coordinate=updatedPos.coordinate},stn3_scan_x_val_1)
                  Move(coordinateArr,"User=2 Tool=1 SpeedS=5 AccelS=100 CP=0 SYNC=1")
                  scan_count = scan_count + 1
                  interfaceOut[5] = 41  --// mac ID 
                  interfaceOut[3] = 3  --// compact max barcode
                  statusACK = send_UDP_ACK_2() 
                  print("scanStatus:",interfaceIn[3])
                  if(statusACK == true) then
                    scanStatus = interfaceIn[3]  --// tube status
                  end
                  if(scanStatus == 1) then 
                    break
                  end
                  if (scan_count >= 10) then
                    break
                  end
                end
                Go(P99,"User=2 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")  
                if(scanStatus == 1) then 
                  Go(coordinateArrSrcDest[1],"User=2 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")  --// Src Pose
                  coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn3_z_plc_val)
                  Move(coordinateArr,"User=2 Tool=1 SpeedS=2 AccelS=5 CP=0 SYNC=1") 
                  --setGripper(50,50,50)
                  setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
                  Move(coordinateArrSrcDest[1],"User=2 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")  
                  DOExecute(9, OFF) --// Turn off process indicator compact max
                  Go(P31,"User=2 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")  --// Stn3 Home Pose
                  interfaceOut[5] = 302 ----- Update grid
                  statusACK = send_UDP_ACK_2()
                  interfaceOut[5] = 0
                else
                  DOExecute(9, OFF) --// Turn off process indicator compact max
                  interfaceOut[3] = 3  --// Lock ID 
                  interfaceOut[4] = 0   ---- scanStatus
                  interfaceOut[5] = 0
                  statusACK = send_UDP_ACK_2() 
                  if(statusACK == true) then
                    srcJob = interfaceIn[4]
                    destJob = interfaceIn[5]
                    Go(P31,"User=2 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")  --// Stn3 Home Pose
                    Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
                    Go(P93,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")
                    Go(coordinateArrSrcDest[1],"User=5 Tool=1 Speed=100 Accel=100 CP=0 SYNC=0")  --// Src Pose
                    coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn10_z_val)
                    Move(coordinateArr,"User=5 Tool=1 SpeedS=50 AccelS=100 CP=0 SYNC=1")  
                    --setGripper(50,50,50)
                    setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
                    Move(coordinateArrSrcDest[1],"User=5 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")  
                    Go(P93,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")
                    Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
                  end
                end
                Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
                setGripper(0,50,50)
                --setGripperCheck( {pos=0,speed=50,force=50},3 )  --// Close the Gripper ,status 3
                resetLockStatus()  --// Reset the Lock Status
                reset_jobs()
              elseif(srcJob == 143) then   --// Place tube in Cobas Pure Rack Holder
                DO(2, ON)
                Go(P101,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
                Move(P100,"User=3 Tool=1 SpeedS=50 AccelS=100 CP=0 SYNC=1")
                jointArr = GetAngle()
                local jointArrStartPos = GetAngle()      --// start pos
                local updatedJointPos = setBarcodeAngle(jointArrStartPos,tubeAngle)
                MoveJ(updatedJointPos,"CP=0 Speed =100 Accel=100 SYNC=1")
                DO(2, OFF)
                setGripper(100,100,100)
                --setGripperCheck( {pos=100},3 )  --// Open the Gripper ,status 3
                DO(2, ON)
                DO(2, OFF)
                --MoveJ(startDecap,"CP=0 Speed =100 Accel=100 SYNC=1")
                Go(P138,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
                --setGripper(0,100,100)
                setGripperCheck( {pos=0},2 )  --// Close the Gripper ,status 2
                --MoveJ(endDecap,"CP=0 Speed =100 Accel=50 SYNC=1")
                Go(P139,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
                Go(P101,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
                --MoveJ(P101,"CP=100 Speed=100 Accel=50 SYNC=1")
                Go(P102,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
                setGripper(100,100,0)
                --setGripperCheck( {pos=100,speed=100,force=0},3 )  --// Open the Gripper ,status 2
                setGripper(0,100,0)
                setGripper(100,100,0)
                setGripper(0,100,0)
                setGripper(100,100,0)
                --setGripperCheck( {pos=100,speed=100,force=0},3 )  --// Open the Gripper ,status 3
                MoveJ(jointArr,"CP=0 Speed =100 Accel=100 SYNC=1")
                Move(P179,"User=3 Tool=1 SpeedS=100 AccelS=100 CP=0 SYNC=1")
                --setGripper(0,20,8)
                setGripperCheck( {pos=0,speed=20,force=8},2 )  --// Close the Gripper ,status 2
                --Sleep(2000)
                DOExecute(2, ON)
                Move(P101,"User=3 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")
                print("coordinateArrSrcDest",coordinateArrSrcDest)
                Go(coordinateArrSrcDest[1],"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")  --// Src Pose
                local coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn14_z_val)
                Move(coordinateArr,"User=3 Tool=1 SpeedS=20 AccelS=100 CP=0 SYNC=1")
                --setGripper(35,50,50)
                setGripperCheck( {pos=35,speed=50,force=50},3 )  --// Open the Gripper ,status 3
                Move(coordinateArrSrcDest[1],"User=3 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")
                Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
                resetLockStatus()  --// Reset the Lock Status
                reset_jobs()
              elseif(srcJob == 102) then   --// Place in Fehler Stand
                Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
                interfaceOut[5] = 706 ----- axis 7 centifuge home
                statusACK = send_UDP_ACK_2()
                interfaceOut[5] = 0
                Go(P93,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")
                Go(coordinateArrSrcDest[1],"User=5 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")  --// Src Pose
                coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn10_z_val)
                Move(coordinateArr,"User=5 Tool=1 SpeedS=50 AccelS=100 CP=0 SYNC=1")  
                --setGripper(50,50,50)
                setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
                Move(coordinateArrSrcDest[1],"User=5 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")  
                --setGripper(0,50,50)
                setGripperCheck( {pos=0,speed=50,force=50},3 )  --// Close the Gripper ,status 3
                Go(P93,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")
                Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
                resetLockStatus()  --// Reset the Lock Status
                reset_jobs()
              end
            end
          elseif(destJob == 62) then    --// Place Racks in Centrifuge Machine  
            if (test == true) then
              print("Centrifuge skipped")
              interfaceOut[5] = 67  --// mac ID 
              statusACK = send_UDP_ACK_2()
              interfaceOut[5] = 68  --// mac ID 
              statusACK = send_UDP_ACK_2()
            else
              Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
              interfaceOut[5] = 706 ----- axis 7 centifuge home
              statusACK = send_UDP_ACK_2()
              interfaceOut[5] = 0
              Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
              Go(P103,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=1")            
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
              statusACK = send_UDP_ACK_2()
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
                statusACK = send_UDP_ACK_2()
                Go(rack_poses[loop_count],"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")  --// Src Pose
                setGripper(50,100,0)
                --setGripperCheck( {pos=50,speed=100,force=0},3 )  --// Open the Gripper ,status 3
                local coordinateArr = setCoordinatePos_z(rack_poses[loop_count],stn5_rack_pick_z_val)
                Move(coordinateArr,"User=3 Tool=1 SpeedS=100 AccelS=100 CP=0 SYNC=1")
                --setGripper(0,50,50)
                setGripperCheck( {pos=0,speed=50,force=50},2 )  --// Close the Gripper ,status 2
                Move(rack_poses[loop_count],"User=3 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0") 
                Go(P103,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")   
                Go(P44,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")                
                Move(P104,"User=3 Tool=1 SpeedS=2 AccelS=1 CP=0 SYNC=1")
                --setGripper(50,100,0)
                setGripperCheck( {pos=50,speed=100,force=0},3 )  --// Open the Gripper ,status 3
                Move(P44,"User=3 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")
                Go(P103,"User=3 Tool=1 Speed=100 Accel=100 CP=50 SYNC=1") 
                if(loop_count >= 4) then
                  break
                end
              end
              --Go(P103,"User=3 Tool=1 Speed=100 Accel=50 CP=50 SYNC=1") 
              interfaceOut[5] = 67  --// mac ID 
              statusACK = send_UDP_ACK_2()
              interfaceOut[5] = 68  --// mac ID 
              statusACK = send_UDP_ACK_2()
              Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
              Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
            end
          elseif(destJob == 55) then   --// Pick from racks and place tube in Counter Weight Pos
            Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
            interfaceOut[5] = 704 ----- axis 7 cam2 home
            statusACK = send_UDP_ACK_2()
            interfaceOut[5] = 0
            Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
            setGripper(50,50,50)
            --setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
            Go(P92,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
            Go(coordinateArrSrcDest[1],"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")  --// Src Pose
            coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn5_z_pick_val)
            Move(coordinateArr,"User=3 Tool=1 SpeedS=50 AccelS=100 CP=0 SYNC=1")
            --setGripper(0,50,50) --// --// Close the Gripper
            setGripperCheck( {pos=0,speed=50,force=50},2 )  --// Close the Gripper ,status 2
            Move(coordinateArrSrcDest[1],"User=3 SpeedS=100 AccelS=20 CP=100 SYNC=0")
            Go(P92,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")              
            Go(coordinateArrSrcDest[2],"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")  --// Src Pose
            coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],stn5_cw_plc_z_val)  
            Move(coordinateArr,"User=3 SpeedS=50 AccelS=100 CP=0 SYNC=1") 
            --setGripper(50,50,50)
            setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
            Move(coordinateArrSrcDest[2],"User=3 SpeedS=100 AccelS=100 CP=100 SYNC=0")  
            setGripper(0,50,50)
            --setGripperCheck( {pos=0,speed=50,force=50},3 )  --// Close the Gripper ,status 3
            Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")   
            Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          end
        elseif(srcJob == 61) then   --// Pick Racks from Centrifuge Machine
          if (test == true) then 
            print("Centrifuge skipped")
          else
            Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
            interfaceOut[5] = 706 ----- axis 7 centrifuge home
            statusACK = send_UDP_ACK_2()
            interfaceOut[5] = 0
            Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
            Go(P103,"User=3 Tool=1 Speed=100 Accel=100 CP=50 SYNC=1")            
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
            statusACK = send_UDP_ACK_2()
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
              statusACK = send_UDP_ACK_2()
              --setGripper(60,50,50)
              setGripperCheck( {pos=60,speed=50,force=50},3 )  --// Open the Gripper ,status 3
              Go(P44,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")                
              Move(P104,"User=3 Tool=1 SpeedS=100 AccelS=100 CP=0 SYNC=1")
              --setGripper(0,50,50)
              setGripperCheck( {pos=0,speed=50,force=50},2 )  --// Close the Gripper ,status 2
              Move(P44,"User=3 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")
              Go(P103,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")
              Go(rack_poses[loop_count],"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")  --// Src Pose
              coordinateArr = setCoordinatePos_z(rack_poses[loop_count],stn5_rack_plc_z_val)
              Move(coordinateArr,"User=3 Tool=1 SpeedS=20 AccelS=100 CP=0 SYNC=1")
              --setGripper(50,100,0)
              setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
              Move(rack_poses[loop_count],"User=3 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0") 
              Go(P103,"User=3 Tool=1 Speed=100 Accel=100 CP=50 SYNC=1") 
              --setGripper(0,100,0)
              setGripperCheck( {pos=0,speed=100,force=0},3 )  --// Close the Gripper ,status 3
              if(loop_count >= 4) then
                break
              end
            end
            Go(P103,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0") 
            interfaceOut[5] = 67  --// mac ID 
            statusACK = send_UDP_ACK_2()
            Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
            Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          end
        elseif(srcJob == 54) then   --// Pick Counter Weight 
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          interfaceOut[5] = 704 ----- axis 7 cam2 home
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(coordinateArrSrcDest[1],"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")  --// Src Pose
          --setGripper(50,100,0)
          setGripperCheck( {pos=50,speed=100,force=0},3 )  --// Open the Gripper ,status 3
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn5_cw_pick_z_val)
          Move(coordinateArr,"User=3 Tool=1 SpeedS=50 AccelS=100 CP=0 SYNC=1")  
          --setGripper(0,50,50)
          setGripperCheck( {pos=0,speed=50,force=50},2 )  --// Close the Gripper ,status 2
          Move(coordinateArrSrcDest[1],"User=3 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")  
          Go(P92,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          if(destJob == 52) then     --// Place Counter Weight in Centrifuge Racks
            Go(coordinateArrSrcDest[2],"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")  --// Dest Pose
            coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],stn5_z_plc_val)
            Move(coordinateArr,"User=3 Tool=1 SpeedS=50 AccelS=100 CP=0 SYNC=1")  --// Src Pose
            --setGripper(50,100,0)
            setGripperCheck( {pos=50,speed=100,force=0},3 )  --// Open the Gripper ,status 3
            Move(coordinateArrSrcDest[2],"User=3 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")  --// Src Pose
            --setGripper(0,100,0)
            setGripperCheck( {pos=0,speed=100,force=0},3 )  --// Close the Gripper ,status 3
            Go(P92,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
            Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
            Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          end
        elseif(srcJob == 21) then
          setGripper(70,100,0)
          --setGripperCheck( {pos=70,speed=100,force=0},3 )  --// Open the Gripper ,status 3
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          interfaceOut[5] = 702 ----- axis 7 Cobas Pure Rack Holder
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P112,"User=6 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(coordinateArrSrcDest[1],"User=6 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          coordinateArr = setCoordinateDiffPos_z(coordinateArrSrcDest[1],stn2_z_diff_pick_val)
          Move(coordinateArr,"User=6 Tool=1 SpeedS=10 AccelS=10 CP=0 SYNC=1")
          --setGripper(0,50,100)
          setGripperCheck( {pos=0,speed=50,force=100},2 )  --// Close the Gripper ,status 2
          Move(coordinateArrSrcDest[1],"User=6 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")
          Go(P112,"User=6 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          --Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          Go(P192,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          interfaceOut[5] = 704 ----- axis 7 cam 2 home
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          --Go(P114,"User=3 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          Go(P193,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P118,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Move(P115,"User=3 Tool=1 SpeedS=2 AccelS=50 CP=0 SYNC=1")
          --setGripper(100,50,100)
          setGripperCheck( {pos=100,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Move(P118,"User=3 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")
          --Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P193,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P192,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          setGripper(0,50,100)
          --setGripperCheck( {pos=0,speed=50,force=100},3 )  --// Close the Gripper ,status 3
          reset_jobs()
        elseif(srcJob == 91) then   --// Pick Rack from Sysmex Rack Holder
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          interfaceOut[5] = 707 ----- axis 7 sysmex home
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          setGripper(0,50,100)
          --setGripperCheck( {pos=0,speed=50,force=100},3 )  --// Close the Gripper ,status 3
          Go(P119,"User=4 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          x_val = coordinateArrSrcDest[1].coordinate[1]
          coordinateArr = setCoordinatePos_x({coordinate=P202.coordinate},x_val)
          Go(coordinateArr,"User=4 Tool=1 CP=100 Speed=50 Accel=100 SYNC=0")
          coordinateArr = setCoordinatePos_x({coordinate=P203.coordinate},x_val)
          Move(coordinateArr,"User=4 Tool=1 CP=100 SpeedS=50 AccelS=100 SYNC=1")
          coordinateArr = setCoordinatePos_x({coordinate=P202.coordinate},x_val)
          Move(coordinateArr,"User=4 Tool=1 CP=100 SpeedS=100 AccelS=100 SYNC=0")
          Go(P119,"User=4 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(coordinateArrSrcDest[1],"User=4 Tool=1 CP=100 Speed=20 Accel=100 SYNC=0")
          x_val = coordinateArrSrcDest[1].coordinate[1]
          coordinateArr = setCoordinatePos_x({coordinate=P182.coordinate},x_val)
          Move(coordinateArr,"User=4 Tool=1 CP=100 SpeedS=50 AccelS=100 SYNC=1")
          coordinateArr = setCoordinatePos_x({coordinate=P183.coordinate},x_val)
          Move(coordinateArr,"User=4 Tool=1 CP=100 SpeedS=10 AccelS=100 SYNC=1")
          coordinateArr = setCoordinatePos_x({coordinate=P184.coordinate},x_val)
          Move(coordinateArr,"User=4 Tool=1 CP=100 SpeedS=10 AccelS=100 SYNC=1")
          coordinateArr = setCoordinatePos_x({coordinate=P182.coordinate},x_val)
          Move(coordinateArr,"User=4 Tool=1 CP=100 SpeedS=50 AccelS=100 SYNC=1")
          setGripper(70,50,100)
          --setGripperCheck( {pos=70,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn9_rack_z_val)
          Move(coordinateArr,"User=4 Tool=1 SpeedS=10 AccelS=5 CP=0 SYNC=1")
          --setGripper(0,50,100)
          setGripperCheck( {pos=0,speed=50,force=100},2 )  --// Close the Gripper ,status 2
          local updatedPos = GetPose()
          coordinateArr = setCoordinatePos_y({coordinate=updatedPos.coordinate},stn9_y_slide_out)
          Move(coordinateArr,"User=4 Tool=1 SpeedS=3 AccelS=1 CP=0 SYNC=1")
          Go(P119,"User=4 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P120,"User=4 Tool=1 CP=100 Speed=50 Accel=100 SYNC=0")
          DOExecute(9, ON) --// Turn on process indicator sysmex 
          Move(P121,"User=4 Tool=1 SpeedS=3 AccelS=1 CP=0 SYNC=1")
          --setGripper(70,50,100)
          setGripperCheck( {pos=70,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Move(P120,"User=4 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=1")
          DOExecute(9, OFF) --// Turn off process indicator sysmex 
          Go(P119,"User=4 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          reset_jobs()
        elseif(srcJob == 71) then   --// Pick Rack from Sysmex Machine
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          interfaceOut[5] = 707 ----- axis 7 sysmex home
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          setGripper(0,50,100)
          --setGripperCheck( {pos=0,speed=50,force=100},3 )  --// Close the Gripper ,status 3
          Go(P119,"User=4 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          Go(P132,"User=4 Tool=1 CP=100 Speed=20 Accel=100 SYNC=1")
          Go(P122,"User=4 Tool=1 CP=100 Speed=20 Accel=5 SYNC=1")
          Go(P180,"User=4 Tool=1 CP=100 Speed=20 Accel=5 SYNC=1")
          Go(P181,"User=4 Tool=1 CP=100 Speed=20 Accel=5 SYNC=1")
          Go(P122,"User=4 Tool=1 CP=100 Speed=20 Accel=5 SYNC=1")
          setGripper(100,50,100)
          --setGripperCheck( {pos=100,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Move(P123,"User=4 Tool=1 SpeedS=5 AccelS=2 CP=0 SYNC=1")
          --setGripper(0,50,100)
          setGripperCheck( {pos=0,speed=50,force=100},2 )  --// Close the Gripper ,status 2
          Move(P133,"User=4 Tool=1 CP=0 SpeedS=3 AccelS=1 SYNC=1")
          Move(P134,"User=4 Tool=1 CP=0 SpeedS=5 AccelS=2 SYNC=1")
          Go(P132,"User=4 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P119,"User=4 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          coordinateArr = setCoordinatePos_y(coordinateArrSrcDest[1],stn9_y_slide_out)
          Move(coordinateArr,"User=4 Tool=1 SpeedS=50 AccelS=100 CP=0 SYNC=1")
          local updatedPos = GetPose()
          coordinateArr = setCoordinatePos_z({coordinate=updatedPos.coordinate},stn9_rack_z_val)
          Move(coordinateArr,"User=4 Tool=1 SpeedS=50 AccelS=100 CP=0 SYNC=1")
          local updatedPos = GetPose()
          coordinateArr = setCoordinatePos_y({coordinate=updatedPos.coordinate},stn9_y_slide_in)
          Move(coordinateArr,"User=4 Tool=1 SpeedS=3 AccelS=100 CP=0 SYNC=1")
          --setGripper(70,50,100)
          setGripperCheck( {pos=70,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Move(coordinateArrSrcDest[1],"User=4 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")
          Go(P119,"User=4 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          reset_jobs()
        elseif(srcJob == 141) then   --// Pick Rack from Cobas Pure Rack Holder
          setGripper(0,100,100) --// Close the gripper
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          interfaceOut[5] = 704 ----- axis 7 cam 2 home
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          --Go(P117,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P200,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P201,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          Go(P200,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P117,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          setGripper(100,100,100)
          --setGripperCheck( {pos=100},3 )  --// Open the Gripper ,status 3
          Move(P116,"User=3 Tool=1 SpeedS=100 AccelS=100 CP=0 SYNC=1")
          --setGripper(0,50,100)
          setGripperCheck( {pos=0,speed=50,force=100},2 )  --// Close the Gripper ,status 2
          Move(P117,"User=3 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")
          Go(P130,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P114,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          interfaceOut[5] = 708 ----- axis 7 Cobas Pure
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P111,"User=0 Tool=1 CP=100 Speed=50 Accel=100 SYNC=0")
          DOExecute(9, ON) --// Turn on process indicator Cobas Pure
          Move(P110,"User=0 Tool=1 SpeedS=5 AccelS=2 CP=0 SYNC=1")
          Move(P109,"User=0 Tool=1 SpeedS=2 AccelS=1 CP=0 SYNC=1")
          --setGripper(100,50,100)
          setGripperCheck( {pos=100,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Move(P110,"User=0 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=1")
          DOExecute(9, OFF) --// Turn off process indicator Cobas Pure
          Go(P111,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          reset_jobs()
        elseif(srcJob == 93) then   --// Pick tube from Sysmex Rack Holder
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          interfaceOut[5] = 707 ----- axis 7 sysmex home
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P30,"User=4 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")
          setGripper(50,50,100)
          --setGripperCheck( {pos=50,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Go(coordinateArrSrcDest[1],"User=4 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn9_z_pick_val)
          Move(coordinateArr,"User=4 Tool=1 SpeedS=100 AccelS=100 CP=0 SYNC=1")
          --setGripper(0,50,50)
          setGripperCheck( {pos=0,speed=50,force=50},2 )  --// Close the Gripper ,status 2
          Move(coordinateArrSrcDest[1],"User=4 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")
          Go(P30,"User=4 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          interfaceOut[5] = 706 ----- axis 7 Centrifuge Home
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P93,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")
          Go(coordinateArrSrcDest[2],"User=5 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")  --// Src Pose
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],stn11_z_val)
          Move(coordinateArr,"User=5 Tool=1 SpeedS=50 AccelS=100 CP=0 SYNC=1")  
          --setGripper(50,50,50)
          setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
          Move(coordinateArrSrcDest[2],"User=5 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")  
          Go(P93,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")
          Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")            
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          setGripper(0,50,50)
          --setGripperCheck( {pos=0,speed=50,force=50},3 )  --// Close the Gripper ,status 3
          reset_jobs()
        elseif(srcJob == 31) then   --// Pick tube from Compact Max
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          interfaceOut[5] = 706 ----- axis 7 Centrifuge Home
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P124,"User=2 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          setGripper(50,50,100)
          --setGripperCheck( {pos=50,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Go(coordinateArrSrcDest[1],"User=2 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn3_z_pick_val)
          Move(coordinateArr,"User=2 Tool=1 SpeedS=10 AccelS=100 CP=0 SYNC=1")
          --setGripper(0,50,50)
          setGripperCheck( {pos=0,speed=50,force=50},2 )  --// Close the Gripper ,status 2
          Move(coordinateArrSrcDest[1],"User=2 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")
          Go(P124,"User=2 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          Go(P93,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")
          Go(coordinateArrSrcDest[2],"User=5 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")  --// Src Pose
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],stn11_z_val)
          Move(coordinateArr,"User=5 Tool=1 SpeedS=50 AccelS=100 CP=0 SYNC=1")  
          --setGripper(50,50,50)
          setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
          Move(coordinateArrSrcDest[2],"User=5 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")  
          Go(P93,"User=3 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0")
          Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")            
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          setGripper(0,50,50)
          --setGripperCheck( {pos=0,speed=50,force=50},3 )  --// Close the Gripper ,status 3
          reset_jobs()
        elseif(srcJob == 152) then   --// Pick Basket from Cobas Pure
          --[[
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          interfaceOut[5] = 708 ----- axis 7 Cobas Pure Machine
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P98,"User=0 Tool=1 Speed=100 Accel=100 CP=50 SYNC=1") --// Cobas Pure Home Pos
          setGripper(100,100,100)
          --setGripperCheck( {pos=100},3 )  --// Open the Gripper ,status 3
          Go(P164,"User=0 Tool=1 Speed=100 Accel=100 CP=50 SYNC=1") --// Cobas Pure Approach 1
          Go(P96,"User=0 Tool=1 Speed=100 Accel=100 CP=50 SYNC=1") --// Cobas Pure Basket Pos
          setGripper(30,100,100)
          --setGripperCheck( {pos=30},3 )  --// Open the Gripper ,status 3
          Move(P163,"User=0 Tool=1 SpeedS=20 AccelS=20 CP=0 SYNC=1") --// Cobas Pure Approach 2
          --setGripper(0,50,100) --// Gripper Closed
          setGripperCheck( {pos=0,speed=50,force=50},2 )  --// Close the Gripper ,status 2 --AP
          Move(P164,"User=0 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --// Cobas Pure Approach 1
          Go(P98,"User=0 Tool=1 Speed=5 Accel=5 CP=50 SYNC=1") --// Cobas Pure Home Pos
          interfaceOut[5] = 703 ----- axis 7 Cobas Pure Rack Holder slow speed
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P152,"User=6 Tool=1 Speed=5 Accel=5 CP=50 SYNC=1") --// Stn 15-16 Basket Help
          Go(P167,"User=6 Tool=1 Speed=5 Accel=5 CP=50 SYNC=1") --// Stn 15 Basket Approach 1 
          Move(P165,"User=6 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --// 
          --setGripper(60,50,100)
          setGripperCheck( {pos=60,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Move(P165,"User=6 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --// 
          setGripper(0,50,100)
          --setGripperCheck( {pos=0,speed=50,force=100},3 )  --// Close the Gripper ,status 3 --AP
          Move(P166,"User=6 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --//
          setGripper(100,50,100)
          --setGripperCheck( {pos=100,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          --Go(P165,"User=6 Tool=1 Speed=20 Accel=20 CP=50 SYNC=1") --// Stn 15 Basket Pos
          Go(P167,"User=6 Tool=1 Speed=100 Accel=100 CP=50 SYNC=0") --// Stn 15 Basket Approach 1 
          Go(P152,"User=6 Tool=1 Speed=100 Accel=100 CP=50 SYNC=0") --// Stn 15-16 Basket Help
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")       
          setGripper(0,50,100) --Gripper Closed     
          --setGripperCheck( {pos=0,speed=50,force=100},3 )  --// Close the Gripper ,status 3
          ]]
          setGripper(100,50,100) --//Open the gripper
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          interfaceOut[5] = 710 ----- axis 7 Cobas Pure loading/unloading
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P253,"User=0 Tool=1 Speed=100 Accel=100 CP=50 SYNC=0") --// Pick Help 1
          Move(P254,"User=0 Tool=1 SpeedS=50 AccelS=10 CP=0 SYNC=1") --// Pick Help 2
          setGripper(30,100,100)
          Move(P255,"User=0 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --// Pick Pose
          setGripperCheck( {pos=0,speed=50,force=100},2 )  --// Close the Gripper ,status 2 
          Move(P256,"User=0 Tool=1 SpeedS=1 AccelS=1 CP=0 SYNC=1") --// Pick Help 3
          Move(P257,"User=0 Tool=1 SpeedS=1 AccelS=1 CP=0 SYNC=1") --// Pick Help 4
          Move(P258,"User=0 Tool=1 SpeedS=1 AccelS=1 CP=0 SYNC=1") --// Pick Help 5
          Go(P259,"User=0 Tool=1 Speed=2 Accel=2 CP=0 SYNC=1") --// Drive Pos
          Go(P260,"User=6 Tool=1 Speed=2 Accel=2 CP=0 SYNC=1") --// Place Help 1
          Go(P261,"User=6 Tool=1 Speed=2 Accel=2 CP=0 SYNC=1") --// Place Help 2
          Move(P262,"User=6 Tool=1 SpeedS=1 AccelS=1 CP=0 SYNC=1") --// Place Pose
          Move(P263,"User=6 Tool=1 SpeedS=1 AccelS=1 CP=0 SYNC=1") --// Place Slide Pose
          setGripperCheck( {pos=100,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          --setGripper(100,50,100) --//Open the gripper
          Go(P264,"User=6 Tool=1 Speed=1 Accel=1 CP=0 SYNC=1") --// Place Help 3
          Go(P265,"User=6 Tool=1 Speed=100 Accel=100 CP=0 SYNC=1") --// Place Help 4
          Go(P260,"User=6 Tool=1 Speed=100 Accel=100 CP=0 SYNC=1") --// Place Help 1
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          reset_jobs()
        elseif(srcJob == 162) then   --// Pick Basket from Cobas Pure
          --[[
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          interfaceOut[5] = 708 ----- axis 7 Cobas Pure Machine
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P98,"User=0 Tool=1 Speed=100 Accel=50 CP=50 SYNC=1") --// Cobas Pure Home Pos
          setGripper(100,100,100)
          --setGripperCheck( {pos=100},3 )  --// Open the Gripper ,status 3
          Go(P169,"User=0 Tool=1 Speed=100 Accel=50 CP=50 SYNC=1") --// Cobas Pure Approach 1
          Go(P96,"User=0 Tool=1 Speed=100 Accel=50 CP=50 SYNC=1") --// Cobas Pure Basket Pos
          setGripper(30,100,100)
          --setGripperCheck( {pos=30},3 )  --// Close the Gripper ,status 3
          Move(P168,"User=0 Tool=1 SpeedS=20 AccelS=20 CP=0 SYNC=1") --// Cobas Pure Approach 2
          --setGripper(0,50,100) --// Gripper Closed
          setGripperCheck( {pos=0,speed=50,force=100},2 )  --// Close the Gripper ,status 2 --AP
          Move(P169,"User=0 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --// Cobas Pure Approach 1
          Go(P98,"User=0 Tool=1 Speed=2 Accel=2 CP=50 SYNC=1") --// Cobas Pure Home Pos
          interfaceOut[5] = 703 ----- axis 7 Cobas Pure Rack Holder slow speed
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P152,"User=6 Tool=1 Speed=5 Accel=5 CP=50 SYNC=1") --// Stn 15-16 Basket Help
          Go(P172,"User=6 Tool=1 Speed=5 Accel=5 CP=50 SYNC=1") --// Stn 16 Basket Approach 1 
          Move(P170,"User=6 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --// Stn 16 Basket Approach 2
          setGripper(60,50,100)
          --setGripperCheck( {pos=60,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Move(P170,"User=6 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --// Stn 16 Basket Approach 2
          setGripper(0,50,100)
          --setGripperCheck( {pos=0,speed=50,force=100},3 )  --// Close the Gripper ,status 3  --AP
          Move(P171,"User=6 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --// Stn 16 Basket Approach 2
          --setGripper(100,50,100)
          setGripperCheck( {pos=100,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Go(P172,"User=6 Tool=1 Speed=100 Accel=100 CP=50 SYNC=0") --// Stn 16 Basket Pos
          Go(P152,"User=6 Tool=1 Speed=100 Accel=100 CP=50 SYNC=0") --// Stn 15-16 Basket Help
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")   
          setGripper(0,50,100) --Gripper Closed
          --setGripperCheck( {pos=0,speed=50,force=100},3 )  --// Close the Gripper ,status 3
          ]]
          setGripper(100,50,100) --//Open the gripper
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          interfaceOut[5] = 710 ----- axis 7 Cobas Pure loading/unloading
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P226,"User=0 Tool=1 Speed=100 Accel=100 CP=50 SYNC=0") --// Pick Help 1
          Move(P227,"User=0 Tool=1 SpeedS=50 AccelS=10 CP=0 SYNC=1") --// Pick Help 2
          setGripper(30,100,100)
          Move(P228,"User=0 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --// Pick Pose
          setGripperCheck( {pos=0,speed=50,force=100},2 )  --// Close the Gripper ,status 2 
          Move(P229,"User=0 Tool=1 SpeedS=1 AccelS=2 CP=0 SYNC=1") --// Pick Help 3
          Move(P230,"User=0 Tool=1 SpeedS=1 AccelS=2 CP=0 SYNC=1") --// Pick Help 4
          Move(P231,"User=0 Tool=1 SpeedS=1 AccelS=2 CP=0 SYNC=1") --// Pick Help 5
          Go(P232,"User=0 Tool=1 Speed=2 Accel=2 CP=0 SYNC=1") --// Drive Pos
          Go(P233,"User=6 Tool=1 Speed=2 Accel=2 CP=0 SYNC=1") --// Place Help 1
          Go(P234,"User=6 Tool=1 Speed=2 Accel=2 CP=0 SYNC=1") --// Place Help 2
          Move(P235,"User=6 Tool=1 SpeedS=2 AccelS=1 CP=0 SYNC=1") --// Place Help 3
          Move(P236,"User=6 Tool=1 SpeedS=1 AccelS=1 CP=0 SYNC=1") --// Place Pose
          Move(P237,"User=6 Tool=1 SpeedS=1 AccelS=1 CP=0 SYNC=1") --// Place Slide Pose
          setGripperCheck( {pos=100,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          --setGripper(100,50,100) --//Open the gripper
          Move(P268,"User=6 Tool=1 SpeedS=1 AccelS=1 CP=0 SYNC=1") --// Place Help Pull 
          Go(P238,"User=6 Tool=1 Speed=1 Accel=1 CP=0 SYNC=1") --// Place Help 4
          Go(P239,"User=6 Tool=1 Speed=100 Accel=100 CP=0 SYNC=1") --// Place Help 5
          Go(P234,"User=6 Tool=1 Speed=100 Accel=100 CP=0 SYNC=1") --// Place Help 2
          Go(P233,"User=6 Tool=1 Speed=100 Accel=100 CP=0 SYNC=1") --// Place Help 1
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          reset_jobs()
        elseif(srcJob == 151) then   --// Pick Basket from Cobas Pure Rack 1
          if (test == true) then
            print("Cobas Pure Basket Picking skipped")
          else
            --[[
            Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
            interfaceOut[5] = 702 ----- axis 7 Cobas Pure Rack Holder
            statusACK = send_UDP_ACK_2()
            interfaceOut[5] = 0
            setGripper(100,50,100)
            --setGripperCheck( {pos=100,speed=50,force=100},3 )  --// Open the Gripper ,status 3
            Go(P152,"User=6 Tool=1 Speed=20 Accel=20 CP=100 SYNC=0") --// Stn 15-16 Basket Help
            Go(P162,"User=6 Tool=1 Speed=20 Accel=20 CP=50 SYNC=1") --// Stn 15 Basket Help 1
            Go(P75,"User=6 Tool=1 Speed=50 Accel=50 CP=50 SYNC=1") --// Stn 15 Basket Pos
            setGripper(40,100,100)
            --setGripperCheck( {pos=40},3 )  --// Open the Gripper ,status 3
            Go(P74,"User=6 Tool=1 Speed=20 Accel=20 CP=50 SYNC=1") --// Stn 15 Basket Approach 2
            --setGripper(0,50,100)
            setGripperCheck( {pos=0,speed=50,force=100}, 2 )  --// Close the Gripper ,status 2  --AP
            Move(P70,"User=6 Tool=1 SpeedS=5 AccelS=5 CP=50 SYNC=1") --// Stn 15 Basket Approach 1 
            Go(P152,"User=6 Tool=1 Speed=20 Accel=20 CP=50 SYNC=1") --// Stn 15-16 Basket Help
            Go(P98,"User=0 Tool=1 Speed=100 Accel=50 CP=50 SYNC=1") --// Cobas Pure Home Pos
            interfaceOut[5] = 709 ----- axis 7 Cobas Pure Home slow speed
            statusACK = send_UDP_ACK_2()
            interfaceOut[5] = 0
            Go(P94,"User=0 Tool=1 Speed=10 Accel=10 CP=50 SYNC=1") --// Cobas Pure Approach 1
            Move(P95,"User=0 Tool=1 SpeedS=2 AccelS=1 CP=0 SYNC=1") --// Cobas Pure Approach 2
            --setGripper(100,5,100) --Gripper Opened
            setGripperCheck( {pos=100,speed=5,force=100},3 )  --// Open the Gripper ,status 3
            --Sleep(2000)
            Go(P96,"User=0 Tool=1 Speed=100 Accel=100 CP=50 SYNC=0") --// Cobas Pure Basket Pos
            --setGripper(100,50,100) --Gripper Opened
            --setGripperCheck( {pos=100,speed=50,force=100},3 )  --// Open the Gripper ,status 3
            Go(P94,"User=0 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0") --// Cobas Pure Approach 1
            Go(P98,"User=0 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0") --// Cobas Pure Home Pos
            Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
            setGripper(0,50,100) --Gripper Closed      
            --setGripperCheck( {pos=0,speed=50,force=100},3 )  --// Close the Gripper ,status 3
            ]]
          setGripper(100,50,100) --//Open the gripper
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          interfaceOut[5] = 710 ----- axis 7 Cobas Pure loading/unloading
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P240,"User=6 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0") --//Pick Help 1
          Move(P241,"User=6 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=1") --//Pick Help 2
          setGripper(30,50,100) --//Close the gripper
          Move(P242,"User=6 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --//Pick Pose
          --setGripper(0,50,100) --//Close the gripper
          setGripperCheck( {pos=0,speed=50,force=100},2 )  --// Close the Gripper ,status 2
          Move(P243,"User=6 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --//Slide Pose
          Move(P244,"User=6 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --//Pick Help 3
          Move(P245,"User=6 Tool=1 SpeedS=5 AccelS=5 CP=0 SYNC=1") --//Pick Help 4
          Go(P246,"User=0 Tool=1 Speed=5 Accel=5 CP=0 SYNC=1") --//Place Drive
          Go(P247,"User=0 Tool=1 Speed=5 Accel=5 CP=0 SYNC=1") --//Place Help 1
          Sleep(2000)
          Move(P248,"User=0 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --//Place Help 2
          Move(P249,"User=0 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --//Place Help 3
          Move(P250,"User=0 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --//Place Pose
          --setGripper(100,50,100) --//Open the gripper
          setGripperCheck( {pos=50,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Go(P251,"User=0 Tool=1 Speed=50 Accel=50 CP=0 SYNC=1") --//Place Help 4
          Move(P252,"User=0 Tool=1 SpeedS=100 AccelS=100 CP=0 SYNC=1") --//Place Help 5
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
            reset_jobs()
          end
        elseif(srcJob == 161) then   --// Pick Basket from Cobas Pure Rack 2
          --[[
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          interfaceOut[5] = 702 ----- axis 7 Cobas Pure Rack Holder
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          setGripper(100,50,100)
          --setGripperCheck( {pos=100,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Go(P152,"User=6 Tool=1 Speed=20 Accel=20 CP=100 SYNC=0") --// Stn 15-16 Basket Help
          Go(P173,"User=6 Tool=1 Speed=20 Accel=20 CP=50 SYNC=0") --// Stn 15-16 Basket Help
          Go(P155,"User=6 Tool=1 Speed=50 Accel=50 CP=50 SYNC=1") --// Stn 16 Basket Pos
          setGripper(40,100,100)
          --setGripperCheck( {pos=40},3 )  --// Open the Gripper ,status 3
          Go(P154,"User=6 Tool=1 Speed=20 Accel=20 CP=50 SYNC=1") --// Stn 16 Basket Approach 2
          --setGripper(0,50,100)
          setGripperCheck( {pos=0,speed=50,force=100},2 )  --// Close the Gripper ,status 2  --AP
          Move(P153,"User=6 Tool=1 SpeedS=5 AccelS=5 CP=50 SYNC=1") --// Stn 16 Basket Approach 1 
          Go(P152,"User=6 Tool=1 Speed=20 Accel=20 CP=50 SYNC=1") --// Stn 15-16 Basket Help
          Go(P98,"User=0 Tool=1 Speed=100 Accel=50 CP=50 SYNC=1") --// Cobas Pure Home Pos
          interfaceOut[5] = 709 ----- axis 7 Cobas Pure Home slow speed
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P174,"User=0 Tool=1 Speed=10 Accel=10 CP=50 SYNC=1") --// Cobas Pure Approach 1
          Move(P175,"User=0 Tool=1 SpeedS=2 AccelS=1 CP=0 SYNC=1") --// Cobas Pure Approach 2
          --setGripper(100,50,100) --Gripper Opened
          setGripperCheck( {pos=100,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Go(P96,"User=0 Tool=1 Speed=100 Accel=50 CP=50 SYNC=1") --// Cobas Pure Basket Pos
          --setGripper(100,50,100) --Gripper Opened
          --setGripperCheck( {pos=100,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Go(P174,"User=0 Tool=1 Speed=100 Accel=100 CP=50 SYNC=0") --// Cobas Pure Approach 1
          Go(P98,"User=0 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0") --// Cobas Pure Home Pos
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          setGripper(0,50,100) --Gripper Closed
          --setGripperCheck( {pos=0,speed=50,force=100},3 )  --// Close the Gripper ,status 3
          ]]
          setGripper(100,50,100) --//Open the gripper
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          interfaceOut[5] = 710 ----- axis 7 Cobas Pure loading/unloading
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P204,"User=6 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0") --//Pick Help 1
          Go(P205,"User=6 Tool=1 Speed=100 Accel=100 CP=100 SYNC=0") --//Pick Help 2
          Move(P206,"User=6 Tool=1 SpeedS=10 AccelS=10 CP=0 SYNC=1") --//Pick Help 3
          setGripper(30,50,100) --//Close the gripper
          Move(P207,"User=6 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --//Pick Pose
          --setGripper(0,50,100) --//Close the gripper
          setGripperCheck( {pos=0,speed=50,force=100},2 )  --// Close the Gripper ,status 2
          Move(P208,"User=6 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --//Slide Pose
          Move(P209,"User=6 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --//Pick Help 4
          Move(P210,"User=6 Tool=1 SpeedS=5 AccelS=5 CP=0 SYNC=1") --//Pick Help 5
          Move(P218,"User=6 Tool=1 SpeedS=5 AccelS=5 CP=0 SYNC=1") --//Pick Help 6
          Go(P219,"User=0 Tool=1 Speed=5 Accel=5 CP=0 SYNC=1") --//Place Drive
          Go(P220,"User=0 Tool=1 Speed=5 Accel=5 CP=0 SYNC=1") --//Place Help 1
          Sleep(2000)
          Move(P221,"User=0 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --//Place Help 2
          Move(P222,"User=0 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --//Place Help 3
          Move(P223,"User=0 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --//Place Pose
          --setGripper(100,50,100) --//Open the gripper
          setGripperCheck( {pos=50,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Go(P224,"User=0 Tool=1 Speed=50 Accel=50 CP=0 SYNC=1") --//Place Help 4
          Move(P225,"User=0 Tool=1 SpeedS=100 AccelS=100 CP=0 SYNC=1") --//Place Help 5
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          setGripper(0,50,100) --//Close the gripper
          reset_jobs()
        elseif(srcJob == 171) then   --// Pick Rack  from Cobas Pure Basket Holder 1 
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          interfaceOut[5] = 702 ----- axis 7 Cobas Pure Rack Holder
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          setGripper(50,50,100)
          Go(P112,"User=6 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0") --// Stn 2 Help Pos
          Go(coordinateArrSrcDest[1],"User=7 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          x_val = coordinateArrSrcDest[1].coordinate[1]
          Move(P196,"User=7 Tool=1 CP=100 SpeedS=100 AccelS=100 SYNC=1")
          Move(P197,"User=7 Tool=1 CP=100 SpeedS=50 AccelS=50 SYNC=1")
          coordinateArr = setCoordinatePos_x({coordinate=P197.coordinate},x_val - stn17_rack_x_in_diff_val)
          Move(coordinateArr,"User=7 Tool=1 CP=100 SpeedS=5 AccelS=5 SYNC=1")
          Move(P197,"User=7 Tool=1 CP=100 SpeedS=10 AccelS=10 SYNC=1")
          Move(P196,"User=7 Tool=1 CP=100 SpeedS=100 AccelS=100 SYNC=0")
          Go(coordinateArrSrcDest[1],"User=7 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          setGripper(40,50,100)
          --setGripperCheck( {pos=40,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn17_rack_z_val)
          Move(coordinateArr,"User=7 Tool=1 SpeedS=10 AccelS=10 CP=0 SYNC=1")
          --setGripper(0,50,50)
          setGripperCheck( {pos=0,speed=50,force=50},2 )  --// Close the Gripper ,status 2
          --Move(P158,"User=6 Tool=1 SpeedS=1 AccelS=1 CP=0 SYNC=1") --// Stn 17 Slide out
          --Move(P159,"User=6 Tool=1 SpeedS=20 AccelS=5 CP=0 SYNC=1") --// Stn 17 Slide out up
          Move(P189,"User=7 Tool=1 SpeedS=1 AccelS=1 CP=0 SYNC=1") --// Stn 17 Slide out
          setGripper(40,50,50)
          setGripper(0,50,50)
          Sleep(1000)
          Move(P190,"User=7 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0") --// Stn 17 Slide out up
          Go(P160,"User=6 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0") --// Stn 17-18 Rack Help Pos
          Go(coordinateArrSrcDest[2],"User=6 Tool=1 Speed=50 Accel=100 CP=100 SYNC=0")  --// Src Pose
          coordinateArr = setCoordinateDiffPos_z(coordinateArrSrcDest[2],stn2_z_diff_plc_val)
          Move(coordinateArr,"User=6 Tool=1 SpeedS=1 AccelS=100 CP=0 SYNC=1")  
          --setGripper(50,50,50)
          setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
          Move(coordinateArrSrcDest[2],"User=6 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")  
          --Go(P160,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1") --// Stn 17-18 Rack Help Pos
          Go(P112,"User=6 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0") --// Stn 2 Help Pos
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          setGripper(0,50,50)
          --setGripperCheck( {pos=0,speed=50,force=50},3 )  --// Close the Gripper ,status 3
          reset_jobs()
        elseif(srcJob == 181) then   --// Pick Rack  from Cobas Pure Basket Holder 2 
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          interfaceOut[5] = 702 ----- axis 7 Cobas Pure Rack Holder
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          setGripper(50,50,100)
          Go(P112,"User=6 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0") --// Stn 2 Help Pos
          Go(coordinateArrSrcDest[1],"User=7 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")
          x_val = coordinateArrSrcDest[1].coordinate[1]
          Move(P198,"User=7 Tool=1 CP=100 SpeedS=100 AccelS=100 SYNC=1")
          Move(P199,"User=7 Tool=1 CP=100 SpeedS=50 AccelS=50 SYNC=1")
          coordinateArr = setCoordinatePos_x({coordinate=P199.coordinate},x_val + stn18_rack_x_in_diff_val)
          Move(coordinateArr,"User=7 Tool=1 CP=100 SpeedS=5 AccelS=5 SYNC=1")
          Move(P199,"User=7 Tool=1 CP=100 SpeedS=10 AccelS=10 SYNC=1")
          Move(P198,"User=7 Tool=1 CP=100 SpeedS=100 AccelS=100 SYNC=0")
          Go(coordinateArrSrcDest[1],"User=7 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          setGripper(40,50,100)
          --setGripperCheck( {pos=40,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn18_rack_z_val)
          Move(coordinateArr,"User=7 Tool=1 SpeedS=10 AccelS=10 CP=0 SYNC=1")
          --setGripper(0,50,50)
          setGripperCheck( {pos=0,speed=50,force=50},2 )  --// Close the Gripper ,status 2
          Move(P156,"User=7 Tool=1 SpeedS=2 AccelS=2 CP=0 SYNC=1") --// Stn 18 Slide out 
          setGripper(40,50,50)
          setGripper(0,50,50)
          Sleep(1000)
          Move(P157,"User=7 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0") --// Stn 18 Slide out up
          Go(P160,"User=6 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0") --// Stn 17-18 Rack Help Pos
          Go(coordinateArrSrcDest[2],"User=6 Tool=1 Speed=50 Accel=100 CP=100 SYNC=0")  --// Src Pose
          coordinateArr = setCoordinateDiffPos_z(coordinateArrSrcDest[2],stn2_z_diff_plc_val)
          Move(coordinateArr,"User=6 Tool=1 SpeedS=1 AccelS=100 CP=0 SYNC=1")  
          --setGripper(50,50,50)
          setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
          Move(coordinateArrSrcDest[2],"User=6 Tool=1 SpeedS=100 AccelS=100 CP=100 SYNC=0")  
          --Go(P160,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1") --// Stn 17-18 Rack Help Pos
          Go(P112,"User=6 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0") --// Stn 2 Help Pos
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          setGripper(0,50,50)
          --setGripperCheck( {pos=0,speed=50,force=100},3 )  --// Close the Gripper ,status 3
          reset_jobs()
        elseif(srcJob == 172) then   --// Pick Tube  from Cobas Pure Basket Holder 1 
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          interfaceOut[5] = 702 ----- axis 7 Cobas Pure Rack Holder
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P112,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1") --// Stn 2 Help Pos
          --setGripper(40,50,100)
          setGripperCheck( {pos=40,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Go(coordinateArrSrcDest[1],"User=7 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn17_z_val)
          Move(coordinateArr,"User=7 Tool=1 SpeedS=10 AccelS=10 CP=0 SYNC=1")
          --setGripper(0,5,5)
          setGripperCheck( {pos=0,speed=5,force=5},2 )  --// Close the Gripper ,status 2
          Move(coordinateArrSrcDest[1],"User=7 Tool=1 SpeedS=10 AccelS=10 CP=0 SYNC=1")
          Go(P112,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1") --// Stn 2 Help Pos
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          interfaceOut[5] = 706 ----- axis 7 Centrifuge Home
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P93,"User=3 Tool=1 Speed=100 Accel=50 CP=50 SYNC=1")
          Go(coordinateArrSrcDest[2],"User=5 Tool=1 Speed=100 Accel=50 CP=0 SYNC=1")  --// Src Pose
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],stn11_z_val)
          Move(coordinateArr,"User=5 Tool=1 SpeedS=5 AccelS=2 CP=0 SYNC=1")  
          --setGripper(50,50,50)
          setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
          Move(coordinateArrSrcDest[2],"User=5 Tool=1 SpeedS=100 AccelS=50 CP=100 SYNC=0")  
          --setGripper(0,50,50)
          setGripperCheck( {pos=0,speed=50,force=100},3 )  --// Close the Gripper ,status 3
          Go(P93,"User=3 Tool=1 Speed=100 Accel=100 CP=50 SYNC=0")
          Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")            
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          reset_jobs()
        elseif(srcJob == 182) then   --// Pick Tube  from Cobas Pure Basket Holder 2 
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          interfaceOut[5] = 702 ----- axis 7 Cobas Pure Rack Holder
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P112,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          --setGripper(40,50,100)
          setGripperCheck( {pos=40,speed=50,force=100},3 )  --// Open the Gripper ,status 3
          Go(coordinateArrSrcDest[1],"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[1],stn17_z_val)
          Move(coordinateArr,"User=6 Tool=1 SpeedS=5 AccelS=2 CP=0 SYNC=1")
          --setGripper(0,5,5)
          setGripperCheck( {pos=0,speed=5,force=5},2 )  --// Close the Gripper ,status 2
          Move(coordinateArrSrcDest[1],"User=6 Tool=1 SpeedS=10 AccelS=10 CP=0 SYNC=1")
          Go(P112,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          interfaceOut[5] = 706 ----- axis 7 Centrifuge Home
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P93,"User=3 Tool=1 Speed=100 Accel=50 CP=50 SYNC=1")
          Go(coordinateArrSrcDest[2],"User=5 Tool=1 Speed=100 Accel=50 CP=0 SYNC=1")  --// Src Pose
          coordinateArr = setCoordinatePos_z(coordinateArrSrcDest[2],stn11_z_val)
          Move(coordinateArr,"User=5 Tool=1 SpeedS=5 AccelS=2 CP=0 SYNC=1")  
          --setGripper(50,50,50)
          setGripperCheck( {pos=50,speed=50,force=50},3 )  --// Open the Gripper ,status 3
          Move(coordinateArrSrcDest[2],"User=5 Tool=1 SpeedS=100 AccelS=50 CP=100 SYNC=0")  
          --setGripper(0,50,50)
          setGripperCheck( {pos=0,speed=50,force=50},3 )  --// Open the Gripper ,status 3
          Go(P93,"User=3 Tool=1 Speed=100 Accel=100 CP=50 SYNC=0")
          Go(P29,"User=3 Tool=1 CP=100 Speed=100 Accel=100 SYNC=0")            
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1")
          reset_jobs()
        elseif(srcJob == 153) then   --// Slide Racks from Basket 1 
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          interfaceOut[5] = 702 ----- axis 7 Cobas Pure Rack Holder
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          setGripper(100,50,50)
          --setGripperCheck( {pos=100,speed=50,force=50},3 )  --// Open the Gripper ,status 3
          Go(P194,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=0") --// Stn 2 Help Pos
          Go(P76,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=0") --// Stn 15 Slide Approach 1 Pos
          Go(P77,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1") --// Stn 15 Slide Approach 2 Pos
          Move(P135,"User=6 Tool=1 CP=0 SpeedS=1 AccelS=1 SYNC=1") --// Stn 15 Slide Pos
          Move(P77,"User=6 Tool=1 CP=0 SpeedS=100 AccelS=100 SYNC=1") --// Stn 15 Slide Approach 2 Pos
          Go(P76,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=0") --// Stn 15 Slide Approach 1 Pos
          Go(P194,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=0") --// Stn 2 Help Pos
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          setGripper(0,50,50)
          --setGripperCheck( {pos=0,speed=50,force=50},3 )  --// Close the Gripper ,status 3
          reset_jobs()
        elseif(srcJob == 163) then   --// Slide Racks from Basket 2 
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          setGripper(100,50,50)
          --setGripperCheck( {pos=100,speed=50,force=50},3 )  --// Open the Gripper ,status 3
          interfaceOut[5] = 702 ----- axis 7 Cobas Pure Rack Holder
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P194,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=0") --// Stn 2 Help Pos
          Go(P78,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1") --// Stn 16 Slide Approach 1 Pos
          Go(P79,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1") --// Stn 16 Slide Approach 2 Pos
          Move(P136,"User=6 Tool=1 CP=0 SpeedS=1 AccelS=1 SYNC=1") --// Stn 16 Slide Pos
          Move(P79,"User=6 Tool=1 CP=0 SpeedS=100 AccelS=100 SYNC=1") --// Stn 15 Slide Approach 2 Pos
          Go(P78,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1") --// Stn 15 Slide Approach 1 Pos
          Go(P194,"User=6 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1") --// Stn 2 Help Pos
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          setGripper(0,50,50)
          --setGripperCheck( {pos=0,speed=50,force=50},3 )  --// Close the Gripper ,status 3
          reset_jobs()
        elseif(srcJob == 34) then   --// Compact max door open
          setGripper(0,50,50)
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=50 SYNC=1")
          interfaceOut[5] = 706 ----- axis 7 Centrifuge Home
          statusACK = send_UDP_ACK_2()
          interfaceOut[5] = 0
          Go(P266,"User=2 Tool=1 CP=100 Speed=100 Accel=50 SYNC=0")    --//Stn2 Open Help 1 Pos
          Move(P267,"User=2 Tool=1 CP=100 SpeedS=2 AccelS=5 SYNC=1")   --//Stn2 Open Help 2 Pos
          Move(P266,"User=2 Tool=1 CP=100 SpeedS=100 AccelS=100 SYNC=0")    --//Stn2 Open Help 1 Pos
          Go(P91,"User=0 Tool=1 CP=100 Speed=100 Accel=100 SYNC=1") 
          --setGripperCheck( {pos=0,speed=50,force=50},3 )  --// Close the Gripper ,status 3
          reset_jobs()
        else
          print("No Job")
        end
      end
      Sync()
    end
else
  print("Error in Connection")
end



