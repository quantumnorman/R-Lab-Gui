import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QRadioButton, QSizePolicy, QPushButton, QWidget, \
    QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout, QInputDialog, QLineEdit, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import csv
from atmcd import *
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QSize
import datetime
from scipy import optimize
from pyAndorShamrock import Shamrock

sham = Shamrock.Shamrock()
now = datetime.datetime.now()
cam = atmcd()

# DataacGui sets up the window and calls the widget Datacontrol
class DataacGui(QMainWindow):

    def __init__(self):
        # app = QApplication(sys.argv)
        # app.setStyle('Fusion')
        super(DataacGui, self).__init__()
        self.title = 'Spectrometer Data Acquisition'

        self.initdataacUI()
        # sys.exit(app.exec_())

    def initdataacUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        control = Datacontrol()
        self.setCentralWidget(control)
        # self.show()

#Data control sets up the layout and functions for data acquisition
class Datacontrol(QWidget):

    def __init__(self):
        super(Datacontrol, self).__init__()
        self.initdataUI()

    #sets up initial values and lays out the various group boxes in a mostly pleasing manner
    def initdataUI(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        # self.wavelength = np.linspace(0, 512, 512)

        #initialising the various sets of buttons and screens that are defined below
        dataaclayout = QGridLayout()
        actimes = self.presetactimes #the preset acquisition time buttons
        continuous = self.continousbtns() #the continuous buttons
        background = self.backgroundbtns() #the background subtraction buttons
        mplplt = WidgetPlot() #initialising the widget plot class
        self.plot = mplplt #naming the widgetplot class
        saveload = self.saveloadbtns() #the save/load data buttons
        # kinscans = self.kineticdatabtns()
        fit = self.fitting() #the fitting panel
        self.plot.setMinimumSize(QSize(600, 600))

        #laying out the buttons and plot
        dataaclayout.addWidget(actimes, 0, 0)
        dataaclayout.addWidget(background, 3, 0, 1, 2)
        dataaclayout.addWidget(mplplt, 0, 1, 5, 5)
        dataaclayout.addWidget(saveload, 4, 0)
        dataaclayout.addWidget(continuous, 2, 0)
        dataaclayout.addWidget(fit, 0, 6, 4, 2)
        # dataaclayout.addWidget(kinscans, 2,0)
        self.setLayout(dataaclayout)

        #initial values so as not to break the code before we even start
        self.data = None
        self.bkgnd = [0]*512
        self.exposuretime = None
        # self.getwavel()

    @property
    ##########Button Layouts##########
    def presetactimes(self):
        btnwid = 40
        btnhgt = 50

        pointonesbtn = QPushButton('0.1s', self) #names and creates a push button
        pointonesbtn.setMinimumHeight(btnhgt) #sets button sizes
        pointonesbtn.clicked.connect(lambda: self.on_click_singleacbtn(.1)) #links the single acquisition function to
        # the clicked button signal

        onesecbtn = QPushButton('1s', self)
        onesecbtn.setMinimumHeight(btnhgt)
        onesecbtn.clicked.connect(lambda: self.on_click_singleacbtn(1))

        tensecbtn = QPushButton('10s', self)
        tensecbtn.setMinimumHeight(btnhgt)
        tensecbtn.clicked.connect(lambda: self.on_click_singleacbtn(10))

        sixtysecbtn = QPushButton('60s', self)
        sixtysecbtn.setMinimumHeight(btnhgt)
        sixtysecbtn.clicked.connect(lambda: self.on_click_singleacbtn(60))

        self.inputbox = QLineEdit(self) #this creates a textbox to allow for arbitrary exposure times
        self.inputbox.setText('0.1') #this auto-sets to the textbox value to 0.1 so that we don't run into issues with
        # a blank box, but you can change it
        self.inputbox.setMaximumWidth(btnhgt)
        self.inputbtn = QPushButton('Acquire (s)', self) #button to actually run acquisition for the textbox
        self.inputbtn.clicked.connect(self.on_click_inputtime) #connects to push button signal to arbitrary time function

        #lays out the single acquisition buttons
        btnlay = QGridLayout()
        btnlay.addWidget(pointonesbtn, 0, 0)
        btnlay.addWidget(onesecbtn, 0, 1)
        btnlay.addWidget(tensecbtn, 0, 2)
        btnlay.addWidget(sixtysecbtn, 0, 3)
        btnlay.addWidget(self.inputbox, 1, 0)
        btnlay.addWidget(self.inputbtn, 1, 2)

        groupbox = QGroupBox()
        groupbox.setLayout(btnlay)
        groupbox.setTitle('Single Scan Data Acquisition')
        return groupbox

    #setting up the save/load buttons
    def saveloadbtns(self):
        btnhgt = 50

        savebtn = QPushButton('save data to txt', self)
        savebtn.setMinimumHeight(btnhgt)
        savebtn.clicked.connect(self.on_click_singlesavedata)

        loadbtn = QPushButton('load data from txt', self)
        loadbtn.setMinimumHeight(btnhgt)
        loadbtn.clicked.connect(self.on_click_loaddata)

        btnlay = QGridLayout()
        btnlay.addWidget(savebtn, 0, 0)
        btnlay.addWidget(loadbtn, 0, 1)

        groupbox = QGroupBox()
        groupbox.setLayout(btnlay)

        return groupbox

    #buttons for continuous acquisition
    def continousbtns(self):
        btnhgt = 50

        self.conexptext = QLineEdit(self)
        self.conexptext.setText('0.1')
        self.conexptext.setMaximumWidth(btnhgt)

        startbtn = QPushButton('Start Scanning', self)
        startbtn.setMinimumHeight(btnhgt)
        startbtn.clicked.connect(self.on_click_continuous)

        stopbtn = QPushButton('Stop Scanning', self)
        stopbtn.setMinimumHeight(btnhgt)
        stopbtn.clicked.connect(self.on_click_stopcontinuous)

        btnlay = QHBoxLayout()
        btnlay.addWidget(self.conexptext)
        btnlay.addWidget(startbtn)
        btnlay.addWidget(stopbtn)

        groupbox = QGroupBox()
        groupbox.setLayout(btnlay)
        groupbox.setTitle('Continuous Scan')

        return groupbox

    #background subtraction options
    def backgroundbtns(self):
        btnhgt = 50

        self.bkgrndexptext = QLineEdit(self)
        self.bkgrndexptext.setText('0.1')
        self.bkgrndexptext.setMaximumWidth(btnhgt)

        self.usebkgrnd = QRadioButton('Use Background')
        self.nousebkgrnd = QRadioButton('No Background')
        self.nousebkgrnd.setChecked(True)

        takebkgrnd = QPushButton('Take Background', self)
        takebkgrnd.setMinimumHeight(btnhgt)
        takebkgrnd.clicked.connect(self.on_click_takebkgrnd)

        selectbkgrnd = QPushButton('Background from File', self)
        selectbkgrnd.setMinimumHeight(btnhgt)
        selectbkgrnd.clicked.connect(self.on_click_selectbkgnd)

        btnlay = QGridLayout()
        btnlay.addWidget(self.usebkgrnd, 0, 0, 1, 2)
        btnlay.addWidget(self.nousebkgrnd, 0, 2, 1, 2)
        btnlay.addWidget(self.bkgrndexptext, 1, 0)
        btnlay.addWidget(takebkgrnd, 1, 1)
        btnlay.addWidget(selectbkgrnd, 1, 2)

        groupbox = QGroupBox()
        groupbox.setLayout(btnlay)
        groupbox.setTitle('Background')

        return groupbox

    #layout of fitting panel
    def fitting(self):
        fitting = QPushButton('Try Fit', self)
        # fitting.clicked.connect(self.on_click_fitfunc)

        self.lorbtn = QRadioButton('Lorentzian')
        self.gaubtn = QRadioButton('Gaussian')

        self.lorbtn.setChecked(True)

        self.lminfit = QLineEdit()
        self.lmaxfit = QLineEdit()
        lmintag = QLabel('Lambda Min')
        lmaxtag = QLabel('Lambda Max')

        self.ampfit = QLineEdit()
        ampfittag = QLabel('Amplitude')

        self.centerfit = QLineEdit()
        centerfittag = QLabel('Center')

        self.sigmafit = QLineEdit()
        sigmafittag = QLabel('Sigma')

        fitselect = QGridLayout()
        fitselect.addWidget(self.lorbtn, 0, 0)
        fitselect.addWidget(self.gaubtn, 0, 1)
        fitselectbox = QGroupBox()
        fitselectbox.setLayout(fitselect)
        fitselectbox.setTitle('Fit Type')

        roifitlay = QGridLayout()
        roifitlay.addWidget(self.lminfit, 0, 1)
        roifitlay.addWidget(lmintag, 0, 0)
        roifitlay.addWidget(lmaxtag, 1, 0)
        roifitlay.addWidget(self.lmaxfit, 1, 1)
        roifitbox = QGroupBox()
        roifitbox.setLayout(roifitlay)
        roifitbox.setTitle('Region of Interest')

        paramfitlay = QGridLayout()
        paramfitlay.addWidget(ampfittag, 0, 0)
        paramfitlay.addWidget(self.ampfit, 0, 1)
        paramfitlay.addWidget(centerfittag, 1, 0)
        paramfitlay.addWidget(self.centerfit, 1, 1)
        paramfitlay.addWidget(sigmafittag, 2, 0)
        paramfitlay.addWidget(self.sigmafit, 2, 1)
        paramfitbox = QGroupBox()
        paramfitbox.setTitle('Initial Guess Parameters')
        paramfitbox.setLayout(paramfitlay)

        fitparalay = QGridLayout()
        retamplbl = QLabel('Amplitude Fit:')
        retcenlbl = QLabel('Center Fit:')
        retsiglbl = QLabel('Sigma Fit:')
        retstdevlbl = QLabel('Standard Dev Fit:')
        self.retampval = QLabel()
        self.retcenval = QLabel()
        self.retsigval = QLabel()
        self.retstdeval = QLabel()
        fitparalay.addWidget(retamplbl, 0, 0)
        fitparalay.addWidget(retcenlbl, 1, 0)
        fitparalay.addWidget(retsiglbl, 2, 0)
        fitparalay.addWidget(retstdevlbl, 3, 0)
        fitparalay.addWidget(self.retampval, 0, 1)
        fitparalay.addWidget(self.retcenval, 1, 1)
        fitparalay.addWidget(self.retsigval, 2, 1)
        fitparalay.addWidget(self.retstdeval, 3, 1)

        fitparabox = QGroupBox()
        fitparabox.setTitle('Returned Fit Parameters')
        fitparabox.setLayout(fitparalay)

        fitlay = QGridLayout()
        fitlay.addWidget(fitselectbox, 0, 0)
        fitlay.addWidget(roifitbox, 1, 0)
        fitlay.addWidget(paramfitbox, 2, 0)
        fitlay.addWidget(fitting, 5, 0)
        fitlay.addWidget(fitparabox, 3, 0)

        fitbox = QGroupBox()
        fitbox.setLayout(fitlay)
        fitbox.setTitle('Fitting')

        return fitbox

    # kinetic buttons
    # def kineticdatabtns(self):
    #     btnwid = 40
    #     btnhgt = 40
    #
    #     tenscans = QPushButton('10 Kinetic Scans', self)
    #     tenscans.clicked.connect(self.on_click_tenscans)
    #
    #     btnlay = QGridLayout()
    #     btnlay.addWidget(tenscans,0,0)
    #
    #     groupbox = QGroupBox()
    #     groupbox.setLayout(btnlay)
    #
    #     return groupbox

    def gauss(self, x, amp, center, sigma):
        return amp * np.exp(-(x - center) ** 2 / (2 * sigma ** 2))

    def lor(self, x, amp, center, sigma):
        return amp * sigma ** 2 / (sigma ** 2 + (x - center) ** 2)

    def getwavel(self):
        wavelength = np.linspace(0, 511, 512)
        return wavelength
        # ret, self.waveset = sham.ShamrockGetWavelength(0)
        # ret, self.gratingset = sham.ShamrockGetGrating(0)
        #
        # if self.gratingset == 1:
        #     wavemin = self.waveset
        #     wavemax = self.waveset
        #     wavelength = np.linspace(wavemin, wavemax, 512)
        #     # print(wavelength)
        #     return wavelength
        #
        # if self.gratingset == 2:
        #     wavemin = self.waveset
        #     wavemax = self.waveset
        #     wavelength = np.linspace(wavemin, wavemax, 512)
        #     # print(wavelength)
        #     return wavelength
        #
        # if self.gratingset == 3:
        #     wavemin = self.waveset
        #     wavemax = self.waveset
        #     wavelength = np.linspace(wavemin, wavemax, 512)
        #     # print(wavelength)
        #     return wavelength


# kinetic acquisition
    # def kineticacquisition(self, exposuretime, imagenumber, cycletime):
    #
    #     numberOfImages = imagenumber
    #     print("Intialising Camera")
    #     (ret) = cam.Initialize("/usr/local/etc/andor")  # initialise camera
    #     print("Initialize returned", ret)
    #
    #     dataarray = np.zeros((numberOfImages, 512))
    #
    #     if atmcd.DRV_SUCCESS == ret:
    #         # configure the acquisition
    #         (ret) = cam.CoolerON()
    #         print("Function CoolerON returned", ret)
    #
    #         (ret) = cam.SetAcquisitionMode(3)
    #         (ret) = cam.SetNumberKinetics(numberOfImages);
    #         (ret) = cam.SetReadMode(4)
    #         (ret) = cam.SetTriggerMode(0)
    #         (ret, xpixels, ypixels) = cam.GetDetector()
    #         (ret) = cam.SetImage(1, 1, 1, xpixels, 1, ypixels)
    #         (ret) = cam.SetExposureTime(exposuretime)
    #         (ret) = cam.SetKineticCycleTime(cycletime)
    #
    #         (ret) = cam.PrepareAcquisition()
    #         print("Function PrepareAcquisition returned", ret)
    #
    #         # Perform Acquisition
    #         (ret) = cam.StartAcquisition()
    #         print("Function StartAcquisition returned", ret)
    #
    #         imageSize = xpixels * ypixels
    #
    #         for currentImage in range(numberOfImages):
    #             print("Acquiring image", currentImage)
    #
    #             (ret) = cam.WaitForAcquisition()
    #             print("Function WaitForAcquisition returned", ret)
    #
    #             (ret, fullFrameBuffer) = cam.GetMostRecentImage(imageSize)
    #             print("Function GetMostRecentImage returned", ret, "first pixel =", fullFrameBuffer[0], "size =",
    #                   imageSize)
    #             data = list(fullFrameBuffer)
    #             data = np.asarray(data)
    #             dataarray[currentImage] = data
    #
    #         # Clean up
    #         (ret) = cam.ShutDown()
    #         print("Shutdown returned", ret)
    #     else:
    #         print("Cannot continue, could not initialise camera")
    #
    #     return dataarray #

    @pyqtSlot()
    # functions for single acquisitions
    def on_click_singleacbtn(self, time): #function for the single acquisition preset time buttons
        self.thread = SingleAcquisitionThread(time) #connects to the thread
        self.thread.start()
        self.thread.signal.connect(self.on_thread_done)
        self.exposuretime = time
        # self.wavelength = self.getwavel()
        self.wavelength = np.linspace(0, 511, 512)
    def on_click_inputtime(self):
        textboxvalue = float(self.inputbox.text())
        self.thread = SingleAcquisitionThread(textboxvalue)
        self.thread.start()
        self.thread.signal.connect(self.on_thread_done)
        self.wavelength = self.getwavel()
        self.exposuretime = textboxvalue


    def on_thread_done(self, data):
        self.data = np.array(list(data)) #sets data to a global variable so we can call it in other functions
        if self.usebkgrnd.isChecked():
            data = self.data-self.bkgnd #subtracts the background so we plot the data without the background
        if self.nousebkgrnd.isChecked():
            data = self.data
        self.plot.plot(self.wavelength, data) #uses the QWidget class for plotting

    # functions for continuous buttons
    def on_click_continuous(self):
        time = float(self.conexptext.text())
        self.thread = ContinuousAcquisitionThread(time)
        self.thread.start()
        self.thread.signal.connect(self.on_thread_done)
        self.wavelength = self.getwavel() #makes sure that the plot updates with the correct wavelength

    def on_click_stopcontinuous(self):
        self.thread.halt()

    #functions for background buttons
    def on_thread_done_bkgnd(self, data):
        self.bkgnd = list(data)
        self.bkgnd = np.array(self.bkgnd)

    def on_click_takebkgrnd(self):
        textboxvalue = float(self.bkgrndexptext.text())
        self.thread = SingleAcquisitionThread(textboxvalue)
        self.thread.start()
        self.thread.signal.connect(self.on_thread_done_bkgnd)
        (ret) = cam.Initialize("/usr/local/etc/andor")  # initialise camera
        (ret, iSerialNumber) = cam.GetCameraSerialNumber()
        (ret, caps) = cam.GetCapabilities()
        (ret, grating) = sham.ShamrockGetGrating(0)
        (ret, lines, blaze, home, offset) = sham.ShamrockGetGratingInfo(0, grating)

        self.bkgrndatafilename = self.saveFileDialog()
        file = open(self.bkgrndatafilename, 'w', newline='')
        tsv_writer = csv.writer(file, delimiter='\t')
        tsv_writer.writerow([now.strftime("%Y-%m-%d %H:%M")])
        tsv_writer.writerow(['Background File'])
        tsv_writer.writerow([])
        if caps.ulCameraType == 14:
            tsv_writer.writerow(['Camera Type:', 'InGaAs'])
        else:
            tsv_writer.writerow(['Camera Type:', 'unknown'])
        tsv_writer.writerow(['Camera Serial Number:', iSerialNumber])
        tsv_writer.writerow([])
        tsv_writer.writerow(['Grating lines:', lines])
        tsv_writer.writerow(['Grating blaze:', blaze])
        tsv_writer.writerow(['Grating offset:', offset])
        tsv_writer.writerow(['Grating home:', home])
        tsv_writer.writerow([])
        tsv_writer.writerow(['Exposure time:', self.exposuretime])
        tsv_writer.writerow([])
        tsv_writer.writerow(['Point', 'Counts'])
        datalist = list(self.bkgnd)
        for i in range(len(datalist)):
            tsv_writer.writerow([i, datalist[i]])
        file.close()

    def on_click_selectbkgnd(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.bkgrndatafilename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                                "All Files (*);;Python Files (*.py)", options=options)
        self.bkgrndatafilename = str(self.bkgrndatafilename)
        print(self.bkgrndatafilename)
        if not self.bkgrndatafilename: return
        self.wavelength, self.data = np.loadtxt(self.bkgrndatafilename, usecols=(0, 1), skiprows=15, unpack=True)
        return self.wavelength, self.bkgnd

    ##########Save/Load##########
    #
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        return fileName

    def loadtext(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        fileName = str(fileName)
        print(fileName)
        if not fileName: return
        self.wavelength, self.data = np.loadtxt(fileName, usecols=(0, 1), skiprows=15, unpack=True)
        return self.wavelength, self.data

    def on_click_loaddata(self):
        self.wavelength, data = self.loadtext()
        self.data = data
        self.plot.plot(self.wavelength, self.data)

    # Formatting save files
    def on_click_singlesavedata(self):
        #here we get spectrometer and camera info for the file saving header
        (ret) = cam.Initialize("/usr/local/etc/andor")  # initialise camera
        (ret, iSerialNumber) = cam.GetCameraSerialNumber()
        (ret, caps) = cam.GetCapabilities()
        (ret, grating) = sham.ShamrockGetGrating(0)
        (ret, lines, blaze, home, offset) = sham.ShamrockGetGratingInfo(0, grating)

        #this is where we start to format the save files
        datafilename = self.saveFileDialog() #using the file name selected in the file dialog
        file = open(datafilename, 'w', newline='') #begin the writing
        tsv_writer = csv.writer(file, delimiter='\t') #defining the filetype as tab-separated
        tsv_writer.writerow([now.strftime("%Y-%m-%d %H:%M")]) #includes date and time
        tsv_writer.writerow([]) #blank row
        tsv_writer.writerow(['Background File Name:', self.bkgrndatafilename])

        #writes camera type and grating info
        if caps.ulCameraType == 14:
            tsv_writer.writerow(['Camera Type:', 'InGaAs'])
        else:
            tsv_writer.writerow(['Camera Type:', 'unknown'])
        tsv_writer.writerow(['Camera Serial Number:', iSerialNumber])
        tsv_writer.writerow([])
        tsv_writer.writerow(['Grating lines:', lines])
        tsv_writer.writerow(['Grating blaze:', blaze])
        tsv_writer.writerow(['Grating offset:', offset])
        tsv_writer.writerow(['Grating home:', home])
        tsv_writer.writerow([])
        tsv_writer.writerow(['Exposure time:', self.exposuretime])
        tsv_writer.writerow([])
        tsv_writer.writerow(['Wavelength', 'Counts']) #writes the data
        datalist = list(self.data)
        for i in range(len(datalist)):
            tsv_writer.writerow([i, self.wavelength[i], datalist[i]])
        file.close()

    def setcolor(self, text):
        print(text)
        if text == 'Heat':
            self.colormap = self.heat
        if text == 'Grayscale':
            self.colormap = self.gray
        if text == 'Rainbow':
            self.colormap = self.rainbow

    #Fitting functions
    # def on_click_fitfunc(self):
    #     #reading in values from texts
    #     amp = float(self.ampfit.text())
    #     center = float(self.centerfit.text())
    #     sigma = float(self.centerfit.text())
    #
    #     #reading in data and wavelength values
    #     data = self.data
    #     x = self.wavelength
    #
    #     #selecting which kind of fitting
    #     if self.lorbtn.isChecked():
    #         func = self.lor
    #
    #     if self.gaubtn.isChecked():
    #         func = self.gauss
    #
    #     #using the scipy fitting functions
    #     popt, pcov = optimize.curve_fit(func, x, data, p0=[amp, center, sigma])
    #
    #     #read out to the fit values
    #     self.ampfitval = popt[0]
    #     self.centerfitval = popt[1]
    #     self.sigmfitval = popt[2]
    #     self.perr = np.sqrt(np.diag(pcov))
    #
    #     #plot the fit over the data
    #     fit = func(x, popt[0], popt[1], popt[2])
    #     self.plot.plotfit(x, fit)
    #
    #     #update the labels
    #     self.retstdeval.setText(str(self.perr))
    #     self.retsigval.setText(str(self.sigmfitval))
    #     self.retcenval.setText(str(self.centerfitval))
    #     self.retampval.setText(str(self.ampfitval))
    #     # TODO: reformat value box
    #
    #     print(popt)


# kinetic scans click
# def on_click_tenscans(self):
#     datarray = self.kineticacquisition(.1, 10, 1)
#     self.data = datarray
#     print(self.data)
#     return self.data


##########Plotting##########
class PlotCanvas(FigureCanvas): #this creates a matplotlib canvas and defines some plotting aspects

    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, x, data):
        self.axes.plot(x, data, 'b.')
        self.axes.set_title('Title')
        self.draw()


class WidgetPlot(QWidget): #this converts the matplotlib canvas into a qt5 widget so we can implement it in the qt
    # framework laid out above
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)


    def plot(self, x, data):
        self.canvas.axes.clear() #it is important to clear out the plot first or everything just gets plotted on top of
        # each other and it becomes useless
        self.canvas.plot(x, data)


