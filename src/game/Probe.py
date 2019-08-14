# coding=utf-8
from time import sleep, time

from src.game.Config import config
from src.game.GameBase import BaseOperator
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
            sleep(0.5)
            teammates_number = config.getint("game", "teammatesNum")
            if teammates_number > 0:
                self.battle_team(teammates_number)
            else:
                self.battle_self()

    def battle_team(self, teammates_number):
        in_team = False
        start_time = time()
        while time() - start_time <= 60:
            sleep(0.1)
            logger.info("等待接受邀请，进入队伍")
            pos = self.find_imgs([u"resource/img/yuhunTeam.png", u"resource/img/inviteTeam.png"])
            if pos is not None:
                if pos[0] == 0:
                    logger.info("进入组队页面")
                    in_team = True
                    self.wait_teammate(u"resource/img/invite.png", teammates_number, 60)
                    sleep(0.5)
                    self.captain = self.check_captain_click()
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

    def check_captain_click(self):
        pos = self.screenshot_find(u"resource/img/battleBeginButton.png")
        if pos is not None:
            logger.info("身为队长,点击开始战斗")
            self.click(u"resource/img/battleBeginButton.png")
            return True
        return False

    def battle_self(self):
        pos = self.wait_img(u"resource/img/yuhunSense.png")
        if pos is not None:
            logger.info("进入御魂页面")
            pos = self.click_img(u"resource/img/challenge.png", True)
            if pos is not None:
                logger.info("开始单人战斗")
                self.battle(0, False)
