from collections import Counter
from datetime import date, datetime
from typing import Any

import pandas as pd

from src.logger import create_logger
from src.readers import reader_files

logger = create_logger(__name__)


def get_by_cards(job_df: pd.DataFrame) -> list[dict[str, Any]]:
    """
    Функция принимает таблицу с транзакциями и возвращает данные, сгруппированные
    в словари по каждой карте: номер карты (4 цифры), общая сумма операций и
    кешбек (1% от суммы)
    :param job_df: (pd.DataFrame) двумерная таблица с транзакциями
    :return: (list[dict | None]) список словарей-данных по каждой карте
    """
    # Проверим наличие необходимых колонок в таблице
    if "Номер карты" not in job_df:
        job_df["Номер карты"] = ["*0000"] * len(job_df)
        logger.warning("В таблице отсутствует колонка 'Номер карты'")

    if "Сумма платежа" not in job_df:
        job_df["Сумма платежа"] = [0] * len(job_df)
        logger.warning("В таблице отсутствует колонка 'Сумма платежа'")

    if "Статус" not in job_df:
        job_df["Статус"] = ["Нет статуса"] * len(job_df)
        logger.warning("В таблице отсутствует колонка 'Статус'")

    # Сгруппируем таблицу по номерам карт, просуммируем и преобразуем в список
    num_df = job_df.groupby(["Номер карты"])
    sum_df = num_df["Сумма платежа"].sum()
    sum_lst = [abs(elem) for elem in sum_df]

    # Формирование вывода
    result = list()

    for i in range(len(sum_lst)):
        result.append(
            {
                "last_digits": sum_df.index[i][1:],
                "total_spent": round(sum_lst[i], 2),
                "cashback": round(sum_lst[i] / 100, 2),
            }
        )
    logger.info("Успешная работа функции")
    return result


def get_top_transactions(job_df: pd.DataFrame) -> list[dict[str, Any]]:
    """
    Функция принимает таблицу, сортирует её по колонке "Сумма платежа"
    и возвращает список с информацией о пяти топовых транзакциях
    :param job_df: (pd.DataFrame) принимаемая двумерная таблица
    :return: (list) результирующий список
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

    if "Описание" not in job_df:
        job_df["Описание"] = ["Нет описания"] * len(job_df)
        logger.warning("В таблице отсутствует колонка 'Описание'")

    if "Статус" not in job_df:
        job_df["Статус"] = ["Нет статуса"] * len(job_df)
        logger.warning("В таблице отсутствует колонка 'Статус'")

    # Отсортируем таблицу по убыванию суммы платежа
    job_df_ = job_df.sort_values(by="Сумма платежа", inplace=False, ascending=True)
    # Создадим новую таблицу топ-5
    top_trans = job_df_.iloc[:5, :]

    # Сформируем вывод
    result = list()

    for _, row in top_trans.iterrows():
        result.append(
            {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": abs(row["Сумма платежа"]),
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )

    logger.info("Успешная работа функции")
    return result


def say_hi() -> str:
    """
    Функция возвращает строку приветствия в зависимости от времени суток
    :return: (str) строка приветствия
    """
    now_: datetime = datetime.now()
    hour: int = now_.hour

    if hour < 3 or hour >= 21:
        logger.info("Успешная работа функции")
        return "Доброй ночи!"
    if hour < 9:
        logger.info("Успешная работа функции")
        return "Доброе утро!"
    if hour < 15:
        logger.info("Успешная работа функции")
        return "Добрый день!"
    logger.info("Успешная работа функции")
    return "Добрый вечер!"


def separation() -> None:
    """
    Функция для разделения вывода в консоли
    """
    print("_" * 20)
    print()


def get_column_dict(column_name: str = "Категория", file_name: str = "operations.xlsx") -> dict[int, str]:
    """
    Функция для получения данных каждой ячейки выбранного столбца таблицы
    :param column_name: (str) название выбранного столбца таблицы
    :param file_name: (str) название выбранного EXCEL-файла
    :return: (dict) словарь с данными всех ячеек
    """
    # Двумерная таблица из EXCEL-файла
    job_df = reader_files(file_name)

    # Проверим наличие необходимых колонок в таблице
    if column_name not in job_df:
        job_df[column_name] = [0] * len(job_df)

    # Избавимся от пустых ячеек в столбце
    job_df = job_df.loc[(job_df[column_name].notnull())]
    # Получим список всех данных ячеек выбранного столбца без повторений
    cells_list = list(Counter(job_df[column_name]))
    # Результирующий словарь из списка через генератор
    cells_dict = {ind + 1: elem for ind, elem in enumerate(cells_list)}

    logger.info("Успешная работа функции")
    return cells_dict
