import logging
import logging.config
import os
from ctypes import windll
import yaml


def setup_logging(default_path='default', default_level=logging.INFO):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = r'\resource\config\log.yaml'
    if default_path == 'default':
        log_dir = base_dir + log_dir
    if os.path.exists(log_dir):
        with open(log_dir, 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


setup_logging()

if __name__ == '__main__':
    user32 = windll.user32
    user32.SetProcessDPIAware()
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    logging.debug('Start')
    logging.info('Exec')
    logging.info('Finished')
    try:
        print(1 / 0)
    except Exception as e:
        logging.exception(e, exc_info=True)
