# -*-coding:utf-8-*-
import random
import time

import win32api
import win32con
import win32gui
import win32ui

from src.image.ImageSearch import *

"""
用于获取windows窗口信息
"""


class Window:

    def __init__(self, window_title):
        self.window_title = window_title
        self.hwnd = win32gui.FindWindow(win32con.NULL, self.window_title)
        if self.hwnd == 0:
            raise Exception("未找到该名称的窗口句柄")

    def get_window_rect(self):
        return win32gui.GetWindowRect(self.hwnd)

    def get_hwnd(self):
        return self.hwnd

    def hwd_screenshot(self):
        # 获取句柄窗口的大小信息
        try:
            _left, _top, _right, _bot = self.get_window_rect()
            _width = _right - _left
            _height = _bot - _top
            # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
            _hwnd_dc = win32gui.GetWindowDC(self.hwnd)
            # 创建设备描述表
            _mfc_dc = win32ui.CreateDCFromHandle(_hwnd_dc)
            # 创建内存设备描述表
            _save_dc = _mfc_dc.CreateCompatibleDC()
            # 创建位图对象准备保存图片
            _save_bit_map = win32ui.CreateBitmap()
            # 为bitmap开辟存储空间
            _save_bit_map.CreateCompatibleBitmap(_mfc_dc, _width, _height)
            # 将截图保存到saveBitMap中
            _save_dc.SelectObject(_save_bit_map)
            # 保存bitmap到内存设备描述表
            _save_dc.BitBlt((0, 0), (_width, _height), _mfc_dc, (0, 0), win32con.SRCCOPY)

            # 如果要截图到打印设备：
            ###最后一个int参数：0-保存整个窗口，1-只保存客户区。如果PrintWindow成功函数返回值为1
            # result = windll.user32.PrintWindow(hWnd,_save_dc.GetSafeHdc(),0)
            # print(result) #PrintWindow成功则输出1

            # 保存图像
            ##方法一：windows api保存
            ###保存bitmap到文件
            # _save_bit_map.SaveBitmapFile(_save_dc, "img_Winapi.bmp")

            ##方法二(第一部分)：PIL保存
            ###获取位图信息
            # bmpinfo = _save_bit_map.GetInfo()
            # bmpstr = _save_bit_map.GetBitmapBits(True)
            ###生成图像
            # im_PIL = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
            ##方法二（后续转第二部分）

            ##方法三（第一部分）：opencv+numpy保存
            ###获取位图信息
            signed_ints_array = _save_bit_map.GetBitmapBits(True)
            return signed_ints_array, _width, _height
            ##方法三（后续转第二部分）
        finally:
            # 内存释放
            win32gui.DeleteObject(_save_bit_map.GetHandle())
            _save_dc.DeleteDC()
            _mfc_dc.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, _hwnd_dc)

        ##方法二（第二部分）：PIL保存
        ###PrintWindow成功,保存到文件,显示到屏幕
        # im_PIL.save("im_PIL.png")  # 保存
        # im_PIL.show()  # 显示

        ##方法三（第二部分）：opencv+numpy保存
        ###PrintWindow成功，保存到文件，显示到屏幕
        # im_opencv = numpy.frombuffer(signed_ints_array, dtype='uint8')
        # im_opencv.shape = (_height, _width, 4)
        # cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)
        # cv2.imwrite("im_opencv.jpg", im_opencv, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # 保存
        # cv2.namedWindow('im_opencv')  # 命名窗口
        # cv2.imshow("im_opencv", im_opencv)  # 显示
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def show_hwd_screenshot(self):
        img, width, height = self.hwd_screenshot()
        im_opencv = numpy.frombuffer(img, dtype='uint8')
        im_opencv.shape = (height, width, 4)
        cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)
        cv2.imwrite("im_opencv.jpg", im_opencv, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # 保存
        cv2.namedWindow('im_opencv')  # 命名窗口
        cv2.imshow("im_opencv", im_opencv)  # 显示
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def click(self, x, y):
        long_position = win32api.MAKELONG(x, y)
        time.sleep(0.05)
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
        time.sleep(0.05)  # 上下行代码不起作用（或者说是没有效果）
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
        time.sleep(0.05)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYFIRST, 68, None)  # 起作用

    def clickRange(self, left_top, right_bottom):
        x = random.randint(left_top[0], right_bottom[0])
        y = random.randint(left_top[1], right_bottom[1])
        self.click(x, y)
