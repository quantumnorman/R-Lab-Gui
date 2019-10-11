import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QSizePolicy, QPushButton, QWidget, QRadioButton, QVBoxLayout, \
    QGroupBox, QHBoxLayout, QGridLayout, QInputDialog, QLineEdit, QFileDialog, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import csv
from atmcd import *
from PyQt5.QtCore import pyqtSlot
import datetime
from scipy import optimize
from pyAndorShamrock import Shamrock

# sham = Shamrock.Shamrock()

now = datetime.datetime.now()

cam = atmcd()


class DataacGui(QMainWindow):

    def __init__(self):
        # app = QApplication(sys.argv)
        # app.setStyle('Fusion')
        super(DataacGui, self).__init__()
        self.title = 'Spectrometer Data Acquisition'

        (ret, xpixels, ypixels) = cam.GetDetector()
        #
        self.imageSize = xpixels * ypixels

        self.initdataacUI()
        # sys.exit(app.exec_())

    def initdataacUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        control = Datacontrol()
        self.setCentralWidget(control)
        # self.show()


class Datacontrol(QWidget):

    def __init__(self):
        super(Datacontrol, self).__init__()
        self.initdataUI()

    def initdataUI(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)

        dataaclayout = QGridLayout()
        actimes = self.presetactimes
        continuous = self.continousbtns()
        mplplt = WidgetPlot()
        self.plot = mplplt
        saveload = self.saveloadbtns()
        # kinscans = self.kineticdatabtns()
        fit = self.fitting()

        dataaclayout.addWidget(actimes, 0, 0)
        dataaclayout.addWidget(mplplt, 0, 1, 5, 5)
        dataaclayout.addWidget(saveload, 4, 0)
        dataaclayout.addWidget(continuous, 2, 0)
        dataaclayout.addWidget(fit, 0, 6, 4, 2)
        # dataaclayout.addWidget(kinscans, 2,0)
        self.setLayout(dataaclayout)
        self.data = None
        self.exposuretime = None

    @property
    ##########Button Layouts##########
    def presetactimes(self):
        btnwid = 40
        btnhgt = 100

        pointonesbtn = QPushButton('0.1s', self)
        # pointonesbtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pointonesbtn.setMinimumHeight(btnhgt)
        pointonesbtn.clicked.connect(self.on_click_pointonesbtn)

        onesecbtn = QPushButton('1s', self)
        # onesecbtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        onesecbtn.setMinimumHeight(btnhgt)
        onesecbtn.clicked.connect(self.on_click_onesecbtn)

        tensecbtn = QPushButton('10s', self)
        # tensecbtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tensecbtn.setMinimumHeight(btnhgt)
        tensecbtn.clicked.connect(self.on_click_tensecbtn)

        sixtysecbtn = QPushButton('60s', self)
        # sixtysecbtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sixtysecbtn.setMinimumHeight(btnhgt)
        sixtysecbtn.clicked.connect(self.on_click_sixtysecbtn)

        self.inputbox = QLineEdit(self)
        self.inputbtn = QPushButton('Acquire (s)', self)
        self.inputbtn.clicked.connect(self.on_click_inputtime)

        btnlay = QGridLayout()
        btnlay.addWidget(pointonesbtn, 0, 0)
        btnlay.addWidget(onesecbtn, 0, 1)
        btnlay.addWidget(tensecbtn, 0, 2)
        btnlay.addWidget(sixtysecbtn, 0, 3)
        btnlay.addWidget(self.inputbox, 1, 0, 1, 2)
        btnlay.addWidget(self.inputbtn, 1, 2)

        groupbox = QGroupBox()
        groupbox.setLayout(btnlay)
        groupbox.setTitle('Single Scan Data Acquisition')
        return groupbox

    def saveloadbtns(self):
        btnhgt = 100

        savebtn = QPushButton('save data to txt', self)
        # savebtn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        savebtn.setMinimumHeight(btnhgt)
        savebtn.clicked.connect(self.on_click_singlesavedata)

        loadbtn = QPushButton('load data from txt', self)
        loadbtn.setMinimumHeight(btnhgt)
        # loadbtn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # loadbtn.clicked.connect(self.on_click_loaddata)

        btnlay = QGridLayout()
        btnlay.addWidget(savebtn, 0, 0)
        btnlay.addWidget(loadbtn, 0, 1)

        groupbox = QGroupBox()
        groupbox.setLayout(btnlay)

        return groupbox

    def continousbtns(self):
        btnhgt = 100

        startbtn = QPushButton('Start Scanning', self)
        startbtn.setMinimumHeight(btnhgt)
        # startbtn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        startbtn.clicked.connect(self.on_click_continuous)

        stopbtn = QPushButton('Stop Scanning', self)
        stopbtn.setMinimumHeight(btnhgt)
        # stopbtn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.)
        stopbtn.clicked.connect(self.on_click_stopcontinuous)

        btnlay = QHBoxLayout()
        btnlay.addWidget(startbtn)
        btnlay.addWidget(stopbtn)

        groupbox = QGroupBox()
        groupbox.setLayout(btnlay)
        groupbox.setTitle('Continuous Scan')

        return groupbox

    def fitting(self):
        fitting = QPushButton('Try Fit', self)
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
        paramfitbox.setTitle('Fitting Parameters')
        paramfitbox.setLayout(paramfitlay)

        fitlay = QGridLayout()
        fitlay.addWidget(fitselectbox, 0, 0)
        fitlay.addWidget(roifitbox, 1, 0)
        fitlay.addWidget(paramfitbox, 2, 0)
        fitlay.addWidget(fitting, 5, 0)

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

    ##########Save/Load##########

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        return fileName

    ##########Acquisition Types##########

    def singleacquisition(self, time):
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
            (ret) = cam.SetExposureTime(time)

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
        return data, time

    def continuousmode(self):
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
            (ret) = cam.SetExposureTime(.1)
            (ret) = cam.SetKineticCycleTime(0)

            (ret) = cam.PrepareAcquisition()
            (ret) = cam.StartAcquisition()
            (ret) = cam.WaitForAcquisition()
            (ret, fullframebuffer) = cam.GetMostRecentImage(imageSize)
            data = fullframebuffer

        else:
            print('Cannot continue, could not initialize camera')
        return data

    def fitfunc(self, func, x, data, amp, center, sigma):
        if self.lorbtn.isChecked():
            func = self.lor

        if self.gaubtn.isChecked():
            func = self.gauss

        popt, _ = optimize.curve_fit(func(x, amp, center, sigma), x, data)
        return popt

    def gauss(self, x, amp, center, sigma):
        return amp * np.exp(-(x - center) ** 2 / (2 * sigma ** 2))

    def lor(self, x, amp, center, sigma):
        return amp * sigma ** 2 / (sigma ** 2 + (x - center) ** 2)

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
    def on_click_pointonesbtn(self):
        # data = [np.tan(i) for i in range(250)]
        self.data, self.exposuretime = self.singleacquisition(0.1)
        self.plot.plot(self.data)
        return self.data, self.exposuretime

    # failed attempt to use single acquisition(time) for on_click(time)

    # def on_click_singleacbtn(self, time):
    #     fullFramebuffer = self.singleacquisition(time)
    #     self.data = fullFramebuffer
    #     self.plot.plot(self.data)
    #     return self.data

    def on_click_onesecbtn(self):
        self.data, self.exposuretime = self.singleacquisition(1)
        self.plot.plot(self.data)
        return self.data, self.exposuretime

    def on_click_tensecbtn(self):
        self.data, self.exposuretime = self.singleacquisition(10)
        self.plot.plot(self.data)
        return self.data, self.exposuretime

    def on_click_sixtysecbtn(self):
        self.data, self.exposuretime = self.singleacquisition(60)
        self.plot.plot(self.data)
        return self.data, self.exposuretime

    def on_click_inputtime(self):
        textboxvalue = self.inputbox.text()
        self.data, self.exposuretime = self.singleacquisition(float(textboxvalue))
        self.plot.plot(self.data)
        return self.data, self.exposuretime

    def on_click_continuous(self):
        self.condition = 1
        while self.condition != 0:
            self.data = self.continuousmode()
            self.plot.plot(self.data)
            time.sleep(.01)
            QApplication.processEvents()

    def on_click_stopcontinuous(self):
        self.condition = 0
        (ret) = cam.ShutDown()
        print("Shutdown returned", ret)
        # todo: implement threading to stop stalling

    def on_click_fit(self):
        data = self.data




    # Formatting save files
    def on_click_singlesavedata(self):
        (ret) = cam.Initialize("/usr/local/etc/andor")  # initialise camera
        (ret, iSerialNumber) = cam.GetCameraSerialNumber()
        (ret, caps) = cam.GetCapabilities()
        (ret, grating) = sham.ShamrockGetGrating(0)
        (ret, lines, blaze, home, offset) = sham.ShamrockGetGratingInfo(0, grating)

        datafilename = self.saveFileDialog()
        file = open(datafilename, 'w', newline='')
        tsv_writer = csv.writer(file, delimiter='\t')
        tsv_writer.writerow([now.strftime("%Y-%m-%d %H:%M")])
        tsv_writer.writerow([])
        if caps.ulCameraType == 14:
            tsv_writer.writerow(['Camera Type: InGaAs'])
        else:
            tsv_writer.writerow(['Camera Type: unknown'])
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
        datalist = list(self.data)
        for i in range(len(datalist)):
            tsv_writer.writerow([i, datalist[i]])
        file.close()


# kinetic scans click
# def on_click_tenscans(self):
#     datarray = self.kineticacquisition(.1, 10, 1)
#     self.data = datarray
#     print(self.data)
#     return self.data


##########Plotting##########

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, data):
        self.axes.plot(data, 'r.')
        self.axes.set_title('PyQt Matplotlib Example')
        self.draw()


class WidgetPlot(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)

    def plot(self, data):
        self.canvas.axes.clear()
        self.canvas.plot(data)

    def plotfit(self, x, fit):
        self.canvas.plot(x, fit)

# TODO: threading for continous mode might make things run smoother

# DataacGui()
