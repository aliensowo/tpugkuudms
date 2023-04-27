from gui.A_auth_page import Ui_MainWindow
from PyQt5 import QtWidgets
from models.database import SessionLocal
from models.crud import custom_users
from logic.B_logic_page import BLogicPage
from settings import DEBUG


class ALogicPage(QtWidgets.QMainWindow):

    def __init__(self):
        super(ALogicPage, self).__init__()
        self.main_window = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Button Logic Connect
        self.ui.pushButton.clicked.connect(self.auth)
        self.sender()

    def auth(self):
        if DEBUG:
            self.main_window = BLogicPage()
            self.main_window.show()
            self.close()
        else:
            password = self.ui.passwordInput.text()
            username = self.ui.usernameInput.text()
            with SessionLocal() as session:
                if self.ui.checkBox.isChecked():
                    print("Register")
                    custom_users.create_user(session, username, password)
                    self.ui.checkBox.setCheckState(False)
                    self.ui.usernameInput.clear()
                    self.ui.passwordInput.clear()
                else:
                    user = custom_users.get_user(session, username, password)
                    if isinstance(user, custom_users.models.CustomUsers):
                        self.main_window = BLogicPage()
                        self.main_window.show()
                        self.close()

                        print("Login")
                    else:
                        print("Error")
