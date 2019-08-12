from src.game.GameBase import BaseOperator
from src.util.log import logger


class Enchantment(BaseOperator):
    def __init__(self, window):
        super().__init__(window)
        self.captain = False
        self.window = window
        self.count = 0

    def begin_battle(self):
        enchantmentSelf = True
        while True:
            self.wait_img(u"resource/img/enchantment/enchantment.png")
            logger.info("进入突破页面")
            hut = self.find_imgs(
                [u"resource/img/enchantment/hutEnchantment.png", u"resource/img/enchantment/defendRecond.png"])
            if hut is not None:
                logger.info("阴阳寮突破")
                if hut[0] == 0:
                    if self.screenshot_find("resource/img/enchantment/battleNumZero.png") is not None:
                        logger.info("阴阳寮没有战斗次数")
                        raise Exception("没有次数")
                elif hut[0] == 1:
                    logger.info("个人突破")
            else:
                raise Exception("非结界界面")
            pos = self.click_img(u"resource/img/enchantment/person.png")
            if pos is not None:
                logger.info("开始第一次战斗尝试")
                pos = self.wait_img_click(u"resource/img/enchantment/attack.png", True)
                print(pos)
                self.battle(0, False)
            else:
                logger.info("不存在未攻击的结界")
                failList = self.screenshot_mutlfind(u"resource/img/enchantment/enchantmentFail.png")
                failSize = len(failList)
                if failSize == 0:
                    logger.info("不存在战斗失败")
                else:
                    logger.info("需要战斗失败重试人数" + str(failSize))
