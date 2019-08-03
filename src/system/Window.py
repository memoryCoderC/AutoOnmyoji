# -*-coding:utf-8-*-
import random
import time

import pyautogui
import win32api
import win32con
import win32gui
import win32ui

from src.image import Image

"""
用于获取windows窗口信息
"""
default_window_width = 1152
default_window_height = 679


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
            return Image.get_img_opencv(signed_ints_array, _width, _height)
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

    def mouse_active(self):
        win32api.SendMessage(self.hwnd, win32con.WM_SETFOCUS)  # 起作用
        win32api.SendMessage(self.hwnd, win32con.WM_NCMBUTTONDOWN)  # 起作用

    def click(self, x, y):
        print('点击-%s,-%s' % (x, y))
        long_position = win32api.MAKELONG(x, y)
        win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
        # time.sleep(0.1)  # 上下行代码不起作用（或者说是没有效果）
        win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)

    def click_range(self, left_top, right_bottom):
        x = random.randint(left_top[0], right_bottom[0])
        y = random.randint(left_top[1], right_bottom[1])
        self.click(x, y)

    def mouse_drag(self, pos1, pos2):
        """
        后台鼠标拖拽
            :param self:
            :param pos1: (x,y) 起点坐标
            :param pos2: (x,y) 终点坐标
        """
        import numpy
        move_x = numpy.linspace(pos1[0], pos2[0], num=20, endpoint=True)[0:]
        move_y = numpy.linspace(pos1[1], pos2[1], num=20, endpoint=True)[0:]
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, 0, win32api.MAKELONG(pos1[0], pos1[1]))
        for i in range(20):
            x = int(round(move_x[i]))
            y = int(round(move_y[i]))
            win32gui.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
            time.sleep(0.01)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(pos2[0], pos2[1]))

    def mouse_move(self, pos1, pos2):
        """
        后台鼠标移动
            :param self:
            :param pos1: (x,y) 起点坐标
            :param pos2: (x,y) 终点坐标
        """
        win32api.PostMessage(self.hwnd, win32con.WM_CAPTURECHANGED, win32con.MK_LBUTTON,
                             win32api.MAKELONG(pos1[0], pos1[1]))
        step_width_list = []
        step_height_list = []
        step_list = []
        width = pos2[0] - pos1[0]
        height = pos2[1] - pos1[1]
        step_width = 6
        step_height = 6

        if width < 0:
            step_width = -step_width
        if height < 0:
            step_height = -step_height

        for i in range(pos1[0], pos2[0], step_width):
            step_width_list.append(i)
        for i in range(pos1[1], pos2[1], step_height):
            step_height_list.append(i)

        if len(step_width_list) < len(step_height_list):
            for i in range(len(step_height_list)):
                if i < len(step_width_list):
                    step_list.append([step_width_list[i], step_height_list[i]])
                else:
                    step_list.append([pos2[0], step_height_list[i]])
        else:
            for i in range(len(step_width_list)):
                if i < len(step_height_list):
                    step_list.append([step_width_list[i], step_height_list[i]])
                else:
                    step_list.append([step_width_list[i], pos2[1]])
        for pos in step_list:
            win32gui.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(pos[0], pos[1]))
            time.sleep(0.01)
