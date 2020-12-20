# coding=utf-8
from time import sleep, time

from src.game.Config import config
from src.game.GameBase import BaseOperator
from src.util.log import logger


class Four(BaseOperator):
    """
    御魂战斗
    """

    def __init__(self, window):
        super().__init__(window)
        self.captain = False
        self.window = window
        self.count = 0

    def range_move(self):
        pos1 = [0, 0]
        while True:
            pos2 = self.random_pos()
            self.window.mouse_move(pos1, pos2)
            pos1 = pos2
            sleep(1)

    def begin_battle(self):
        probe_count = config.getint("game", "probeCount")
        while probe_count == 0 or self.count < probe_count:
            sleep(0.5)
            self.battle_self()


    def battle_self(self):
        pos = self.wait_img(u"resource/img/four/elcx.png")
        if pos is not None:
            logger.info("进入御魂页面")
            pos = self.click_img(u"resource/img/four/challenge.png", True)
            if pos is not None:
                logger.info("开始单人战斗")
                self.count = self.count + 1
                logger.info("第" + str(self.count) + "次御魂")
                self.battle(0, False)
