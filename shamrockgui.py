import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from pyAndorShamrock import Shamrock
sham = Shamrock.Shamrock()
inifile = 'C:\\Users\\R-Lab\\Desktop\\detector.ini'

sham.ShamrockInitialize(inifile)


class SpectrometerGui(QMainWindow):
    def __init__(self):
        super(SpectrometerGui, self).__init__()
        self.title = 'Shamrock Spectrometer Control'
        self.left = 50
        self.top = 50
        self.width = 400
        self.height = 250
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

        speclayout = QVBoxLayout()

        specbtns = self.initializespecbtns()
        flipbtns = self.flipspecbtns()
        gratingsbtns = self.gratingsbtns()

        speclayout.addWidget(flipbtns)
        speclayout.addWidget(gratingsbtns)
        speclayout.addWidget(specbtns)
        self.setLayout(speclayout)


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

        groupbox = QGroupBox()
        groupbox.setLayout(vbox)
        return groupbox

    def flipspecbtns(self):
        zeroinbtn = QPushButton('Straight Input Flipper Mirror', self)
        zeroinbtn.clicked.connect(self.on_click_straightinflip)

        zerooutbtn = QPushButton('Straight Output Flipper Mirror', self)
        zerooutbtn.clicked.connect(self.on_click_straightoutflip)

        maxinbtn = QPushButton('Right Input Flipper Mirror', self)
        maxinbtn.clicked.connect(self.on_click_rightinflip)

        maxoutbtn = QPushButton('Left Output Flipper Mirror', self)
        maxoutbtn.clicked.connect(self.on_click_leftoutflip)

        resetoutbtn = QPushButton('Zero Output Flipper Mirror', self)
        resetoutbtn.clicked.connect(self.on_click_resetoutflip)

        resetinbtn = QPushButton('Zero Input Flipper Mirror', self)
        resetinbtn.clicked.connect(self.on_click_resetoutflip)

        gbox = QGridLayout()
        gbox.addWidget(zerooutbtn, 0, 0)
        gbox.addWidget(zeroinbtn, 0, 1)
        gbox.addWidget(maxoutbtn, 1, 0)
        gbox.addWidget(maxinbtn, 1, 1)
        gbox.addWidget(resetoutbtn, 2,0)
        gbox.addWidget(resetinbtn, 2,1)


        groupbox = QGroupBox()
        groupbox.setLayout(gbox)
        groupbox.setTitle('Flipper Mirror controls')

        return groupbox

    def gratingsbtns(self):
        grating1 = QPushButton('1250nm Grating', self)
        grating1.clicked.connect(self.on_click_switch1)

        grating2 = QPushButton('750nm Grating', self)
        grating2.clicked.connect(self.on_click_switch2)

        grating3 = QPushButton('1300nm Grating', self)
        # grating3.clicked.connect(self.on_click_maxinflip)

        gbox = QGridLayout()
        gbox.addWidget(grating1, 0, 0)
        gbox.addWidget(grating2, 0, 1)
        gbox.addWidget(grating3, 0, 3)


        groupbox = QGroupBox()
        groupbox.setLayout(gbox)
        groupbox.setTitle('Grating Controls')

        return groupbox





    @pyqtSlot()
    def on_click_close(self):
        sham.ShamrockClose()
        print('Shutdown Shamrock')

    def on_click_reinit(self):
        sham.ShamrockInitialize(inifile)
        print('Reinitialize Shamrock')

    def on_click_resetoutflip(self):
        zeroinflip = sham.ShamrockFlipperMirrorReset(0, 1)
        print('Input Flipper Reset')

    def on_click_resetinflip(self):
        zerooutflip = sham.ShamrockFlipperMirrorReset(0, 2)
        print('Output Flipper Reset')

    def on_click_straightinflip(self):
        maxvalue = sham.ShamrockSetFlipperMirrorPosition(0, 1, 0)
        print(maxvalue[0])
        print(maxvalue[1])

    def on_click_straightoutflip(self):
        maxvalue = sham.ShamrockSetFlipperMirrorPosition(0, 2, 0)

    def on_click_rightinflip(self):
        maxvalue = sham.ShamrockSetFlipperMirrorPosition(0, 1, -400)


    def on_click_leftoutflip(self):
        maxvalue = sham.ShamrockSetFlipperMirrorPosition(0, 2, -400)


    def on_click_switch1(self):
        setgrate = sham.ShamrockSetGrating(0, 1)
        grateinfo = sham.ShamrockGetGratingInfo(0, 1)

    def on_click_switch2(self):
        setgrate = sham.ShamrockSetGrating(0, 2)
        grateinfo = sham.ShamrockGetGratingInfo(0, 2)

    def on_click_switch3(self):
        setgrate = sham.ShamrockSetGrating(0, 3)
        grateinfo = sham.ShamrockGetGratingInfo(0, 3)


#TODO: add updating QLabels with inner/outer flipper positions. See https://www.riverbankcomputing.com/pipermail/pyqt/2013-July/033053.html
#TODO: add status bar with moving/finished for flipper and grating
#TODO: add 'other' option for flipper?
#TODO: add offset option for grating?

