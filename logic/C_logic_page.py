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
        if criteria_name and criteria_code:
            with SessionLocal() as session:
                already_exis = criteria.get_by_name(criteria_name)
                if already_exis is None:
                    criteria.create(session, criteria_name, criteria_code)
                else:
                    self.error_window = DLogicPage("Данная запись уже существует")
                    self.error_window.show()
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()
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
            contractor_name, work_cost, availability_of_technology, tech_equipment,
            availability_of_production_facilities, qualified_human_resources_personnel
        ]):
            with SessionLocal() as session:
                already_exist = contractors.get_by_name(contractor_name)
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
                id_item.setText(str(row["id"]))
                id_item.setFlags(id_item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                name_item.setText(row["name"])
                self.ui.tableWidget.setItem(criteria_data_list.index(row), 0, id_item)
                self.ui.tableWidget.setItem(criteria_data_list.index(row), 1, name_item)

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

    """
    
    
    
    
    """
    #
    # def set__task_4_pages(self):
    #     criteria_list = self.get_data_criteria()
    #     for item in criteria_list:
    #         self.task_4_pages.append(item["name"])
    #
    # def list_tabs_pagination_logic(self):
    #     table_name = self.ui.label_task_4.text()
    #     if table_name == "Сравнение критериев":
    #         self.compare_criteria_to_criteria_get_data_from_table()
    #         if self.calculate():
    #             winner_obj = self.get_winner()
    #             self.winner_window = ELogicPage(winner=winner_obj, compare_id=self.compare_id, username=self.username)
    #             self.winner_window.show()
    #         else:
    #             self.error_window = DLogicPage()
    #             self.error_window.show()
    #     else:
    #         try:
    #             next_index = self.task_4_pages.index(table_name) + 1
    #             if next_index < len(self.task_4_pages):
    #                 # TODO: collect data and compare
    #                 self.collect_table_data(table_name)
    #                 if not self.calculate_iis_oos(table_name):
    #                     self.error_window = DLogicPage()
    #                     self.error_window.show()
    #                     return
    #                 # next page
    #                 self.ui.label_task_4.setText(self.task_4_pages[next_index])
    #                 self.ui.label_task_4.adjustSize()
    #                 # rebuild widget
    #                 self.display_task_4_widget()
    #             elif next_index >= len(self.task_4_pages):
    #                 # end of collect contractors compare
    #                 self.ui.label_task_4.setText("Сравнение критериев")
    #                 # self.ui.label_task_4.setVisible(False)
    #                 self.compare_criteria_to_criteria()
    #         except ValueError:
    #             self.ui.label_task_4.setText(self.task_4_pages[0])
    #             self.ui.label_task_4.adjustSize()
    #             self.display_task_4_widget()
    #
    # def compare_criteria_to_criteria_get_data_from_table(self):
    #     column = self.ui.tableWidget_task_4.columnCount()
    #     row = self.ui.tableWidget_task_4.rowCount()
    #     for i in range(row):
    #         for j in range(column):
    #             if i > j:
    #                 item = self.ui.tableWidget_task_4.item(i, j)
    #                 criteria_list = self.get_data_criteria()
    #                 header = []
    #                 for item_list in criteria_list:
    #                     header.append(item_list["id"])
    #                 c1 = header[i]
    #                 c2 = header[j]
    #                 if c1 != c2:
    #                     with SessionLocal() as session:
    #                         exist_crits = criteria_to_criteria.get_by_ids(
    #                             session, c1, c2, self.compare_id
    #                         )
    #                         if not exist_crits:
    #                             criteria_to_criteria.create(
    #                                 session,
    #                                 c1, c2, item.text(), self.compare_id
    #                             )
    #                         else:
    #                             if exist_crits.value != item.text():
    #                                 criteria_to_criteria.edit(
    #                                     session,
    #                                     c1, c2, item.text(), self.compare_id
    #                                 )
    #
    # def compare_criteria_to_criteria(self):
    #     criteria_list = self.get_data_criteria()
    #     header = []
    #     for item in criteria_list:
    #         header.append(item["name"])
    #     self.ui.tableWidget_task_4.setColumnCount(5)
    #     self.ui.tableWidget_task_4.setRowCount(5)
    #     self.ui.tableWidget_task_4.setHorizontalHeaderLabels(header)
    #     self.ui.tableWidget_task_4.setVerticalHeaderLabels(header)
    #     for row in range(len(header)):
    #         for column in range(len(header)):
    #             item = QTableWidgetItem()
    #             if row == column:
    #                 item.setText("1")
    #                 item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
    #                 self.ui.tableWidget_task_4.setItem(row, column, item)
    #             else:
    #                 with SessionLocal() as session:
    #                     c1 = criteria.get_by_name(session, header[row])
    #                     c2 = criteria.get_by_name(session, header[column])
    #                     pair = criteria_to_criteria.get_by_ids(
    #                         session, c1.id_criteria, c2.id_criteria, self.compare_id
    #                     )
    #                 if pair is not None:
    #                     item.setText(pair.value)
    #                     item_reverse = QTableWidgetItem()
    #                     item_reverse.setText(str(1 / float(pair.value)))
    #                     item_reverse.setFlags(item_reverse.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
    #                     if row < column:
    #                         item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
    #                     else:
    #                         item.setBackground(QColor(255, 128, 128))
    #                     self.ui.tableWidget_task_4.setItem(row, column, item)
    #                     self.ui.tableWidget_task_4.setItem(column, row, item_reverse)
    #                 else:
    #                     item.setText("")
    #                     if row < column:
    #                         item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
    #                     else:
    #                         item.setBackground(QColor(255, 128, 128))
    #                     self.ui.tableWidget_task_4.setItem(row, column, item)
    #
    # def collect_table_data(self, current_page_name: str = None):
    #     column = self.ui.tableWidget_task_4.columnCount()
    #     row = self.ui.tableWidget_task_4.rowCount()
    #     with SessionLocal() as session:
    #         criteria_obj = criteria.get_by_name(session, current_page_name)
    #     for i in range(row):
    #         for j in range(column):
    #             if i > j:
    #                 item = self.ui.tableWidget_task_4.item(i, j)
    #                 contractors_data_list = self.get_contractors_query()
    #                 header = []
    #                 for elem in contractors_data_list:
    #                     header.append(elem.id_contractor)
    #                 contactor1 = header[i]
    #                 contactor2 = header[j]
    #                 if contactor1 != contactor2:
    #                     with SessionLocal() as session:
    #                         if not contractors_to_contractors.get_by_ids(
    #                                 session, contactor1, contactor2, criteria_obj.id_criteria, self.compare_id
    #                         ):
    #                             contractors_to_contractors.create(
    #                                 session,
    #                                 contactor1, contactor2, item.text(), criteria_obj.id_criteria, self.compare_id
    #                             )
    #                         else:
    #                             contractors_to_contractors.edit(
    #                                 session,
    #                                 contactor1, contactor2, criteria_obj.id_criteria, item.text(), self.compare_id
    #                             )
    #
    # def calculate_iis_oos(self, current_page_name: str):
    #     if current_page_name == "Начать":
    #         return
    #     sum_by_column = 0
    #     contractors_list_dict = self.get_data_contractors()
    #     vector_2d: List[List[float]] = []
    #     for i in range(len(contractors_list_dict)):
    #         temp = [0 for _ in range(len(contractors_list_dict))]
    #         vector_2d.append(temp.copy())
    #     for i in range(len(contractors_list_dict)):
    #         for j in range(len(contractors_list_dict)):
    #             if i == j:
    #                 vector_2d[i][j] = 1
    #             else:
    #                 with SessionLocal() as session:
    #                     criteria_obj = criteria.get_by_name(session, current_page_name)
    #                     pair = contractors_to_contractors.get_by_ids(
    #                         session, contractors_list_dict[i]["id_contractor"],
    #                         contractors_list_dict[j]["id_contractor"],
    #                         criteria_obj.id_criteria, self.compare_id
    #                     )
    #                     if pair is not None:
    #                         vector_2d[i][j] = float(pair.value)
    #                         vector_2d[j][i] = 1 / float(pair.value)
    #     # оценка компонентов вектора
    #     for i in range(len(contractors_list_dict)):
    #         elem_sum = 1
    #         for j in range(len(contractors_list_dict)):
    #             value = vector_2d[i][j]
    #             elem_sum *= value
    #         power = 1 / 6
    #         elem_sum = math.pow(elem_sum, power)
    #         sum_by_column += elem_sum
    #         vector_2d[i].append(elem_sum)
    #     # считаем локальные приоритеты
    #     for i in range(len(contractors_list_dict)):
    #         vector_2d[i].append(vector_2d[i][-1] / sum_by_column)
    #     # считаем лямбда макс
    #     sum_l = 0
    #     for i in range(len(contractors_list_dict)):
    #         temp_sum = 0
    #         for j in range(len(contractors_list_dict)):
    #             temp_sum += vector_2d[j][i]
    #         sum_l += temp_sum * vector_2d[i][-1]
    #     # считаем индекс согласованности
    #     iis = (sum_l - len(contractors_list_dict)) / (len(contractors_list_dict) - 1)
    #     # считаем значения соотнощение согласованности
    #     oos = iis / 1.12
    #     self.ui.label.setVisible(True)
    #     self.ui.label_2.setVisible(True)
    #     self.ui.label.setText(f"ИС: {iis}")
    #     self.ui.label.adjustSize()
    #     self.ui.label_2.setText(f"ОС: {oos}")
    #     self.ui.label_2.adjustSize()
    #     # TODO: если oos < 0.1 о ок, если нет то алерт на исправление
    #     if oos < 0.1:
    #         return vector_2d
    #     else:
    #         return []
    #
    # def display_task_4_widget(self):
    #     self.ui.label.setVisible(False)
    #     self.ui.label_2.setVisible(False)
    #     self.ui.label.setText(f"ИС: ")
    #     self.ui.label.adjustSize()
    #     self.ui.label_2.setText(f"ОС: ")
    #     self.ui.label_2.adjustSize()
    #     contractors_data_list = self.get_contractors_query()
    #     header = []
    #     for item in contractors_data_list:
    #         header.append(item.contractor_name)
    #     self.ui.tableWidget_task_4.setColumnCount(5)
    #     self.ui.tableWidget_task_4.setRowCount(5)
    #     self.ui.tableWidget_task_4.setHorizontalHeaderLabels(header)
    #     self.ui.tableWidget_task_4.setVerticalHeaderLabels(header)
    #     self.ui.tableWidget_task_4.cellChanged.connect(self.cell_on_changed)
    #     for row in range(len(header)):
    #         for column in range(len(header)):
    #             item = QTableWidgetItem()
    #             if row == column:
    #                 item.setText("1")
    #                 item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
    #                 self.ui.tableWidget_task_4.setItem(row, column, item)
    #             else:
    #                 with SessionLocal() as session:
    #                     table_name = self.ui.label_task_4.text()
    #                     criteria_obj = criteria.get_by_name(session, table_name)
    #                     c1 = contractors.get_by_name(session, header[row])
    #                     c2 = contractors.get_by_name(session, header[column])
    #                     pair = contractors_to_contractors.get_by_ids(
    #                         session, c1.id_contractor, c2.id_contractor, criteria_obj.id_criteria, self.compare_id
    #                     )
    #                 if pair is not None:
    #                     item.setText(pair.value)
    #                     item_reverse = QTableWidgetItem()
    #                     item_reverse.setText(str(1 / float(pair.value)))
    #                     item_reverse.setFlags(item_reverse.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
    #                     if row < column:
    #                         item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
    #                     else:
    #                         item.setBackground(QColor(255, 128, 128))
    #                     self.ui.tableWidget_task_4.setItem(row, column, item)
    #                     self.ui.tableWidget_task_4.setItem(column, row, item_reverse)
    #                 else:
    #                     item.setText("")
    #                     if row < column:
    #                         item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
    #                     else:
    #                         item.setBackground(QColor(255, 128, 128))
    #                     self.ui.tableWidget_task_4.setItem(row, column, item)
    #
    # def cell_on_changed(self):
    #     cell = self.ui.tableWidget_task_4.currentItem()
    #     if cell is not None:
    #         new_value = cell.text().replace(",", ".")
    #         if not new_value.__contains__("."):
    #             try:
    #                 cell.setText(str(float(new_value)))
    #             except ValueError:
    #                 cell.setText(".ERR")
    #             return
    #         if cell.column() > cell.row():
    #             return
    #         with SessionLocal() as s:
    #             table_name = self.ui.label_task_4.text()
    #             if table_name == "Сравнение критериев":
    #                 c = criteria_to_criteria.get_by_ids(s, cell.row() + 1, cell.column() + 1, self.compare_id)
    #             else:
    #                 criteria_obj = criteria.get_by_name(s, table_name)
    #                 c = contractors_to_contractors.get_by_ids(
    #                     s, cell.row() + 1, cell.column() + 1, criteria_obj.id_criteria, self.compare_id
    #                 )
    #             if c is not None and c.value == new_value:
    #                 return
    #         try:
    #             invert_value = str(1 / float(new_value))
    #         except ValueError:
    #             invert_value = ".ERR"
    #         if cell.row() + 1 != cell.column() + 1:
    #             with SessionLocal() as s:
    #                 if table_name == "Сравнение критериев":
    #                     if not criteria_to_criteria.get_by_ids(
    #                             s, cell.row() + 1, cell.column() + 1, self.compare_id
    #                     ):
    #                         criteria_to_criteria.create(
    #                             s, cell.row() + 1, cell.column() + 1, new_value, self.compare_id
    #                         )
    #                     else:
    #                         criteria_to_criteria.edit(
    #                             s,
    #                             cell.row() + 1, cell.column() + 1, new_value, self.compare_id
    #                         )
    #                 else:
    #                     if not contractors_to_contractors.get_by_ids(
    #                             s, cell.row() + 1, cell.column() + 1, criteria_obj.id_criteria, self.compare_id
    #                     ):
    #                         contractors_to_contractors.create(
    #                             s, cell.row() + 1, cell.column() + 1, new_value, criteria_obj.id_criteria,
    #                             self.compare_id
    #                         )
    #                     else:
    #                         contractors_to_contractors.edit(
    #                             s,
    #                             cell.row() + 1, cell.column() + 1, criteria_obj.id_criteria, new_value, self.compare_id
    #                         )
    #         new_item = QTableWidgetItem()
    #         new_item.setText(invert_value)
    #         new_item.setFlags(new_item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
    #         self.ui.tableWidget_task_4.setItem(cell.column(), cell.row(), new_item)
    #
    # def calculate(self):
    #     sum_by_column = 0
    #     criteria_id_name = self.get_data_criteria()
    #     vector_2d: List[List[float]] = []
    #
    #     for i in range(len(criteria_id_name)):
    #         temp = [0 for _ in range(len(criteria_id_name))]
    #         vector_2d.append(temp.copy())
    #     for i in range(len(criteria_id_name)):
    #         for j in range(len(criteria_id_name)):
    #             if i == j:
    #                 vector_2d[i][j] = 1
    #             else:
    #                 with SessionLocal() as session:
    #                     pair = criteria_to_criteria.get_by_ids(
    #                         session, criteria_id_name[i]["id"], criteria_id_name[j]["id"], self.compare_id
    #                     )
    #                     if pair is not None:
    #                         vector_2d[i][j] = float(pair.value)
    #                         vector_2d[j][i] = 1 / float(pair.value)
    #
    #     # оценка компонентов вектора
    #     for i in range(len(criteria_id_name)):
    #         elem_sum = 1
    #         for j in range(len(criteria_id_name)):
    #             value = vector_2d[i][j]
    #             elem_sum *= value
    #         power = 1 / 6
    #         elem_sum = math.pow(elem_sum, power)
    #         sum_by_column += elem_sum
    #         vector_2d[i].append(elem_sum)
    #
    #     # считаем локальные приоритеты
    #     for i in range(len(criteria_id_name)):
    #         vector_2d[i].append(vector_2d[i][-1] / sum_by_column)
    #
    #     # считаем лямбда макс
    #     sum_l = 0
    #     for i in range(len(criteria_id_name)):
    #         temp_sum = 0
    #         for j in range(len(criteria_id_name)):
    #             temp_sum += vector_2d[j][i]
    #         sum_l += temp_sum * vector_2d[i][-1]
    #     # считаем индекс согласованности
    #     iis = (sum_l - len(criteria_id_name)) / (len(criteria_id_name) - 1)
    #     # считаем значения соотнощение согласованности
    #     oos = iis / 1.12
    #     self.ui.label.setVisible(True)
    #     self.ui.label_2.setVisible(True)
    #     self.ui.label.setText(f"ИС: {iis}")
    #     self.ui.label.adjustSize()
    #     self.ui.label_2.setText(f"ОС: {oos}")
    #     self.ui.label_2.adjustSize()
    #     # TODO: если oos < 0.1 о ок, если нет то алерт на исправление
    #     if oos < 0.1:
    #         return vector_2d
    #     else:
    #         return []
    #
    # def get_winner(self):
    #     criteria_matrix = self.calculate()
    #     criteria_id_name = self.get_data_criteria()
    #     ctc_list = self.get_data_contractors()
    #     result_sum = []
    #     for criteria_element in criteria_id_name:
    #         criteria_name = criteria_element["name"]
    #         contractor_matrix = self.calculate_iis_oos(criteria_name)
    #         summary = 0
    #         for i in range(len(contractor_matrix)):
    #             summary += contractor_matrix[i][-1] * criteria_matrix[i][-1]
    #         result_sum.append(summary)
    #     max_res = max(*result_sum)
    #     for ctc in ctc_list:
    #         if ctc["id_contractor"] == result_sum.index(max_res):
    #             return ctc
