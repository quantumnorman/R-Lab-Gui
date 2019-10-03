import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout, QLabel

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from pyAndorShamrock import Shamrock
sham = Shamrock.Shamrock()
inifile = 'C:\\Users\\R-Lab\\Desktop\\detector.ini'

class SpectrometerGui(QMainWindow):
    def __init__(self):
        # app = QApplication(sys.argv)
        # app.setStyle('Fusion')
        super(SpectrometerGui, self).__init__()
        self.title = 'Shamrock Spectrometer Control'
        self.left = 200
        self.top = 50
        self.width = 400
        self.height = 250
        sham.ShamrockInitialize(inifile)
        self.initspecUI()
        # sys.exit(app.exec_())


    def initspecUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        controlbtns = SpecControlbtns()
        self.setCentralWidget(controlbtns)
        # self.show()


class SpecControlbtns(QWidget):
    def __init__(self):
        super(SpecControlbtns, self).__init__()

        # Initializes the status updating labels #
        self.infliplbl = QLabel('Input Flipper Straight')
        self.outfliplbl = QLabel('Output Flipper Straight')
        self.specstatlbl = QLabel('Spectrometer Initialized')
        self.gratinglbl = QLabel('1250nm')

        self.initspecUI()

    def initspecUI(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)

        speclayout = QGridLayout()
        specbtns = self.initializespecbtns()
        flipbtns = self.flipspecbtns()
        gratingsbtns = self.gratingsbtns()
        update = self.updatelbls()

        speclayout.addWidget(flipbtns, 1, 0)
        speclayout.addWidget(gratingsbtns, 0,0)
        speclayout.addWidget(specbtns, 2,0)
        speclayout.addWidget(update, 0,1, 3, 3)

        self.setLayout(speclayout)

    # Creates the initialization control buttons #
    def initializespecbtns(self):
        closebtn = QPushButton('Shutdown Shamrock', self)
        closebtn.clicked.connect(self.on_click_close)

        reinitbtn = QPushButton('Reinitialize Shamrock', self)
        reinitbtn.clicked.connect(self.on_click_reinit)

        hbox = QHBoxLayout()
        hbox.addWidget(reinitbtn)
        hbox.addWidget(closebtn)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        groupbox = QGroupBox()
        groupbox.setLayout(vbox)
        return groupbox

    # Creates the flipper mirror control buttons #
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

    # Creates the gratings control buttons #
    def gratingsbtns(self):
        grating1 = QPushButton('1250nm Grating', self)
        grating1.clicked.connect(self.on_click_switch1)

        grating2 = QPushButton('750nm Grating', self)
        grating2.clicked.connect(self.on_click_switch2)

        grating3 = QPushButton('1300nm Grating', self)
        grating3.clicked.connect(self.on_click_switch3)

        gbox = QGridLayout()
        gbox.addWidget(grating1, 0, 0)
        gbox.addWidget(grating2, 0, 1)
        gbox.addWidget(grating3, 0, 3)


        groupbox = QGroupBox()
        groupbox.setLayout(gbox)
        groupbox.setTitle('Grating Controls')

        return groupbox

    # Creates the separate box for status updates #
    def updatelbls(self):
        labelslayout = QGridLayout()
        groupbox = QGroupBox() #creates the total update box
        groupbox.setLayout(labelslayout) #sets the layout of the update box
        groupbox.setTitle('Shamrock Status Information') #sets the title of the update box

        flipperlayout = QGridLayout()
        flipperbox = QGroupBox() #creates the sub-box for flipper mirror information
        flipperbox.setLayout(flipperlayout)
        flipperbox.setTitle('Flipper Information:')
        flipperlayout.addWidget(self.infliplbl, 0 , 0) #calls the input flipper label from the __init__ function
        flipperlayout.addWidget(self.outfliplbl, 1, 0) #calls the output flipper label from the __init__ function

        statuslayout = QGridLayout()
        statusbox = QGroupBox() #creates the sub-box for the Shamrock status information
        statusbox.setTitle('Shamrock Status:')
        statusbox.setLayout(statuslayout)
        statuslayout.addWidget(self.specstatlbl, 0, 0) #calls the spectrometer status label from the __init__ function

        gratinglayout = QGridLayout()
        gratingbox = QGroupBox() #creates the sub-box for the grating setting
        gratingbox.setTitle('Grating:')
        gratingbox.setLayout(gratinglayout)
        gratinglayout.addWidget(self.gratinglbl, 0, 0) #calls the grating label from the __init__ function


        # Adds the sub-boxes to the main update box #
        labelslayout.addWidget(flipperbox, 0, 0)
        labelslayout.addWidget(gratingbox, 1, 0)
        labelslayout.addWidget(statusbox, 2, 0)

        groupbox.setLayout(labelslayout)

        return groupbox





    @pyqtSlot()

    # Shamrock initialization buttons #
    def on_click_close(self):
        sham.ShamrockClose()
        print('Shutdown Shamrock')
        self.specstatlbl.setText('Shamrock Shutdown')

    def on_click_reinit(self):
        sham.ShamrockInitialize(inifile)
        print('Reinitialize Shamrock')
        self.specstatlbl.setText('Shamrock Initialized')


    # Shamrock flipper mirror buttons #
    def on_click_resetoutflip(self):
        zeroinflip = sham.ShamrockFlipperMirrorReset(0, 1)
        print('Input Flipper Reset')
        self.infliplbl.setText('Input Flipper Straight')

    def on_click_resetinflip(self):
        zerooutflip = sham.ShamrockFlipperMirrorReset(0, 2)
        print('Output Flipper Reset')
        self.outfliplbl.setText('Output Flipper Straight')

    def on_click_straightinflip(self):
        print('Input Flipper Straight')
        direct_inputflipper = sham.ShamrockSetFlipperMirror(0, 1, 0)
        self.infliplbl.setText('Input Flipper Straight')

    def on_click_straightoutflip(self):
        print('Output Flipper Straight')
        direct_outputflipper = sham.ShamrockSetFlipperMirrorPosition(0, 2, 0)
        self.outfliplbl.setText('Output Flipper Straight')

    def on_click_rightinflip(self):
        print('Input Flipper Side')
        side_inputflipper = sham.ShamrockSetFlipperMirror(0, 1, 1)
        self.infliplbl.setText('Input Flipper Side')

    def on_click_leftoutflip(self):
        print('Output Flipper Side')
        side_outputflipper = sham.ShamrockSetFlipperMirror(0, 2, 1)
        self.outfliplbl.setText('Output Flipper Side')

    # Shamrock gratings buttons #
    def on_click_switch1(self):
        print('Grating Switched to 1')
        setgrate = sham.ShamrockSetGrating(0, 1)
        self.gratinglbl.setText('1250nm')


    def on_click_switch2(self):
        print('Grating Switched to 2')
        setgrate = sham.ShamrockSetGrating(0, 2)
        self.gratinglbl.setText('750nm')


    def on_click_switch3(self):
        print('Grating Switched to 3')
        setgrate = sham.ShamrockSetGrating(0, 3)
        self.gratinglbl.setText('1300nm')

# SpectrometerGui()