import pytest

from exceptions.my_error import MyError
from src.readers import reader_files
from src.reports import spending_by_category

df = reader_files()


def test_spending_by_category_good(capsys):
    assert spending_by_category(df, "Супермаркеты", "2021-12-31 20:00:00").shape == (133, 3)

    captured = capsys.readouterr()
    assert captured.out[-51:-1] == "проведено 133 транзакций на общую сумму 26028 руб."


def test_spending_by_category_wrong_category():
    with pytest.raises(MyError) as err:
        spending_by_category(df, "picture.jpeg")
    assert str(err.value) == "Ошибка: в таблице нет такой категории."


def test_spending_by_category_no_category():
    with pytest.raises(TypeError) as err:
        spending_by_category(df)
    assert str(err.value)[-50:] == "missing 1 required positional argument: 'category'"
