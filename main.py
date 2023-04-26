import sys
from PyQt5 import QtWidgets
from models.models import Base
from models.database import engine
from logic import ALogicPage

Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = ALogicPage()
    application.show()

    sys.exit(app.exec())
