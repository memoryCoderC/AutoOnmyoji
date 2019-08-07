# coding=utf-8
from src.game import config
from src.game.Probe import Probe
from src.system.Window import Window
from src.util import permissionUtil

from src.util.log import logger

if __name__ == '__main__':
    try:
        logger.info("开始运行")
        permissionUtil.check_get_permission()
        logger.info("权限判断结束")
        window = Window(config.get("windowTitle"))
        probe = Probe(window)
        probe.battle()
    except Exception as e:
        logger.error(e)
