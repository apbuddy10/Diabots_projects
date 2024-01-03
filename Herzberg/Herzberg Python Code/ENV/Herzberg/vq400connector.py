import asyncio
from command_sender import CommandSender
from q400 import Q400Connection
from settings import Color

class TubeResults:
    def __init__(self):
        self.color: Color=Color.NONE
        self.bloodLevel:float=0
        self.plasmaLevel:float=0
        self.stn4Pose:bool=False
        self.barCode:str=''

class Vq400Connector:
    def __init__(self, host: str = "127.0.0.1", port: int = 9094):
        self.__dict__['spread_sheet'] = {}
        self.__dict__['results_cam1'] = []
        self.__dict__['results_cam2'] = {}
        self.__dict__['mode'] = ""
        self.vq_timeout = 10
        self.host=host
        self.port=port
        self.conn_Q400:Q400Connection = None
        self.tubeResults = TubeResults()
    
    async def initVQ400(self):
        if self.conn_Q400 is not None:
            await self.conn_Q400.end()
        self.conn_Q400 = Q400Connection(self.host,self.port)
        self.conn_Q400.addHandler(self.q400_handler)
        self.vq_wait_for_ready: asyncio.Future = asyncio.get_event_loop().create_future()
        self.vq_wait_for_spreadsheet: asyncio.Future = asyncio.get_event_loop().create_future()
        await self.conn_Q400.send(CommandSender.command_change_mode("run"))
    
    def getCurrentTubeResults(self):
        return self.tubeResults

    def resetCurrentTubeResults(self):
        self.tubeResults=TubeResults()
        
    async def execute_execution_group_Q400(self, vq_group: int):
        if self.conn_Q400 is not None and self.conn_Q400.isConnected():
            self.vq_wait_for_ready: asyncio.Future = asyncio.get_event_loop().create_future()
            await self.conn_Q400.send(CommandSender.command_start_execution_group(vq_group))
            try:
                await asyncio.wait_for(self.vq_wait_for_ready, self.vq_timeout)
            except asyncio.TimeoutError:
                self.vq_wait_for_ready: asyncio.Future = asyncio.get_event_loop().create_future()

    async def spreadsheet_from_Q400(self):
        self.__dict__['spread_sheet'], self.__dict__['results_cam1'], self.__dict__['results_cam2'] = {}, [], {}
        if self.conn_Q400 is not None and self.conn_Q400.isConnected():
            self.vq_wait_for_spreadsheet: asyncio.Future = asyncio.get_event_loop().create_future()
            await self.conn_Q400.send(CommandSender.command_get_spreadsheet())
            try:
                await asyncio.wait_for(self.vq_wait_for_spreadsheet, self.vq_timeout)
            except asyncio.TimeoutError:
                self.vq_wait_for_spreadsheet: asyncio.Future = asyncio.get_event_loop().create_future()
        return self.spreadsheet_processor()

    async def spreadsheet_result_from_Q400(self, row:str, column:str):
        self.__dict__['spread_sheet'], self.__dict__['results_cam1'], self.__dict__['results_cam2'] = {}, [], {}
        if self.conn_Q400 is not None and self.conn_Q400.isConnected():
            self.vq_wait_for_spreadsheet: asyncio.Future = asyncio.get_event_loop().create_future()
            await self.conn_Q400.send(CommandSender.command_get_spreadsheet_result(row, column))
            try:
                await asyncio.wait_for(self.vq_wait_for_spreadsheet, self.vq_timeout)
            except asyncio.TimeoutError:
                self.vq_wait_for_spreadsheet: asyncio.Future = asyncio.get_event_loop().create_future()
        return self.spreadsheet_result_processor()

    def spreadsheet_result_processor(self):
        for k, v in self.__dict__['spread_sheet'].items():
            self.__dict__['results_cam2'] = v
        return self.__dict__['results_cam2']

    async def spreadsheet_row_from_Q400(self, row:str):
        self.__dict__['spread_sheet'], self.__dict__['results_cam1'], self.__dict__['results_cam2'] = {}, [], {}
        if self.conn_Q400 is not None and self.conn_Q400.isConnected():
            self.vq_wait_for_spreadsheet: asyncio.Future = asyncio.get_event_loop().create_future()
            await self.conn_Q400.send(CommandSender.command_get_spreadsheet_row(row))
            try:
                await asyncio.wait_for(self.vq_wait_for_spreadsheet, self.vq_timeout)
            except asyncio.TimeoutError:
                self.vq_wait_for_spreadsheet: asyncio.Future = asyncio.get_event_loop().create_future()
        return self.spreadsheet_row_processor()

    def spreadsheet_row_processor(self):
        for k, v in self.__dict__['spread_sheet'].items():
            self.__dict__['results_cam2'] = v
        return self.__dict__['results_cam2']

    async def q400_execute_cam1(self, group: int):
        await self.execute_execution_group_Q400(group)
        c1, _ = await self.spreadsheet_from_Q400()
        return c1

    async def q400_execute_cam2(self, group: int):
        await self.execute_execution_group_Q400(group)
        if group == 13:
            # Color
            color_value = await self.spreadsheet_result_from_Q400("stn4_color", "value")
            if int(color_value['value']) == 11:
                self.tubeResults.color = Color.GREEN
                return 11
            elif int(color_value['value']) == 12 or int(color_value['value']) == 18:
                self.tubeResults.color = Color.ORANGE
                return 12
            elif int(color_value['value']) == 13:
                self.tubeResults.color = Color.RED
                return 13
            elif int(color_value['value']) == 14:
                self.tubeResults.color = Color.CRED
                return 14
            return 0
        if group == 14:
            # Barcode, first time
            barcode_judgement = await self.spreadsheet_result_from_Q400("stn4_pose", "judgement")
            if barcode_judgement['judgement'] == 'OK':
                self.tubeResults.stn4Pose = True
                barcode_row = await self.spreadsheet_result_from_Q400("stn4_barcode", "value")
                barcode = str(barcode_row['value'])
                if await self.validateBarCode(barcode):
                    if self.tubeResults.color == Color.RED or self.tubeResults.color == Color.CRED:
                        barcode_red_judgement = await self.spreadsheet_result_from_Q400("stn4_barcode_y", "judgement")
                        if barcode_red_judgement['judgement'] == 'OK':
                            self.tubeResults.barCode = barcode
                            return True
                        return False
                    self.tubeResults.barCode = barcode
                    return True
                return False
            return False
        if group == 15:
            # Barcode, from second time
            barcode_judgement = await self.spreadsheet_result_from_Q400("stn4_pose", "judgement")
            if barcode_judgement['judgement'] == 'OK':
                self.tubeResults.stn4Pose = True
                barcode_row = await self.spreadsheet_result_from_Q400("stn4_barcode", "value")
                barcode = str(barcode_row['value'])
                if await self.validateBarCode(barcode):
                    if barcode == self.tubeResults.barCode:
                        return True
                    return False
                return False
            return False
        if group == 16:
            # Green plasma level
            green_plasma_row = await self.spreadsheet_row_from_Q400("stn4_level_green")
            self.tubeResults.plasmaLevel = float(green_plasma_row['value'])
            if green_plasma_row['judgement'] != 'OK':
                return False 
            return True
        if group == 17:
            # Orange plasma level
            orange_plasma_row = await self.spreadsheet_row_from_Q400("stn4_level_orange")
            self.tubeResults.plasmaLevel = float(orange_plasma_row['value'])
            if orange_plasma_row['judgement'] != 'OK':
                return False 
            return True
        if group == 18:
            # Red blood level
            red_blood_row = await self.spreadsheet_row_from_Q400("stn4_level_red")
            self.tubeResults.bloodLevel = float(red_blood_row['value'])
            if red_blood_row['judgement'] != 'OK':
                return False            
            return True
        if group == 19:
            # CRED level
            return True
        if group == 20:
            # Level NG
            return True
        return False

    async def q400_execute_cam3(self, group: int):
        await self.execute_execution_group_Q400(group)        
        if group == 3:
            # Barcode, first time
            judgement = await self.spreadsheet_result_from_Q400("stn3_status", "judgement")
            if judgement['judgement'] == 'OK':
                return True
            return False
        return False

    async def validateBarCode(self,barcode:str):
        return barcode != "0" and barcode != "" and len(barcode) == 10 # and barcode.startswith("455")

    def spreadsheet_processor(self):
        for k, v in self.__dict__['spread_sheet'].items():
            if v['comment'].find('G') != -1:
                self.__dict__['results_cam1'].append({'position': (v['comment'])[1:], 'color':int(v['value'])})
        return self.__dict__['results_cam1'], self.__dict__['results_cam2']

    async def q400_handler(self, data: dict, s: str):
        if data is not None:
            if 'events' in data:
                if data.get('events') is not None:
                    for event in data.get('events'):
                        if event.get('type') == 'ModeStateChanged':
                            self.__dict__['mode'] = event.get('newMode')  

                    if event.get('type') == 'ProjectStateChanged':
                        project = event.get('project')
                        self.__dict__['project_state'] = project.get('state')
                        if self.__dict__['project_state'] == "Ready":
                            self.vq_wait_for_ready.set_result(True)
        
        if 'parameter' in data:
            parameter = data.get('parameter')
            if 'spreadsheet' in parameter:
                self.__dict__['spread_sheet'] = parameter.get('spreadsheet')              
                self.vq_wait_for_spreadsheet.set_result(True)

            if 'state' in parameter:
                state = parameter.get('state')
                if 'mode' in state:
                    self.__dict__['mode'] = state.get('mode')

        return False