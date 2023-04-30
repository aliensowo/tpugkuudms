from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem
from models.database import SessionLocal
from models.crud import criteria, contractors, contractors_to_contractors
from gui.B_main_page import Ui_MainWindow as BPage
from logic.C_logic_page import CLogicPage
from logic._base_class_logic import BaseClassLogic

from logic.table_model import MyTableModel


class BLogicPage(QtWidgets.QMainWindow, BaseClassLogic):

    def __init__(self):
        super(BLogicPage, self).__init__()
        self.ui = BPage()
        self.ui.setupUi(self)

        self.ui.widget_db.setVisible(False)
        # Widget logic
        self.ui.pushButton_4.clicked.connect(self.display_task_4_widget)
        self.ui.pushButton_db.clicked.connect(self.display_db_widget)
        # Button logic
        self.ui.pushButton.clicked.connect(self.criteria_create)
        self.ui.pushButton_3.clicked.connect(self.contractor_create)

    def display_task_4_widget(self):
        # TODO: нужно проверять на наличие критериев и подрядчиков
        try:
            self.main_window = CLogicPage()
            self.main_window.show()
        except Exception as e:
            print(e)
            # show alert

    def display_db_widget(self):
        self.ui.widget_db.setVisible(not self.ui.widget_db.isVisible())
        if self.ui.widget_db.isVisible():
            # Criteria set
            criteria_data_list = self.get_data_criteria()
            if criteria_data_list:
                struct_to_list = []
                for elem_criteria in criteria_data_list:
                    struct_to_list.append([elem_criteria["id"], elem_criteria["name"]])
                model_criteria = MyTableModel(self, data=criteria_data_list, header=[
                    "id", "Критерий"
                ], vertHeader=None)
                self.ui.tableView.setModel(model_criteria)
            # Contractors set
            contractors_data_list = self.get_data_contractors()
            contr_elem_list = []
            for contr_elem in contractors_data_list:
                contr_elem_list.append(list(contr_elem.values()))
            if contractors_data_list:
                model_contractors = MyTableModel(self, data=contr_elem_list, header=[
                    "id", "Наименование подрядчика", "Стоимость работ", "Наличие технологий",
                    "Тех. оснащенность", "Наличие произвенных мощностей",
                    "Квалифицированный кадровый персонал"
                ])
                self.ui.tableView_3.setModel(model_contractors)

    def criteria_create(self):
        criteria_name = self.ui.lineEdit_2.text()
        if criteria_name:
            with SessionLocal() as session:
                criteria.create_criteria(session, criteria_name)
                self.ui.lineEdit_2.clear()

    def contractor_create(self):
        contractor_name = self.ui.lineEdit_4.text()
        work_cost = self.ui.lineEdit.text()
        availability_of_technology = self.ui.lineEdit_5.text()
        tech_equipment = self.ui.lineEdit_6.text()
        availability_of_production_facilities = self.ui.lineEdit_7.text()
        qualified_human_resources_personnel = self.ui.lineEdit_8.text()
        if all([
            contractor_name, work_cost, availability_of_technology, tech_equipment,
            availability_of_production_facilities, qualified_human_resources_personnel
        ]):
            with SessionLocal() as session:
                contractors.create(
                    session, contractor_name, work_cost, availability_of_technology, tech_equipment,
                    availability_of_production_facilities, qualified_human_resources_personnel
                )
                self.ui.lineEdit_4.clear()
                self.ui.lineEdit.clear()
                self.ui.lineEdit_5.clear()
                self.ui.lineEdit_6.clear()
                self.ui.lineEdit_7.clear()
                self.ui.lineEdit_8.clear()