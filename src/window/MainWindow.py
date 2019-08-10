# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from src.game.Probe import Probe
from src.system.Window import Window
from src.util import permissionUtil
from src.util.log import logger
from src.window.pyspy import SpyLabel


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.appNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.appNameLabel.setGeometry(QtCore.QRect(250, 0, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.appNameLabel.setFont(font)
        self.appNameLabel.setObjectName("appNameLabel")

        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(510, 440, 111, 31))
        self.startButton.setObjectName("startButton")
        self.startButton.setToolTip("点击辅助开始运行")
        self.startButton.clicked[bool].connect(self.began_clicked)

        self.spyLabel = SpyLabel(self.centralwidget)
        self.spyLabel.setObjectName("spyLabel")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AutoOnmyoji"))
        self.appNameLabel.setText(_translate("MainWindow", "AutoOnmyoji"))
        self.startButton.setText(_translate("MainWindow", "启动"))

    def began_clicked(self):
        hwnd = self.spyLabel.get_select_window()
        if hwnd is not None:
            try:
                logger.info("开始运行")
                permissionUtil.check_get_permission()
                logger.info("权限判断结束")
                window = Window(hwnd)
                probe = Probe(window)
                probe.begin_battle()
            except Exception as e:
                logger.exception(e)
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('错误')
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("先选择指定的窗口")
            msgBox.setStandardButtons(QMessageBox.Close)
            reply = msgBox.exec()