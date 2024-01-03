from datetime import date
import logging
from logging.handlers import TimedRotatingFileHandler
import os

from settings import Settings
class PingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("aiohttp")==-1
        #record.getMessage().find("method.rpc_ping")==-1 and 
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
class Logger:
    def __init__(self,logLevel=logging.INFO):            

        self.intialLogger=self.prepareLogger('initial',logLevel)
        self.timerLogger=self.prepareLogger('timers',logLevel)
        self.jobsLogger=self.prepareLogger('jobs',logLevel)
        self.errorLogger=self.prepareLogger('errors',logLevel)

    def prepareLogger(self,name:str,logLevel):
        logger=logging.getLogger(name)  
        logger.setLevel(logLevel)
        file_handler = TimedRotatingFileHandler(os.path.join(Settings.logpath,name+'.log'),"midnight")        
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

logger=Logger(Settings.loglevel)
initlogger=logger.intialLogger
timerlogger=logger.timerLogger
jobslogger=logger.jobsLogger
errorlogger=logger.errorLogger
            
            




