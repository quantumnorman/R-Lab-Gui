import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QSlider, QStatusBar

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from shamrockgui import SpecControlbtns
from ingaasgui import Cameracontrols
from dataacgui import Datacontrol
from mirrorgui import MirrorControlbtns

from pyAndorShamrock import Shamrock
sham = Shamrock.Shamrock()
from atmcd import *
inifile = 'C:\\Users\\R-Lab\\Desktop\\detector.ini'
cam = atmcd()
class SystemGUI(QMainWindow):
    # This and initspecui sets some default values to load in upon startup
    def __init__(self):
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        super(SystemGUI, self).__init__()
        self.left = 200
        self.top = 50
        self.width = 1000
        self.height = 1000
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        sham.ShamrockInitialize(inifile)
        self.initspecUI()
        ret = app.exec()
        cam.ShutDown
        sham.ShamrockClose()
        sys.exit(ret)


    def initspecUI(self):
        # self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # tabs = CentralTabs()
        # self.setCentralWidget(tabs)

        layout = Layout()
        self.setCentralWidget(layout)
        self.show()

class Layout(QWidget):
    def __init__(self):
        super(Layout, self).__init__()

        layout = QVBoxLayout()

        tabs = CentralTabs()
        layout.addWidget(tabs)

        info = Systemsinfo()
        layout.addWidget(info)
        self.setLayout(layout)


class CentralTabs(QWidget):
    def __init__(self):
        super(CentralTabs, self).__init__()

        datacontrol = Datacontrol()
        mirrorcontrol = MirrorControlbtns()

        self.tabs = QTabWidget()
        self.dataactab = QWidget()
        self.plmaptab = QWidget()

        self.tabs.addTab(self.dataactab, 'Data Acquisition')
        self.tabs.addTab(self.plmaptab, 'PL Scan')

        self.dataactab.layout = QVBoxLayout(self)
        self.dataactab.layout.addWidget(datacontrol)
        self.dataactab.setLayout((self.dataactab.layout))

        self.plmaptab.layout = QVBoxLayout(self)
        self.plmaptab.layout.addWidget(mirrorcontrol)
        self.plmaptab.setLayout(self.plmaptab.layout)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class Systemsinfo(QWidget):
    def __init__(self):
        super(Systemsinfo, self).__init__()
        layout1 = QHBoxLayout()
        layout = QGridLayout()
        groupbox = QGroupBox()
        groupbox.setLayout(layout1)

        specinfobox = QGroupBox()
        spectrometer = SpecControlbtns()
        specinfolayout = QGridLayout()
        specinfolayout.addWidget(spectrometer,0,0)
        specinfobox.setLayout(specinfolayout)
        specinfobox.setTitle('Spectrometer Information')
        layout1.addWidget(specinfobox)

        caminfobox = QGroupBox()
        camerainfo = Cameracontrols()
        caminfolayout = QGridLayout()
        caminfolayout.addWidget(camerainfo,0,0)
        caminfobox.setLayout(caminfolayout)
        caminfobox.setTitle('Camera Information')
        layout1.addWidget(caminfobox)
        layout.addWidget(groupbox, 2, 0, 2, 2)

        wavebox = QGroupBox()
        mySlider = QSlider(Qt.Horizontal, self)
        mySlider.setMinimum(0)
        mySlider.setSingleStep(5)
        mySlider.setGeometry(30, 40, 200, 30)
        # mySlider.valueChanged[int].connect(self.changeValue)
        wavelayout = QHBoxLayout()
        wavelayout.addWidget(mySlider)
        wavebox.setTitle('Wavelength')
        wavebox.setLayout(wavelayout)
        layout.addWidget(wavebox, 0, 0, 1, 2)


        self.setLayout(layout)

        # def changeValue(self, value):
        #     print(value)



SystemGUI()