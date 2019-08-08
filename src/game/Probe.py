# coding=utf-8
from time import sleep, time

from src.game.GameBase import BaseOperator
from src.game.config import config
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
        logger.info("检查队友")
        start_time = time()
        while time() - start_time <= max_time:
            sleep(1)
            pos = self.screenshot_mutlfind(img_path)
            if len(pos) < 2:
                return pos
            logger.info("等待队友中...")
        return None

    def begin_battle(self):
        probe_count = config.getint("game", "probeCount")
        while probe_count == 0 or self.count < probe_count:
            if self.wait_img(u"resource/img/yuhunTeam.png", 60) is not None:
                if self.wait_teammate(u"resource/img/invite.png", 60) is not None:
                    sleep(0.5)
                    logger.info("点击开始战斗")
                    self.click_img(u"resource/img/battleBegin.png")
                    self.count = self.count + 1
                    logger.info("第" + str(self.count) + "次御魂")
                    self.battle()
                else:
                    logger.error("等待队友失败")
            else:
                logger.error("进入组队页面失败")
