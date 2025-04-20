class MyError(Exception):
    """
    Создаёт экземпляр пользовательской ошибки, расширяет класс исключений Exeption.
    """

    def __init__(self, *args: tuple | str) -> None:
        """
        Инициализирует новый экземпляр класса
        """
        self.message = args[0] if args else None

    def __str__(self) -> str:
        """
        Возвращает строку с информацией для пользователя об экземпляре класса.
        """
        if self.message:
            return f"Ошибка: {self.message}."
        else:
            return "Ошибка ввода."
