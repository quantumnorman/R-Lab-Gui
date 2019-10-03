import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow,  QApplication, QSizePolicy, QPushButton, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout, QInputDialog, QLineEdit, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import csv
from atmcd import *
from PyQt5.QtCore import pyqtSlot

cam = atmcd()
#
# inifile = 'C:\\Users\\R-Lab\\Desktop\\cam.ini'
# cam.Initialize(inifile)
# print('Camera Initialized')
# cam.CoolerON()
# print('Cooler On')
# cam.SetAcquisitionMode(1) ##Sets acquisition mode to single scan
# print('Acquisition mode set to single scan')
# cam.SetTriggerMode(0)
# (ret, xpixels, ypixels) = cam.GetDetector()
# imageSize = xpixels * ypixels
# cam.SetImage(1, 1, 1, xpixels, 1, ypixels)



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
        actimes = self.presetactimes()
        continuous = self.continousbtns()
        mplplt = WidgetPlot()
        self.plot = mplplt
        saveload = self.saveloadbtns()
        # kinscans = self.kineticdatabtns()


        dataaclayout.addWidget(actimes, 0, 0)
        dataaclayout.addWidget(mplplt, 0, 1, 5, 5)
        dataaclayout.addWidget(saveload, 5,0)
        dataaclayout.addWidget(continuous, 2, 0)
        # dataaclayout.addWidget(kinscans, 2,0)
        self.setLayout(dataaclayout)
        self.data = None

    def presetactimes(self):
        btnwid = 40
        btnhgt = 40

        pointonesbtn = QPushButton('0.1s', self)
        pointonesbtn.clicked.connect(self.on_click_pointonesbtn)

        onesecbtn = QPushButton('1s', self)
        onesecbtn.clicked.connect(self.on_click_onesecbtn)


        tensecbtn = QPushButton('10s', self)
        tensecbtn.clicked.connect(self.on_click_tensecbtn)


        sixtysecbtn = QPushButton('60s', self)
        sixtysecbtn.clicked.connect(self.on_click_sixtysecbtn)

        btnlay = QGridLayout()
        btnlay.addWidget(pointonesbtn, 0, 0)
        btnlay.addWidget(onesecbtn, 0,1)
        btnlay.addWidget(tensecbtn, 0, 2)
        btnlay.addWidget(sixtysecbtn, 0, 3)

        groupbox = QGroupBox()
        groupbox.setLayout(btnlay)
        groupbox.setTitle('Single Scan Data Acquisition')
        return groupbox

    def saveloadbtns(self):
        btnwid = 40
        btnhgt = 40

        savebtn = QPushButton('save data to txt', self)
        savebtn.clicked.connect(self.on_click_singlesavedata)

        loadbtn = QPushButton('load data from txt', self)
        # loadbtn.clicked.connect(self.on_click_loaddata)

        btnlay = QHBoxLayout()
        btnlay.addWidget(savebtn)
        btnlay.addWidget(loadbtn)

        groupbox = QGroupBox()
        groupbox.setLayout(btnlay)

        return groupbox

    def continousbtns(self):
        startbtn = QPushButton('Start Continuous Mode', self)
        startbtn.clicked.connect(self.on_click_continuous)

        stopbtn = QPushButton('Stop Continuous Mode', self)
        stopbtn.clicked.connect(self.on_click_stopcontinuous)

        btnlay = QHBoxLayout()
        btnlay.addWidget(startbtn)
        btnlay.addWidget(stopbtn)

        groupbox = QGroupBox()
        groupbox.setLayout(btnlay)

        return groupbox


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

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        return fileName

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
        return data

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
    #     return dataarray

    @pyqtSlot()
    def on_click_pointonesbtn(self):
        # data = [np.tan(i) for i in range(250)]
        fullFramebuffer = self.singleacquisition(0.1)
        self.data = fullFramebuffer
        self.plot.plot(self.data)
        return self.data

    # def on_click_singleacbtn(self, time):
    #     fullFramebuffer = self.singleacquisition(time)
    #     self.data = fullFramebuffer
    #     self.plot.plot(self.data)
    #     return self.data

    def on_click_onesecbtn(self):
        fullFramebuffer = self.singleacquisition(1)
        self.data = fullFramebuffer
        self.plot.plot(self.data)
        return self.data


    def on_click_tensecbtn(self):
        fullFramebuffer = self.singleacquisition(10)
        self.data = fullFramebuffer
        self.plot.plot(self.data)
        return self.data


    def on_click_sixtysecbtn(self):
        fullFramebuffer = self.singleacquisition(60)
        self.data = fullFramebuffer
        self.plot.plot(self.data)
        return self.data

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


#
    def on_click_singlesavedata(self):
        datafilename = self.saveFileDialog()
        file = open(datafilename, 'w')
        tsv_writer = csv.writer(file, delimiter='\t')
        tsv_writer.writerow(['Counts', 'point'])
        datalist = list(self.data)
        for i in range(len(datalist)):
            tsv_writer.writerow([datalist[i], i])
        file.close()
# filename+'_i'

    # def on_click_tenscans(self):
    #     datarray = self.kineticacquisition(.1, 10, 1)
    #     self.data = datarray
    #     print(self.data)
    #     return self.data


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


#TODO: add continuous view mode (video mode I think?)

# DataacGui()