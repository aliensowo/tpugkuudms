from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QTableWidgetItem

from logic.D_logic_page import DLogicPage
from models.database import SessionLocal
from gui.B_main_page import Ui_MainWindow as BPage
from logic.C_logic_page_new_calc_w1 import CLogicPage
from logic.F_logic_page import FLogicPage
from logic.G_logic_page import GLogicPage
from logic.H_logic_page import HLogicPage
from logic.I_logic_page import ILogicPage
from logic._base_class_logic import BaseClassLogic
from models.crud import criteria, contractors




class BLogicPage(QtWidgets.QMainWindow, BaseClassLogic):

    def __init__(self, username: str):
        super(BLogicPage, self).__init__()
        self.error_window = None
        self.main_window = None
        self.ui = BPage()
        self.ui.setupUi(self)
        self.compare_id = 2
        self.username = username
        self.ui.label_2.setText("Пользователь {}\nСравнение: {}".format(self.username, self.compare_id))
        self.ui.label_2.adjustSize()
        self.ui.widget_db.setVisible(False)
        # Widget logic
        self.ui.pushButton_db.clicked.connect(self.display_db_widget)
        self.ui.pushButton_4.clicked.connect(self.display_task_1_widget)
        self.ui.pushButton_6.clicked.connect(self.display_task_2_widget)
        self.ui.pushButton_8.clicked.connect(self.display_task_3_widget)
        self.ui.pushButton_9.clicked.connect(self.display_task_4_widget)
        self.ui.pushButton_7.clicked.connect(self.display_guide_widget)

        # Button logic
        self.ui.pushButton.clicked.connect(self.criteria_create)
        self.ui.pushButton_3.clicked.connect(self.contractor_create)
        self.ui.tableWidget.cellChanged.connect(self.cell_on_changed_criteria)
        self.ui.tableWidget_2.cellChanged.connect(self.cell_on_changed_contractor)
        self.ui.pushButton_2.clicked.connect(self.delete_object_contractor)
        self.ui.pushButton_5.clicked.connect(self.delete_object_criteria)

    def display_guide_widget(self):
        self.main_window = ILogicPage()
        self.main_window.show()

    def display_task_1_widget(self):
        # TODO: нужно проверять на наличие критериев и подрядчиков
        try:
            self.main_window = CLogicPage(compare_id=self.compare_id, username=self.username)
            self.main_window.show()
        except Exception as _:
            self.error_window = DLogicPage("В базе нет критериев или подрядчиков")
            self.error_window.show()

    def display_task_2_widget(self):
        self.main_window = FLogicPage()
        self.main_window.show()

    def display_task_3_widget(self):
        self.main_window = GLogicPage()
        self.main_window.show()

    def display_task_4_widget(self):
        self.main_window = HLogicPage()
        self.main_window.show()

    def delete_object_contractor(self):
        id_text = self.ui.lineEdit_3.text()
        if id_text.isdigit():
            with SessionLocal() as s:
                contractors.criteria_delete(s, int(id_text))
        self.ui.lineEdit_3.clear()

    def delete_object_criteria(self):
        id_text = self.ui.lineEdit_9.text()
        if id_text.isdigit():
            with SessionLocal() as s:
                criteria.criteria_delete(s, int(id_text))
        self.ui.lineEdit_9.clear()

    def cell_on_changed_criteria(self):
        cell = self.ui.tableWidget.currentItem()
        if cell is not None:
            id_item = self.ui.tableWidget.item(cell.row(), cell.column()-1)
            with SessionLocal() as s:
                c = criteria.get_by_id(s, int(id_item.text()))
                if c is not None and c.criteria_name != cell.text():
                    criteria.edit(s, int(id_item.text()), cell.text())

    def cell_on_changed_contractor(self):
        cell = self.ui.tableWidget_2.currentItem()
        if cell is not None:
            header = [
                "id_contractor",
                "contractor_name",
                "work_cost",
                "availability_of_technology",
                "tech_equipment",
                "availability_of_production_facilities",
                "qualified_human_resources_personnel"
            ]
            id_item = self.ui.tableWidget_2.item(cell.row(), 0)
            with SessionLocal() as s:
                c = contractors.get_by_id(s, int(id_item.text()))
                if c is not None:
                    try:
                        contractors.edit(s, int(id_item.text()), **{header[cell.column()]: cell.text()})
                    except Exception as e:
                        print(e)
                        exit()

    def display_db_widget(self):
        self.ui.widget_db.setVisible(not self.ui.widget_db.isVisible())
        if self.ui.widget_db.isVisible():
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
            # Contractors set
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
                    self.ui.tableWidget_2.setItem(contractors_data_list.index(row), 5, availability_of_production_facilities_item)
                    qualified_human_resources_personnel_item = QTableWidgetItem()
                    qualified_human_resources_personnel_item.setText(str(row["qualified_human_resources_personnel"]))
                    self.ui.tableWidget_2.setItem(contractors_data_list.index(row), 6, qualified_human_resources_personnel_item)

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
