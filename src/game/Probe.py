# coding=utf-8
import logging
from time import sleep, time

from src.game.GameBase import BaseOperator
from src.util.log import logger


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
            sleep(1)

    def wait_teammate(self, img_path, max_time=30 * 1000):
        """
        等待游戏图像并点击
            :param max_time:
            :param self:
            :param img_path:
            :return: 成功返回图片位置[left_top,right_bottom]，失败返回None
        """
        start_time = time()
        while time() - start_time <= max_time:
            sleep(1)
            pos = self.screenshot_mutlfind(img_path)
            if len(pos) < 2:
                return pos
            logger.info("等待队友中...")
        return None

    def battle(self):
        logger.info("开始战斗")
        while self.wait_img(u"resource/img/yuhunTeam.png", 60) is not None:
            # _thread.start_new_thread(self.range_move, ())
            self.wait_teammate(u"resource/img/invite.png")
            sleep(0.5)
            self.click_img(u"resource/img/battleBegin.png")
            self.count = self.count + 1
            if self.wait_img(u"resource/img/battleLeftTop.png") is not None:
                self.wait_img_click(u"resource/img/btn_ready.png")
            else:
                logging.error("开始战斗失败")
            sleep(0.5)
            self.wait_img_click(u"resource/img/win.png", 120)
            sleep(0.5)
            self.wait_img_click(u"resource/img/battleDawta.png", 120)
            for i in range(3):
                sleep(1)
                window_size = self.window_size()
                self.click_range((50, 50), (int(window_size[0] / 5), window_size[1] - 50))
            if self.wait_img(u"resource/img/inviteDefatlt.png", 5) is not None:
                logging.info("需要点击默认邀请")
                sleep(0.5)
                self.click_img(u"resource/img/check.png", True)
                sleep(0.5)
                self.click_img(u"resource/img/okButton.png", True)
