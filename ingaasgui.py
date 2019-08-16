import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QGridLayout

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class InGaAsGui(QMainWindow):
    def __init__(self):
        super(InGaAsGui, self).__init__()
        self.title = 'InGaAs Camera Control'
        self.left = 50
        self.top = 50
        self.width = 500
        self.height = 500
        self.initingaasUI()

    def initingaasUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)