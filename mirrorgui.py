import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QSizePolicy
import numpy as np
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from atmcd import *


class MirrorGui(QMainWindow):
    def __init__(self):
        app = QApplication(sys.argv)
        super(MirrorGui, self).__init__()

        self.title = 'Fast Steering Mirror Control'
        self.left = 200
        self.top = 50
        self.width = 1000
        self.height = 600
        self.initmirrorUI()
        sys.exit(app.exec_())

    def initmirrorUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        controlbtns = MirrorControlbtns()
        self.setCentralWidget(controlbtns)
        self.show()

class MirrorControlbtns(QWidget):
    def __init__(self):
        super(MirrorControlbtns, self).__init__()
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

        mplplt = WidgetPlot()
        self.plot = mplplt

        grid.addWidget(xlayout,0,0, 1, 6)
        grid.addWidget(ylayout, 1,0, 1, 6)
        grid.addWidget(llayout, 2,0, 1, 6)
        grid.addWidget(runbtn,3,5, 1, 1)

        gridbox = QGroupBox()
        gridbox.setLayout(grid)
        gridbox.setTitle('Scan Settings')
        movebtns = self.movebuttons()

        grid.addWidget(movebtns, 4, 0, 2,2)
        layout = QHBoxLayout()
        layout.addWidget(gridbox)
        layout.addWidget(mplplt)
        self.setLayout(layout)

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

        lambdalay.addWidget(self.lminlabel, 2,0)
        lambdalay.addWidget(self.lambdamaxbox, 2,1)
        lambdalay.addWidget(self.lmaxlabel, 2, 2)
        lambdalay.addWidget(self.lambdaminbox,2,3)
        lambdalay.addWidget(self.exposuretime, 2, 4)
        lambdalay.addWidget(self.deltatbox, 2,5)


        lambdabox = QGroupBox()
        lambdabox.setLayout(lambdalay)

        return lambdabox

    def runscan(self):
        runbtn = QPushButton('Run Scan')
        # runbtn.clicked.connect(self.on_click_runscan)

        return runbtn

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
        return movebox
    #todo: add 'move by'




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


        return xmin, xmax, delx, ymin, ymax, dely, lmin, lmax, exptime, xsteps, ysteps

    def scan(self, xmin, xmax, ymin, ymax, delx, dely, exptime):

        xsteps = np.rint((xmax-xmin)/delx)
        ysteps = np.rint((ymax-ymin)/dely)


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
            y = ymin
            x = xmin
            self.dataarray = np.zeroes((ysteps, xsteps, imageSize))

            for i in range(ysteps):
                # move to y


                for j in range(xsteps):
                    # move to x and acquire
                    (ret) = cam.PrepareAcquisition()
                    # Perform Acquisition
                    (ret) = cam.StartAcquisition()
                    (ret) = cam.WaitForAcquisition()
                    (ret, fullFrameBuffer) = cam.GetMostRecentImage(imageSize)
                    data = fullFrameBuffer
                    data = list(data)

                    for k in range(xpixels):
                        self.dataarray[i][j][k] = data[k]

                    x = xmin + j * delx
                y = ymin + i * dely
            (ret) = cam.ShutDown()
            print("Shutdown returned", ret)
#todo calibrate voltage and movement
        else:
            print("Cannot continue, could not initialise camera")

        return self.dataarray

    def roiinteg(self, lmin, lmax, xmin, xmax, ymin, ymax, delx, dely, exptime):
        scandata = self.scan(self, xmin, xmax, ymin, ymax, delx, dely, exptime)
        #todo: figure out how to convert lambda to points



    @pyqtSlot()

    def on_click_movex(self):
        xmove = self.xmovetxt.text()
        print('Move to x')
        #todo add functionality

    def on_click_movey(self):
        ymove = self.ymovetxt.text()
        print('Move to y')
        #todo: add functionality


    # def on_click_runscan(self):
    #     xmin = self.inputbox.text()
    #     self.data, self.exposuretime = self.singleacquisition(float(xmin))
    #     self.plot.plot(self.data)
    #     return self.data, self.exposuretime

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
MirrorGui()
