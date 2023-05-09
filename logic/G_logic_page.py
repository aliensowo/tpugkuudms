from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem

from gui.G_work3_page import Ui_MainWindow as GPage
from models.database import SessionLocal
from models.crud import criteria, contractors, contractors_to_contractors, criteria_to_criteria
from logic._base_class_logic import BaseClassLogic
from logic.D_logic_page import DLogicPage
from logic.E_logic_page import ELogicPage
from typing import List
import math


class GLogicPage(QtWidgets.QMainWindow, BaseClassLogic):

    def __init__(self):
        super(GLogicPage, self).__init__()
        self.error_window = None
        self.winner_window = None
        self.ui = GPage()
        self.ui.setupUi(self)

