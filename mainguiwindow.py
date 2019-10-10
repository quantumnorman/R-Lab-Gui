import sys

from PyQt5.QtWidgets import QToolButton, QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from shamrockgui import *
from dataacgui import *
from ingaasgui import *
from mirrorgui import *



class MainGui(QMainWindow):
    """This is the main window."""
    def __init__(self):
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        super(MainGui, self).__init__()
        self.title = 'R-Lab Instrumentation Controls'
        self.left = 200
        self.top = 50
        self.width = 300
        self.height = 300
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
        self.dataacgui = DataacGui()
        self.mirror = MirrorGui()


    def initspecbtns(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        shamrockbtn = QPushButton('Shamrock', self)
        shamrockbtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        shamrockbtn.clicked.connect(self.on_click_shamrock)

        ingaasbtn = QPushButton('InGaAs Camera', self)
        ingaasbtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        ingaasbtn.clicked.connect(self.on_click_ingaas)

        mirrorbtn = QPushButton('Fast Steering Mirror', self)
        mirrorbtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        mirrorbtn.clicked.connect(self.on_click_mirror)

        dataacbtn = QPushButton('Data Acquisition', self)
        dataacbtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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

    def on_click_mirror(self):
        self.mirror.show()



MainGui()
