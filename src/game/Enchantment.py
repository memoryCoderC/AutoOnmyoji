import time

from src.game.GameBase import BaseOperator
from src.util.log import logger

hutRecoverTime = 3 * 60 * 5
selfRecoverTime = 5 * 60


class Enchantment(BaseOperator):
    def __init__(self, window):
        super().__init__(window)
        self.captain = False
        self.window = window
        self.count = 0

    def re_in(self):
        """
        重新进入来刷新阴阳寮的战斗状态
        :return:
        """
        logger.info("刷新阴阳寮状态")
        self.wait_img(u"resource/img/enchantment/enchantment.png")
        self.click_img(u"resource/img/enchantment/exit.png")
        time.sleep(1)
        self.wait_img_click(u"resource/img/enchantment/enchantmentIcon.png", center=True)
        time.sleep(1)
        self.wait_img_click(u"resource/img/enchantment/hutButton.png", center=True)

    def begin_battle(self):
        while True:
            self.wait_img(u"resource/img/enchantment/enchantment.png")
            logger.info("进入突破页面")
            personal = self.check_personal()
            if self.check_canbattle_num(personal):
                if not personal:
                    logger.info("等待突破次数恢复")
                    time.sleep(hutRecoverTime)
                    logger.info("突破次数恢复继续战斗")
                    self.re_in()
                else:
                    logger.info("退出挑战")
                    return
            else:
                time.sleep(0.5)
                pos = self.wait_imgs([u"resource/img/enchantment/person.png", u"resource/img/enchantment/person1.png"],
                                     max_time=5)
                if pos[0] is not 0:
                    logger.info("开始第一次战斗尝试")
                    self.click(pos[0])
                    time.sleep(0.5)
                    pos = self.wait_img_click(u"resource/img/enchantment/attack.png", center=True)
                    time.time()
                    print(pos)
                    self.battle(0, False)
                elif pos[1] is not 0:
                    logger.info("开始第一次战斗尝试")
                    self.click(pos[1])
                    time.sleep(0.5)
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
            # pos = self.wait_img_click(u"resource/img/enchantment/person.png", max_time=5)
            # if pos is not None:
            #     logger.info("开始第一次战斗尝试")
            #     time.sleep(0.5)
            #     pos = self.wait_img_click(u"resource/img/enchantment/attack.png", center=True)
            #     time.time()
            #     print(pos)
            #     self.battle(0, False)
            # else:
            #     logger.info("不存在未攻击的结界")
            #     if self.refresh(personal):
            #         logger.info("找到战斗目标继续战斗")
            #     else:
            #         logger.info("已经全部攻击过")
            #         return

    def check_canbattle_num(self, personal):
        if personal:
            if self.screenshot_find("resource/img/enchantment/personZero.png") is not None:
                logger.info("个人没有结界挑战卷")
                return True
        else:
            if self.screenshot_find("resource/img/enchantment/battleNumZero.png") is not None:
                logger.info("阴阳寮没有战斗次数")
                return True
        return False

    def check_personal(self):
        """
        检查是个人突破还是阴阳寮突破
        :return:个人：True，阴阳寮：False
                否则抛出异常
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
        刷新突破界面寻找新的
        :param enchantment_personal: 是否是个人突破
        :return:
        """
        if enchantment_personal:
            return self.refresh_personal()
        else:
            return self.refresh_hut()

    def refresh_personal(self):
        """
        刷新个人突破
        :return:
        """
        logger.info("个人突破刷新")
        pos = self.click_img(u"resource/img/enchantment/refreshButton.png")
        if pos is None:
            return False
        else:
            self.wait_img_click(u"resource/img/enchantment/refreshPersonal.png")
            time.sleep(0.2)
            self.click_img(u"resource/img/okButton.png")
            return True

    def refresh_hut(self):
        """
        阴阳寮突破向下滑动
        :return:
        """
        logger.info("阴阳寮突破下滑")
        fail_list = self.screenshot_mutlfind(u"resource/img/enchantment/enchantmentFail.png")
        attacked = self.screenshot_mutlfind(u"resource/img/enchantment/attacked.png")
        list = fail_list + attacked
        fail_size = len(list)
        if fail_size == 0:
            logger.info("不存在攻击失败的结界")
        else:
            logger.info("寮突破向下移动")
            x = int((list[0][0][0] + list[0][1][0]) / 2)
            y = int((list[0][0][1] + list[0][1][1]) / 2)
            while True:
                self.window.mouse_drag_distance((x, y), (0, -10))
                sense = self.find_imgs(
                    [u"resource/img/enchantment/person.png", u"resource/img/enchantment/slideEnd.png",
                     u"resource/img/enchantment/hutEnchantment.png"])
                if sense is not None:
                    if sense[0] == 0:
                        logger.info("找到了可攻击目标")
                        return True
                    elif sense[0] == 1:
                        logger.info("滑动到了底部")
                        return False
                    time.sleep(0.3)
                else:
                    raise Exception("非寮突破界面")
