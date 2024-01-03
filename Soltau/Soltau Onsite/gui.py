from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout, QWidget, QTableWidget, QApplication, QHeaderView,
                             QTableWidgetItem)
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QFont 
from settings import Settings


class GUI:
    def __init__(self):
        self.window = QWidget()
        self.gridLayoutMain = QGridLayout()
        self.machineACLWidget = machineInitWidget(Settings.coagulation_standby_time)
        self.machineSysmexWidget = machineInitWidget(Settings.haematology_standby_time)
        self.machineTubesACL = machineTubesWidget(8, 3, 3)
        self.machineCPCountWidget = machineCPCountWidget()
        self.machineTubesCP = machineTubesWidget(5, 2, 3)
        self.machineAdultTubesSysmex = machineTubesWidget(10, 4, 3)
        self.machineChildTubesSysmex = machineTubesWidget(10, 4, 3)

        self.machineCerntrifugatorBatch1 = machineCentrifugator()
        self.machineCerntrifugatorBatch2 = machineCentrifugator()

        self.stationBin = stationBin()
        self.stationArchiv = stationArchiv()
        self.stationError = stationError()

        self.addToLayout()
        self.window.setWindowTitle("V.Q Bot's Monitor")
        self.window.setLayout(self.gridLayoutMain)
        self.window.show()

    def addToLayout(self):
        self.gridLayoutMain.addWidget(self.layoutACL(), 0, 0)
        self.gridLayoutMain.addWidget(self.layoutCP(), 0, 1)
        self.gridLayoutMain.addWidget(self.layoutSysmex(), 0, 2)
        self.gridLayoutMain.addWidget(self.layoutCentrifugator(), 1, 0, 1, 2)
        self.gridLayoutMain.addWidget(self.stationBin.setBin(), 1, 2)
        self.gridLayoutMain.addWidget(self.stationArchiv.setArchiv(), 0, 3)
        self.gridLayoutMain.addWidget(self.stationError.setError(), 1, 3)

        # self.gridLayoutMain.setColumnStretch(0,1)
        # self.gridLayoutMain.setColumnStretch(1,1)
        # self.gridLayoutMain.setColumnStretch(2,1)
        
    def layoutACL(self):
        groupBox = QGroupBox("ACL Elite Pro (GREEN)")
        groupBox.setStyleSheet('QGroupBox:title { color: green}')
        groupBox.setFont(QFont(str('Times'),20,10,0))
        vboxACL = QVBoxLayout()
        vboxACL.addWidget(self.machineACLWidget.machine(height=93),stretch=0)
        vboxACL.addWidget(self.machineTubesACL.setTubesTable(""),stretch=1)
        groupBox.setLayout(vboxACL)
        return groupBox
    
    def layoutCP(self):
        groupBox = QGroupBox("Cobas Pure (Orange)")
        groupBox.setStyleSheet('QGroupBox:title { color: rgb(209, 132, 17)}')
        groupBox.setFont(QFont(str('Times'),20,10,0))
        vboxCP = QVBoxLayout()
        vboxCP.addWidget(self.machineCPCountWidget.setRacksAndTubes())
        vboxCP.addWidget(self.machineTubesCP.setTubesTable(""))
        groupBox.setLayout(vboxCP)
        return groupBox
    
    def layoutSysmex(self):
        groupBox = QGroupBox("Sysmex (RED)")
        groupBox.setStyleSheet('QGroupBox:title { color: red}')
        groupBox.setFont(QFont(str('Times'),20,10,0))
        vboxSys = QVBoxLayout()
        vboxSys.addWidget(self.machineSysmexWidget.machine(height=118,doors=True))
        vboxSys.addWidget(self.machineAdultTubesSysmex.setTubesTable("Adult Tubes"))
        vboxSys.addWidget(self.machineChildTubesSysmex.setTubesTable("Child Tubes"))
        groupBox.setLayout(vboxSys)
        return groupBox
    
    def layoutCentrifugator(self):
        groupBox = QGroupBox("Centrifugation (GREEN and ORANGE)")
        groupBox.setStyleSheet('QGroupBox:title { color: black}')
        groupBox.setFont(QFont(str('Times'),20,10,0))
        vboxSys = QHBoxLayout()
        vboxSys.addWidget(self.machineCerntrifugatorBatch1.setBatch("Batch 1"))
        vboxSys.addWidget(self.machineCerntrifugatorBatch2.setBatch("Batch 2"))
        groupBox.setLayout(vboxSys)
        return groupBox
         
         
