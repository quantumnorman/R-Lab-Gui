import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from shamrockgui import *
from dataacgui import *
from ingaasgui import *



class MainGui(QMainWindow):
    """This is the main window."""
    def __init__(self):
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        super(MainGui, self).__init__()
        self.title = 'R-Lab Instrumentation Controls'
        self.left = 50
        self.top = 50
        self.width = 300
        self.height = 500
        self.setCentralWidget(Spectbtns())
        self.initUI()
        sys.exit(app.exec_())



    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()


class Spectbtns(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Spectrometer Controls"
        self.left = 12.5
        self.top = 12.5
        self.width = 275
        self.height = 475
        self.initspecbtns()
        grid = QGridLayout()
        grid.addWidget(self.initspecbtns(), 0, 0)
        self.setLayout(grid)
        self.spectrometergui = SpectrometerGui()
        self.ingaasgui = InGaAsGui()
        # self.dataacgui = DataacGui()


    def initspecbtns(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        shamrockbtn = QPushButton('Shamrock', self)
        shamrockbtn.clicked.connect(self.on_click_shamrock)

        ingaasbtn = QPushButton('InGaAs Camera', self)
        ingaasbtn.clicked.connect(self.on_click_ingaas)

        dataacbtn = QPushButton('Data Acquisition', self)
        dataacbtn.clicked.connect(self.on_click_dataac)

        spectbox = QGroupBox('Spectrometer Controls')
        spectvbox = QVBoxLayout()
        vbox1 = QVBoxLayout()
        spectvbox.addWidget(shamrockbtn)
        spectvbox.addWidget(ingaasbtn)
        spectvbox.addWidget(dataacbtn)
        spectvbox.addLayout(vbox1)
        spectbox.setLayout(spectvbox)

        return spectbox

    @pyqtSlot()
    def on_click_ingaas(self):
        self.ingaasgui.show()

    def on_click_dataac(self):
        self.dataacgui.show()

    def on_click_shamrock(self):
        self.spectrometergui.show()



MainGui()
