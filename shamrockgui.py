import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

# from pyAndorShamrock import Shamrock
# sham = Shamrock.Shamrock()
# inifile = 'C:\\Users\\Victoria\\Desktop\\detector.ini'

# sham.ShamrockInitialize(inifile)


class SpectrometerGui(QMainWindow):
    def __init__(self):
        super(SpectrometerGui, self).__init__()
        self.title = 'Shamrock Spectrometer Control'
        self.left = 50
        self.top = 50
        self.width = 500
        self.height = 500
        self.initspecUI()

    def initspecUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        controlbtns = SpecControlbtns()
        self.setCentralWidget(controlbtns)


class SpecControlbtns(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 12.5
        self.top = 12.5
        self.width = 275
        self.height = 475
        self.initializespecbtns()



    def initializespecbtns(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        closebtn = QPushButton('Shutdown Shamrock', self)
        closebtn.clicked.connect(self.on_click_close)

        reinitbtn = QPushButton('Reinitialize Shamrock', self)
        reinitbtn.clicked.connect(self.on_click_reinit)


    @pyqtSlot()
    def on_click_close(self):
        # sham.ShamrockClose()
        print('Shutdown Shamrock')

    def on_click_reinit(self):
        # sham.ShamrockInitialize(inifile)
        print('Reinitialize Shamrock')


class Flipperspecbtns(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 12.5
        self.top = 12.5
        self.width = 275
        self.height = 475
        self.initializespecbtns()
        grid = QGridLayout()
        grid.addWidget(self.initializespecbtns(), 0, 0)
        self.setLayout(grid)

    def initializeflipbtns(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        closebtn = QPushButton('Shutdown Shamrock', self)
        closebtn.clicked.connect(self.on_click_close)

        reinitbtn = QPushButton('Reinitialize Shamrock', self)
        reinitbtn.clicked.connect(self.on_click_reinit)

        spectbox = QGroupBox()
        spectvbox = QVBoxLayout()
        vbox1 = QVBoxLayout()
        spectvbox.addWidget(closebtn)
        spectvbox.addWidget(reinitbtn)
        spectvbox.addLayout(vbox1)
        spectbox.setLayout(spectvbox)

        return spectbox

    @pyqtSlot()
    def on_click_zeroinflip(self):
        # zeroinflip = sham.ShamrockFlipperMirrorReset(0, 1)
        print('Input Flipper Reset')

    def on_click_zerooutflip(self):
        # zerooutflip = sham.ShamrockFlipperMirrorReset(0, 2)
        print('Output Flipper Reset')
