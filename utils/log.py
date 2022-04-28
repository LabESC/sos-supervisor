import logging.config
import logging

def create_log(name, filename, level=logging.DEBUG):
    logger = logging.getLogger(name)
    if len(logger.handlers) > 0:
        return logger

    logger.setLevel(level)

    handler = logging.FileHandler(filename)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
