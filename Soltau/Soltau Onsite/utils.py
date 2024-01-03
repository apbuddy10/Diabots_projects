from logger import jobslogger
import os
import time
import asyncio


class Utils:
    def __init__(self):
        self.task=None
  
    async def isFileReady(self, file_path,timeout,loop_count):
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                ret = False
                loop = 0
                while (loop <= loop_count):
                    initial_stat = os.stat(file_path)
                    await asyncio.sleep(timeout) # time.sleep(timeout)  # Wait for the specified timeout duration
                    current_stat = os.stat(file_path)
                    if initial_stat.st_mtime == current_stat.st_mtime:
                        ret = True
                        break                        
                    else:
                        jobslogger.info("File {0} is still being written to.".format(file_path))
                    loop+=1
                return ret
            else:
                jobslogger.info("File {0} is not a regular file.".format(file_path))
                return False
        else:
            jobslogger.info("File {0} does not exist.".format(file_path))
            return False
 

utils = Utils()
