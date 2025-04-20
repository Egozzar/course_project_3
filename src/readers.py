import os

import pandas as pd

from constants import ROOT_PATH
from exceptions.my_error import MyError

default_path = os.path.join(ROOT_PATH, "data", "operations.xlsx")


def reader_files(path_file: str = default_path) -> pd.DataFrame:
    """
    Функция для считывания данных из файла. Принимает путь
    к файлу, выдает объект DataFrame - двумерную таблицу
    :param path_file:(str) путь к файлу
    :return: объект DataFrame
    """
    pos_dot = path_file.rindex(".")
    file_format = path_file[pos_dot:]

    match file_format:
        case ".xlsx":
            df_result = pd.read_excel(path_file)
            if df_result.shape == (0, 0):
                raise MyError("пустая таблица")

            return df_result
        case _:
            raise MyError("неизвестный формат файла")
