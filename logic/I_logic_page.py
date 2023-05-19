from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem

from gui.I_guide_page import Ui_MainWindow as IPage
from models.database import SessionLocal
from models.crud import neighborhood_directory
from models.crud import objects_contracts
from logic._base_class_logic import BaseClassLogic


class ILogicPage(QtWidgets.QMainWindow, BaseClassLogic):

    def __init__(self):
        super(ILogicPage, self).__init__()
        self.error_window = None
        self.winner_window = None
        self.ui = IPage()
        self.ui.setupUi(self)
        self.ui.action_5.triggered.connect(self.display_criteria_list)
        self.ui.action_3.triggered.connect(self.display_directions)
        self.ui.action_4.triggered.connect(self.display_contracts)

    def display_criteria_list(self):
        self.ui.tableWidget.clear()
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

    def display_directions(self):
        self.ui.tableWidget.clear()
        with SessionLocal() as session:
            d_list = neighborhood_directory.list(session)
            if d_list:
                self.ui.tableWidget.setColumnCount(d_list[0].__len__())
                self.ui.tableWidget.setRowCount(d_list.__len__())
                self.ui.tableWidget.setHorizontalHeaderLabels(list(d_list[0].keys()))
                for row in d_list:
                    for key in row.keys():
                        item = QTableWidgetItem()
                        item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                        item.setText(str(row[key]))
                        self.ui.tableWidget.setItem(d_list.index(row), list(row.keys()).index(key), item)

    def display_contracts(self):
        self.ui.tableWidget.clear()
        with SessionLocal() as session:
            d_list = objects_contracts.list(session)
            if d_list:
                self.ui.tableWidget.setColumnCount(d_list[0].__len__())
                self.ui.tableWidget.setRowCount(d_list.__len__())
                self.ui.tableWidget.setHorizontalHeaderLabels(list(d_list[0].keys()))
                for row in d_list:
                    for key in row.keys():
                        item = QTableWidgetItem()
                        item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                        item.setText(str(row[key]))
                        self.ui.tableWidget.setItem(d_list.index(row), list(row.keys()).index(key), item)
