from src.image.ImageSearch import *
from src.window.WndowController import Window

if __name__ == '__main__':
    windowTitle = "阴阳师-网易游戏"
    window = Window(windowTitle)
    screenshot_bytes, _width, _height = window.hwd_screenshot()
    _img_opencv = get_img_opencv(screenshot_bytes, _width, _height)
    left_top, right_bottom = best_match(_img_opencv, read_img(u"resource/img/tansuo.png", 0), 0.7, True)
    print(left_top, right_bottom)
    window.clickRange(left_top, right_bottom)
