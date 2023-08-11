import configparser
import logging


def getConfig():
    try:
        config = configparser.ConfigParser()
        config.read('ConfigFile.properties')
        return config
    except Exception as e:
        logging.exception('getConfig():' + str(e), exc_info=True)
        raise e
