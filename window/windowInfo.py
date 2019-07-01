import win32api
import win32con
import win32gui


def getWindowInfo():
    window_title = '课件学习 - Google Chrome'
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)
    hwnd = win32gui.FindWindow(win32con.NULL, window_title)
    window_left, window_top, window_right, window_bottom = win32gui.GetWindowRect(hwnd)
