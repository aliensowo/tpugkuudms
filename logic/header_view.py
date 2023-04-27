from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class MyHeaderView(QtWidgets.QHeaderView):
    def __init__(self, parent):
        QtWidgets.QHeaderView.__init__(self, Qt.Horizontal, parent)
        self.sectionResized.connect(self.myresize)

    def myresize(self, *args):
        '''Resize while keep total width constant'''

        # keep a copy of column widths
        ws = []
        for c in range(self.count()):
            wii = self.sectionSize(c)
            ws.append(wii)

        if args[0] > 0 or args[0] < self.count():
            for ii in range(args[0], self.count()):
                if ii == args[0]:
                    # resize present column
                    self.resizeSection(ii, args[2])
                elif ii == args[0] + 1:
                    # if present column expands, shrink the one to the right
                    self.resizeSection(ii, ws[ii] - (args[2] - args[1]))
                else:
                    # keep all others as they were
                    self.resizeSection(ii, ws[ii])

    def resizeEvent(self, event):
        """Resize table as a whole, need this to enable resizing"""

        super(QtWidgets.QHeaderView, self).resizeEvent(event)
        self.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        for column in range(self.count()):
            width = self.sectionSize(column)
            self.setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
            self.setSectionResizeMode(column, QtWidgets.QHeaderView.Interactive)
            self.resizeSection(column, width)

        return
