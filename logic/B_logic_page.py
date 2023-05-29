from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem

from logic.D_logic_page import DLogicPage
from models.database import SessionLocal
from gui.B_new_main_page import Ui_MainWindow as BPage
from logic.C_logic_page import CLogicPage
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
        # self.compare_id = compare_id
        self.username = username

        # Логика кнопок в блоке задач
        self.ui.pushButton_4.clicked.connect(self.display_task_1_widget)
        self.ui.pushButton_5.clicked.connect(self.display_task_2_widget)
        self.ui.pushButton_6.clicked.connect(self.display_task_3_widget)
        self.ui.pushButton_7.clicked.connect(self.display_task_4_widget)

        # Логика кнопок в верхнем блоке
        self.ui.pushButton.clicked.connect(self.button_help)
        self.ui.pushButton_2.clicked.connect(self.button_about)
        self.ui.pushButton_3.clicked.connect(self.button_exit)

    def display_task_1_widget(self):
        self.main_window = CLogicPage(username=self.username)
        self.main_window.show()

    def display_task_2_widget(self):
        self.main_window = FLogicPage()
        self.main_window.show()

    def display_task_3_widget(self):
        self.main_window = GLogicPage()
        self.main_window.show()

    def display_task_4_widget(self):
        self.main_window = HLogicPage()
        self.main_window.show()

    def button_help(self):
        self.error_window = DLogicPage("Помощь")
        self.error_window.show()

    def button_about(self):
        self.error_window = DLogicPage("О программе")
        self.error_window.show()

    def button_exit(self):
        self.close()
