import os
from datetime import datetime

from freezegun import freeze_time

from constants import ROOT_PATH
from src.data_capture import get_by_cards, get_column_dict, get_top_transactions, say_hi, separation
from src.readers import reader_files
from src.selection_util import select_transactions


def test_get_by_cards_good(list_less_good_result):
    less_path = os.path.join(ROOT_PATH, "data", "less.xlsx")
    df = reader_files(less_path)

    assert get_by_cards(df) == list_less_good_result


def test_get_by_cards_empty():
    empty_path = os.path.join(ROOT_PATH, "data", "empty.xlsx")
    df = reader_files(empty_path)

    assert get_by_cards(df) == []


def test_get_by_cards_no_columns():
    no_columns_path = os.path.join(ROOT_PATH, "data", "no_columns.xlsx")
    df = reader_files(no_columns_path)

    assert get_by_cards(df) == [{"cashback": 0.0, "last_digits": "0000", "total_spent": 0}]


def test_get_top_transactions_no_columns():
    no_columns_path = os.path.join(ROOT_PATH, "data", "no_columns.xlsx")
    df = reader_files(no_columns_path)

    assert (
        get_top_transactions(df)
        == [{"date": "01.01.1", "amount": 0, "category": "Нет категории", "description": "Нет описания"}] * 5
    )


def test_get_top_transactions_empty():
    empty_path = os.path.join(ROOT_PATH, "data", "empty.xlsx")
    df = reader_files(empty_path)

    assert get_top_transactions(df) == []


def test_get_top_transactions_good(list_top_transactions):
    less_path = os.path.join(ROOT_PATH, "data", "less.xlsx")
    df = reader_files(less_path)
    df_selected = select_transactions(df, datetime(2021, 12, 30), datetime(2022, 1, 1))

    assert get_top_transactions(df_selected) == list_top_transactions


def test_separation(capsys):
    separation()
    captured = capsys.readouterr()

    assert captured.out == "____________________\n\n"


def test_get_column_dict_right():
    assert get_column_dict("Категория", "less.xlsx") == {
        1: "Супермаркеты",
        2: "Различные товары",
        3: "Переводы",
        4: "Каршеринг",
    }


def test_get_column_dict_empty():
    assert get_column_dict("Категория", "empty.xlsx") == {}


def test_say_hi():
    with freeze_time("2000-01-01 1:00:00"):
        assert say_hi() == "Доброй ночи!"

    with freeze_time("2000-01-01 7:00:00"):
        assert say_hi() == "Доброе утро!"

    with freeze_time("2000-01-01 13:00:00"):
        assert say_hi() == "Добрый день!"

    with freeze_time("2000-01-01 19:00:00"):
        assert say_hi() == "Добрый вечер!"
