from src.readers import reader_files
from src.reports import spending_by_category

df = reader_files()
df_no_columns = reader_files("no_columns.xlsx")


def test_spending_by_category_good(capsys):
    assert spending_by_category(df, "Супермаркеты", "2021-12-31 20:00:00").shape == (133, 3)

    captured = capsys.readouterr()
    assert captured.out[-51:-1] == "проведено 133 транзакций на общую сумму 26028 руб."


def test_spending_by_category_wrong_category(capsys):
    assert spending_by_category(df, "www", "2021-12-31 20:00:00").shape == (0, 3)

    captured = capsys.readouterr()
    assert captured.out[-45:-1] == "проведено 0 транзакций на общую сумму 0 руб."


def test_spending_by_category_no_columns(capsys):
    assert spending_by_category(df_no_columns, "Супермаркеты", "2021-12-31 20:00:00").shape == (0, 3)

    captured = capsys.readouterr()
    assert captured.out[-45:-1] == "проведено 0 транзакций на общую сумму 0 руб."
