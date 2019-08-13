import time

from src.game import Config
from src.game.GameBase import BaseOperator
from src.util.log import logger

hutRecoverTime = 5 * 60 * 5
selfRecoverTime = 5 * 60


class Enchantment(BaseOperator):
    def __init__(self, window):
        super().__init__(window)
        self.captain = False
        self.window = window
        self.count = 0

    def begin_battle(self):
        while True:
            if not Config.isRun:
                logger.info("手动退出")
                break
            self.wait_img(u"resource/img/enchantment/enchantment.png")
            logger.info("进入突破页面")
            personal = self.check_personal()
            if not personal:
                if self.screenshot_find("resource/img/enchantment/battleNumZero.png") is not None:
                    logger.info("阴阳寮没有战斗次数")
            pos = self.wait_img_click(u"resource/img/enchantment/person.png", max_time=5)
            if pos is not None:
                logger.info("开始第一次战斗尝试")
                pos = self.wait_img_click(u"resource/img/enchantment/attack.png", center=True)
                time.time()
                print(pos)
                self.battle(0, False)
            else:
                logger.info("不存在未攻击的结界")
                if self.refresh(personal):
                    logger.info("找到战斗目标继续战斗")
                else:
                    logger.info("已经全部攻击过")
                    return

    def check_personal(self):
        """
        检查是是个人突破还是阴阳寮突破
        :return:
        """
        hut = self.find_imgs(
            [u"resource/img/enchantment/hutEnchantment.png", u"resource/img/enchantment/defendRecond.png"])
        if hut is not None:
            if hut[0] == 0:
                logger.info("阴阳寮突破")
                return False
            elif hut[0] == 1:
                logger.info("个人突破")
                return True
        else:
            raise Exception("非结界界面")

    def refresh(self, enchantment_personal):
        """
        个人突破和
        :param enchantment_personal: 是否是个人突破
        :return:
        """
        if enchantment_personal:
            logger.info("个人突破刷新")
            pos = self.click_img(u"resource/img/enchantment/refreshButton.png")
            if pos is None:
                return False
            else:
                return True
        else:
            failList = self.screenshot_mutlfind(u"resource/img/enchantment/enchantmentFail.png")
            failSize = len(failList)
            if failSize == 0:
                logger.info("不存在攻击失败的结界")
            elif failSize == 8:
                logger.info("寮突破向下移动")
                x = int((failList[0][0][0] + failList[0][1][0]) / 2)
                y = int((failList[0][0][1] + failList[0][1][1]) / 2)
                _width, _height = self.window_size()
                while True:
                    self.window.mouse_drag_distance((x, y), (0, -10))
                    sense = self.find_imgs(
                        [u"resource/img/enchantment/person.png", u"resource/img/enchantment/slideEnd.png"])
                    if sense is not None:
                        if sense[0] == 0:
                            logger.info("找到了可攻击目标")
                            return True
                        elif sense[1] == 1:
                            logger.info("滑动到了底部")
                            return False
