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
            user = custom_users.get_user(session, username, password)
            if self.ui.checkBox.isChecked():
                try:
                    if user is None:
                        custom_users.create_user(session, username, password)
                        self.ui.checkBox.setCheckState(False)
                        self.ui.usernameInput.clear()
                        self.ui.passwordInput.clear()
                    else:
                        self.error_window = DLogicPage("Данный пользователь уже зарегистрирован")
                        self.error_window.show()
                except Exception as _:
                    print(_)
                    self.error_window = DLogicPage("Произошла ошибка при регистрации")
                    self.error_window.show()
            elif user is None:
                self.error_window = DLogicPage("Пользователь не зарегистрирован")
                self.error_window.show()
            else:
                if user.role == "default":
                    self.error_window = DLogicPage("Ваша заявка на регистрацию на рассмотрении")
                    self.error_window.show()
                else:
                    if isinstance(user, custom_users.models.CustomUsers):
                        self.main_window = BLogicPage(username=user.username)
                        self.main_window.show()
                        self.close()
                    else:
                        self.error_window = DLogicPage("Неверный логин или пароль")
                        self.error_window.show()