class machineTubesWidget:
    def __init__(self, tubesSize, rows, cols):          
          self.tubesSize = tubesSize
          self.rows = rows
          self.cols = cols

    def setTubesTable(self, name):
        groupBox = QGroupBox(name)
        groupBox.setFont(QFont(str('Times'),17,10,0))
        vbox = QVBoxLayout()
        self.tableWidget = QTableWidget()
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0,QHeaderView.ResizeMode(1))
        header.setSectionResizeMode(1,QHeaderView.ResizeMode(1))
        self.tableWidget.setRowCount(self.rows)
        self.tableWidget.setColumnCount(self.cols)
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide() 
        # for i in range(self.tubesSize):
        #     self.tableWidget.setItem(i,0, QTableWidgetItem("Barcode " + str(i)))
        #     self.tableWidget.setItem(i,1, QTableWidgetItem("Level " + str(i)))
        #     self.tableWidget.setItem(i,2, QTableWidgetItem("Status " + str(i)))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

        vbox.addWidget(self.tableWidget)     
        groupBox.setLayout(vbox)
        return groupBox
    
    def updateTubes(self, barcode):        
        row_number = self.tableWidget.rowCount()        
        self.tableWidget.insertRow(row_number)
        # self.tableWidget.setItem(row_number, row_number%3, QTableWidgetItem(str(barcode)))
        self.tableWidget.setItem(row_number, row_number%3, QTableWidgetItem(str(barcode)))

