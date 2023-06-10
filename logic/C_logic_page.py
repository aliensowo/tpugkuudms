from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem

from gui.C_new_work1_page import Ui_MainWindow as CPage
from models.database import SessionLocal
from models.crud import criteria, contractors, contractors_to_contractors, criteria_to_criteria
from logic._base_class_logic import BaseClassLogic
from logic.D_logic_page import DLogicPage
from logic.C_logic_page_new_calc_w1 import CLogicPage as StartW1
from logic.E_logic_page import ELogicPage
from typing import List
import math


class CLogicPage(QtWidgets.QMainWindow, BaseClassLogic):

    def __init__(self, username: str):
        super(CLogicPage, self).__init__()
        self.error_window = None
        self.winner_window = None
        self.ui = CPage()
        self.ui.setupUi(self)
        self.username = username

        self.click_close_widget()

        # Логика кнопок вне таба
        self.ui.pushButton.clicked.connect(self.start_to_work_1)
        self.ui.pushButton_3.clicked.connect(self.back_to_main)
        # Логика кнопок в табе (создание / удаление)
        self.ui.pushButton_2.clicked.connect(self.click_button_create_criteria)
        self.ui.pushButton_4.clicked.connect(self.click_button_delete_criteria)
        self.ui.pushButton_5.clicked.connect(self.click_button_create_contractor)
        self.ui.pushButton_6.clicked.connect(self.click_button_delete_contractor)

        # Создание таблиц
        self.create_or_update_tabs_table()

        # Проверка перед работой 1
        self.ui.pushButton_7.clicked.connect(self.click_get_compare_id)
        self.ui.pushButton_8.clicked.connect(self.click_close_widget)

    def click_close_widget(self):
        self.ui.groupBox.setVisible(False)

    def click_get_compare_id(self):
        compare_id = self.ui.lineEdit_11.text()
        if compare_id:
            self.main_window = StartW1(username=self.username, compare_id=compare_id)
            self.main_window.show()
        else:
            self.error_window = DLogicPage("Поле id сравнение пустое")
            self.error_window.show()
        self.click_close_widget()

    def start_to_work_1(self):
        self.ui.groupBox.setVisible(True)

    def back_to_main(self):
        self.close()

    def click_button_create_criteria(self):
        criteria_name = self.ui.lineEdit.text()
        criteria_code = self.ui.lineEdit_2.text()
        if criteria_name.isalnum() and criteria_code.isalnum():
            with SessionLocal() as session:
                already_exis = criteria.get_by_name(session, criteria_name)
                if already_exis is None:
                    criteria.create(session, criteria_name, criteria_code)
                else:
                    self.error_window = DLogicPage("Данная запись уже существует")
                    self.error_window.show()
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()
        else:
            self.error_window = DLogicPage("Введены недопустимые значения")
            self.error_window.show()
        self.create_or_update_tabs_table()

    def click_button_delete_criteria(self):
        id_text = self.ui.lineEdit_3.text()
        if id_text.isdigit():
            with SessionLocal() as s:
                criteria.criteria_delete(s, int(id_text))
        self.ui.lineEdit_3.clear()
        self.create_or_update_tabs_table()

    def click_button_create_contractor(self):
        contractor_name = self.ui.lineEdit_4.text()
        work_cost = self.ui.lineEdit_5.text()
        availability_of_technology = self.ui.lineEdit_6.text()
        tech_equipment = self.ui.lineEdit_7.text()
        availability_of_production_facilities = self.ui.lineEdit_8.text()
        qualified_human_resources_personnel = self.ui.lineEdit_9.text()
        if all([
            contractor_name.isalnum(), self.is_number(work_cost), availability_of_technology.isalpha(), tech_equipment.isalpha(),
            availability_of_production_facilities.isalpha(), qualified_human_resources_personnel.isalpha()
        ]):
            with SessionLocal() as session:
                already_exist = contractors.get_by_name(session, contractor_name)
                if already_exist is None:
                    contractors.create(
                        session, contractor_name, work_cost, availability_of_technology, tech_equipment,
                        availability_of_production_facilities, qualified_human_resources_personnel
                    )
                else:
                    self.error_window = DLogicPage("Данная запись уже существует")
                    self.error_window.show()
                self.ui.lineEdit_4.clear()
                self.ui.lineEdit_5.clear()
                self.ui.lineEdit_6.clear()
                self.ui.lineEdit_7.clear()
                self.ui.lineEdit_8.clear()
                self.ui.lineEdit_9.clear()
        else:
            self.error_window = DLogicPage("Введены недопустимые значения")
            self.error_window.show()
        self.create_or_update_tabs_table()

    def click_button_delete_contractor(self):
        id_text = self.ui.lineEdit_10.text()
        if id_text.isdigit():
            with SessionLocal() as s:
                contractors.delete(s, int(id_text))
        self.ui.lineEdit_10.clear()
        self.create_or_update_tabs_table()

    def create_or_update_tabs_table(self):
        self._tab_criteria_list()
        self._tab_contractor_list()

    def _tab_criteria_list(self):
        criteria_data_list = self.get_data_criteria()
        if criteria_data_list:
            self.ui.tableWidget.setColumnCount(3)
            self.ui.tableWidget.setRowCount(criteria_data_list.__len__())
            self.ui.tableWidget.setHorizontalHeaderLabels(["id", "Критерий", "Код критерия"])
            self.ui.tableWidget.setVerticalHeaderLabels(["" for _ in criteria_data_list])
            for row in criteria_data_list:
                id_item = QTableWidgetItem()
                name_item = QTableWidgetItem()
                code_item = QTableWidgetItem()
                id_item.setText(str(row["id"]))
                id_item.setFlags(id_item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                name_item.setText(row["name"])
                code_item.setText(row["code"])
                self.ui.tableWidget.setItem(criteria_data_list.index(row), 0, id_item)
                self.ui.tableWidget.setItem(criteria_data_list.index(row), 1, name_item)
                self.ui.tableWidget.setItem(criteria_data_list.index(row), 2, code_item)

    def _tab_contractor_list(self):
        contractors_data_list = self.get_data_contractors()
        if contractors_data_list:
            header = [
                "id", "Наименование подрядчика", "Стоимость работ", "Наличие технологий",
                "Тех. оснащенность", "Наличие произвенных мощностей",
                "Квалифицированный кадровый персонал"
            ]
            self.ui.tableWidget_2.setColumnCount(header.__len__())
            self.ui.tableWidget_2.setRowCount(contractors_data_list.__len__())
            self.ui.tableWidget_2.setHorizontalHeaderLabels(header)
            self.ui.tableWidget_2.setVerticalHeaderLabels(["" for _ in contractors_data_list])
            for row in contractors_data_list:
                id_contractor_item = QTableWidgetItem()
                id_contractor_item.setText(str(row["id_contractor"]))
                id_contractor_item.setFlags(id_contractor_item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                self.ui.tableWidget_2.setItem(contractors_data_list.index(row), 0, id_contractor_item)
                contractor_name_item = QTableWidgetItem()
                contractor_name_item.setText(str(row["contractor_name"]))
                self.ui.tableWidget_2.setItem(contractors_data_list.index(row), 1, contractor_name_item)
                work_cost_item = QTableWidgetItem()
                work_cost_item.setText(str(row["work_cost"]))
                self.ui.tableWidget_2.setItem(contractors_data_list.index(row), 2, work_cost_item)
                availability_of_technology_item = QTableWidgetItem()
                availability_of_technology_item.setText(str(row["availability_of_technology"]))
                self.ui.tableWidget_2.setItem(contractors_data_list.index(row), 3, availability_of_technology_item)
                tech_equipment_item = QTableWidgetItem()
                tech_equipment_item.setText(str(row["tech_equipment"]))
                self.ui.tableWidget_2.setItem(contractors_data_list.index(row), 4, tech_equipment_item)
                availability_of_production_facilities_item = QTableWidgetItem()
                availability_of_production_facilities_item.setText(str(row["availability_of_production_facilities"]))
                self.ui.tableWidget_2.setItem(contractors_data_list.index(row), 5,
                                              availability_of_production_facilities_item)
                qualified_human_resources_personnel_item = QTableWidgetItem()
                qualified_human_resources_personnel_item.setText(str(row["qualified_human_resources_personnel"]))
                self.ui.tableWidget_2.setItem(contractors_data_list.index(row), 6,
                                              qualified_human_resources_personnel_item)
