import json
import os
import re
from functools import reduce
from typing import Any

import pandas as pd

from constants import ROOT_PATH
from src.logger import create_logger
from src.readers import reader_files

logger = create_logger(__name__)


def simple_search(expression: str = "qwerty", file_name: str = "operations.xlsx") -> None:
    """
    Функция осуществляет поиск транзакций по определённому выражению в описании
    и в категории, записывает результат в JSON-файл и выводит результирующее
    сообщение для пользователя
    :param expression:(str) выражение для поиска и отбора транзакций
    :param file_name:(str) файл с таблицей для поиска
    """

    pattern: Any = re.compile(expression)
    table_path: str = os.path.join(ROOT_PATH, "data", file_name)

    job_df: pd.DataFrame = reader_files(table_path)

    # Проверим наличие необходимых колонок в таблице
    if "Сумма платежа" not in job_df:
        job_df["Сумма платежа"] = [0] * len(job_df)
        logger.warning("В таблице отсутствует колонка 'Сумма платежа'")

    if "Категория" not in job_df:
        job_df["Категория"] = ["Нет категории"] * len(job_df)
        logger.warning("В таблице отсутствует колонка 'Категория'")

    if "Описание" not in job_df:
        job_df["Описание"] = ["Нет описания"] * len(job_df)
        logger.warning("В таблице отсутствует колонка 'Описание'")

    if "Статус" not in job_df:
        job_df["Статус"] = ["Нет статуса"] * len(job_df)
        logger.warning("В таблице отсутствует колонка 'Статус'")

    # при наличии пустых ячеек таблицы (NaN) установим значение 0
    # и преобразуем DataFrame в список объектов (транзакций)
    job_df = job_df.loc[(job_df["Категория"].notnull()) & (job_df["Описание"].notnull())]
    job_df.fillna(0, inplace=True)
    job_lst = job_df.to_dict(orient="records")

    # отфильтруем транзакции по выражению
    filter_obj: filter = filter(lambda x: pattern.search(x["Категория"]) or pattern.search(x["Описание"]), job_lst)
    filter_lst: list = list(filter_obj)
    # отправим отчёт в JSON-файл
    default_path: str = os.path.join(ROOT_PATH, "reports_record", "simple_search.json")

    with open(default_path, "w", encoding="UTF-8") as file:
        json.dump(filter_lst, file, indent=4, ensure_ascii=False)

    # нас интересуют только выполненные операции
    executed_lst: list = [elem for elem in filter_lst if elem["Статус"] == "OK"]

    # Формирование результирующего сообщения
    total: int = reduce(lambda summ, val: summ + val["Сумма платежа"], executed_lst, 0)
    length: int = len(executed_lst)

    logger.info("Успешная работа функции")
    print(
        f"По указанному выражению найдено {length} завершённых транзакций\n" f"на общую сумму {abs(round(total))} руб."
    )
