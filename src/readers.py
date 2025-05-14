import os

import pandas as pd

from constants import ROOT_PATH
from src.logger import create_logger

logger = create_logger(__name__)


def reader_files(file_name: str = "operations.xlsx") -> pd.DataFrame:
    """
    Функция для считывания данных из файла. Принимает имя файла,
    выдает объект DataFrame - двумерную таблицу
    :param file_name:(str) имя файла
    :return: объект DataFrame
    """
    path_file = os.path.join(ROOT_PATH, "data", file_name)
    empty_table = os.path.join(ROOT_PATH, "data", "empty.xlsx")

    if not path_file.endswith(".xlsx"):
        path_file = empty_table

    try:
        logger.info("Успешная работа функции")
        return pd.read_excel(path_file)

    except FileNotFoundError:
        logger.warning("Функция возвращает пустую таблицу")
        return pd.read_excel(empty_table)
