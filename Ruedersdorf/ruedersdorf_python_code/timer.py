from logger import timerlogger
import asyncio
class Timer:
    def __init__(self):
        self.set_timer_val:int=0 # seconds
        self.callback=None
        self.task=None
        
    def set_alarm(self,set_timer_val:int,callback):
        self.cancel_alarm()
        self.set_timer_val = set_timer_val
        self.callback=callback
        self.task = asyncio.ensure_future(self.job())
 
    async def job(self):        
        await asyncio.sleep(self.set_timer_val)
        await self.callback()
    
    def cancel_alarm(self):
        if self.task is not None:            
            self.task.cancel()
            self.callback=None
            self.set_timer_val=0
            
        
