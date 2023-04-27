from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, Qt


class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, data, header):
        super().__init__(parent)
        self.data = data
        self.headerdata = header

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headerdata[col]
        return None

    def columnCount(self, parent=None):
        return len(self.data[0])

    def rowCount(self, parent=None):
        return len(self.data)

    def data(self, index: QModelIndex, role: int):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return str(self.data[row][col])