#this is where the threading happens (credit to Tristan Rasmussen for walking me through most of this)
class SingleAcquisitionThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, time): #'time' is the exposure time. This line makes it such that we can enter an exposure time that then gets passed down to the part of the thread where we actually run the code
        QThread.__init__(self)
        self.time = time

    def run(self): #This code was taken from the Andor pythonsdk2 'single scan' example with only a few tweaks
        print("Intialising Camera")
        cam = atmcd()  # load the atmcd library
        (ret) = cam.Initialize("/usr/local/etc/andor")  # initialise camera
        print("Initialize returned", ret)

        if atmcd.DRV_SUCCESS == ret:
            (ret, iSerialNumber) = cam.GetCameraSerialNumber()

            # configure the acquisition
            (ret) = cam.CoolerON()
            (ret) = cam.SetAcquisitionMode(1)
            (ret) = cam.SetReadMode(4)
            (ret) = cam.SetTriggerMode(0)
            (ret, xpixels, ypixels) = cam.GetDetector()
            (ret) = cam.SetImage(1, 1, 1, xpixels, 1, ypixels)
            (ret) = cam.SetExposureTime(self.time)

            (ret) = cam.PrepareAcquisition()
            # Perform Acquisition
            (ret) = cam.StartAcquisition()
            (ret) = cam.WaitForAcquisition()

            imageSize = xpixels * ypixels
            (ret, fullFrameBuffer) = cam.GetMostRecentImage(imageSize)
            data = fullFrameBuffer
            (ret) = cam.ShutDown()
            print("Shutdown returned", ret)
        else:
            print("Cannot continue, could not initialise camera")
        self.signal.emit(data) #This sends out the data into the main process when the thread is finished.
        # There's another function above 'on_thread_done' that 'data' gets passed to that handles updating the plot and
        # passing the data on to the rest of the functions

