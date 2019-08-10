from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QLabel

__author__ = 'CoderZh'

import win32gui
import win32con
import win32api


class SpyLabel(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.parent = parent
        self.spying = False
        self.rectanglePen = win32gui.CreatePen(win32con.PS_SOLID, 3, win32api.RGB(255, 0, 0))
        self.prevWindow = None
        self.setCursor(QtCore.Qt.SizeAllCursor)
        self.spyingCur = QCursor(QPixmap('resource/img/window/searchw.cur'))
        self.setGeometry(QtCore.QRect(170, 20, 41, 41))
        self.setPixmap(QtGui.QPixmap("resource/img/window/finderf.bmp"))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.spying = True
            self.setCursor(self.spyingCur)
            self.setPixmap(QtGui.QPixmap("resource/img/window/findere.bmp"))
            self.prevWindow = None

    # def mouseMoveEvent(self, event):
    #     if self.spying:
    #         curX, curY = win32gui.GetCursorPos()
    #         hwnd = win32gui.WindowFromPoint((curX, curY))
    #         if self.checkWindowValidity(hwnd):
    #             if self.prevWindow:
    #                 self.refreshWindow(self.prevWindow)
    #             self.prevWindow = hwnd
    #             self.highlightWindow(hwnd)
    #             self.displayWindowInformation(hwnd)

    def mouseReleaseEvent(self, event):
        if self.spying:
            curX, curY = win32gui.GetCursorPos()
            hwnd = win32gui.WindowFromPoint((curX, curY))
            if self.checkWindowValidity(hwnd):
                # if self.prevWindow:
                #     self.refreshWindow(self.prevWindow)
                self.prevWindow = hwnd
                self.highlightWindow(hwnd)
                self.displayWindowInformation(hwnd)
            # if self.prevWindow:
            #     self.refreshWindow(self.prevWindow)
            win32gui.ReleaseCapture()
            self.setCursor(QtCore.Qt.CrossCursor)
            self.setPixmap(QtGui.QPixmap("resource/img/window/finderf.bmp"))
            self.spying = False

    def highlightWindow(self, hwnd):
        if hwnd is not None:
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            windowDc = win32gui.GetWindowDC(hwnd)
            if windowDc:
                prevPen = win32gui.SelectObject(windowDc, self.rectanglePen)
                prevBrush = win32gui.SelectObject(windowDc, win32gui.GetStockObject(win32con.HOLLOW_BRUSH))
                win32gui.Rectangle(windowDc, 0, 0, right - left, bottom - top)
                win32gui.SelectObject(windowDc, prevPen)
                win32gui.SelectObject(windowDc, prevBrush)
                win32gui.ReleaseDC(hwnd, windowDc)

    def get_select_window(self):
        return self.prevWindow

    #
    # def refreshWindow(self, hwnd):
    #     win32gui.InvalidateRect(hwnd, None, True)
    #     win32gui.UpdateWindow(hwnd)
    #     win32gui.RedrawWindow(hwnd, None, None,
    #                           win32con.RDW_FRAME | win32con.RDW_INVALIDATE | win32con.RDW_UPDATENOW | win32con.RDW_ALLCHILDREN)

    def checkWindowValidity(self, hwnd):
        if not hwnd:
            return False
        if not win32gui.IsWindow(hwnd):
            return False
        if self.prevWindow == hwnd:
            return False
        if self.parent == hwnd:
            return False
        return True

    def displayWindowInformation(self, hwnd):
        className = win32gui.GetClassName(hwnd)
        print(className)

# class SpyDialog(QtGui.QDialog, Ui_SpyDialog):
#     def __init__(self, parent=None):
#         QtGui.QDialog.__init__(self, parent)
#         self.setupUi(self)
#         self.spyLabel = SpyLabel(self)
#         self.spyLabel.setGeometry(QtCore.QRect(170, 20, 41, 41))
#         self.spyLabel.setPixmap(QtGui.QPixmap(":/res/finderf.bmp"))
#         self.spyLabel.setObjectName("spyLabel")
#
#     def output(self, message):
#         self.textEditInformation.setText(message)


# if __name__ == "__main__":
#     import sys
#
#     app = QtGui.QApplication(sys.argv)
#     dlg = SpyDialog()
#     dlg.show()
#     sys.exit(app.exec_())
