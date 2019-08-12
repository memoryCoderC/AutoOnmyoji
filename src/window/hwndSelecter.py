# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hwndSelecter.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog
from qtpy import QtGui

from src.util.log import logger
from src.window.pyspy import SpyLabel


class Ui_SelectHwndDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        pass

    def closeEvent(self, event):
        sys.exit()

    def setupUi(self):
        self.setObjectName("SelectHwndDialog")
        self.resize(261, 182)
        self.setModal(True)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.promptLabel = QtWidgets.QLabel(self)
        self.promptLabel.setGeometry(QtCore.QRect(60, 0, 131, 31))
        self.promptLabel.setObjectName("promptLabel")

        self.okButton = QtWidgets.QPushButton(self)
        self.okButton.setGeometry(QtCore.QRect(180, 150, 75, 23))
        self.okButton.setObjectName("okButton")

        self.spyLabel = SpyLabel(self)
        self.spyLabel.setObjectName("spyLabel")

        self.okButton.clicked.connect(lambda: self.start_assist())
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SelectHwndDialog", "窗口选择器"))
        self.promptLabel.setText(_translate("SelectHwndDialog", "阴阳师游戏窗口选择器"))
        self.okButton.setText(_translate("SelectHwndDialog", "启动辅助"))

    def start_assist(self):
        logger.info("启动辅助")
        hwnd = self.spyLabel.get_select_window()
        if hwnd is not None:
            self.parent.hwnd = hwnd
            self.hide()
        else:
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle('错误')
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("先选择阴阳师窗口")
            msgBox.setStandardButtons(QMessageBox.Close)
            msgBox.setModal(True)
            msgBox.show()
