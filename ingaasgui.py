import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout, QLabel, QLineEdit
import matplotlib as plt
from atmcd import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QTimer

cam = atmcd()

class InGaAsGui(QMainWindow):
    def __init__(self):
        # app = QApplication(sys.argv)
        # app.setStyle('Fusion')
        super(InGaAsGui, self).__init__()
        self.title = 'InGaAs Camera Control'
        self.left = 50
        self.top = 50
        # self.width = 500
        # self.height = 500
        self.initingaasUI()
        # sys.exit(app.exec_())

    def initingaasUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        # QTimer.singleShot(5000, cameracontrols.updatetemplbl)
        self.setCentralWidget(Cameracontrols())
        # self.show()

class Cameracontrols(QWidget):
    def __init__(self):
        super(Cameracontrols, self).__init__()
        grid = QGridLayout()
        grid.addWidget(self.cameracontrolbtns(), 0,0)
        self.setLayout(grid)
        # self.temp = cam.GetTemperature()
        self.updatetemplbl()

    def cameracontrolbtns(self):
        labels = self.labels()
        settemp = self.settemp()

        layout = QGridLayout()
        layout.addWidget(settemp, 0, 0)
        layout.addWidget(labels, 0, 1)
        groupbox = QGroupBox()
        groupbox.setLayout(layout)

        return groupbox

    def settemp(self):
        self.settempbox = QLineEdit('-80')
        self.settempbox.setMaximumWidth(100)
        self.settempbtn = QPushButton('Set Temp')
        self.settempbtn.clicked.connect(self.on_click_settemp)

        cooleronbtn = QPushButton('Cooler On')
        cooleronbtn.setMaximumWidth(100)
        cooleronbtn.clicked.connect(self.on_click_cooleron)

        cooleroffbtn = QPushButton('Cooler Off')
        cooleroffbtn.setMaximumWidth(100)
        cooleroffbtn.clicked.connect(self.on_click_cooleroff)

        layout = QGridLayout()
        layout.addWidget(self.settempbox, 0,0)
        layout.addWidget(self.settempbtn, 0,1)
        layout.addWidget(cooleronbtn, 1,0)
        layout.addWidget(cooleroffbtn,1,1)

        groupbox = QGroupBox()
        groupbox.setLayout(layout)
        return groupbox

    def labels(self):
        self.settemplbl = QLabel()
        settemp = QLabel('Temperature Set point:')
        self.templbl = QLabel()
        temp = QLabel('Current Temperature')
        # self.templbl.setText(str(self.temp))
        cmap = plt.colors.Colormap('Jet')
        coolstatus = QLabel('Cooler Status')
        self.coolerlbl = QLabel()
        layout = QGridLayout()
        groupbox = QGroupBox()
        layout.addWidget(settemp, 1,0)
        layout.addWidget(self.settemplbl, 1, 1)
        layout.addWidget(self.coolerlbl, 0, 1)
        layout.addWidget(coolstatus, 0, 0)
        layout.addWidget(self.templbl, 2,1)
        layout.addWidget(temp, 2,0)

        groupbox.setLayout(layout)
        return groupbox

    def updatetemplbl(self):
        self.thread = Tempthread()
        self.thread.start()
        self.thread.signal.connect(lambda x: self.on_thread_done(x))


    @pyqtSlot()
    def on_thread_done(self, temp):
        self.templbl.setText(temp)



    def on_click_settemp(self): #defines the function associated with the set temperature button
        settemp = int(self.settempbox.text())
        ret = cam.CoolerON()
        ret, temp = cam.GetTemperature()

        if ret ==20075:
            self.settemplbl.setText('Camera not initialized')
            self.templbl.setText(str(temp))
        else:
            cam.SetTemperature(temp)
            self.settemplbl.setText(str(settemp))
            self.templbl.setText(str(temp))
            print(ret)

    def on_click_cooleron(self):
        ret = cam.CoolerON()
        if ret == 20075:
            self.coolerlbl.setText('Camera not initialized')
        if ret== 20002:
            self.coolerlbl.setText('Cooler On')

    def on_click_cooleroff(self):
        ret = cam.CoolerOFF()
        if ret == 20002:
            self.coolerlbl.setText('Cooler Off')

# InGaAsGui()

class Tempthread(QThread):
    signal = pyqtSignal('PyQt_PyObject')


    def __init__(self):
        QThread.__init__(self)

        self.condition = 1

    def run(self):
        print('temp')
        ret, temp = cam.GetTemperature()
        if ret == 20075:
            templblsettext = 'Camera Not Initialized'

        while self.condition ==1:
            ret, temp = cam.GetTemperature()
            temp = str(temp)
            self.signal.emit(temp)
            print('temperature = ', temp, 'return', ret)
            time.sleep(5)
        print('temp', ret, temp)

    def halt(self):
        self.condition = 0