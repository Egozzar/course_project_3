from typing import Final
import os

# Универсальный адрес корня проекта
ROOT_PATH: Final[str] = os.path.dirname(__file__)

# Адрес для запросов по курсу акций
STOCK_EXCHANGE: Final[str] = "https://www.alphavantage.co/query"

# Адрес для запросов по курсу валют
RATE_EXCHANGE: Final[str] = "https://api.apilayer.com/exchangerates_data/convert"

#pytest --cov=src --cov-report=html -генерация отчета о покрытии в HTML-формате
# Путь в проекте для логирования
LOG_PATH: Final[str] = os.path.join(ROOT_PATH, "logs", "src.log")
