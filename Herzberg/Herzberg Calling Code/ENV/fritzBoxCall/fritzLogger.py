import logging
from logging.handlers import TimedRotatingFileHandler
import os

# logpath="C:\\Users\\arunk\\OneDrive - Diabots\\Diabots\\Development\\Python_Programs\\QVITEC Work\\Herzberg\\HerzBergCallingCode\\ENV\\fritzBoxCall\\Logs"
logpath="C:\\Diabots\\Herzberg\\Logs"
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')


class Logger:
    def __init__(self,logLevel=logging.INFO):
        self.callsLogger=self.prepareLogger('calls',logLevel)

    def prepareLogger(self,name:str,logLevel):
        logger=logging.getLogger(name)  
        logger.setLevel(logLevel)
        file_handler = TimedRotatingFileHandler(os.path.join(logpath,name+'.log'),"midnight")        
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

logger=Logger(logging.INFO)
callslogger=logger.callsLogger
            
            




