from gui.A_auth_page import Ui_MainWindow
from PyQt5 import QtWidgets

from logic.D_logic_page import DLogicPage
from logic._base_class_logic import BaseClassLogic
from models.database import SessionLocal
from models.crud import custom_users
from logic.B_logic_page import BLogicPage


class ALogicPage(QtWidgets.QMainWindow, BaseClassLogic):

    def __init__(self):
        super(ALogicPage, self).__init__()
        self.main_window = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Button Logic Connect
        self.ui.pushButton.clicked.connect(self.auth)
        self.sender()

    def auth(self):
        password = self.ui.passwordInput.text()
        username = self.ui.usernameInput.text()
        with SessionLocal() as session:
            if self.ui.checkBox.isChecked():
                custom_users.create_user(session, username, password)
                self.ui.checkBox.setCheckState(False)
                self.ui.usernameInput.clear()
                self.ui.passwordInput.clear()
            else:
                user = custom_users.get_user(session, username, password)
                if isinstance(user, custom_users.models.CustomUsers):
                    compare_name = self.ui.lineEdit.text()
                    compare_id = self.get_or_create_compare(compare_name=compare_name)
                    self.main_window = BLogicPage(compare_id=compare_id, username=user.username)
                    self.main_window.show()
                    self.close()
                else:
                    self.error_window = DLogicPage("Неверный логин или пароль")
                    self.error_window.show()
