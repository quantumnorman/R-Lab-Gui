import sys
from bisect import bisect_left
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QSizePolicy, QComboBox
import numpy as np
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QSize
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from atmcd import *
# import nidaqmx
import dataacgui
from pyAndorShamrock import Shamrock
# sham = Shamrock.Shamrock()
# inifile = 'C:\\Users\\R-Lab\\Desktop\\detector.ini'
# sham.ShamrockInitialize(inifile)

# ytaskwrite = nidaqmx.Task()
# ytaskwrite.ao_channels.add_ao_voltage_chan('Dev1/ao0')
#
# xtaskwrite = nidaqmx.Task()
# xtaskwrite.ao_channels.add_ao_voltage_chan('Dev1/ao1')


umwidth = 10.
pixwidth = 40.

microncalib = pixwidth/umwidth

voltstep = 0.25
pixstep = 14

voltcalib = voltstep/pixstep

xcenterpoint = 512
ycenterpoint = 512

class MirrorGui(QMainWindow):
    def __init__(self):
        # app = QApplication(sys.argv)
        super(MirrorGui, self).__init__()
        self.title = 'Fast Steering Mirror Control'
        self.left = 200
        self.top = 50
        self.width = 1000
        self.height = 600
        self.initmirrorUI()
        # sys.exit(app.exec_())

    def initmirrorUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        controlbtns = MirrorControlbtns()
        self.setCentralWidget(controlbtns)

        # self.show()