#Continuous acquisition thread is almost identicaly to the single acquisition thread, but the acquisition mode is set
# to 5 (video mode) and I implemented a while loop to keep the thread running and updating until the 'stop continuous'
# button interrupts it
class ContinuousAcquisitionThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, time):
        QThread.__init__(self)
        self.time = time
        self.condition = 1

    def run(self):
        print("Intialising Camera")
        cam = atmcd()  # load the atmcd library
        (ret) = cam.Initialize("/usr/local/etc/andor")
        if atmcd.DRV_SUCCESS == ret:

            # configure the acquisition
            (ret) = cam.CoolerON()
            # print("Function CoolerON returned", ret)
            print('scan')

            (ret) = cam.SetAcquisitionMode(5)
            (ret) = cam.SetReadMode(4)
            (ret) = cam.SetTriggerMode(0)
            (ret, xpixels, ypixels) = cam.GetDetector()
            imageSize = xpixels * ypixels

            (ret) = cam.SetImage(1, 1, 1, xpixels, 1, ypixels)
            (ret) = cam.SetExposureTime(self.time)
            while self.condition == 1:
                (ret) = cam.PrepareAcquisition()
                (ret) = cam.StartAcquisition()
                (ret) = cam.WaitForAcquisition()
                (ret, fullframebuffer) = cam.GetMostRecentImage(imageSize)
                data = fullframebuffer
                self.signal.emit(data)
                # time.sleep(.01)

        else:
            print('Cannot continue, could not initialize camera')

    def halt(self):
        self.condition = 0

# DataacGui()