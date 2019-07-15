from src.image.ImageSearch import *
from src.window.WndowController import Window

if __name__ == '__main__':
    default_window_width = 1152
    default_window_height = 679
    windowTitle = "阴阳师-网易游戏"
    window = Window(windowTitle)
    screenshot_bytes, screenshot_width, screenshot_height = window.hwd_screenshot()
    _img_opencv = get_img_opencv(screenshot_bytes, screenshot_width, screenshot_height)
    _img_tansuo_button = read_img(u"resource/img/tansuo.png", 0)
    zoom = screenshot_width / default_window_width  # 计算缩放比例
    if zoom != 1:
        height, width = _img_tansuo_button.shape[:2]
        _img_tansuo_button = cv2.resize(_img_tansuo_button, (int(width * zoom), int(height * zoom)),
                                        interpolation=cv2.INTER_CUBIC)
    left_top, right_bottom = best_match(_img_opencv, _img_tansuo_button, 0.6, True)
    if left_top is not None:
        print(left_top, right_bottom)
        window.clickRange(left_top, right_bottom)

    # result, _, _ = siftImageAlignment(_img_opencv, _img_tansuo_button)
    # allImg = np.concatenate((_img_opencv, _img_tansuo_button, result), axis=1)
    # cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
    # cv2.imshow('Result', allImg)
    # cv2.waitKey(0)
