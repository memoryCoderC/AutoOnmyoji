# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import _thread
from time import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QComboBox

from src.game import Config
from src.game.Enchantment import Enchantment
from src.game.Probe import Probe
from src.system.Window import Window
from src.util import permissionUtil
from src.util.ThreadUtil import stop_thread
from src.util.log import logger
from src.window.hwndSelecter import Ui_SelectHwndDialog


class Ui_MainWindow(object):
    def __init__(self):
        self.hwnd = None
        self.battle_thread = None
        self.time = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.appNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.appNameLabel.setGeometry(QtCore.QRect(250, 0, 121, 41))

        self.battleTypeBox = QComboBox(self.centralwidget, minimumWidth=200)
        self.battleTypeBox.addItems(["御魂/业原火/觉醒", "结界突破"])

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
        self.startButton.clicked[bool].connect(self.change)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pop_selector()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AutoOnmyoji"))
        self.appNameLabel.setText(_translate("MainWindow", "AutoOnmyoji"))
        self.startButton.setText(_translate("MainWindow", "启动"))

    def pop_selector(self):
        selectHwndDialog = Ui_SelectHwndDialog(self)
        selectHwndDialog.setupUi()
        selectHwndDialog.show()

    def stop(self):
        Config.isRun = False
        self.startButton.setText("启动")
        self.startButton.setToolTip("点击结束运行")

    def change(self):
        self.time = time()
        if not Config.isRun:
            self.battle()
        else:
            stop_thread(self.battle_thread)
            logger.info("手动停止战斗")
            self.stop()

    def battle(self):
        logger.info("开始运行")
        window = Window(self.hwnd)
        battle = None
        if self.battleTypeBox.currentIndex() == 0:
            battle = Probe(window)
        else:
            battle = Enchantment(window)
        self.battle_thread = _thread.start_new_thread(battle.on_begin_battle, (self.stop,))
        Config.isRun = True
        self.startButton.setText("关闭")
        self.startButton.setToolTip("点击结束运行")
