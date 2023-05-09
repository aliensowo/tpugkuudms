from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem

from gui.I_guide_page import Ui_MainWindow as IPage
from models.database import SessionLocal
from models.crud import criteria, contractors, contractors_to_contractors, criteria_to_criteria
from logic._base_class_logic import BaseClassLogic
from logic.D_logic_page import DLogicPage
from logic.E_logic_page import ELogicPage
from typing import List
import math


class ILogicPage(QtWidgets.QMainWindow, BaseClassLogic):

    def __init__(self):
        super(ILogicPage, self).__init__()
        self.error_window = None
        self.winner_window = None
        self.ui = IPage()
        self.ui.setupUi(self)
        self.ui.menu.triggered.connect(self.display_criteria_list)

    def display_criteria_list(self):
        # Criteria set
        criteria_data_list = self.get_data_criteria()
        if criteria_data_list:
            self.ui.tableWidget.setColumnCount(2)
            self.ui.tableWidget.setRowCount(criteria_data_list.__len__())
            self.ui.tableWidget.setHorizontalHeaderLabels(["id", "Критерий"])
            self.ui.tableWidget.setVerticalHeaderLabels(["" for _ in criteria_data_list])
            for row in criteria_data_list:
                id_item = QTableWidgetItem()
                name_item = QTableWidgetItem()
                id_item.setText(str(row["id"]))
                id_item.setFlags(id_item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                name_item.setText(row["name"])
                self.ui.tableWidget.setItem(criteria_data_list.index(row), 0, id_item)
                self.ui.tableWidget.setItem(criteria_data_list.index(row), 1, name_item)

