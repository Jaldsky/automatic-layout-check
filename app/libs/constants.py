from app.libs.common.general import StringEnum

# TODO Вынести на уровень app

# text color coloring of words on the page, GREEN color
FILL_TEXT_COLOR = (0, 255, 0)  # GREEN color

class Language(StringEnum):
    """Класс с языками."""

    ENGLISH = 'en'
    RUSSIAN = 'ru'
