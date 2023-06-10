import sys
from PyQt5 import QtWidgets
from models.models import Base
from models.database import engine
from logic import ALogicPage
from logic.D_logic_page import DLogicPage


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    try:
        Base.metadata.create_all(bind=engine)
        application = ALogicPage()
        application.show()
    except Exception:
        application = DLogicPage("Ошибка подключения к базе данных.")
        application.show()

    sys.exit(app.exec())
