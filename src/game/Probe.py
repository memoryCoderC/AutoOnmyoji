# coding=utf-8
import _thread
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

    def click_ready(self):
        """
        检测并点击开始按钮
        :return:
        """
        max_time = 30
        start_time = time()
        while time() - start_time <= max_time:
            sleep(1)
            pos = self.check_sense([u"resource/img/needBegin.png", u"resource/img/auto.png"])
            if pos is not None:
                if pos[0] == 0:
                    logger.info("点击ready按钮")
                    self.wait_img_click(u"resource/img/btn_ready.png")
                else:
                    logger.info("战斗已经开始")
                    return

    def win_deal(self):
        self.wait_img_click(u"resource/img/win.png", 240)
        sleep(0.5)
        self.wait_img_click(u"resource/img/battleData.png", 240)
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

    def fail_deal(self):
        self.click_img(u"resource/img/fail.png")
        sleep(0.5)
        self.wait_img_click(u"resource/img/battleData.png", 240)
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

    def battle(self):
        logger.info("开始战斗" + str(self.count))
        while self.wait_img(u"resource/img/yuhunTeam.png", 60) is not None:
            self.wait_teammate(u"resource/img/invite.png")
            sleep(0.5)
            self.click_img(u"resource/img/battleBegin.png")
            if self.wait_img(u"resource/img/battleLeftTop.png") is not None:
                """
                进入了战斗画面
                """
                _thread.start_new_thread(self.click_ready, ())
            else:
                raise Exception("开始战斗失败")
            self.count = self.count + 1
            sleep(0.5)
            pos = self.wait_senses([u"resource/img/win.png", u"resource/img/fail.png"], 240)
            if pos is not None:
                if pos[0] == 0:
                    logger.info("战斗胜利")
                    self.win_deal()
                elif pos[0] == 1:
                    logger.info("战斗失败")
                    self.fail_deal()
