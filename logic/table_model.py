from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, Qt


class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, data, header, vertHeader=None, comparator: bool = False):
        super().__init__(parent)
        self.data = data
        self.headerdata = header
        self.vertdata = vertHeader
        self.comparator = comparator

    def headerData(self, col, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headerdata[col]
            else:
                if self.vertdata is not None:
                    return self.vertdata[col]
        return None

    def columnCount(self, parent=None):
        return len(self.data[0])

    def rowCount(self, parent=None):
        return len(self.data)

    def data(self, index: QModelIndex, role: int):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            if self.comparator and row == col:
                return str(1)
            return str(self.data[row][col])
