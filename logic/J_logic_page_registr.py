from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox

from gui.J_logic_page_registrating import Ui_MainWindow as JPage
from models.database import SessionLocal
from models.crud import neighborhood_directory
from models.crud import custom_users
from models.crud import roles
from logic._base_class_logic import BaseClassLogic


class JLogicPage(QtWidgets.QMainWindow, BaseClassLogic):

    def __init__(self):
        super(JLogicPage, self).__init__()
        self.error_window = None
        self.winner_window = None
        self.ui = JPage()
        self.ui.setupUi(self)

        self.build_table()

        # button logic
        self.ui.pushButton.clicked.connect(self.save_data)
        self.ui.pushButton_2.clicked.connect(self.close)

    def build_table(self):
        self.ui.tableWidget.setColumnCount(2)
        with SessionLocal() as session:
            all_roles = roles.all(session)
            new_users = custom_users.all(session)
            self.ui.tableWidget.setRowCount(len(new_users))
            self.ui.tableWidget.setHorizontalHeaderLabels(["Пользователь", "Роль",])
            for user in new_users:
                user_item = QTableWidgetItem()
                user_item.setText(user["username"])
                user_item.setFlags(user_item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                self.ui.tableWidget.setItem(new_users.index(user), 0, user_item)
                role_item = QComboBox()
                role_item.addItems([item["name"] for item in all_roles])
                self.ui.tableWidget.setCellWidget(new_users.index(user), 1, role_item)

    def save_data(self):
        rows_count = self.ui.tableWidget.rowCount()
        for row in range(rows_count):
            cell_user = self.ui.tableWidget.item(row, 0)
            cell_role = self.ui.tableWidget.cellWidget(row, 1)
            print(cell_user.text(), cell_role.currentText())
            with SessionLocal() as session:
                custom_users.add_role(session, cell_user.text(), cell_role.currentText())
        self.close()

    def cancel(self):
        self.close()
