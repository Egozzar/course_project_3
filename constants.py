from typing import Final
import os

# Универсальный адрес корня проекта
ROOT_PATH: Final[str] = os.path.dirname(__file__)

#pytest --cov=src --cov-report=html -генерация отчета о покрытии в HTML-формате
