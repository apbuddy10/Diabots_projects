import os 
import sys
import subprocess
class MicroSipCalling:
    def __init__(self):
        self.voipPhoneClient=None
        self.mobile_number = ""
        self.totalCallTimes = 1
        self.exe_path = "C:/Diabots/Herzberg/MicroSIP/microsip.exe"
    async def initMicroSipCalling(self,mobile_number,sleepBetweenCalls,totalCalling):
        try:
          self.mobile_number  = mobile_number
          self.totalCallTimes = totalCalling
          self.sleepBetweenCalls = sleepBetweenCalls
        except Exception as e: 
            print(e)


    async def startCallMicroSipCalling(self):        
        try:
            # call_cmd = [self.exe_path,self.mobile_number]
            # subprocess.run(call_cmd)
            call_cmd = self.exe_path + " " + self.mobile_number
            os.system('cmd /c start ' + call_cmd)
        except Exception as e: 
            print(e)
            return
        
    async def endCallMicroSipCalling(self):        
        try:
            end_cmd = self.exe_path + " " + "/hangupall"
            os.system('cmd /c start ' + end_cmd)
            # subprocess.run(end_cmd)
        except Exception as e: 
            print(e)
            return
        
    async def killMicroSipExeCalling(self):        
        try:
            exe_cmd = "microsip.exe"
            os.system('taskkill /im ' + exe_cmd)
            # subprocess.run(end_cmd)
        except Exception as e: 
            print(e)
            return
        
microSipCalling = MicroSipCalling()  