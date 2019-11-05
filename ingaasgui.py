import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout, QLabel, QLineEdit
import matplotlib as plt
from atmcd import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QTimer

cam = atmcd()

class InGaAsGui(QMainWindow):
    def __init__(self):
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        super(InGaAsGui, self).__init__()
        self.title = 'InGaAs Camera Control'
        self.left = 50
        self.top = 50
        # self.width = 500
        # self.height = 500
        self.initingaasUI()
        sys.exit(app.exec_())

    def initingaasUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)

        self.setCentralWidget(cameracontrols())
        self.show()

class cameracontrols(QWidget):
    def __init__(self):
        super(cameracontrols, self).__init__()
        grid = QGridLayout()
        grid.addWidget(self.cameracontrolbtns(), 0,0)
        self.setLayout(grid)

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
        self.templbl = QLabel()
        temp = QLabel('Temperature:')
        cmap = plt.colors.Colormap('Jet')
        QTimer.singleShot(10000, lambda: self.updatetemplbl()) #updates temperature every 10 seconds
        coolstatus = QLabel('Cooler Status')
        self.coolerlbl = QLabel()
        layout = QGridLayout()
        groupbox = QGroupBox()
        layout.addWidget(temp, 1,0)
        layout.addWidget(self.templbl, 1, 1)
        layout.addWidget(self.coolerlbl, 0, 1)
        layout.addWidget(coolstatus, 0, 0)

        groupbox.setLayout(layout)
        return groupbox

    def updatetemplbl(self):
        self.temp = cam.GetTemperature()
        self.temp = str(self.temp)
        self.templbl.setText(self.temp)

    @pyqtSlot()
    def on_click_settemp(self): #defines the function associated with the set temperature button
        temp = int(self.settempbox.text())
        ret = cam.CoolerON()
        if ret ==20075:
            self.templbl.setText('Camera not initialized')
        else:
            cam.SetTemperature(temp)
            self.templbl.setText(str(temp))
            print(ret)

    def on_click_cooleron(self):
        ret = cam.CoolerON()
        if ret == 20075:
            self.coolerlbl.setText('Camera not initialized')
        # if ret == 20002:
            # self.initlbl.setText('Cooler On')
    def on_click_cooleroff(self):
        ret = cam.CoolerOFF()
        if ret == 20002:
            self.coolerlbl.setText('Cooler Off')

InGaAsGui()