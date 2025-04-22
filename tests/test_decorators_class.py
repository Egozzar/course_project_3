import json
import os

from constants import ROOT_PATH
from src.decorators_class import DecorCategory
from src.readers import reader_files
from src.reports import spending_by_category


def test_decorcategory_good(capsys, table_less_good_result):
    test_path = os.path.join(ROOT_PATH, "reports_record", "category_default.json")
    less_path = os.path.join(ROOT_PATH, "data", "less.xlsx")
    df = reader_files(less_path)
    spending_by_category_dec = DecorCategory(spending_by_category, test_path)

    assert spending_by_category_dec(df, "Супермаркеты", "2021-12-31 20:00:00").shape == (4, 3)
    assert os.path.exists(test_path)

    with open(test_path, encoding="UTF-8") as file:
        assert json.load(file) == table_less_good_result

    captured = capsys.readouterr()
    assert captured.out[-47:-1] == "проведено 4 транзакций на общую сумму 421 руб."
