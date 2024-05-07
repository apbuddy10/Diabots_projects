import asyncio
from command_sender import CommandSender
from q400 import Q400Connection
from settings import Settings,Color

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

    async def q400_execute_cam2(self, group:int):
        await self.execute_execution_group_Q400(int(group))
        if group == 3:
            # Compact Max Barcode
            compact_barcode = await self.spreadsheet_row_from_Q400("stn3_barcode")
            if compact_barcode['judgement'] == 'OK':
                return 1
            return 0
        if group == 22:
            # Compact Max Status
            compact_status = await self.spreadsheet_result_from_Q400("stn3_status", "judgement")
            if compact_status['judgement'] == 'OK':
                return 1
            return 0
        if group == 23:
            # Compact Max open
            stago_open = await self.spreadsheet_result_from_Q400("stago_open", "judgement")
            if stago_open['judgement'] == 'OK':
                return 1
            return 0
        if group == 24:
            # Compact Max close
            stago_close = await self.spreadsheet_result_from_Q400("stago_close", "judgement")
            if stago_close['judgement'] == 'OK':
                return 1
            return 0
        if group == 25:
            # Compact Max dd
            compact_dd_1 = await self.spreadsheet_result_from_Q400("stago_dd_1", "judgement")
            compact_dd_2 = await self.spreadsheet_result_from_Q400("stago_dd_2", "judgement")
            if compact_dd_1['judgement'] == 'OK' and compact_dd_2['judgement'] == 'OK':
                return 2
            elif compact_dd_1['judgement'] == 'OK':
                return 1
            return 0
        if group == 26:
            # Compact Max special
            stago_special = await self.spreadsheet_result_from_Q400("stago_special", "judgement")
            if stago_special['judgement'] == 'OK':
                return 1
            return 0
        if group == 13:
            # Color
            color_value = await self.spreadsheet_result_from_Q400("stn4_color", "value")
            if int(color_value['value']) == 11:
                self.tubeResults.color = Color.GREEN
                return 11
            elif int(color_value['value']) == 12:
                self.tubeResults.color = Color.ORANGE
                return 12
            elif int(color_value['value']) == 18:
                self.tubeResults.color = Color.BROWN
                return 18
            elif int(color_value['value']) == 13:
                self.tubeResults.color = Color.YELLOW
                return 13
            elif int(color_value['value']) == 14:
                self.tubeResults.color = Color.RED
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
                    self.tubeResults.barCode = barcode
                    return 1
                return 0
            return 0
        if group == 15:
            # Barcode, from second time
            barcode_judgement = await self.spreadsheet_result_from_Q400("stn4_pose", "judgement")
            if barcode_judgement['judgement'] == 'OK':
                self.tubeResults.stn4Pose = True
                barcode_row = await self.spreadsheet_result_from_Q400("stn4_barcode", "value")
                barcode = str(barcode_row['value'])
                if await self.validateBarCode(barcode):
                    if barcode == self.tubeResults.barCode:
                        return 1
                    return 0
                return 0
            return 0
        if group == 16:
            # Red level
            red_plasma_row = await self.spreadsheet_row_from_Q400("stn4_level")
            self.tubeResults.plasmaLevel = float(red_plasma_row['value'])
            if red_plasma_row['judgement'] == 'OK':
                return 1
            return 0
        if group == 17:
            # Green level
            green_plasma_row = await self.spreadsheet_row_from_Q400("stn4_green_level_final")
            self.tubeResults.plasmaLevel = float(green_plasma_row['value'])
            if green_plasma_row['judgement'] == 'OK':
                return 1
            return 0
        if group == 21:
            # Level NG
            return 1
        return 0

    async def validateBarCode(self,barcode:str):
        return barcode != "0" and barcode != "" # and len(barcode) == 10 #and barcode.startswith("713")

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

conn_Q400=Vq400Connector(Settings.vq400host)