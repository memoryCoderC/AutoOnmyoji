# coding=utf-8
import abc
from random import randint
from time import time, sleep

from PIL.Image import fromarray

from src.game.Config import config
from src.image import Image
from src.image.ImageSearch import best_match, mutl_match
from src.system.Window import Window
from src.util.log import logger

default_window_width = 1152
default_window_height = 679


class BaseOperator(Window):
    """
    游戏基本操作方式
    """

    def __init__(self, window):
        super().__init__(window)
        self.window = window

    def find_imgs(self, template_img_paths):
        """
        检查当前场景是否存在其中一个图片
        :param template_img_paths:要查找的图片位置
        :return: 成功返回True，失败返回False
        """
        screenshot = self.screenshot()
        screenshot_height, screenshot_width = screenshot.shape[:2]
        zoom = screenshot_width / default_window_width  # 计算缩放比例
        for i in range(0, len(template_img_paths)):
            template_img = Image.read_img(template_img_paths[i], 0)
            pos = self.find_img_zoom(template_img, screenshot, zoom)
            if pos is not None:
                return [i, pos, template_img_paths[i]]
        return None

    def click_img(self, template_img_path, center=False):
        """
        点击图片
        :param center:
        :param template_img_path:要点击的图片
        :return:
        """
        pos = self.screenshot_find(template_img_path)
        if pos is not None:
            self.click(pos, center)
            return pos
        else:
            logger.debug("点击图片失败，未找到图片" + template_img_path)

    def find_img_zoom(self, template_img, target_img, zoom):
        """
        缩放查找图片
        :param template_img: 要查找的图片
        :param target_img: 需要查找的目标图片
        :param zoom: 缩放
        :return: 成功返回图片位置[x,y]，失败返回None
        """
        template_img = Image.resize_by_zoom(zoom, template_img)
        threshold = config.getfloat("game", "imageSearchThreshold")
        debug = config.getboolean("game", "debug")
        return best_match(target_img, template_img, threshold, debug)

    def find_imgs_zoom(self, template_img_paths):
        """
        检查当前场景是否存在全部图片
        :param template_img_paths:要查找的图片位置
        :return: 成功返回True，失败返回False
        """
        list = []
        screenshot = self.screenshot()
        screenshot_height, screenshot_width = screenshot.shape[:2]
        zoom = screenshot_width / default_window_width  # 计算缩放比例
        for i in range(0, len(template_img_paths)):
            template_img = Image.read_img(template_img_paths[i], 0)
            pos = self.find_img_zoom(template_img, screenshot, zoom)
            if pos is None:
                return None
            else:
                list.append([i, pos, template_img_paths[i]])
        return list

    def search_mutlimg_zoom(self, template_img, target_img, zoom):

        """
        缩放查找图片
        :param template_img: 要查找的图片
        :param target_img: 需要查找的目标图片
        :param zoom: 缩放
        :return: 成功返回图片位置的列表[x,y]，失败返回空列表
        """
        template_img = Image.resize_by_zoom(zoom, template_img)
        threshold = config.getfloat("game", "imageSearchThreshold")
        return mutl_match(target_img, template_img, threshold)

    def wait_imgs(self, sense_paths, max_time=30):
        """
        等待多个图片其中一个存在，返回检测到的数组下标
        :return:
        """
        logger.debug("等待游戏场景")
        start_time = time()
        while time() - start_time <= max_time:
            sleep(0.1)
            pos = self.find_imgs(sense_paths)
            if pos is not None:
                return pos
        return None

    def wait_img(self, img_path, max_time=30):
        """
        等待游戏图像
            :param max_time:
            :param self:
            :param img_path:
            :return: 成功返回图片位置[left_top,right_bottom]，失败返回None
        """
        logger.debug("等待游戏图像")
        start_time = time()
        while time() - start_time <= max_time:
            sleep(0.1)
            pos = self.screenshot_find(img_path)
            if pos is not None:
                return pos
        logger.debug("等待图像失败" + img_path)
        return None

    def wait_img_click(self, img_path, center=False, max_time=30):
        """
        等待游戏图像并点击
            :param center:
            :param max_time:
            :param self:
            :param img_path:
            :return: 成功返回图片位置[left_top,right_bottom]，失败返回None
        """
        pos = self.wait_img(img_path, max_time)
        if pos is not None:
            self.click(pos, center)
            return pos
        return None

    def click(self, pos, center=False):
        pos[0] = (pos[0][0] - 8, pos[0][1] - 35)
        pos[1] = (pos[1][0] - 8, pos[1][1] - 35)
        if center:
            x = int((pos[1][0] + pos[0][0]) / 2)
            y = int((pos[1][1] + pos[0][1]) / 2)
            self.window.click(x, y)
        else:
            self.window.click_range(pos[0], pos[1])

    def click_range(self, left_top, right_bottom):
        """
        在范围内随机点击
        :param left_top:
        :param right_bottom:
        :return:
        """
        self.window.click_range(left_top, right_bottom)

    def screenshot_find(self, template_img_path):
        """
        截取游戏画面并查找图片位置
        :param template_img_path: 差早图片位置
        :return: 成功返回图片位置[left_top,right_bottom]，失败返回None
        """
        screenshot = self.window.hwd_screenshot()
        screenshot_height, screenshot_width = screenshot.shape[:2]
        template_img = Image.read_img(template_img_path, 0)
        zoom = screenshot_width / default_window_width  # 计算缩放比例
        return self.find_img_zoom(template_img, screenshot, zoom)

    def screenshot_mutlfind(self, template_img_path):
        """
        截取游戏画面并查找图片位置
        :param template_img_path: 差早图片位置
        :return: 成功返回图片位置[left_top,right_bottom]，失败返回None
        """
        screenshot = self.window.hwd_screenshot()
        screenshot_height, screenshot_width = screenshot.shape[:2]
        template_img = Image.read_img(template_img_path, 0)
        zoom = screenshot_width / default_window_width  # 计算缩放比例
        return self.search_mutlimg_zoom(template_img, screenshot, zoom)

    def screenshot(self):
        """
        截取游戏画面
        :return:
        """
        return self.window.hwd_screenshot()

    def random_pos(self):
        _width, _height = self.window_size()
        x = randint(10, _width)
        y = randint(10, _height)
        return [x, y]

    def window_size(self):
        """
        获取游戏窗口大小
        :return:
        """
        _left, _top, _right, _bot = self.window.get_window_rect()
        _width = _right - _left
        _height = _bot - _top
        return [_width, _height]

    def find_color(self, region, color, tolerance=0):
        """
        寻找颜色
            :param tolerance: 容差值
            :param region: ((x1,y1),(x2,y2)) 欲搜索区域的左上角坐标和右下角坐标
            :param color: (r,g,b) 欲搜索的颜色
            :return: 成功返回客户区坐标，失败返回None
        """
        screenshot = self.window.hwd_screenshot()
        height, width = screenshot.shape[:2]
        img = fromarray(screenshot, 'RGB')
        r1, g1, b1 = color[:3]
        for x in range(width):
            for y in range(height):
                pixel = img.getpixel((x, y))
                r2, g2, b2 = pixel[:3]
                if abs(r1 - r2) <= tolerance and abs(g1 - g2) <= tolerance and abs(b1 - b2) <= tolerance:
                    return x + region[0][0], y + region[0][1]
        return None

    def wait_game_color(self, region, color, tolerance=0, max_time=30):
        """
        等待游戏颜色
            :param max_time:最大时间
            :param tolerance:容差值
            :param region: ((x1,y1),(x2,y2)) 欲搜索的区域
            :param color: (r,g,b) 欲等待的颜色
            :return: 成功返回True，失败返回False
        """
        start_time = time()
        while time() - start_time <= max_time:
            pos = self.find_color(region, color, tolerance)
            if pos is not None:
                return True
            sleep(1)
        else:
            return False

    def check_color(self, pos, color, tolerance=0):
        """
        对比窗口内某一点的颜色
            :param tolerance:
            :param pos: (x,y) 欲对比的坐标
            :param color: (r,g,b) 欲对比的颜色
            :return: 成功返回True,失败返回False
        """
        _img_opencv = self.window.hwd_screenshot()
        r1, g1, b1 = color[:3]
        r2, g2, b2 = _img_opencv.getpixel(pos)[:3]
        if abs(r1 - r2) <= tolerance and abs(g1 - g2) <= tolerance and abs(b1 - b2) <= tolerance:
            return True
        else:
            return False

    def battle(self, teammates_number, captain=False):
        """
        战斗模块
        :return:
        """
        isWin = False
        logger.info("等待战斗开始")
        if self.wait_img(u"resource/img/battleLeftTop.png", 120) is not None:
            logger.info("进入战斗场景")
            """
            进入了战斗画面
            """
            self.click_ready()
        else:
            raise Exception("进入战斗场景失败")
        logger.info("等待战斗结束")
        count = 0
        while True:
            sleep(0.2)
            pos = self.wait_imgs([u"resource/img/win.png", u"resource/img/fail.png", u"resource/img/guihuo.png"], 10)
            if pos is not None:
                count = 0
                if pos[0] == 0:
                    logger.info("战斗胜利")
                    isWin = True
                    self.win_deal(teammates_number, captain)
                    break
                elif pos[0] == 1:
                    logger.info("战斗失败")
                    self.fail_deal(teammates_number, captain)
                    break
                elif pos[0] == 2:
                    logger.debug("战斗中...")
            else:
                count = count + 1
                if count > 5:
                    raise Exception("未知战斗场景")
        return isWin

    def check_auto_battle(self):
        auto_sense = self.find_imgs([u"resource/img/auto.png", u"resource/img/manual.png"])
        if auto_sense[0] == 0:
            logger.debug("已经自动战斗")
        elif auto_sense[0] == 1:
            logger.debug("开启自动战斗")
            self.wait_img_click(u"resource/img/manual.png", 1)

    def click_ready(self):
        """
        检测并点击开始按钮
        :return:
        """
        max_time = 120
        start_time = time()
        while time() - start_time <= max_time:
            sleep(0.1)
            pos = self.find_imgs([u"resource/img/needBegin.png", u"resource/img/guihuo.png"])
            if pos is not None:
                if pos[0] == 0:
                    ready_sense = self.find_imgs([u"resource/img/btn_ready.png", u"resource/img/readyed.png"])
                    if ready_sense is not None:
                        if ready_sense[0] == 0:
                            logger.info("点击ready按钮")
                            self.click_img(u"resource/img/btn_ready.png")
                        elif ready_sense[0] == 1:
                            logger.info("等待队友准备")
                elif pos[0] == 1:
                    logger.info("战斗已经开始")
                    sleep(0.5)
                    self.check_auto_battle()
                    return

    def win_deal(self, teammates_number, captain):
        """
        战斗成功处理
        :return:
        """
        while self.wait_img_click(u"resource/img/clickToContinue.png", max_time=2) is not None:
            logger.info("结算后点击")
            sleep(0.2)
        if teammates_number > 0:
            if captain and self.wait_img(u"resource/img/inviteDefatlt.png", max_time=3) is not None:
                logger.info("需要点击默认邀请")
                sleep(0.5)
                if config.getboolean("game", "inviteDefaultMode"):
                    logger.info("默认邀请队友")
                    self.click_img(u"resource/img/check.png", True)
                sleep(0.5)
                logger.info("邀请队友")
                self.click_img(u"resource/img/okButton.png", True)

    def fail_deal(self, teammates_number, captain):
        """
        战斗失败处理
        :return:
        """
        self.click_img(u"resource/img/fail.png")
        if teammates_number > 0 and captain:
            sleep(1)
            if self.screenshot_find(u"resource/img/battleData.png") is not None:
                logger.info("等待邀请画面")
                if self.wait_img(u"resource/img/inviteDefatlt.png", 5) is not None:
                    logger.info("需要点击默认邀请")
                    sleep(0.5)
                    self.click_img(u"resource/img/okButton.png", True)

    def wait_teammate(self, img_path, teammates_number, max_time=30 * 1000):
        """
        等待游戏图像并点击
            :param teammates_number:
            :param max_time:
            :param self:
            :param img_path:
            :return: 成功返回图片位置[left_top,right_bottom]，失败返回None
        """
        if teammates_number > 0:
            logger.info("检查队友")
            start_time = time()
            while time() - start_time <= max_time:
                sleep(1)
                pos = self.screenshot_mutlfind(img_path)
                if len(pos) <= 2 - teammates_number:
                    logger.info("队友已就位")
                    return True
                logger.info("等待队友中...")
            logger.error("等待队友失败")
            raise Exception("等待队友失败")
        else:
            return True

    @abc.abstractmethod
    def begin_battle(self):
        pass

    def on_begin_battle(self, end_method):
        try:
            self.begin_battle()
        except Exception as e:
            logger.exception(e)
        finally:
            logger.info("战斗结束")
            end_method()
