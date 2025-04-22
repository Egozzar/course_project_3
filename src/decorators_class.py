import json
import os
from datetime import datetime
from functools import reduce
from typing import Any, Callable

import pandas as pd
from dateutil import parser

from constants import ROOT_PATH


class DecorCategory:
    """
    Класс-декоратор, декорирует функцию и принимает название файла, в который записывает результаты
    работы этой функции
    """

    def __init__(self, func: Callable, file_name: str = "category_default.json") -> None:
        """
        Инициализирует новый экземпляр класса
        """
        self.__func = func
        self.__path_file = os.path.join(ROOT_PATH, "reports_record", file_name)

    def __call__(self, *args: Any, **kwargs: dict) -> Any:
        """
        Вызывает целевую функцию, принимает и передаёт возможные аргументы и добавляет
        возможность формирования и записи отчёта в формате JSON
        :param args:(tuple) возможные позиционные аргументы
        :param kwargs:(dict) возможные именованные аргументы
        :return: результат работы целевой функции
        """
        df = self.__func(*args, **kwargs)

        # df.fillna(0, inplace=True) - при наличии пустых ячеек таблицы (NaN)
        result_lst = df.to_dict(orient="records")

        # Переменные для формирования отчёта
        category: str = args[1]
        length: int = len(result_lst)

        total: int | float = reduce(lambda summ, val: summ + val["Сумма платежа"], result_lst, 0)
        total_str: str = str(abs(round(total)))
        date_: datetime = (parser.parse(args[2])) if len(args) > 2 else datetime.now() - pd.DateOffset(years=4)

        finish: str = date_.strftime("%d.%m.%Y %H:%M:%S")
        start: str = (date_ - pd.DateOffset(months=3)).strftime("%d.%m.%Y %H:%M:%S")

        report = {
            "period": f"{start} - {finish}",
            "category": category,
            "number_of_transactions": length,
            "amount_of_transactions": f"{total_str} руб",
        }
        # Запись отчёта в файл
        with open(self.__path_file, "w", encoding="UTF-8") as file:
            json.dump(report, file, indent=4, ensure_ascii=False)

        return df