class machineInitWidget:
    def __init__(self, timerTime):
          self.timer = QTimer()
          self.timerTime = timerTime
    
    def machine(self, height, doors=False):
        groupBox = QGroupBox()
        vbox = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setFont(QFont(str('Arial'),15,0,0))
        self.createInitTable(doors)
        groupBox.setFixedHeight(height)
        vbox.addWidget(self.tableWidget)    
        groupBox.setLayout(vbox)
        return groupBox
    
    def createInitTable(self, doors):
        if doors:
            self.tableWidget.setRowCount(3)
        else:
            self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(2)
        # Header ResizeMode to 1 for Stretch Mode
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0,QHeaderView.ResizeMode(1))
        header.setSectionResizeMode(1,QHeaderView.ResizeMode(1))
        verHeader = self.tableWidget.verticalHeader()      
        self.tableWidget.setItem(0,0, QTableWidgetItem("Machine Standby Timer"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("0"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Machine Run Timer"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("0"))
        if doors:
            self.tableWidget.setItem(2,0, QTableWidgetItem("Status of Doors"))
            self.tableWidget.setItem(2,1, QTableWidgetItem("Closed"))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()        
        self.timer.timeout.connect(self.showTime) 
        self.timer.start(100)
        self.initTimerStart = True
        self.count = 10 * self.timerTime

    def showTime(self):
        if self.initTimerStart:
            self.count -= 1
            if self.count == 0:
                self.initTimerStart = False
        if self.initTimerStart:
            text = str(self.count / 10) + " s"
            self.tableWidget.item(0,1).setText(text)


class machineCPCountWidget:
    def __init__(self):
        self.tubesCount = 0
        self.racksCount = 0
    
    def setRacksAndTubes(self):
        groupBox = QGroupBox()
        vbox = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(2)
        groupBox.setFixedHeight(88)
        # Header ResizeMode to 1 for Stretch Mode
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0,QHeaderView.ResizeMode(1))
        header.setSectionResizeMode(1,QHeaderView.ResizeMode(1))
        self.tableWidget.setFont(QFont(str('Times'),15,0,0))
        self.tableWidget.setItem(0,0, QTableWidgetItem("Tubes in Machine"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("0"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Racks in Machine"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("0"))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        vbox.addWidget(self.tableWidget)            
        groupBox.setLayout(vbox)
        return groupBox
    
    def updateRacks(self):
        self.racksCount+=1
        self.tableWidget.item(1,1).setText(str(self.racksCount))

    def updateTubes(self):
        self.tubesCount+=1
        self.tableWidget.item(0,1).setText(str(self.tubesCount))

    def initRacksAndTubes(self):
        self.tubesCount = 0
        self.racksCount = 0


class machineCentrifugator:
    def __init__(self):
        self.status = "Empty"
    
    def setBatch(self, name):
        groupBox = QGroupBox(name)
        groupBox.setFont(QFont(str('Times'),17,10,0))
        groupBox.setFixedHeight(245)
        vbox = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(6)
        self.tableWidget.setColumnCount(2)
        # Header ResizeMode to 1 for Stretch Mode
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0,QHeaderView.ResizeMode(1))
        header.setSectionResizeMode(1,QHeaderView.ResizeMode(1))
        self.tableWidget.setFont(QFont(str('Times'),15,0,0))
        self.tableWidget.setItem(0,0, QTableWidgetItem("Total racks used"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("4"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Status"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("Empty"))
        self.tableWidget.setItem(2,0, QTableWidgetItem("Green Tubes"))
        self.tableWidget.setItem(2,1, QTableWidgetItem("0"))
        self.tableWidget.setItem(3,0, QTableWidgetItem("Orange Tubes"))
        self.tableWidget.setItem(3,1, QTableWidgetItem("0"))
        self.tableWidget.setItem(4,0, QTableWidgetItem("Counter Weight"))
        self.tableWidget.setItem(4,1, QTableWidgetItem("Empty"))
        self.tableWidget.setItem(5,0, QTableWidgetItem("Run Timer"))
        self.tableWidget.setItem(5,1, QTableWidgetItem("0"))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        vbox.addWidget(self.tableWidget)            
        groupBox.setLayout(vbox)
        return groupBox

    def updateGreenTubes(self, count):
        self.tableWidget.item(0,1).setText(str(count))
    
    def updateOrangeTubes(self, count):
        self.tableWidget.item(2,1).setText(str(count))

    def updateGreenTubes(self, status):
        self.tableWidget.item(0,1).setText(str(status))


class stationBin:
    def __init__(self):
        self.count = 0
    
    def setBin(self):
        groupBox = QGroupBox("Sysmex Bin (RED)")
        groupBox.setStyleSheet('QGroupBox:title { color: red}')
        groupBox.setFont(QFont(str('Times'),20,10,0))
        vbox = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        vbox.addWidget(self.tableWidget)            
        groupBox.setLayout(vbox)
        return groupBox

    def updateBin(self, barcode):
        row_number = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_number)
        self.tableWidget.setItem(row_number, row_number%3, QTableWidgetItem(str(barcode)))


class stationArchiv:
    def __init__(self):
        self.count = 0
    
    def setArchiv(self):
        groupBox = QGroupBox("Archiv (GREEN)")
        groupBox.setStyleSheet('QGroupBox:title { color: green}')
        groupBox.setFont(QFont(str('Times'),20,10,0))
        vbox = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        vbox.addWidget(self.tableWidget)            
        groupBox.setLayout(vbox)
        return groupBox

    def updateArchiv(self, color, barcode):
        row_number = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_number)
        self.tableWidget.setItem(row_number, 0, QTableWidgetItem(str(barcode)))
        self.tableWidget.setItem(row_number, 1, QTableWidgetItem(str(color)))


class stationError:
    def __init__(self):
        self.count = 0
    
    def setError(self):
        groupBox = QGroupBox("Error Stand (GREEN, ORANGE and RED)")
        groupBox.setStyleSheet('QGroupBox:title {font-size: 208px; color: blue}')
        groupBox.setFont(QFont(str('Times'),20,10,0))
        vbox = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        vbox.addWidget(self.tableWidget)            
        groupBox.setLayout(vbox)
        return groupBox

    def updateError(self, color, barcode, level):
        row_number = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_number)        
        self.tableWidget.setItem(row_number, 0, QTableWidgetItem(str(color)))
        self.tableWidget.setItem(row_number, 1, QTableWidgetItem(str(barcode)))
        self.tableWidget.setItem(row_number, 2, QTableWidgetItem(str(level)))


if __name__ == '__main__':
    app = QApplication([])
    gui = GUI()
    app.exec()