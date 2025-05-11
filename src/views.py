import json
import os.path
from datetime import datetime

import pandas as pd
from dateutil import parser

from constants import ROOT_PATH
from src.data_capture import get_by_cards, get_top_transactions, say_hi
from src.external_requests import get_exchange_rate, get_stock_price
from src.logger import create_logger
from src.readers import reader_files
from src.selection_util import select_transactions

logger = create_logger(__name__)


def general_function(tense: str = "", job_file: str = "operations.xlsx", settings: str = "user_settings.json") -> dict:
    """
    Основная функция работы главной страницы приложения. Формирует JSON-отчёт на основе
    завершённых транзакций за вычисляемый период времени, добавляет в него курсы интересующих
    пользователя валют и котировки акций. Возвращает результирующий словарь
    :param tense: (str) строка с датой, до которой проводятся вычисления
    :param job_file: (str) файл с EXCEL-таблицей
    :param settings: (str) файл с пользовательскими настройками
    :return: результирующая аналитическая информация в виде словаря
    """
    # Приветствие
    greetings = say_hi()

    # Период времени для анализа
    finish_date: datetime = parser.parse(tense) if tense else datetime.now() - pd.DateOffset(years=4)
    start_date: datetime = finish_date.replace(day=1, hour=0, minute=0, second=0)

    # Создадим двумерную таблицу на основе EXCEL-таблицы
    path_file: str = os.path.join(ROOT_PATH, "data", job_file)
    job_df: pd.DataFrame = reader_files(path_file)

    # Отберём успешные транзакции с начала указанного месяца
    selected_by_term: pd.DataFrame = select_transactions(job_df, start_date, finish_date)

    # Исключим из таблицы неизвестные карты и незавершённые операции
    selected_not_nan: pd.DataFrame = selected_by_term.loc[selected_by_term["Номер карты"].notnull()]

    # Получим информацию по транзакциям по каждой карте
    each_card: list = get_by_cards(selected_not_nan)

    # Получим информацию о топовых по сумме платежа транзакциях
    top_payments: list = get_top_transactions(selected_not_nan)

    # Получим информацию о котировках наших акций на фондовой бирже
    settings_path: str = os.path.join(ROOT_PATH, "data", settings)

    with open(settings_path, encoding="UTF-8") as file:
        user_data = json.load(file)

    currencies, stocks = user_data.values()
    stock_prices: list = get_stock_price(stocks)

    # Получим информацию о курсах валют
    currency_rates: list = get_exchange_rate(currencies)

    # Формирование результирующего словаря
    result: dict = {
        "greeting": greetings,
        "cards": each_card,
        "top_transactions": top_payments,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    default_path: str = os.path.join(ROOT_PATH, "reports_record", "general_page.json")

    with open(default_path, "w", encoding="UTF-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    logger.info("Успешная работа функции")
    return result
