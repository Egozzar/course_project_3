from pprint import pp
from time import sleep

import pandas as pd

from src.data_capture import get_column_dict, say_hi, separation
from src.decorators_class import DecorCategory
from src.readers import reader_files
from src.reports import spending_by_category
from src.services import simple_search
from src.views import general_function


def main() -> None:
    """
    Функция формирует основную логику проекта и связывает функциональности между собой.
    :return: None
    """
    # Объявление и получение локальных переменных
    menu_item: str  # пункт меню
    user_date: str  # указанная пользователем дата
    user_category: str  # указанный пользователем номер категории
    general_report: dict  # результат работы функции Главной страницы
    job_df: pd.DataFrame  # двумерная таблица из EXCEL-файла

    negative_loop_message: str = "Такого номера в меню нет. Попробуйте ещё раз."
    select_category: str = """Выбери номер категории:
                         1. Супермаркеты   11. Связь         22. Сервис          32. Медицина         42. Отели
                         2. Разл. товары   12. Такси         23. ЖКХ             33. Фото и видео     43. Кино
                         3. Переводы       13. Транспорт     24. Дет.товары      34. Онлайн-к-театры  44. Спорттовары
                         4. Каршеринг      14. Цветы         25. Косметика       35. Авиабилеты       45. Автоуслуги
                         5. Пополнения     15. Развлечения   26. Одежда и обувь  36. Образование      47. Финансы
                         6. Канцтовары     16. Госуслуги     27. НКО             37. Рестораны        48. Искусство
                         7. Ж/д билеты     17. Мест. тр-рт   28. Электроника     38. Частные услуги   49. Duty Free
                         8. Фастфуд        18. Другое        29. Наличные        39. Красота
                         9. Дом и ремонт   20. Топливо       30. Сувениры        40. Турагентства
                         10. Аптеки        21. Услуги банка  31. Моб.связь       41. Книги"""
    # Получим словарь категорий таблицы
    categories: dict = get_column_dict()

    # Приветствие
    print(say_hi())
    print(
        "Разработано небольшое приложение для анализа транзакций.\n"
        "Предлагаю 'погонять' функционал в трёх основных разделах."
    )
    separation()

    while True:
        print(
            "Выбери номер раздела:\n"
            "1. Веб-страницы - Главная\n"
            "2. Сервисы - Простой поиск\n"
            "3. Отчёты - Траты по категориям\n"
            "4. Выйти"
        )
        menu_item = input().strip()
        separation()

        match menu_item:
            case "1":
                print("Добро пожаловать на Главную страницу!")
                print(
                    "Здесь ты сможешь получить аналитическую информацию по транзакциям\n"
                    "за время с начала введённого тобой месяца; курсы валют\n"
                    "и цены на отслеживаемые акции"
                )
                # Дату можно вводить в любом формате
                user_date = input("Введи дату с 01.01.2018 по 31.12.2021 :\n").strip()
                general_report = general_function(user_date)

                separation()
                pp(general_report, depth=3, sort_dicts=False, indent=2)
                print("Отчёт о работе записан в файл 'general_page.json' в директории 'reports_record'")
                separation()

                sleep(1)

            case "2":
                print("Добро пожаловать в Простой поиск!")
                print("Сервис осуществляет поиск транзакций по выражению в 'описании' или в 'категории'.")
                print(select_category)
                user_category = input().strip()

                simple_search(categories[int(user_category)])
                print("Отчёт о работе записан в файл 'simple_search.json' в директории 'reports_record'")
                separation()
                sleep(1)

            case "3":
                print(
                    "Это раздел Отчёты, мой друг! Тебе доступна информация о тратах\n"
                    "в любой категории за трёхмесячный период до введённой тобой даты"
                )
                print(select_category)
                user_category = input().strip()
                user_date = input("Введи дату с 01.01.2018 по 31.12.2021 :\n").strip()

                # Добавим функции возможность записи отчёта в JSON-файл,
                # название которого можно дописать вторым аргументом при декорировании
                spending_by_category_def = DecorCategory(spending_by_category)
                job_df = reader_files()
                spending_by_category_def(job_df, categories[int(user_category)], user_date)

                print("Отчёт о работе записан в файл 'category_default.json' в директории 'reports_record'")
                separation()
                sleep(1)

            case "4":
                print("Всего хорошего!")
                return

            case _:
                print(negative_loop_message)
                sleep(1)


if __name__ == "__main__":
    main()
