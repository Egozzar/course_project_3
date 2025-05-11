import logging
from logging import Logger

from constants import LOG_PATH


def create_logger(name: str) -> Logger:
    """
    Функция создаёт и возвращает объект, позволяющий логировать
    работу модулей всего проекта
    :param name: (str) имя модуля, на котором запускается функция
    :return: (Logger) объект логгера
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(LOG_PATH, mode="a")
    file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s")

    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger
