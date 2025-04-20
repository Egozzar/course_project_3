import os

import pytest

from constants import ROOT_PATH
from exceptions.my_error import MyError
from src.readers import reader_files


def test_reader_files():
    less = os.path.join(ROOT_PATH, "data", "less.xlsx")
    result = reader_files(less)
    assert result.shape == (9, 15)


def test_reader_files_no_format():
    with pytest.raises(MyError) as err:
        reader_files("picture.jpeg")
    assert str(err.value) == "Ошибка: неизвестный формат файла."


def test_reader_files_empty_table():
    empty = os.path.join(ROOT_PATH, "data", "empty.xlsx")
    with pytest.raises(MyError) as err:
        reader_files(empty)
    assert str(err.value) == "Ошибка: пустая таблица."


def test_reader_files_not_find():
    not_find = os.path.join(ROOT_PATH, "data", "not_find.xlsx")
    with pytest.raises(FileNotFoundError) as err:
        reader_files(not_find)
    assert str(err.value)[10:35] == "No such file or directory"
