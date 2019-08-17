import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class DataacGui(QMainWindow):
    def __init__(self):
        super(DataacGui, self).__init__()
        self.title = 'Spectrometer Data Acquisition'
        self.left = 50
        self.top = 50
        self.width = 500
        self.height = 500
        self.initdataacUI()

    def initdataacUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


#TODO: set matplotlib plotting window
#TODO: create buttons for preset acquisition .1s, 1s, 10s 60s
#TODO: create saving for both txt and pngs
#TODO: LATER: add continuous view mode (video mode I think?)
#TODO: LATER: add kinetic series button