from src.game.GameBase import BaseOperator
from src.util.log import logger


class Enchantment(BaseOperator):
    def __init__(self, window):
        super().__init__(window)
        self.captain = False
        self.window = window
        self.count = 0

    def begin_battle(self):
        while True:
            pos = self.wait_img(u"resource/img/enchantment/enchantment.png")
            hut = self.screenshot_find("resource/img/enchantment/hutEnchantment.png")
            if hut is not None:
                logger.info("阴阳寮突破")
                if self.screenshot_find("resource/img/enchantment/battleNumZero.png") is None:
                    logger.info("阴阳寮没有战斗次数")
                    raise Exception("没有次数")
            print(pos)
            pos = self.wait_img_click(u"resource/img/enchantment/person.png")
            print(pos)
            pos = self.wait_img_click(u"resource/img/enchantment/attack.png", True)
            print(pos)
            self.battle(0, False)
