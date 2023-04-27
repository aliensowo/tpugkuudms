from PyQt5 import QtWidgets
from gui.B_main_page import Ui_MainWindow as BPage
from models.database import SessionLocal
from models.crud import criteria, contractors
from logic.header_view import MyHeaderView
from logic.table_model import MyTableModel


class BLogicPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(BLogicPage, self).__init__()
        self.ui = BPage()
        self.ui.setupUi(self)

        # prepare
        self.ui.tabWidget.setVisible(False)
        # Button logic
        self.ui.pushButton_db.clicked.connect(self.display_db_tab)
        self.ui.pushButton.clicked.connect(self.criteria_create)
        self.ui.pushButton_3.clicked.connect(self.contractor_create)

    def display_db_tab(self):
        self.ui.tabWidget.setVisible(not self.ui.tabWidget.isVisible())
        if self.ui.tabWidget.isVisible():
            # Criteria set
            criteria_data_list = self.get_data_criteria()
            if criteria_data_list:
                model_criteria = MyTableModel(self, data=criteria_data_list, header=[
                    "id", "Критерий"
                ])
                self.ui.tableView.setModel(model_criteria)
                hh_criteria = MyHeaderView(self)
                self.ui.tableView.setHorizontalHeader(hh_criteria)
            # Contractors set
            contractors_data_list = self.get_data_contractors()
            if contractors_data_list:
                model_contractors = MyTableModel(self, data=contractors_data_list, header=[
                    "id", "Наименование подрядчика", "Стоимость работ", "Наличие технологий",
                    "Тех. оснащенность", "Наличие произвенных мощностей",
                    "Квалифицированный кадровый персонал"
                ])
                self.ui.tableView_3.setModel(model_contractors)
                hh_contractors = MyHeaderView(self)
                self.ui.tableView_3.setHorizontalHeader(hh_contractors)

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

    @staticmethod
    def get_data_contractors() -> list:
        data = []
        with SessionLocal() as session:
            contractors_list = contractors.get_list(session)
        for unit in contractors_list:
            data.append([
                unit.id_contractor, unit.contractor_name, unit.work_cost, unit.availability_of_technology,
                unit.tech_equipment, unit.availability_of_production_facilities,
                unit.qualified_human_resources_personnel
            ])
        return data

    @staticmethod
    def get_data_criteria() -> list:
        data = []
        with SessionLocal() as session:
            criteria_list = criteria.get_criteria_list(session)
        for criteria_unit in criteria_list:
            data.append([criteria_unit.id_criteria, criteria_unit.criteria_name])
        return data
