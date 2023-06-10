from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem

from gui.C_work1_page import Ui_MainWindow as CPage
from models.database import SessionLocal
from models.crud import criteria, contractors, contractors_to_contractors, criteria_to_criteria
from logic._base_class_logic import BaseClassLogic
from logic.D_logic_page import DLogicPage
from logic.E_logic_page import ELogicPage
from typing import List
import math


class CLogicPage(QtWidgets.QMainWindow, BaseClassLogic):
    task_4_struct = {
        "contractor_name": "Наименование подрядчика",
        "work_cost": "Стоимость работ",
        "tech_equipment": "Наличие технологий",
        "qualified_human_resources_personnel": "Наличие технологий",
        "availability_of_technology": "Наличие произвенных мощностей",
        "availability_of_production_facilities": "Квалифицированный кадровый персонал",
    }
    task_4_pages = []
    task_4_temp_data = []
    init_int = 0

    def __init__(self, compare_id: int, username: str):
        super(CLogicPage, self).__init__()
        self.error_window = None
        self.winner_window = None
        self.ui = CPage()
        self.ui.setupUi(self)

        self.compare_id = compare_id
        self.username = username
        self.ui.label_3.setText("Пользователь {}\nСравнение: {}".format(self.username, self.compare_id))
        self.ui.label_3.adjustSize()
        self.ui.label.setVisible(False)
        self.ui.label_2.setVisible(False)
        # prepare
        self.set__task_4_pages()
        self.ui.pushButton_task_4.clicked.connect(self.list_tabs_pagination_logic)
        # self.list_tabs_pagination_logic()

    def set__task_4_pages(self):
        criteria_list = self.get_data_criteria()
        for item in criteria_list:
            self.task_4_pages.append(item["name"])

    def list_tabs_pagination_logic(self):
        table_name = self.ui.label_task_4.text()
        if table_name == "Сравнение критериев":
            self.compare_criteria_to_criteria_get_data_from_table()
            if self.calculate():
                winner_obj = self.get_winner()
                self.winner_window = ELogicPage(winner=winner_obj, compare_id=self.compare_id, username=self.username)
                self.winner_window.show()
            else:
                self.error_window = DLogicPage()
                self.error_window.show()
        else:
            try:
                next_index = self.task_4_pages.index(table_name) + 1
                if next_index < len(self.task_4_pages):
                    # TODO: collect data and compare
                    self.collect_table_data(table_name)
                    if not self.calculate_iis_oos(table_name):
                        self.error_window = DLogicPage()
                        self.error_window.show()
                        return
                    # next page
                    self.ui.label_task_4.setText(self.task_4_pages[next_index])
                    self.ui.label_task_4.adjustSize()
                    # rebuild widget
                    self.display_task_4_widget()
                elif next_index >= len(self.task_4_pages):
                    # end of collect contractors compare
                    self.ui.label_task_4.setText("Сравнение критериев")
                    # self.ui.label_task_4.setVisible(False)
                    self.compare_criteria_to_criteria()
            except ValueError:
                self.ui.label_task_4.setText(self.task_4_pages[0])
                self.ui.label_task_4.adjustSize()
                self.display_task_4_widget()

    def compare_criteria_to_criteria_get_data_from_table(self):
        column = self.ui.tableWidget_task_4.columnCount()
        row = self.ui.tableWidget_task_4.rowCount()
        for i in range(row):
            for j in range(column):
                if i > j:
                    item = self.ui.tableWidget_task_4.item(i, j)
                    criteria_list = self.get_data_criteria()
                    header = []
                    for item_list in criteria_list:
                        header.append(item_list["id"])
                    c1 = header[i]
                    c2 = header[j]
                    if c1 != c2:
                        with SessionLocal() as session:
                            exist_crits = criteria_to_criteria.get_by_ids(
                                session, c1, c2, self.compare_id
                            )
                            if not exist_crits:
                                criteria_to_criteria.create(
                                    session,
                                    c1, c2, item.text(), self.compare_id
                                )
                            else:
                                if exist_crits.value != item.text():
                                    criteria_to_criteria.edit(
                                        session,
                                        c1, c2, item.text(), self.compare_id
                                    )

    def compare_criteria_to_criteria(self):
        criteria_list = self.get_data_criteria()
        header = []
        for item in criteria_list:
            header.append(item["name"])
        self.ui.tableWidget_task_4.setColumnCount(5)
        self.ui.tableWidget_task_4.setRowCount(5)
        self.ui.tableWidget_task_4.setHorizontalHeaderLabels(header)
        self.ui.tableWidget_task_4.setVerticalHeaderLabels(header)
        for row in range(len(header)):
            for column in range(len(header)):
                item = QTableWidgetItem()
                if row == column:
                    item.setText("1")
                    item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.ui.tableWidget_task_4.setItem(row, column, item)
                else:
                    with SessionLocal() as session:
                        c1 = criteria.get_by_name(session, header[row])
                        c2 = criteria.get_by_name(session, header[column])
                        pair = criteria_to_criteria.get_by_ids(
                            session, c1.id_criteria, c2.id_criteria, self.compare_id
                        )
                    if pair is not None:
                        item.setText(pair.value)
                        item_reverse = QTableWidgetItem()
                        item_reverse.setText(str(1 / float(pair.value)))
                        item_reverse.setFlags(item_reverse.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                        if row < column:
                            item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                        else:
                            item.setBackground(QColor(255, 128, 128))
                        self.ui.tableWidget_task_4.setItem(row, column, item)
                        self.ui.tableWidget_task_4.setItem(column, row, item_reverse)
                    else:
                        item.setText("")
                        if row < column:
                            item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                        else:
                            item.setBackground(QColor(255, 128, 128))
                        self.ui.tableWidget_task_4.setItem(row, column, item)

    def collect_table_data(self, current_page_name: str = None):
        column = self.ui.tableWidget_task_4.columnCount()
        row = self.ui.tableWidget_task_4.rowCount()
        with SessionLocal() as session:
            criteria_obj = criteria.get_by_name(session, current_page_name)
        for i in range(row):
            for j in range(column):
                if i > j:
                    item = self.ui.tableWidget_task_4.item(i, j)
                    contractors_data_list = self.get_contractors_query()
                    header = []
                    for elem in contractors_data_list:
                        header.append(elem.id_contractor)
                    contactor1 = header[i]
                    contactor2 = header[j]
                    if contactor1 != contactor2:
                        with SessionLocal() as session:
                            if not contractors_to_contractors.get_by_ids(
                                    session, contactor1, contactor2, criteria_obj.id_criteria, self.compare_id
                            ):
                                contractors_to_contractors.create(
                                    session,
                                    contactor1, contactor2, item.text(), criteria_obj.id_criteria, self.compare_id
                                )
                            else:
                                contractors_to_contractors.edit(
                                    session,
                                    contactor1, contactor2, criteria_obj.id_criteria, item.text(), self.compare_id
                                )

    def calculate_iis_oos(self, current_page_name: str):
        if current_page_name == "Начать":
            return
        sum_by_column = 0
        contractors_list_dict = self.get_data_contractors()
        vector_2d: List[List[float]] = []
        for i in range(len(contractors_list_dict)):
            temp = [0 for _ in range(len(contractors_list_dict))]
            vector_2d.append(temp.copy())
        for i in range(len(contractors_list_dict)):
            for j in range(len(contractors_list_dict)):
                if i == j:
                    vector_2d[i][j] = 1
                else:
                    with SessionLocal() as session:
                        criteria_obj = criteria.get_by_name(session, current_page_name)
                        pair = contractors_to_contractors.get_by_ids(
                            session, contractors_list_dict[i]["id_contractor"],
                            contractors_list_dict[j]["id_contractor"],
                            criteria_obj.id_criteria, self.compare_id
                        )
                        if pair is not None:
                            vector_2d[i][j] = float(pair.value)
                            vector_2d[j][i] = 1 / float(pair.value)
        # оценка компонентов вектора
        for i in range(len(contractors_list_dict)):
            elem_sum = 1
            for j in range(len(contractors_list_dict)):
                value = vector_2d[i][j]
                elem_sum *= value
            power = 1 / 6
            elem_sum = math.pow(elem_sum, power)
            sum_by_column += elem_sum
            vector_2d[i].append(elem_sum)
        # считаем локальные приоритеты
        for i in range(len(contractors_list_dict)):
            vector_2d[i].append(vector_2d[i][-1] / sum_by_column)
        # считаем лямбда макс
        sum_l = 0
        for i in range(len(contractors_list_dict)):
            temp_sum = 0
            for j in range(len(contractors_list_dict)):
                temp_sum += vector_2d[j][i]
            sum_l += temp_sum * vector_2d[i][-1]
        # считаем индекс согласованности
        iis = (sum_l - len(contractors_list_dict)) / (len(contractors_list_dict) - 1)
        # считаем значения соотнощение согласованности
        oos = iis / 1.12
        self.ui.label.setVisible(True)
        self.ui.label_2.setVisible(True)
        self.ui.label.setText(f"ИС: {iis}")
        self.ui.label.adjustSize()
        self.ui.label_2.setText(f"ОС: {oos}")
        self.ui.label_2.adjustSize()
        # TODO: если oos < 0.1 о ок, если нет то алерт на исправление
        if oos < 0.1:
            return vector_2d
        else:
            return []

    def display_task_4_widget(self):
        self.ui.label.setVisible(False)
        self.ui.label_2.setVisible(False)
        self.ui.label.setText(f"ИС: ")
        self.ui.label.adjustSize()
        self.ui.label_2.setText(f"ОС: ")
        self.ui.label_2.adjustSize()
        contractors_data_list = self.get_contractors_query()
        header = []
        for item in contractors_data_list:
            header.append(item.contractor_name)
        self.ui.tableWidget_task_4.setColumnCount(5)
        self.ui.tableWidget_task_4.setRowCount(5)
        self.ui.tableWidget_task_4.setHorizontalHeaderLabels(header)
        self.ui.tableWidget_task_4.setVerticalHeaderLabels(header)
        self.ui.tableWidget_task_4.cellChanged.connect(self.cell_on_changed)
        for row in range(len(header)):
            for column in range(len(header)):
                item = QTableWidgetItem()
                if row == column:
                    item.setText("1")
                    item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.ui.tableWidget_task_4.setItem(row, column, item)
                else:
                    with SessionLocal() as session:
                        table_name = self.ui.label_task_4.text()
                        criteria_obj = criteria.get_by_name(session, table_name)
                        c1 = contractors.get_by_name(session, header[row])
                        c2 = contractors.get_by_name(session, header[column])
                        pair = contractors_to_contractors.get_by_ids(
                            session, c1.id_contractor, c2.id_contractor, criteria_obj.id_criteria, self.compare_id
                        )
                    if pair is not None:
                        item.setText(pair.value)
                        item_reverse = QTableWidgetItem()
                        item_reverse.setText(str(1 / float(pair.value)))
                        item_reverse.setFlags(item_reverse.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                        if row < column:
                            item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                        else:
                            item.setBackground(QColor(255, 128, 128))
                        self.ui.tableWidget_task_4.setItem(row, column, item)
                        self.ui.tableWidget_task_4.setItem(column, row, item_reverse)
                    else:
                        item.setText("")
                        if row < column:
                            item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                        else:
                            item.setBackground(QColor(255, 128, 128))
                        self.ui.tableWidget_task_4.setItem(row, column, item)

    def cell_on_changed(self):
        cell = self.ui.tableWidget_task_4.currentItem()
        if cell is not None:
            if cell.column() > cell.row():
                return
            new_value = cell.text().replace(",", ".")
            if not self.is_number(new_value):
                self.error_window = DLogicPage("Введены недопустимые значения")
                self.error_window.show()
                cell.setText(".ERR")
                return
            try:
                cell.setText(str(float(new_value)))
            except ValueError:
                cell.setText(".ERR")
                return
            with SessionLocal() as s:
                table_name = self.ui.label_task_4.text()
                if table_name == "Сравнение критериев":
                    c = criteria_to_criteria.get_by_ids(s, cell.row() + 1, cell.column() + 1, self.compare_id)
                else:
                    criteria_obj = criteria.get_by_name(s, table_name)
                    c = contractors_to_contractors.get_by_ids(
                        s, cell.row() + 1, cell.column() + 1, criteria_obj.id_criteria, self.compare_id
                    )
                if c is not None and c.value == new_value:
                    return
            # for invert value
            try:
                invert_value = str(1 / float(new_value))
            except ValueError:
                invert_value = ".ERR"
            if cell.row() + 1 != cell.column() + 1:
                with SessionLocal() as s:
                    if table_name == "Сравнение критериев":
                        if not criteria_to_criteria.get_by_ids(
                                s, cell.row() + 1, cell.column() + 1, self.compare_id
                        ):
                            criteria_to_criteria.create(
                                s, cell.row() + 1, cell.column() + 1, new_value, self.compare_id
                            )
                        else:
                            criteria_to_criteria.edit(
                                s,
                                cell.row() + 1, cell.column() + 1, new_value, self.compare_id
                            )
                    else:
                        if not contractors_to_contractors.get_by_ids(
                                s, cell.row() + 1, cell.column() + 1, criteria_obj.id_criteria, self.compare_id
                        ):
                            contractors_to_contractors.create(
                                s, cell.row() + 1, cell.column() + 1, new_value, criteria_obj.id_criteria,
                                self.compare_id
                            )
                        else:
                            contractors_to_contractors.edit(
                                s,
                                cell.row() + 1, cell.column() + 1, criteria_obj.id_criteria, new_value, self.compare_id
                            )
            new_item = QTableWidgetItem()
            new_item.setText(invert_value)
            new_item.setFlags(new_item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
            self.ui.tableWidget_task_4.setItem(cell.column(), cell.row(), new_item)

    def calculate(self):
        sum_by_column = 0
        criteria_id_name = self.get_data_criteria()
        vector_2d: List[List[float]] = []

        for i in range(len(criteria_id_name)):
            temp = [0 for _ in range(len(criteria_id_name))]
            vector_2d.append(temp.copy())
        for i in range(len(criteria_id_name)):
            for j in range(len(criteria_id_name)):
                if i == j:
                    vector_2d[i][j] = 1
                else:
                    with SessionLocal() as session:
                        pair = criteria_to_criteria.get_by_ids(
                            session, criteria_id_name[i]["id"], criteria_id_name[j]["id"], self.compare_id
                        )
                        if pair is not None:
                            vector_2d[i][j] = float(pair.value)
                            vector_2d[j][i] = 1 / float(pair.value)

        # оценка компонентов вектора
        for i in range(len(criteria_id_name)):
            elem_sum = 1
            for j in range(len(criteria_id_name)):
                value = vector_2d[i][j]
                elem_sum *= value
            power = 1 / 6
            elem_sum = math.pow(elem_sum, power)
            sum_by_column += elem_sum
            vector_2d[i].append(elem_sum)

        # считаем локальные приоритеты
        for i in range(len(criteria_id_name)):
            vector_2d[i].append(vector_2d[i][-1] / sum_by_column)

        # считаем лямбда макс
        sum_l = 0
        for i in range(len(criteria_id_name)):
            temp_sum = 0
            for j in range(len(criteria_id_name)):
                temp_sum += vector_2d[j][i]
            sum_l += temp_sum * vector_2d[i][-1]
        # считаем индекс согласованности
        iis = (sum_l - len(criteria_id_name)) / (len(criteria_id_name) - 1)
        # считаем значения соотнощение согласованности
        oos = iis / 1.12
        self.ui.label.setVisible(True)
        self.ui.label_2.setVisible(True)
        self.ui.label.setText(f"ИС: {iis}")
        self.ui.label.adjustSize()
        self.ui.label_2.setText(f"ОС: {oos}")
        self.ui.label_2.adjustSize()
        # TODO: если oos < 0.1 о ок, если нет то алерт на исправление
        if oos < 0.1:
            return vector_2d
        else:
            return []

    def get_winner(self):
        criteria_matrix = self.calculate()
        criteria_id_name = self.get_data_criteria()
        ctc_list = self.get_data_contractors()
        result_sum = []
        for criteria_element in criteria_id_name:
            criteria_name = criteria_element["name"]
            contractor_matrix = self.calculate_iis_oos(criteria_name)
            summary = 0
            for i in range(len(contractor_matrix)):
                summary += contractor_matrix[i][-1] * criteria_matrix[i][-1]
            result_sum.append(summary)
        max_res = max(*result_sum)
        for ctc in ctc_list:
            if ctc["id_contractor"] == result_sum.index(max_res):
                return ctc
