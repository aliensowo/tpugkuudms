import sys
from PyQt5 import QtWidgets
from models.models import Base
from models.database import engine, SessionLocal
from models.crud import custom_users
from gui.A_auth_page import Ui_MainWindow
from gui.B_main_page import Ui_MainWindow as BPage

Base.metadata.create_all(bind=engine)


class Auth(QtWidgets.QMainWindow):

    def __init__(self):
        super(Auth, self).__init__()
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
                print("Register")
                custom_users.create_user(session, username, password)
                self.ui.checkBox.setCheckState(False)
                self.ui.usernameInput.clear()
                self.ui.passwordInput.clear()
            else:
                user = custom_users.get_user(session, username, password)
                if isinstance(user, custom_users.models.CustomUsers):
                    self.main_window = MainWindow()
                    self.main_window.show()
                    self.close()

                    print("Login")
                else:
                    print("Error")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = BPage()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = Auth()
    application.show()

    sys.exit(app.exec())
