from pyVoIP.VoIP import VoIPPhone,VoIPCall

class VoipCalling:
    def __init__(self):
        self.voipPhoneClient=None
        self.mobile_number = int('03535')
        self.totalCallTimes = 1

    async def connectToVoipCalling(self, address, port, user, password, myIP, totalCalling):
        try:
            if self.voipPhoneClient is None:
                # self.fritzBoxClient = FritzCall(address='192.168.140.100', user='ROBO', password='ROBO_tb_14929') 
                self.voipPhoneClient = VoIPPhone(server=address, port=port, username=user, password=password , myIP=myIP)
                # self.mobile_number = number 
                self.totalCallTimes = totalCalling
        except Exception as e: 
            print(e)
            self.voipClient=None

    async def startCallViaVoipCalling(self):        
        try:
            if not self.voipPhoneClient:
                print("VOIP Client is none.")
                return
            self.voipPhoneClient.start()
        except Exception as e: 
            print(e)
            return
        
    async def endCallViaVoipCalling(self):        
        try:
            if not self.voipPhoneClient:
                print("VOIP Client is none.")
                return
            self.voipPhoneClient.stop()
        except Exception as e: 
            print(e)
            return
        
voipCalling = VoipCalling()  