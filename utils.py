import sys

from PyQt5.QtWidgets import QToolButton, QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, \
    QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot
from shamrockgui import *
from dataacgui import *
from ingaasgui import *
from mirrorgui import *
from atmcd import *
cam = atmcd()

class scanthread(QThread): ##This class creates a QThread for data acquisition from the spectrometer camera and based on
                            # 'type' makes it a single scan with acquisition time 'time' (type==1) or continuous scan
                            # with acquisition time 'time' (type==2)
    signal = pyqtSignal('PyQt_PyObject') #defines the output of the thread as a signal that can be read out upstream
    def __init__(self, type, time):
        QThread.__init__(self)
        self.time = time
        self.condition = 1 #sets up the run condition for if we do decide to run continuously
        self.type = type #reads in the type and allows it to pass to the run function
    def run(self):
        print("Intialising Camera")
        cam = atmcd()  # load the atmcd library
        (ret) = cam.Initialize("/usr/local/etc/andor")  # initialise camera
        if atmcd.DRV_SUCCESS == ret: #if the initialisation is successful, continue with acquisition
            (ret) = cam.IsCoolerOn()
            if ret!= atmcd.DRV_SUCCESS:
                (ret) = cam.CoolerON()  # makes sure the cooler is on
            (ret) = cam.SetReadMode(4) #sets the read out mode to 'image'
            (ret) = cam.SetTriggerMode(0) #sets the trigger mode to 'internal' so it starts upon button click
            (ret, xpixels, ypixels) = cam.GetDetector() #finds information for reading out
            (ret) = cam.SetImage(1, 1, 1, xpixels, 1, ypixels) #sets up the readout array
            (ret) = cam.SetExposureTime(self.time) #sets the exposure time
            imageSize = xpixels * ypixels #sets the fullframebuffer array size
            if self.type == 1: #if we're doing a single scan
                (ret) = cam.SetAcquisitionMode(1) #sets acqusition mode to single scan
                (ret) = cam.PrepareAcquisition()
                (ret) = cam.StartAcquisition()
                (ret) = cam.WaitForAcquisition()
                (ret, fullFrameBuffer) = cam.GetMostRecentImage(imageSize) #full frame buffer is the data
                data = fullFrameBuffer
                (ret) = cam.ShutDown()
                print("Shutdown returned", ret)
                self.signal.emit(data)  # This sends out the data into the main process when the thread is finished.
            if self.type ==2:
                (ret) = cam.SetAcquisitionMode(5) #sets acquisition mode to 'run till abort'
                (ret) = cam.SetKineticCycleTime(0) #sets the pause time in between scans to zero seconds
                while self.condition == 1: #sets up the run condition
                    (ret) = cam.PrepareAcquisition()
                    (ret) = cam.StartAcquisition()
                    (ret) = cam.WaitForAcquisition()
                    (ret, fullframebuffer) = cam.GetMostRecentImage(imageSize)
                    data = fullframebuffer
                    self.signal.emit(data) #sends out data into main process
        else:
            print('Cannot continue, could not initialize camera') #quits the loop

            def halt(self):
                self.condition = 0 #quits the continuous scan loop
                (ret) = cam.ShutDown()
                print("Shutdown returned", ret)


class PlotCanvas(FigureCanvas): #this creates a matplotlib canvas and defines some plotting aspects

    def __init__(self, color, character, title, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.color = str(color)
        self.character = str(character)
        self.marker = self.color+self.character
        self.title = str(title)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def plot(self, x, data, colormap = plt.get_cmap('hot'), xmin=0, xmax=0, ymin=0, ymax=0):
        self.axes.plot(x, data, self.marker)
        self.axes.set_title(self.title)
        self.draw()
        # if self.type ==2:
        #     self.axes = self.fig.add_subplot(111)
        #     self.axes.set_title('Photoluminescence Scan')
        #     im = self.axes.imshow(data, cmap=colormap, interpolation='none', extent=[xmin, xmax, ymin, ymax],
        #                           origin='lower')
        #     colorbar = self.fig.colorbar(im)

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