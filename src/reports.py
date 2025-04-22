from collections import Counter
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil import parser

from exceptions.my_error import MyError


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция обрабатывает полученную двумерную таблицу и возвращает траты по заданной
    категории за последние три месяца (от переданной даты).
    :param transactions:(pd.DataFrame)
    :param category:(str) категория транзакции для фильтрации
    :param date:(str) конечная дата транзакций; при отсутствии - настоящее время
    :return:(pd.DataFrame) отсортированный по категории объект DataFrame
    """

    if category not in Counter(transactions["Категория"]):
        raise MyError("в таблице нет такой категории")

    # Определение периода времени для отбора
    finish = parser.parse(date) if date else datetime.now() - pd.DateOffset(years=4)
    start = finish - pd.DateOffset(months=3)

    transactions["Дата операции"] = transactions["Дата операции"].map(
        lambda p: datetime.strptime(p, "%d.%m.%Y %H:%M:%S") if isinstance(p, str) else None
    )
    # Отбор транзакций за полученный период
    operations_for_period = transactions.loc[
        ((finish >= transactions["Дата операции"]) & (transactions["Дата операции"] >= start))
    ]
    # Фильтрация по категории
    sorted_by_category = operations_for_period.loc[(operations_for_period["Категория"] == category)]

    # Формирование результирующего DataFrame
    result_df = sorted_by_category[["Дата операции", "Сумма платежа", "Категория"]].copy()

    # Формирование и вывод отчёта
    total = result_df["Сумма платежа"].sum()
    length, _ = result_df.shape
    print(
        f"В период с {start.strftime("%d.%m.%Y %H:%M:%S")} по {finish.strftime("%d.%m.%Y %H:%M:%S")}\
 в категории '{category}'\nпроведено {length} транзакций на общую сумму {abs(round(total))} руб."
    )

    return result_df
