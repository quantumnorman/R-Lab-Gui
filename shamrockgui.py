import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout, QLabel, QLineEdit

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from pyAndorShamrock import Shamrock
sham = Shamrock.Shamrock()
inifile = 'C:\\Users\\R-Lab\\Desktop\\detector.ini'

# This class sets up the window and framework for the spectrometer controls
class SpectrometerGui(QMainWindow):
    # This and initspecui sets some default values to load in upon startup
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

#This class defines the qwidgets for the spectrometer controls
class SpecControlbtns(QWidget):
    def __init__(self):
        super(SpecControlbtns, self).__init__()

        # Initializes the status updating labels #
        ret, gratingset = sham.ShamrockGetGrating(0)
        self.gratinglbl = QLabel()
        if gratingset == 1:
            self.gratinglbl.setText('1250')
        if gratingset ==2:
            self.gratinglbl.setText('750')
        if gratingset ==3:
            self.gratinglbl.setText('1300')

        self.outfliplbl = QLabel()
        ret, outflipset = sham.ShamrockGetFlipperMirror(0,2)
        print(outflipset)
        print(ret)
        if outflipset ==0:
            self.outfliplbl.setText('Output Flipper Straight')
        if outflipset ==1:
            self.outfliplbl.setText('Output Flipper Side')

        self.infliplbl = QLabel()
        ret, inflipset = sham.ShamrockGetFlipperMirror(0,1)
        print(inflipset)
        print(ret)
        if inflipset==0:
            self.infliplbl.setText('Input Flipper Straight')
        if inflipset==1:
            self.infliplbl.setText("Input Flipper Side")

        self.wavelbl = QLabel()
        ret, waveset = sham.ShamrockGetWavelength(0)
        waveset = str(waveset)
        self.wavelbl.setText(waveset)

        self.specstatlbl = QLabel('Spectrometer Initialized')
        self.btnslayout()
    #This sets up the layout for the buttons
    def btnslayout(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)

        speclayout = QGridLayout()
        specbtns = self.initializespecbtns()
        flipbtns = self.flipspecbtns()
        gratingsbtns = self.gratingsbtns()
        wavelength = self.wavelengthbox()
        update = self.updatelbls()

        speclayout.addWidget(flipbtns, 1, 0,1, 2)
        speclayout.addWidget(gratingsbtns, 0,0,1, 2)
        speclayout.addWidget(specbtns, 3,0,1,2)
        speclayout.addWidget(update, 0,4, 3, 4)
        speclayout.addWidget(wavelength,2,0, 1,1)

        self.setLayout(speclayout)

    #The following few functions are for setting up and laying out the various buttons
    #It follows a basic outline: 1) intialising the buttons
                                #2) adding the buttons to a layout
                                #3) adding the buttons to a groupbox which what the fuction returns when called upstream in btnslayout
    # Creates the initialization control buttons #
    def initializespecbtns(self):

        closebtn = QPushButton('Shutdown Shamrock', self) #this creates a button
        closebtn.clicked.connect(self.on_click_close) #this assigns a function (defined below) to be executed when clicked

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
        gbox.addWidget(zeroinbtn,0, 1)
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
        grating1 = QPushButton('1250 Grating', self)
        grating1.clicked.connect(self.on_click_switch1)

        grating2 = QPushButton('750 Grating', self)
        grating2.clicked.connect(self.on_click_switch2)

        grating3 = QPushButton('1300 Grating', self)
        grating3.clicked.connect(self.on_click_switch3)

        gbox = QGridLayout()
        gbox.addWidget(grating1, 0, 0)
        gbox.addWidget(grating2, 0, 1)
        gbox.addWidget(grating3, 0, 3)


        groupbox = QGroupBox()
        groupbox.setLayout(gbox)
        groupbox.setTitle('Grating Controls')

        return groupbox

    # Creates the set wavelength box #
    def wavelengthbox(self):
        self.wavelengthbox = QLineEdit() #this defines a textbox
        wavesetbtn = QPushButton('Set Wavelength', self) #this defines the button
        wavesetbtn.clicked.connect(self.on_click_wavelength)

        gbox = QGridLayout()
        gbox.addWidget(self.wavelengthbox, 0, 0)
        gbox.addWidget(wavesetbtn, 0, 1)

        groupbox = QGroupBox()
        groupbox.setLayout(gbox)
        groupbox.setTitle('Set Wavelength')

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

        wavelayout = QGridLayout()
        wavebox = QGroupBox()
        wavebox.setLayout(wavelayout)
        wavebox.setTitle('Wavelength')
        wavelayout.addWidget(self.wavelbl, 0,0)



        # Adds the sub-boxes to the main update box #
        labelslayout.addWidget(flipperbox, 0, 0)
        labelslayout.addWidget(gratingbox, 1, 0)
        labelslayout.addWidget(statusbox, 2, 0)
        labelslayout.addWidget(wavebox,3,0)

        groupbox.setLayout(labelslayout)

        return groupbox



    #Below are the signals that actually make the buttons work at all

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
        # calib = sham.ShamrockSetWavelength(0,1035)
        # offset = sham.ShamrockSetDetectorOffset(0, -96)
        ret, grate = sham.ShamrockGetGrating(0)
        print(grate)

        if grate ==1:
            self.gratinglbl.setText('1250')


    def on_click_switch2(self):
        print('Grating Switched to 2')
        setgrate = sham.ShamrockSetGrating(0, 2)
        # calib = sham.ShamrockSetWavelength(0,1296.5)
        # offset = sham.ShamrockSetDetectorOffset(0, -280)
        ret, grate = sham.ShamrockGetGrating(0)
        print(grate)

        if grate ==2:
            self.gratinglbl.setText('750')


    def on_click_switch3(self):
        setgrate = sham.ShamrockSetGrating(0, 3)
        # calib = sham.ShamrockSetWavelength(0,1286.89)
        # offset = sham.ShamrockSetDetectorOffset(0, -300)
        ret, grate = sham.ShamrockGetGrating(0)
        print(grate)

        if grate ==3:
            self.gratinglbl.setText('1300')

    # Set wavelength button and textbox #
    def on_click_wavelength(self):
        wavel = self.wavelengthbox.text() #this reads in the text written in the textbox wavelengthbox
        wavel = float(wavel) #this converts the text from a string to a float
        sham.ShamrockSetWavelength(0, wavel)
        ret, self.waveset = sham.ShamrockGetWavelength(0)
        self.waveset = str(self.waveset)
        self.wavelbl.setText(self.waveset) #this updates the label on the side


# SpectrometerGui()