import os

import requests
from dotenv import load_dotenv

from constants import RATE_EXCHANGE, STOCK_EXCHANGE
from src.logger import create_logger

logger = create_logger(__name__)


def get_stock_price(watched_stocks: list[str]) -> list[dict]:
    """
    Функция делает запрос на внешний сервис, получает информацию по котировкам
    необходимых акций и возвращает полученную информацию
    :param watched_stocks: (list[str]) список пользовательских акций
    :return: (list[dict]) список словарей с данными по каждой акции
    """
    # Загрузка переменных из .env-файла
    load_dotenv()
    alphavantage_key = os.getenv("ALPHAVANTAGE_KEY")

    # Создадим список для накопления ответов на запросы
    stock_data = list()

    for elem in watched_stocks:
        url = f"{STOCK_EXCHANGE}?function=GLOBAL_QUOTE&symbol={elem}&apikey={alphavantage_key}"
        r = requests.get(url)
        data = r.json()

        stock_data.append(data)

    # Формирование вывода
    stock_prices = list()

    for data in stock_data:
        stock: str = data.get("Global Quote", {}).get("01. symbol", "")
        price: float = round(float(data.get("Global Quote", {}).get("05. price", 0.0)), 2)
        stock_prices.append({"stock": stock, "price": price})

    logger.info("Успешная работа функции")
    return stock_prices


def get_exchange_rate(currencies: list[str]) -> list[dict]:
    """
    Функция делает запрос на внешний сервис, получает информацию по курсам
    необходимых валют и возвращает полученную информацию
    :param currencies: (list[str]) список пользовательских валют
    :return: (list[dict]) список словарей с данными по каждой валюте
    """
    # Загрузка переменных из .env-файла
    load_dotenv()
    apilayer_key = os.getenv("APILAYER_KEY")

    # Создадим список для накопления ответов на запросы
    currencies_data = list()

    for currency in currencies:
        payload = {"amount": "1", "from": currency, "to": "RUB"}

        headers = {"apikey": apilayer_key}

        response = requests.get(RATE_EXCHANGE, headers=headers, params=payload)
        result = response.json()
        currencies_data.append(result)

    # Формирование вывода
    currencies_rates = list()

    for elem in currencies_data:
        currency_name = elem.get("query", {}).get("from", "")
        rate = round(elem.get("result", 0.0), 2)
        currencies_rates.append({"currency": currency_name, "rate": rate})

    logger.info("Успешная работа функции")
    return currencies_rates
