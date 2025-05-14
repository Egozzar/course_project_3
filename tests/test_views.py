import os

from constants import ROOT_PATH
from src.views import general_function


def test_general_function_right(general_report):
    general_path = os.path.join(ROOT_PATH, "reports_record", "category_default.json")
    result = general_function("31.12.2021", "less.xlsx")

    assert os.path.exists(general_path)
    assert [result["cards"], result["top_transactions"]] == general_report
