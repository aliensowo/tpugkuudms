from gui.D_error_page import Ui_MainWindow as DPage
from PyQt5 import QtWidgets


class DLogicPage(QtWidgets.QMainWindow):

    def __init__(self):
        super(DLogicPage, self).__init__()
        self.ui = DPage()
        self.ui.setupUi(self)

        self.ui.buttonBox.clicked.connect(self.close)
