import pytest


@pytest.fixture
def table_less_good_result():
    return {
        "period": "30.09.2021 20:00:00 - 31.12.2021 20:00:00",
        "category": "Супермаркеты",
        "number_of_transactions": 4,
        "amount_of_transactions": "421 руб",
    }
