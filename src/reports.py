from collections import Counter
from datetime import date, datetime
from typing import Optional

import pandas as pd
from dateutil import parser

from src.logger import create_logger
from src.selection_util import select_transactions

logger = create_logger(__name__)


def spending_by_category(job_df: pd.DataFrame, category: str, term: Optional[str] = None) -> pd.DataFrame:
    """
    Функция обрабатывает полученную двумерную таблицу и возвращает траты по заданной
    категории за последние три месяца (от переданной даты).
    :param job_df:(pd.DataFrame)
    :param category:(str) категория транзакции для фильтрации
    :param term:(str) конечная дата транзакций; при отсутствии - настоящее время
    :return:(pd.DataFrame) отсортированный по категории объект DataFrame
    """
    # Проверим наличие необходимых колонок в таблице
    if "Сумма платежа" not in job_df:
        job_df["Сумма платежа"] = [0] * len(job_df)
        logger.warning("В таблице отсутствует колонка 'Сумма платежа'")

    if "Дата операции" not in job_df:
        job_df["Дата операции"] = [date(1, 1, 1)] * len(job_df)
        logger.warning("В таблице отсутствует колонка 'Дата операции'")

    if "Категория" not in job_df:
        job_df["Категория"] = ["Нет категории"] * len(job_df)
        logger.warning("В таблице отсутствует колонка 'Категория'")

    if "Статус" not in job_df:
        job_df["Статус"] = ["Нет статуса"] * len(job_df)
        logger.warning("В таблице отсутствует колонка 'Статус'")

    if category not in Counter(job_df["Категория"]):
        logger.warning("В таблице отсутствует заданная категория")

    # Определение периода времени для отбора
    finish = parser.parse(term) if term else datetime.now() - pd.DateOffset(years=4)
    start = finish - pd.DateOffset(months=3)

    # Отберём успешные транзакции за 3 месяца
    selected_by_term = select_transactions(job_df, start, finish)

    # Фильтрация по категории
    sorted_by_category = selected_by_term.loc[(selected_by_term["Категория"] == category)]

    # Формирование результирующего DataFrame
    result_df = sorted_by_category[["Дата операции", "Сумма платежа", "Категория"]].copy()

    # Формирование и вывод отчёта
    total = result_df["Сумма платежа"].sum()
    length, _ = result_df.shape

    print(
        f"В период с {start.strftime("%d.%m.%Y %H:%M:%S")} по {finish.strftime("%d.%m.%Y %H:%M:%S")}\
 в категории '{category}'\nпроведено {length} транзакций на общую сумму {abs(round(total))} руб."
    )

    logger.info("Успешная работа функции")
    return result_df
