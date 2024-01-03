import struct


class InterfaceIn():
    def __init__(self):
        self.dataFromRobot = 0

    def setData(self,data):
        # data = struct.unpack(">"+ str(len(data)) + "s",data)
        data = [float(value) for value in data[:-1].split(',')]
        self.dataFromRobot = data
    
class InterfaceOut():
    def __init__(self):
        self.stateOfHandshake   = 0
        self.lockID             = 1
        self.status             = 0
        self.srcJob             = 0
        self.destJob            = 0
        self.pingStatus         = 0
        self.srcPos             = [0,0,0,0,0,0]
        self.destPos            = [0,0,0,0,0,0]

    def getData(self):
        return (
            str(self.stateOfHandshake)                  + "," +
            str(self.lockID)                            + "," +
            str(self.status)                            + "," +
            str(self.srcJob)                            + "," +
            str(self.destJob)                           + "," +
            str(self.pingStatus)                        + "," +
            ' '.join(str(val) + "," for val in  self.srcPos) +
            ' '.join(str(val) + "," for val in  self.destPos)
        )
    


class InterfaceOutPing():
    def __init__(self):
        self.stateOfHandshake   = 0

    def getData(self):
        return (
            str(self.stateOfHandshake)   + ","
        )
    
         