class MirrorControlbtns(QWidget):
    def __init__(self):
        super(MirrorControlbtns, self).__init__()
        ytaskwrite.write([0])
        xtaskwrite.write([0])

        self.xpos = 0
        self.ypos = 0
        # Initializes the status updating labels #
        self.xposlab = QLabel('X Position='+str(self.xpos))
        self.yposlab = QLabel('Y Position='+str(self.ypos))
        self.mirstat = QLabel('Mirror Control Initialized')

        self.initmirrorUI()


    def initmirrorUI(self):

        grid = QGridLayout()
        xlayout = self.xscansettings()
        ylayout = self.yscansettings()
        llayout = self.lambdascansettings()
        runbtn = self.runscan()
        stopbtn = self.stopscan()
        color = self.scansettings()

        mplplt = WidgetPlot()
        self.plot = mplplt
        self.plot.setMinimumSize(QSize(600,600))

        grid.addWidget(xlayout,0,0, 1, 6)
        grid.addWidget(ylayout, 1,0, 1, 6)
        grid.addWidget(llayout, 2,0, 1, 6)
        grid.addWidget(runbtn,3,4, 1, 1)
        grid.addWidget(stopbtn,3,5,1,1)
        grid.addWidget(color, 4,5,1,1)

        gridbox = QGroupBox()
        gridbox.setLayout(grid)
        gridbox.setTitle('Scan Settings')
        movebtns = self.movebuttons()

        grid.addWidget(movebtns, 4, 0, 2,2)
        layout = QHBoxLayout()
        layout.addWidget(gridbox)
        layout.addWidget(mplplt)
        self.setLayout(layout)

        ##setting colormap names##
        self.heat = plt.get_cmap('hot')
        self.rainbow = plt.get_cmap('rainbow')
        self.gray = plt.get_cmap('gray')
        self.colormap = self.heat


    def xscansettings(self):
        self.xminbox = QLineEdit()
        self.xminlabel = QLabel('X Min')
        self.xmaxbox = QLineEdit()
        self.xmaxlabel = QLabel('X Max')
        self.deltaxbox = QLineEdit()
        self.deltaxlabel = QLabel('Delta X')


        xlay = QGridLayout()

        xlay.addWidget(self.xminlabel, 0, 0)
        xlay.addWidget(self.xminbox, 0, 1)
        xlay.addWidget(self.xmaxlabel, 0, 2)
        xlay.addWidget(self.xmaxbox, 0, 3)
        xlay.addWidget(self.deltaxlabel, 0, 4)
        xlay.addWidget(self.deltaxbox, 0, 5)

        xgroup = QGroupBox()
        xgroup.setLayout(xlay)

        return xgroup
    def yscansettings(self):
        self.deltaybox = QLineEdit()
        self.deltaybox.setText('10')
        self.deltaylabel = QLabel('Delta Y')
        self.yminbox = QLineEdit()
        self.yminlabel = QLabel('Y Min')
        self.ymaxbox = QLineEdit()
        self.ymaxlabel = QLabel('Y Max')

        ylay = QGridLayout()

        ylay.addWidget(self.yminlabel,0,0)
        ylay.addWidget(self.yminbox,0,1)
        ylay.addWidget(self.ymaxlabel, 0,2)
        ylay.addWidget(self.ymaxbox,0,3)
        ylay.addWidget(self.deltaylabel, 0,4)
        ylay.addWidget(self.deltaybox, 0, 5)


        ygroup = QGroupBox()
        ygroup.setLayout(ylay)

        return ygroup

    def lambdascansettings(self):
        self.lambdaminbox = QLineEdit()
        self.lminlabel = QLabel('Lambda Min')
        self.lambdamaxbox = QLineEdit()
        self.lmaxlabel = QLabel('Lambda Max')

        self.deltatbox = QLineEdit()
        self.exposuretime = QLabel('Exposure Time')

        lambdalay = QGridLayout()

        lambdalay.addWidget(self.lminlabel, 0,0)
        lambdalay.addWidget(self.lambdamaxbox, 0,1)
        lambdalay.addWidget(self.lmaxlabel, 0, 2)
        lambdalay.addWidget(self.lambdaminbox,0,3)
        lambdalay.addWidget(self.exposuretime, 0, 4)
        lambdalay.addWidget(self.deltatbox, 0,5)


        lambdabox = QGroupBox()
        lambdabox.setLayout(lambdalay)

        return lambdabox

    def scansettings(self):
        self.vminbox = QLineEdit()
        self.vmaxbox = QLineEdit()
        color = self.colorsetting()
        vminlbl = QLabel('Minimum Colorbar PL Scan')
        vmaxlbl = QLabel('Maximum Colorbar PL Scan')

        layout = QGridLayout()
        layout.addWidget(vminlbl, 0, 0)
        layout.addWidget(self.vminbox,0,1)
        layout.addWidget(vmaxlbl, 1, 0)
        layout.addWidget(self.vmaxbox, 1,1)
        layout.addWidget(color, 2,1)

        box = QGroupBox()
        box.setLayout(layout)
        return box

    def runscan(self):
        runbtn = QPushButton('Run Scan')
        runbtn.clicked.connect(self.on_click_runscan)
        return runbtn

    def stopscan(self):
        stopbtn = QPushButton('Stop Scan')
        stopbtn.clicked.connect(self.on_click_stopscan)
        return stopbtn

    def movebuttons(self):
        self.xmovetxt = QLineEdit()
        xmovebtn = QPushButton('Go to X Value')
        xmovebtn.clicked.connect(self.on_click_movex)

        self.ymovetxt = QLineEdit()
        ymovebtn = QPushButton('Go to Y Value')
        ymovebtn.clicked.connect(self.on_click_movey)

        movelay = QGridLayout()
        movelay.addWidget(self.xmovetxt, 0, 0)
        movelay.addWidget(xmovebtn, 0, 1)
        movelay.addWidget(self.ymovetxt, 1,0)
        movelay.addWidget(ymovebtn, 1,1)

        movebox = QGroupBox()
        movebox.setLayout(movelay)


        self.deltaybox.setText('10')
        self.deltaxbox.setText('10')
        self.deltatbox.setText('0.1')
        self.xminbox.setText('316')
        self.xmaxbox.setText('708')
        self.ymaxbox.setText('820')
        self.yminbox.setText('180')
        self.lambdaminbox.setText('1050')
        self.lambdamaxbox.setText('1150')

        return movebox

    def colorsetting(self):
        combo = QComboBox()
        combo.addItem('Heat')
        combo.addItem('Rainbow')
        combo.addItem('Grayscale')
        combo.activated[str].connect(lambda x: self.setcolor(x))
        return combo

    def setcolor(self,text):
        if text == 'Heat':
            self.colormap = self.heat
        if text == 'Grayscale':
            self.colormap = self.gray
        if text == 'Rainbow':
            self.colormap = self.rainbow

    def readboxes(self):
        xmin = float(self.xminbox.text())
        xmax = float(self.xmaxbox.text())
        delx = float(self.deltaxbox.text())

        ymin = float(self.yminbox.text())
        ymax = float(self.ymaxbox.text())
        dely = float(self.deltaybox.text())

        lmin = float(self.lambdaminbox.text())
        lmax = float(self.lambdamaxbox.text())

        exptime = float(self.deltatbox.text())

        xsteps = np.rint((xmax-xmin)/delx)
        ysteps = np.rint((ymax-ymin)/dely)

        if self.vmaxbox.text() == '':
            vmax = None
        else:
            vmax = int(self.vmaxbox.text())
        if self.vminbox.text() == '':
            vmin = None
        else:
            vmin = int(self.vminbox.text())

        return xmin, xmax, delx, ymin, ymax, dely, lmin, lmax, exptime, xsteps, ysteps, vmin, vmax

    def scan(self, xmin, xmax, delx, ymin, ymax, dely, lmin, lmax, exptime, xsteps, ysteps, vmin, vmax):
        xsteps = round((xmax-xmin)/delx)
        ysteps = round((ymax-ymin)/dely)

        self.dataarray = np.zeros((ysteps, xsteps))

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
            (ret) = cam.SetExposureTime(exptime)

            imageSize = xpixels * ypixels

            yvolt = (ymin-ycenterpoint)*voltcalib

            wavelength = self.find_wavelength()

            roihigh = int(bisect_left(wavelength, lmin))
            roilow = int(bisect_left(wavelength, lmax))
            self.set = 1
            for i in range(ysteps):
                # move to y
                ytaskwrite.write(yvolt)
                # print('yvolt=',yvolt)
                xvolt = (xmin - xcenterpoint) * voltcalib

                for j in range(xsteps):
                    # move to x and acquire
                    xtaskwrite.write(xvolt)
                    # print('xvolt=',xvolt)

                    (ret) = cam.PrepareAcquisition()
                    # Perform Acquisition
                    (ret) = cam.StartAcquisition()
                    # print('starting')
                    (ret) = cam.WaitForAcquisition()
                    (ret, fullFrameBuffer) = cam.GetMostRecentImage(imageSize)
                    data = fullFrameBuffer
                    data = list(data)
                    # print(data)
                    # print('roilow=',roilow)
                    # print('rohigh=',roihigh)

                    data = sum(data[roilow:roihigh])
                    # print(data)
                    self.dataarray[i][j] = data
                    # self.dataarray[i][j] = i+j
                    time.sleep(0.05)
                    xvolt = xvolt+delx*voltcalib
                    self.plot.plot(self.dataarray, xmin, xmax, ymin, ymax, self.colormap)
                    QApplication.processEvents()
                    print(self.set)
                    if self.set !=1:
                        break
                    # print("Step", j)
                    # print(data)
                    # print(self.dataarray)
                if self.set != 1:
                    break

                yvolt=yvolt+dely*voltcalib
            (ret) = cam.ShutDown()

            print("Shutdown returned", ret)
            print('Finished')
        else:
            print("Cannot continue, could not initialise camera")

        ytaskwrite.write(0)
        xtaskwrite.write(0)
    @pyqtSlot()

    def on_click_movex(self):
        xmove = float(self.xmovetxt.text())
        print(xmove)
        xvolt = xmove * voltcalib
        print(xvolt)
        xtaskwrite.write(xvolt)
        print('Move to x')

    def on_click_movey(self):
        ymove = self.ymovetxt.text()
        yvolt = ymove * voltcalib
        ytaskwrite.write(yvolt)
        print('Move to y')

    def on_click_runscan(self):
        xmin, xmax, delx, ymin, ymax, dely, lmin, lmax, exptime, xsteps, ysteps, vmin, vmax =self.readboxes()
        self.scan(xmin, xmax, delx, ymin, ymax, dely, lmin, lmax, exptime, xsteps, ysteps, vmin, vmax)

    def on_click_stopscan(self):
        self.set = 0

    def find_wavelength(self):
        ret, self.waveset = sham.ShamrockGetWavelength(0)
        ret, self.gratingset = sham.ShamrockGetGrating(0)

        if self.gratingset==1:
            wavemin = self.waveset-55.185
            wavemax = self.waveset+55.185
            wavelength = np.linspace(wavemin, wavemax, 512)
            # print(wavelength)
            return wavelength

        if self.gratingset==2:
            wavemin = self.waveset-12.225
            wavemax = self.waveset+12.225
            wavelength = np.linspace(wavemin, wavemax, 512)
            # print(wavelength)
            return wavelength

        if self.gratingset == 3:
            wavemin = self.waveset-6.93
            wavemax = self.waveset+6.93
            wavelength = np.linspace(wavemin, wavemax, 512)
            # print(wavelength)
            return wavelength


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None):
        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def imshow(self,data, xmin, xmax, ymin, ymax, colormap):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title('Photoluminescence Scan')
        im = self.axes.imshow(data, cmap=colormap, interpolation = 'none', extent=[xmin, xmax, ymin, ymax], origin='lower')
        colorbar = self.fig.colorbar(im)


class WidgetPlot(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)

    def plot(self, data, xmin, xmax, ymin, ymax, colormap):
        self.canvas.imshow(data, xmin, xmax, ymin, ymax, colormap,)
        self.canvas.draw()

# MirrorGui()