from PyQt5 import QtWidgets
from gui.B_main_page import Ui_MainWindow as BPage


class BLogicPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(BLogicPage, self).__init__()
        self.ui = BPage()
        self.ui.setupUi(self)
