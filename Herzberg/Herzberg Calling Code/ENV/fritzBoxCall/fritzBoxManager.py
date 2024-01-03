from fritzconnection.lib.fritzcall import FritzCall


class FritzBoxManager:
    def __init__(self):
            self.fritzBoxClient=None
            self.mobile_number = ''
            self.totalCallTimes = 1

    async def connectToFritzBox(self, address, user, password, number, totalCalling):
        try:
            if self.fritzBoxClient is None:
                # self.fritzBoxClient = FritzCall(address='192.168.140.100', user='ROBO', password='ROBO_tb_14929') 
                self.fritzBoxClient = FritzCall(address=address, user=user, password=password)    
                self.mobile_number = number 
                self.totalCallTimes = totalCalling
        except Exception as e: 
            print(e)
            self.fritzBoxClient=None     

    async def callViaFritzBox(self):        
        try:
            if not self.fritzBoxClient:
                print("FritzBox Client is none.")
                return
            self.fritzBoxClient.dial(self.mobile_number)
        except Exception as e: 
            print(e)
            return

fritzManager=FritzBoxManager()  

# fritzManager.connectToFritzBox('192.168.140.100', 'ROBO', 'ROBO_tb_14929', '+4917628066831')
# fritzManager.callViaFritzBox()