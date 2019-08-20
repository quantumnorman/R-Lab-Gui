import sys
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QSizePolicy, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5.QtGui import QIcon
import random

from PyQt5.QtCore import pyqtSlot

class DataacGui(QMainWindow):
    def __init__(self):
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        super(DataacGui, self).__init__()
        self.title = 'Spectrometer Data Acquisition'
        # self.left = 50
        # self.top = 50
        # self.width = 500
        # self.height = 500
        self.initdataacUI()
        sys.exit(app.exec_())

    def initdataacUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        control = Datacontrol()
        self.setCentralWidget(control)


        self.show()


class Datacontrol(QWidget):

    def __init__(self):
        super(Datacontrol, self).__init__()
        self.initdataUI()

    def initdataUI(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)

        dataaclayout = QGridLayout()
        actimes = self.presetactimes()

        dataaclayout.addWidget(actimes, 0, 0)
        # dataaclayout.addWidget(self.matplotlibgui, 1, 1)
        # dataaclayout.addWidget(self.matplotlibgui(), 0, 1, 4, 4)
        # dataaclayout.addWidget()
        self.setLayout(dataaclayout)

    def presetactimes(self):
        btnwid = 40
        btnhgt = 40

        pointonesbtn = QPushButton('0.1s', self)
        pointonesbtn.clicked.connect(self.on_click_pointonesbtn)
        pointonesbtn.resize(40, 40)

        onesecbtn = QPushButton('1s', self)
        onesecbtn.clicked.connect(self.on_click_onesecbtn)
        onesecbtn.resize(16, btnhgt)


        tensecbtn = QPushButton('10s', self)
        tensecbtn.clicked.connect(self.on_click_tensecbtn)
        tensecbtn.resize(btnwid, btnhgt)


        sixtysecbtn = QPushButton('60s', self)
        sixtysecbtn.clicked.connect(self.on_click_sixtysecbtn)
        sixtysecbtn.resize(40, 40)

        btnlay = QGridLayout()
        btnlay.addWidget(pointonesbtn, 0, 0)
        btnlay.addWidget(onesecbtn, 0,1)
        btnlay.addWidget(tensecbtn, 0, 2)
        btnlay.addWidget(sixtysecbtn, 0, 3)



        groupbox = QGroupBox()
        groupbox.setLayout(btnlay)
        groupbox.setTitle('Data Acquisition')
        return groupbox

# class PlotCanvas(FigureCanvas):
#     def __init__(self, parent = None, width=5, height=4, dpi = 100):
#         fig = Figure(figsize=(width, height), dpi = dpi)
#         self.axes = fig.add_subplot(111)
#
#         FigureCanvas.__init__(self, fig)
#         self.setParent(parent)
#
#         FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
#         FigureCanvas.updateGeometry(self)
#
#         self.plot()
#
#     def plot(self):
#         data = [random.random() for i in range(25)]
#         ax = self.figure.add_subplot(111)
#         ax.plot(data, 'r-')
#         ax.set_title('PyQt Matplotlib Example')
#         self.draw()



    @pyqtSlot()
    def on_click_pointonesbtn(self):
        #TODO: addfunctionality
        print('0.1 Second Acquisition')

    def on_click_onesecbtn(self):
        #TODO: add functionality
        print('1 Second Acquisition')

    def on_click_tensecbtn(self):
        #TODO: add functionality
        print('10 Second Acquisition')

    def on_click_sixtysecbtn(self):
        #TODO: add functionality
        print('60 Second Acquisition')



#TODO: set matplotlib plotting window
#TODO: create saving for both txt and pngs
#TODOLATER: add continuous view mode (video mode I think?)
#TODOLATER: add kinetic series button

DataacGui()