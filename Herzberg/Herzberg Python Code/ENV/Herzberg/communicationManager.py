from settings import Settings
from logger import jobslogger,errorlogger
from skpy import Skype
# from fritzconnection.lib.fritzcall import FritzCall


class CommunicationManager:
    def __init__(self):
            self.username:str =Settings.skuser
            self.pswrd:str=Settings.skpswrd
            self.toContacts=[Settings.toskypeid]
            self.client=None           
            self.fritzBoxClient=None
            self.mobile_number = ""
        
    async def connectToSkype(self):
        try:
            if self.client is None:
                self.client=Skype(self.username, self.pswrd)                              
        except Exception as e: 
            errorlogger.exception(e)
            self.client=None 

    # async def connectToFritzBox(self, address, user, password, number):
    #     try:
    #         if self.fritzBoxClient is None:
    #             # self.fritzBoxClient = FritzCall(address='192.168.140.100', user='ROBO', password='ROBO_tb_14929') 
    #             self.fritzBoxClient = FritzCall(address=address, user=user, password=password)    
    #             self.mobile_number = number         
    #     except Exception as e: 
    #         errorlogger.exception(e)
    #         self.fritzBoxClient=None     
    
    def reset(self):
        self.toContacts=[]    
    
    async def registerIds(self,commaNumbers:str):
        self.toContacts=commaNumbers.split(",")
        jobslogger.info("Registerd numbers:{0}".format(commaNumbers))

    async def sendMessage(self,message:str):
        try:
            if not self.client:
                errorlogger.error("skype client is none.")
                return
            for contact in self.toContacts:
                chat = self.client.contacts[contact].chat
                chat.sendMsg(message)
                jobslogger.info("sent message '{0}' to :{1}".format(message,contact))
        except Exception as e: 
            errorlogger.exception(e)
            return

    # async def callViaFritzBox(self):        
    #     try:
    #         if not self.fritzBoxClient:
    #             errorlogger.error("FritzBox Client is none.")
    #             return
    #         self.fritzBoxClient.dial(self.mobile_number)
    #     except Exception as e: 
    #         errorlogger.exception(e)
    #         return

commManager=CommunicationManager()  