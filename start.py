# coding=utf-8
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from src.window.MainWindow import Ui_MainWindow
from src.window.mainFrame import Example

if __name__ == '__main__':
    # 创建应用程序和对象
    app = QApplication(sys.argv)
    ex = Ui_MainWindow()
    MainWindow = QMainWindow()
    ex.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

    # 系统exit()方法确保应用程序干净的退出
    # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替

    # try:
    #     logger.info("开始运行")
    #     permissionUtil.check_get_permission()
    #     logger.info("权限判断结束")
    #     window = Window(config.get("game", "windowTitle"))
    #     probe = Probe(window)
    #     probe.begin_battle()
    # except Exception as e:
    #     logger.exception(e)
