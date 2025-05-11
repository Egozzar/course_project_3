import pytest


@pytest.fixture
def table_less_good_result():
    return {
        "period": "30.09.2021 20:00:00 - 31.12.2021 20:00:00",
        "category": "Супермаркеты",
        "number_of_transactions": 4,
        "amount_of_transactions": "421 руб",
    }


@pytest.fixture
def list_less_good_result():
    return [
        {"cashback": 5.71, "last_digits": "5091", "total_spent": 571.07},
        {"cashback": 4.22, "last_digits": "7197", "total_spent": 422.38},
    ]


@pytest.fixture
def list_top_transactions():
    return [
        {"amount": 20000.0, "category": "Переводы", "date": "30.12.2021", "description": "Константин Л."},
        {"amount": 800.0, "category": "Переводы", "date": "31.12.2021", "description": "Константин Л."},
        {"amount": 564.0, "category": "Различные товары", "date": "31.12.2021", "description": "Ozon.ru"},
        {"amount": 160.89, "category": "Супермаркеты", "date": "31.12.2021", "description": "Колхоз"},
        {"amount": 118.12, "category": "Супермаркеты", "date": "31.12.2021", "description": "Магнит"},
    ]


@pytest.fixture
def stock_price():
    return {
        "Global Quote": {
            "01. symbol": "AAPL",
            "02. open": "199.0000",
            "03. high": "200.5399",
            "04. low": "197.5350",
            "05. price": "198.5300",
            "06. volume": "36453923",
            "07. latest trading day": "2025-05-09",
            "08. previous close": "197.4900",
            "09. change": "1.0400",
            "10. change percent": "0.5266%",
        }
    }


@pytest.fixture
def exchange_rate():
    return {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": 1},
        "info": {"timestamp": 1746920895, "rate": 82.455285},
        "date": "2025-05-10",
        "result": 82.455285,
    }


@pytest.fixture
def url_exchange_rate():
    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": "E9KWAxtVW0A1btd00rwEzI5OjQRxOti0"}
    params = {"amount": "1", "from": "USD", "to": "RUB"}

    return (url, headers, params)


@pytest.fixture
def general_report():
    return [
        [
            {"cashback": 0.07, "last_digits": "5091", "total_spent": 7.07},
            {"cashback": 0.01, "last_digits": "7197", "total_spent": 1.32},
        ],
        [
            {"amount": 7.07, "category": "Каршеринг", "date": "30.12.2021", "description": "Ситидрайв"},
            {"amount": 1.32, "category": "Каршеринг", "date": "30.12.2021", "description": "Ситидрайв"},
        ],
    ]
