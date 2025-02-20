import logging
import os
import shutil
from dataclasses import dataclass
from enum import Enum

from app.libs.types import Path


@dataclass
class FormException(Exception):
    """Базовая форма для исключений."""

    message: str

    def __str__(self) -> str:
        """Строковое представление исключения."""
        return self.message

class StringEnum(str, Enum):
    """Базовая форма для энумерации."""

    def __str__(self) -> str:
        """Магический метод возвращения строкового представления.

        Returns:
            Строковое представление.
        """
        return str.__str__(self)


def setup_logging(level=logging.INFO, **kwargs) -> logging.Logger:
    """Функция логирования.

    Args:
        level: Уровень логирования для установки.
        **kwargs: Дополнительные именованные аргументы для настройки логирования.

    Returns:
        Объект логгера для регистрации сообщений.
    """
    logging.basicConfig(level=level, **kwargs)
    logger = logging.getLogger(__name__)
    return logger


def is_file_exists(file_path: str) -> bool:
    """Функция проверки существования файла.

    Args:
        file_path: Путь до файла.

    Returns:
        Утверждение существует ли файл.
    """
    return os.path.isfile(file_path)


def get_current_path() -> Path:
    """Функция для получения текущего пути.

    Returns:
        Текущий путь.
    """
    return os.getcwd()


def remove_file_or_folder(file_or_folder_path: str) -> None:
    """Функция удаления файла или папки.

    Args:
        file_or_folder_path: Путь до файла или папки.
    """
    if is_file_exists(file_or_folder_path):
        if os.path.isfile(file_or_folder_path):
            os.remove(file_or_folder_path)
            return
        shutil.rmtree(file_or_folder_path)


def merge_path_elements(path_parts: list[str]) -> Path:
    """Функция формирования пути.

    Args:
        path_parts: Части пути в виде словоря.

    Returns:
        Сформированный путь.
    """
    return os.path.join(*path_parts).__str__()
