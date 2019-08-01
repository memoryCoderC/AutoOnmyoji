import random
import time
import _thread

from src.game.GameBase import BaseOperator


class Probe(BaseOperator):
    """
    御魂战斗
    """

    def __init__(self, window):
        super().__init__(window)
        self.window = window

    def range_move(self):
        pos1 = [0, 0]
        while True:
            pos2 = self.random_pos()
            self.window.mouse_move(pos1, pos2)
            pos1 = pos2

    def battle(self):
        if self.check_sense(u"resource/img/yuhunTeam.png"):
            _thread.start_new_thread(self.range_move, ())
            # ready_btn_pos = self.screenshot_find(u"resource/img/battelBegin.png")
            # print(ready_btn_pos)
            # print(self.wait_game_color(ready_btn_pos, TansuoColor.ready_btn.color, TansuoColor.ready_btn.tolerance))
            # time.sleep(100)
            time.sleep(0.5)
            self.wait_img_click(u"resource/img/battelBegin.png")
            # self.wait_img_click(u"resource/img/btn_ready.png")
            self.wait_img_click(u"resource/img/win.png", 180 * 1000)
            self.wait_img_click(u"resource/img/battleData.png", 180 * 1000)
            for i in range(3):
                time.sleep(1)
                window_size = self.window_size()
                self.click_range((50, 50), (int(window_size[0] / 5), window_size[1] - 50))
                print("点击一次")
