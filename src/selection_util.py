from datetime import datetime

import pandas as pd

from src.logger import create_logger

logger = create_logger(__name__)


def select_transactions(job_df: pd.DataFrame, start_date: datetime, finish_date: datetime) -> pd.DataFrame:
    """
    Функция отбирает и возвращает завершённые транзакции за
    необходимый период времени
    :param job_df: (pd.DataFrame) двумерная таблица для преобразований
    :param start_date: (datetime) начало периода для анализа
    :param finish_date: (datetime) конец периода для анализа
    :return: (pd.DataFrame) результирующая двумерная таблица
    """
    # Преобразуем временную колонку рабочей таблицы
    job_df["Дата операции"] = job_df["Дата операции"].map(
        lambda p: datetime.strptime(p, "%d.%m.%Y %H:%M:%S") if isinstance(p, str) else None
    )
    # Отберём операции за введённый промежуток времени
    selected_by_term = job_df.loc[((job_df["Дата операции"] >= start_date) & (job_df["Дата операции"] <= finish_date))]

    # Нам нужны только успешные операции
    executed_df = selected_by_term.loc[(selected_by_term["Статус"] == "OK")]

    logger.info("Успешная работа функции")
    return executed_df
