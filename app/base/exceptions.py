from app.base.common.general import FormException, StringEnum


class PlayWrightActionException(FormException):
    """Исключение PlayWrightAction."""


class PlayWrightActionMessages(StringEnum):
    """Сообщения для класса PlayWright."""

    INITIALIZE_BROWSER_ERROR: str = "Браузер не инициализирован!"
    INITIALIZE_PAGE_ERROR: str = "Страница браузера не инициализирован!"
    BROWSER_LAUNCH_ERROR: str = "Ошибка при запуске браузера: {msg}!"
    PAGE_TYPE_LOCATOR_ERROR: str = "Некорректный тип локатора страницы!"
    PAGE_LOCATOR_ERROR: str = "Ошибка при переходе на страницу браузера: {msg}!"
    PAGE_TYPE_ERROR: str = "Неверный тип страницы!"
    GET_SCREENSHOT_PAGE_ERROR: str = "Ошибка при получении скриншота страницы: {msg}!"


class ImageException(FormException):
    """Исключение Image."""


class ImageMessages(StringEnum):
    """Сообщения для класса PlayWright."""

    UNKNOWN_FROM_FORMAT_ERROR: str = "Не поддерживаемый формат изображения!"
    UNKNOWN_TO_FORMAT_ERROR: str = "Не поддерживаемый формат для конвертации!"
    INVALID_IMG_PATH_ERROR: str = "Некорректный путь к изображению!"
    IMG_PERMISSION_ERROR: str = "Недостаточно прав для работы с изображением!"
    IMG_OPEN_ERROR: str = "Ошибка при открытии изображения: {msg}!"
    IMG_COMPOSITE_ERROR: str = "Ошибка при компоновке изображения: {msg}!"
    IMG_SAVE_ERROR: str = "Ошибка при сохранении изображения: {msg}!"


class ImageCVException(FormException):
    """Исключение ImageCV."""


class ImageCVMessages(StringEnum):
    """Сообщения для класса ImageCV."""

    INVALID_IMG_PATH_ERROR: str = "Некорректный путь к изображению!"
    INVALID_IMG_SAVE_PATH_ERROR: str = "Некорректный путь для сохранения изображения!"
    IMG_PERMISSION_ERROR: str = "Недостаточно прав для работы с изображением!"
    IMG_MATRIX_TYPE_ERROR: str = "Ошибка типа изображения!"
    IMG_IS_SAME_TYPE_ERROR: str = "Ошибка типа при сравнении изображений!"
    IMG_SIZE_TYPE_ERROR: str = "Ошибка типа изменения изображения!"
    IMG_READ_ERROR: str = "Ошибка при считывании изображения: {msg}!"
    IMG_SAVE_ERROR: str = "Ошибка при сохранении изображения: {msg}!"
    IMG_RESIZE_ERROR: str = "Ошибка при изменении разрешения изображения: {msg}!"
    IMG_CONVERT_RGB_ERROR: str = "Ошибка при конвертации изображения к RGB-формату: {msg}!"
    IMG_CONVERT_GRAYSCALE_ERROR: str = "Ошибка при конвертации изображения к черно-белому: {msg}!"
    IMG_FOUND_AND_HIDE_TEXT_ERROR: str = "Ошибка при поиске и закраски текста на изображении: {msg}!"

class ComparatorException(FormException):
    """Исключение Comparator."""


class ComparatorMessages(StringEnum):
    """Сообщения для класса Comparator."""

    INVALID_IMG_TYPE_ERROR: str = "Некорректный тип изображения!"
    PREPARE_IMG_TYPE_ERROR: str = "Ошибка типа при подготовке к сравнению изображений!"
    PREPARE_IMG: str = "Подготовка изображения к сравнению..."
    RESULT_COMPARATOR: str = "Изображения похожи на {percent} процента"


class ModelManagerException(FormException):
    """Исключение ModelManager."""


class ModelManagerMessages(StringEnum):
    """Сообщения для класса ModelManager."""

    INVALID_MODEL_NAME_TYPE_ERROR: str = "Некорректный тип имени модели!"
    EMPTY_KWARGS_ERROR: str = "Отсутствуют аргументы фильтрации!"

    GET_MODEL_ERROR: str = "Ошибка во время получения модели: {msg}"
    DELETE_RECORD_ERROR: str = "Ошибка во время удаления записи: {msg}"
    GET_OR_CREATE_RECORD_ERROR: str = "Ошибка во время создания/получения записи: {msg}"
    GET_ALL_RECORDS_ERROR: str = "Ошибка во время получения всех записей в таблице: {msg}"
