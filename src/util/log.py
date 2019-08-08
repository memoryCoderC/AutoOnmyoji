import logging
import logging.config
from os.path import exists

from yaml import load, FullLoader


class logger:
    @classmethod
    def debug(cls, msg, *args, **kwargs):
        cls.log.debug(msg, *args, **kwargs)

    @classmethod
    def info(cls, msg, *args, **kwargs):
        cls.log.info(msg, *args, **kwargs)

    @classmethod
    def warning(cls, msg, *args, **kwargs):
        cls.log.warning(msg, *args, **kwargs)

    @classmethod
    def error(cls, msg, *args, **kwargs):
        cls.log.error(msg, *args, **kwargs)

    @classmethod
    def exception(cls, msg, *args, exc_info=True, **kwargs):
        cls.log.exception(msg, *args, exc_info, **kwargs)

    def setup_logging(log_path='default', default_level=logging.INFO):
        log_dir = r'resource\config\log.yaml'
        if log_path == 'default':
            log_dir = log_dir
        else:
            log_dir = log_path
        if exists(log_dir):
            with open(log_dir, 'r', encoding='utf-8') as f:
                config = load(f, Loader=FullLoader)
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)

    setup_logging()
    log = logging.getLogger()
