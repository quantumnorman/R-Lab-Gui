import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow,  QApplication, QLabel, QRadioButton, QSizePolicy, QPushButton, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout, QInputDialog, QLineEdit, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import csv
from atmcd import *
from PyQt5.QtCore import pyqtSlot
import datetime
from scipy import optimize
from pyAndorShamrock import Shamrock
sham = Shamrock.Shamrock()

now = datetime.datetime.now()

cam = atmcd()


class PlotGui(QMainWindow):

    def __init__(self):
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        super(PlotGui, self).__init__()
        self.title = 'Plotting GUI'

        self.initdataacUI()
        sys.exit(app.exec_())

    def initdataacUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        control = Dataplot()
        self.setCentralWidget(control)
        self.show()


class Dataplot(QWidget):

    def __init__(self):
        super(Dataplot, self).__init__()
        self.initdataUI()

    def initdataUI(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        # self.wavelength = np.linspace(0, 512, 512)

        dataaclayout = QGridLayout()
        actimes = self.presetactimes
        continuous = self.continousbtns()
        mplplt = WidgetPlot()
        self.plot = mplplt
        self.plot.setMinimumSize(600)
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
        self.getwavel()

#TODO:set up plotting gui using fit modules from dataacgui
#TODO: set up drop down lists for customization of plots


    def saveloadbtns(self):
        btnhgt = 100

        savebtn = QPushButton('save data to txt', self)
        # savebtn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        savebtn.setMinimumHeight(btnhgt)
        savebtn.clicked.connect(self.on_click_singlesavedata)

        loadbtn = QPushButton('load data from txt', self)
        loadbtn.setMinimumHeight(btnhgt)
        loadbtn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        loadbtn.clicked.connect(self.on_click_loaddata)

        btnlay = QGridLayout()
        btnlay.addWidget(savebtn, 0, 0)
        btnlay.addWidget(loadbtn, 0, 1)

        groupbox = QGroupBox()
        groupbox.setLayout(btnlay)

        return groupbox

    def fitting(self):
        fitting = QPushButton('Try Fit', self)
        fitting.clicked.connect(self.on_click_fitfunc)

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

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        return fileName

    def gauss(self, x, amp, center, sigma):
        return amp * np.exp(-(x - center) ** 2 / (2 * sigma ** 2))


    def lor(self, x, amp, center, sigma):
        return amp * sigma ** 2 / (sigma ** 2 + (x - center) ** 2)

    @pyqtSlot()

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
        datalist = list(self.data)
        for i in range(len(datalist)):
            tsv_writer.writerow([i, datalist[i]])
        file.close()

    def loadtext(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        fileName = str(fileName)
        print(fileName)
        self.wavelength, self.data = np.loadtxt(fileName, usecols=(0,1), skiprows=13, unpack=True)
        return self.wavelength, self.data

    def on_click_fitfunc(self):

        amp = float(self.ampfit.text())
        center = float(self.centerfit.text())
        sigma = float(self.centerfit.text())

        data = self.data
        x = self.wavelength

        if self.lorbtn.isChecked():
            func = self.lor

        if self.gaubtn.isChecked():
            func = self.gauss


        popt, pcov = optimize.curve_fit(func, x, data, p0=[amp, center, sigma])

        self.ampfitval = popt[0]
        self.centerfitval = popt[1]
        self.sigmfitval = popt[2]
        self.perr = np.sqrt(np.diag(pcov))

        fit = func(x, popt[0], popt[1], popt[2])
        self.plot.plotfit(x, fit)

        self.retstdeval.setText(str(self.perr))
        self.retsigval.setText(str(self.sigmfitval))
        self.retcenval.setText(str(self.centerfitval))
        self.retampval.setText(str(self.ampfitval))
        #TODO: reformat value box

        print(popt)


#kinetic scans click
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

    def plot(self, x, data):
        self.axes.plot(x, data, 'r.')
        self.axes.set_title('PyQt Matplotlib Example')
        self.draw()

    def plotfit(self, x,fit):
        self.axes.plot(x,fit, 'bo')
        self.draw()


class WidgetPlot(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)

    def plot(self, x, data):
        self.canvas.axes.clear()
        self.canvas.plot(x, data)
    #
    def plotfit(self,x, fit):
        self.canvas.plotfit(x, fit)


PlotGui()