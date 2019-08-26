import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QSizePolicy, QPushButton, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
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

        # self.inifile = 'C:\\Users\\R-Lab\\Desktop\\cam.ini'
        # cam.Initialize(self.inifile)
        # print('Camera Initialized')
        #
        # cam.CoolerON()
        # print('Cooler On')
        #
        # cam.SetAcquisitionMode(1)  ##Sets acquisition mode to single scan
        # print('Acquisition mode set to single scan')
        #
        # cam.SetTriggerMode(0)
        (ret, xpixels, ypixels) = cam.GetDetector()
        #
        self.imageSize = xpixels * ypixels
        # cam.SetImage(1, 1, 1, xpixels, 1, ypixels)
        # self.left = 50
        # self.top = 50
        # self.width = 500
        # self.height = 500
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
        mplplt = WidgetPlot()

        dataaclayout.addWidget(actimes, 0, 0)
        dataaclayout.addWidget(mplplt, 0, 1, 5, 5)
        self.setLayout(dataaclayout)

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
        groupbox.setTitle('Data Acquisition')
        return groupbox

    def acquisition(self, time):
        cam.SetExposureTime(time)
        cam.PrepareAcquisition()
        cam.StartAcquisition()
        cam.WaitForAcquisition()
        (ret, fullFrameBuffer) = cam.GetMostRecentImage(self.imageSize)
        cam.ShutDown()
        return fullFrameBuffer

    @pyqtSlot()
    def on_click_pointonesbtn(self):
        # TODO: check functionality
        print('0.1 Second Acquisition')
        # fullFramebuffer = self.acquisition(0.1)
        # return fullFrameBuffer

    def on_click_onesecbtn(self):
        print('1 Second Acquisition')
        # fullFramebuffer = self.acquisition(1)
        # return fullFrameBuffer
        # TODO: check functionality

    def on_click_tensecbtn(self):
        # TODO: check functionality
        print('10 Second Acquisition')
        # fullFramebuffer = self.acquisition(10)
        # return fullFrameBuffer

    def on_click_sixtysecbtn(self):
        # TODO: check functionality
        print('60 Second Acquisition')
        # fullFramebuffer = self.acquisition(60)
        # return fullFrameBuffer

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        data = [np.tan(i) for i in range(250)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r.')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()

class WidgetPlot(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)

#TODO: create saving mode for txt
#TODOLATER: add continuous view mode (video mode I think?)
#TODOLATER: Use radio buttons to switch between single, continuous, kinetic
#TODOLATER: add kinetic series button

# DataacGui()