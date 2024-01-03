import time
import serial
import asyncio
from settings import Settings
from stations import CommonError
from logger import initlogger,errorlogger

# Centrifuge Commands 
CLEAR_BC = b'A00685'
CHECK_LOCK_BC = b'A00635'
HATCH_STATUS_BC = b'A00528'
CHECK_ROTOR_POS = b'A00640'

OPEN_HATCH = b'A00526=0060	'
CLOSE_HATCH = b'A00526=0070'
IS_RUNNING = b'A00634'

SET_ROTOR_POS_1 = b'A00640=0401	'
SET_ROTOR_POS_2 = b'A00640=0002'
SET_ROTOR_POS_3 = b'A00640=0004'
SET_ROTOR_POS_4 = b'A00640=0008'

MOVE_TO_POSITION = b'A00526=0001'
# MOVE_TO_POSITION_FAST = b'A00526=0002'
MOVE_TO_POSITION_FAST = b'A00526=0002\x0D'
START_CENTRIFUGE = b'''A00521=0002
'''
STOP_CENTRIFUGE = b'A00521=0001	'
GET_RUNTIME_HRS = b'A00500'
GET_RUNTIME_MIN = b'A00502'
ACK = b'A\x06'


class CentrifugeInterface:
  def __init__(self):
    self.port = Settings.centrifugeComPort
    self.conn_centrifuge = None
    self.conn_timeout = 5
    self.establish_connection()

  def establish_connection(self):
    try:
      if self.conn_centrifuge is None:
        self.conn_centrifuge = serial.Serial(port=self.port,baudrate=9600,bytesize=serial.SEVENBITS,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE,timeout=self.conn_timeout)
        initlogger.info("Centrifuge connection established")
    except Exception as e:
      self.conn_centrifuge = None
      print(e)
      errorlogger.exception("Centrifuge connection Failed. {0}".format(e))

  def closeConnection(self):
    if self.conn_centrifuge is not None:        
        self.conn_centrifuge.close()
        initlogger.info("Centrifuge connection closed")

  async def check_lock(self):
    try:
      if self.conn_centrifuge is not None:
        result = await self.just_write(CHECK_LOCK_BC)
        return (list(result))[11] == 50
      return False
    except Exception as e:
        print ("Checking of Lock, Failed", e)
        return False

  async def hatch_open(self):
    try:
      if self.conn_centrifuge is not None:
        result = list(await self.clear_and_write(OPEN_HATCH))
        # await asyncio.sleep(Settings.centri_sleep)
        timeout = time.time() + 30
        status = False
        while time.time() < timeout:
            res = await self.hatch_status()
            if res[13] == 112 or res[13] == 116:
              status = True
              break
        return result[1] == 6 and status == True
      return False
    except:
        print ("Opening of Hatch failed")
        return False

  async def hatch_close(self):
    try:
      if self.conn_centrifuge is not None:
        result = list(await self.clear_and_write(CLOSE_HATCH))
        timeout = time.time() + 30
        status = False
        while time.time() < timeout:
            res = await self.hatch_status()
            if res[13] == 0:
              status = True
              break
        return result[1] == 6 and status == True
      return False
    except:
        print ("Closing of Hatch failed")
        return False

  async def hatch_status(self):
    try:
      if self.conn_centrifuge is not None:
        result = list(await self.clear_and_write(HATCH_STATUS_BC))
        return result
      return []
    except:
        print ("Getting of Hatch status failed")
        return []

  async def is_running(self):
    try:
      if self.conn_centrifuge is not None:
        read = [chr(r) for r in list(await self.just_write(IS_RUNNING))]
        return (list(bin(int.from_bytes(read[11].encode(),'big'))))[6] == '0'
      else:
        return False
    except Exception as e:
        print(e)
        raise CommonError( "Failed to check cetrifuge is running")

  async def set_rotor_position(self, position):
    try:
      if self.conn_centrifuge is not None:
        command, check = self.get_rotor_command(position)
        result = list(await self.clear_and_write(command))
        timeout = time.time() + 30
        rotor_set = False
        while time.time() < timeout:
            res = await self.check_rotor_position()
            if res[13] == check:
              rotor_set = True
              break
        return result[1] == 6 and rotor_set == True
      return False
    except Exception as e:
      print("Setting of rotor position Failed")
      print(e)
      return False

  async def check_rotor_position(self):
    try:
      if self.conn_centrifuge is not None:
        result = list(await self.clear_and_write(CHECK_ROTOR_POS))
        return result
      return []
    except Exception as e:
      print("Setting of rotor position Failed")
      print(e)
      return []

  async def start_centrifuge(self):
    try:
      if self.conn_centrifuge is not None:
        return (list(await self.clear_and_write(START_CENTRIFUGE)))[1] == 6
      return False
    except Exception as e:
      print("Starting of Centrifuge Failed")
      print(e)
      return False
  
  async def getRunTime(self):
    total_time_in_sec = -1
    try:
      if self.conn_centrifuge is not None:
        read_hrs = [chr(n) for n in list(await self.clear_and_write(GET_RUNTIME_HRS))]
        read_time_hrs = int((read_hrs[10] + read_hrs[11]), base=16)
        read_mins = [chr(n) for n in list(await self.just_write(GET_RUNTIME_MIN))]
        read_time_mins = int(read_mins[10] + read_mins[11], base=16)
        total_time_in_sec = (read_time_hrs * 60) +  read_time_mins * 60
        return total_time_in_sec
      else:
        return total_time_in_sec
    except Exception as e:
      print("Getting of run time Failed")
      print(e)
      return total_time_in_sec
  
  async def clear_and_write(self, write_command):
    self.conn_centrifuge.write(CLEAR_BC)
    await asyncio.sleep(0.1)
    self.conn_centrifuge.read(self.conn_centrifuge.in_waiting)
    self.conn_centrifuge.write(write_command)
    await asyncio.sleep(0.1)
    result = self.conn_centrifuge.read(self.conn_centrifuge.in_waiting)
    return result
    
  async def just_write(self, write_command):
    self.conn_centrifuge.write(write_command)
    await asyncio.sleep(0.1)
    return self.conn_centrifuge.read(self.conn_centrifuge.in_waiting)
  
  def get_rotor_command(self, position):
    if position == 1 :
      return SET_ROTOR_POS_1, 126
    elif position == 2 :
      return SET_ROTOR_POS_2, 125
    elif position == 3 :
      return SET_ROTOR_POS_3, 123
    elif position == 4 :
      return SET_ROTOR_POS_4, 119
