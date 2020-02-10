# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Google Sync\Aviato0.01\MS\Speach_proj\bot\design\bar_design.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(386, 441)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.plainTextEdit.setBaseSize(QtCore.QSize(0, 0))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 3)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 50))
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 2, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 2, 1, 1)
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "Отправить"))
        self.toolButton.setText(_translate("MainWindow", "..."))
