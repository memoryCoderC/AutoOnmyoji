import configparser

config = configparser.ConfigParser()
config.read('game.conf', "utf-8")


def get(key, header="game"):
    return config[header][key]


def set(key, value, header="game"):
    config.set(key, value, header)
