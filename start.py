import random

from src.game.Probe import Probe
from src.system.Window import Window
from src.util import permissionUtil

if __name__ == '__main__':
    print("run")
    permissionUtil.check_get_permission()
    default_window_width = 1152
    default_window_height = 679
    windowTitle = "阴阳师-网易游戏"
    window = Window(windowTitle)
    print(window.get_window_rect())
    probe = Probe(window)
    probe.battle()

    # _img_opencv = get_img_opencv(screenshot_bytes, screenshot_width, screenshot_height)
    # _img_tansuo_button = read_img(u"resource/img/tansuo.png", 0)
    # zoom = screenshot_width / default_window_width  # 计算缩放比例
    # if zoom != 1:
    #     height, width = _img_tansuo_button.shape[:2]
    #     _img_tansuo_button = cv2.resize(_img_tansuo_button, (int(width * zoom), int(height * zoom)),
    #                                     interpolation=cv2.INTER_CUBIC)
    # pos = best_match(_img_opencv, _img_tansuo_button, 0.6, True)
    # if pos is not None:
    #     print(pos[0], pos[1])
    #     window.click_range(pos[0], pos[1])

    # result, _, _ = siftImageAlignment(_img_opencv, _img_tansuo_button)
    # allImg = np.concatenate((_img_opencv, _img_tansuo_button, result), axis=1)
    # cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
    # cv2.imshow('Result', allImg)
    # cv2.waitKey(0)
