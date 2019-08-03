import time

from src.game.GameBase import BaseOperator
from src.image import Image, ImageSearch


class Probe(BaseOperator):
    """
    御魂战斗
    """

    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.count = 0

    def range_move(self):
        pos1 = [0, 0]
        while True:
            pos2 = self.random_pos()
            self.window.mouse_move(pos1, pos2)
            pos1 = pos2
            time.sleep(1)

    def wait_teammate(self, img_path, max_time=30 * 1000):
        """
      等待游戏图像并点击
          :param max_time:
          :param self:
          :param img_path:
          :return: 成功返回图片位置[left_top,right_bottom]，失败返回None
      """
        start_time = time.time()
        while time.time() - start_time <= max_time:
            time.sleep(1)
            pos = self.screenshot_mutlfind(img_path)
            if len(pos) < 2:
                return pos
            print("等待队友中")
        return None

    def battle(self):
        while self.wait_img(u"resource/img/yuhunTeam.png", 60) is not None:
            # _thread.start_new_thread(self.range_move, ())
            self.wait_teammate(u"resource/img/invite.png")
            time.sleep(0.5)
            self.click_img(u"resource/img/battleBegin.png")
            print("战斗开始")
            self.count = self.count + 1
            # if self.wait_img(u"resource/img/battleLeftTop.png") is not None:
            #    self.wait_img_click(u"resource/img/btn_ready.png")
            time.sleep(0.5)
            self.wait_img_click(u"resource/img/win.png", 120)
            time.sleep(0.5)
            self.wait_img_click(u"resource/img/battleDawta.png", 120)
            for i in range(3):
                time.sleep(1)
                window_size = self.window_size()
                self.click_range((50, 50), (int(window_size[0] / 5), window_size[1] - 50))
                print("点击一次")
            if self.wait_img(u"resource/img/inviteDefatlt.png", 5) is not None:
                print("需要点击默认邀请")
                time.sleep(0.5)
                self.click_img(u"resource/img/check.png", True)
                time.sleep(0.5)
                self.click_img(u"resource/img/okButton.png", True)
