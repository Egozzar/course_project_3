import os

from constants import ROOT_PATH
from src.services import simple_search


def test_simple_search_right(capsys):
    simple_search("Супермаркеты", "less.xlsx")

    captured = capsys.readouterr()
    assert captured.out[:-1] == "По указанному выражению найдено 4 завершённых транзакций\nна общую сумму 421 руб."

    report_path = os.path.join(ROOT_PATH, "reports_record", "simple_search.json")
    assert os.path.exists(report_path)


def test_simple_search_no_columns(capsys):
    simple_search("Супермаркеты", "no_columns.xlsx")

    captured = capsys.readouterr()
    assert captured.out[:-1] == "По указанному выражению найдено 0 завершённых транзакций\nна общую сумму 0 руб."

    report_path = os.path.join(ROOT_PATH, "reports_record", "simple_search.json")
    assert os.path.exists(report_path)
