from unittest.mock import patch

from src.external_requests import get_exchange_rate, get_stock_price


@patch("requests.get")
def test_get_stock_price(mock_get, stock_price):
    mock_get.return_value.json.return_value = stock_price

    assert get_stock_price(["AAPL"]) == [{"stock": "AAPL", "price": 198.53}]

    url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=FZ89KJ3Z9G0P1JM7"
    mock_get.assert_called_once_with(url)


@patch("requests.get")
def test_get_stock_price_empty(mock_get):
    mock_get.return_value.json.return_value = {}

    assert get_stock_price(["AAPL"]) == [{"price": 0.0, "stock": ""}]

    url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=FZ89KJ3Z9G0P1JM7"
    mock_get.assert_called_once_with(url)


@patch("requests.get")
def test_get_exchange_rate(mock_get, exchange_rate, url_exchange_rate):
    mock_get.return_value.json.return_value = exchange_rate

    assert get_exchange_rate(["USD"]) == [{"currency": "USD", "rate": 82.46}]

    mock_get.assert_called_once_with(url_exchange_rate[0], headers=url_exchange_rate[1], params=url_exchange_rate[2])


@patch("requests.get")
def test_get_exchange_rate_empty(mock_get, exchange_rate, url_exchange_rate):
    mock_get.return_value.json.return_value = {}

    assert get_exchange_rate(["USD"]) == [{"currency": "", "rate": 0.0}]

    mock_get.assert_called_once_with(url_exchange_rate[0], headers=url_exchange_rate[1], params=url_exchange_rate[2])
