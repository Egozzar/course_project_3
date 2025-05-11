from src.readers import reader_files


def test_reader_files():
    result = reader_files("less.xlsx")

    assert result.shape == (9, 15)


def test_reader_files_no_format():
    result = reader_files("empty.xlsx")

    assert reader_files("picture.jpeg").equals(result)


def test_reader_files_not_find():
    result = reader_files("empty.xlsx")

    assert reader_files("picture.xlsx").equals(result)
