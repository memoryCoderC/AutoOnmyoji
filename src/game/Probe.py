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
            teammates_number = config.getint("game", "teammatesNum")
            in_team = False
            start_time = time()
            while time() - start_time <= 60:
                sleep(0.1)
                logger.info("等待接受邀请，进入队伍")
                pos = self.check_sense([u"resource/img/yuhunTeam.png", u"resource/img/inviteTeam.png"])
                if pos is not None:
                    if pos[0] == 0:
                        logger.info("进入组队页面")
                        in_team = True
                        if teammates_number > 0:
                            if self.wait_teammate(u"resource/img/invite.png", teammates_number, 60) is not None:
                                logger.info("队友已就位")
                            else:
                                logger.error("等待队友失败")
                        sleep(0.5)
                        if self.screenshot_find(u"resource/img/battleBegin.png") is not None:
                            logger.info("身为队长,点击开始战斗")
                            self.captain = True
                            sleep(0.5)
                            self.click_img(u"resource/img/battleBegin.png")
                        self.count = self.count + 1
                        logger.info("第" + str(self.count) + "次御魂")
                        self.battle(teammates_number, self.captain)
                        break
                    elif pos[0] == 1:
                        logger.info("接受组队邀请")
                        self.click_img(u"resource/img/accept.png")
                        sleep(0.5)
            if not in_team:
                raise Exception("进入组队页面失败")
