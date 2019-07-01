import y_functions as yf
import cv2
from settings import Settings

"""这个文件作用是将y_function中的函数集成为几个模块，
防止主程序中出现太多循环"""


# 准备模块
# 导入模板，设置刷御魂次数模块
def begin():
    t_start = cv2.imread('D:\python_code\yys\yys1.1\img\start.png', 0)
    t_end = cv2.imread('D:\python_code\yys\yys1.1\img\end.png', 0)
    n = input("请输入刷御魂次数：")
    n = int(n)
    return t_start, t_end, n


# 匹配模块
# 检测模板，点击屏幕
def matchT(t, x, y):
    sd = 0
    while sd < 15:
        img1 = yf.get_screen()
        res = yf.match(img1, t)
        if res > 0.97:
            break
        else:
            yf.get_randtime(0.8, 1.3)
        sd += 1
    sx, sy = yf.get_randxy(x, y)
    yf.get_randtime(0.5, 1)
    yf.click(sx, sy)
    print('匹配成功，共匹配{}次'.format(sd + 1))
    yf.get_randtime(4, 5)


# 跳过动画模块
# 开始战斗后等待一段时间后点击三下跳过动画
def endclick(y_settings):
    print('等待战斗中......')
    yf.get_randtime(27, 29)
    for i in range(1, 4):
        # 点击
        ex, ey = yf.get_randxy(y_settings.end_x, y_settings.end_y)
        yf.click(ex, ey)
        # 等待
        yf.get_randtime(0.8, 1.5)
