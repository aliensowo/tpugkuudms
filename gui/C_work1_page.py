# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/C_work1_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1190, 596)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget_task_4 = QtWidgets.QWidget(self.centralwidget)
        self.widget_task_4.setGeometry(QtCore.QRect(0, 30, 1171, 521))
        self.widget_task_4.setObjectName("widget_task_4")
        self.tableWidget_task_4 = QtWidgets.QTableWidget(self.widget_task_4)
        self.tableWidget_task_4.setGeometry(QtCore.QRect(0, 10, 1181, 451))
        self.tableWidget_task_4.setObjectName("tableWidget_task_4")
        self.tableWidget_task_4.setColumnCount(0)
        self.tableWidget_task_4.setRowCount(0)
        self.pushButton_task_4 = QtWidgets.QPushButton(self.widget_task_4)
        self.pushButton_task_4.setGeometry(QtCore.QRect(370, 470, 171, 31))
        self.pushButton_task_4.setObjectName("pushButton_task_4")
        self.label_task_4 = QtWidgets.QLabel(self.widget_task_4)
        self.label_task_4.setGeometry(QtCore.QRect(20, 470, 121, 31))
        self.label_task_4.setWordWrap(True)
        self.label_task_4.setObjectName("label_task_4")
        self.label = QtWidgets.QLabel(self.widget_task_4)
        self.label.setGeometry(QtCore.QRect(770, 470, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget_task_4)
        self.label_2.setGeometry(QtCore.QRect(770, 490, 55, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(990, 10, 55, 16))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_task_4.setText(_translate("MainWindow", "Вперед"))
        self.label_task_4.setText(_translate("MainWindow", "Начать"))
        self.label.setText(_translate("MainWindow", "ИС: "))
        self.label_2.setText(_translate("MainWindow", "ОС: "))
        self.label_3.setText(_translate("MainWindow", "TextLabel"))
