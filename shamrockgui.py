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
        super(SpecControlbtns, self).__init__()
        self.initspecUI()

    def initspecUI(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)

        # flipbtns = self.flipspecbtns()
        # zeroutbtn =
        specbtns = self.initializespecbtns()
        self.setLayout(specbtns)
        # hbox.addWidget(flipbtns)


    def initializespecbtns(self):
        closebtn = QPushButton('Shutdown Shamrock', self)
        closebtn.clicked.connect(self.on_click_close)

        reinitbtn = QPushButton('Reinitialize Shamrock', self)
        reinitbtn.clicked.connect(self.on_click_reinit)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(reinitbtn)
        hbox.addWidget(closebtn)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        return vbox

    # def flipspecbtns(self):
    #     zeroinbtn = QPushButton('Zero Input Flipper Mirror', self)
    #     zeroinbtn.clicked.connect(self.on_click_zeroinflip)
    #
    #     zerooutbtn = QPushButton('Zero Output Flipper Mirror', self)
    #     zerooutbtn.clicked.connect(self.on_click_zerooutflip)

        return zeroinbtn, zerooutbtn


    @pyqtSlot()
    def on_click_close(self):
        # sham.ShamrockClose()
        print('Shutdown Shamrock')

    def on_click_reinit(self):
        # sham.ShamrockInitialize(inifile)
        print('Reinitialize Shamrock')

    def on_click_zeroinflip(self):
        # zeroinflip = sham.ShamrockFlipperMirrorReset(0, 1)
        print('Input Flipper Reset')

    def on_click_zerooutflip(self):
        # zerooutflip = sham.ShamrockFlipperMirrorReset(0, 2)
        print('Output Flipper Reset')
