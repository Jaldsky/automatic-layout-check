from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import NoReturn

from app.libs.exceptions import PlayWrightActionException, PlayWrightActionMessages
from app.libs.types import Driver, Browser, Config, PageLocator, PlayWrightPage, ScreenSavePath


class WebDriver(ABC):
    """Класс веб-драйвера."""

    def __init__(self, driver: Driver) -> None:
        """Инициализация параметров для запуска."""
        self._driver: Driver = driver
        self._browser: Browser | None = None

    @abstractmethod
    def browser(self) -> Browser:
        """Метод возвращения экземпляра браузера.

        Returns:
            Экземпляр браузера.
        """

    @abstractmethod
    def initialize_browser(self, configure: Config) -> None:
        """Метод инициализации браузера."""


@dataclass
class PlaywrightSettings:
    """Класс playwright веб-драйвера с настройками."""

    headless: bool = True
    args: list[str] = field(default_factory=lambda: ["--start-maximized"])
    ignore_default_args: list[str] = field(default_factory=lambda: ["--mute-audio", "--disable-gpu"])

    def __str__(self) -> Config:
        """Магический метод возвращения строкового представления.

        Returns:
            Возвращение строкового представления в виде словаря настроек.
        """
        return self.__dict__


class PlayWrightBrowser(WebDriver):
    """Класс playwright веб-драйвера."""

    exception = PlayWrightActionException
    messages = PlayWrightActionMessages

    def __init__(self, driver: Driver, configure: 'PlaywrightSettings' = None):
        """Инициализация параметров для запуска."""
        super().__init__(driver)
        self.initialize_browser(configure.__dict__)

    def initialize_browser(self, configure: Config) -> None:
        """Метод инициализации браузера.

        Args:
            configure: Настройки для инициализации барузера.
        """
        try:
            self._browser = self._driver.chromium.launch(**configure)
        except Exception as e:
            raise self.exception(self.messages.BROWSER_LAUNCH_ERROR.format(msg=e.__str__()))

    @property
    def browser(self) -> Browser:
        """Свойство получения экземпляра браузера.

        Returns:
            Экземпляр браузера.
        """
        browser: Browser = self._browser
        if not browser:
            raise self.exception(self.messages.INITIALIZE_BROWSER_ERROR)
        return browser

    @property
    def new_page(self) -> PlayWrightPage | NoReturn:
        """Свойство получения экземпляра новой страницы браузера.

        Returns:
            Экземпляр страницы браузера.
        """
        if not self._browser:
            raise self.exception(self.messages.INITIALIZE_BROWSER_ERROR)
        return self.browser.new_page()


class PlayWrightAction(PlayWrightBrowser):
    """Класс для взаимодействия с playwright."""

    def __init__(self, driver: Driver, configure: 'PlaywrightSettings' = None):
        """Инициализация параметров для запуска."""
        super().__init__(driver, configure)

    def goto_page(self, page: PlayWrightPage, url: PageLocator) -> PageLocator:
        """Метод перехода на страницу.

        Args:
            page: Инициализированная страница.
            url: Локатор страницы.

        Returns:
            Локатор страницы.
        """
        if not page:
            raise self.exception(self.messages.INITIALIZE_PAGE_ERROR)
        if not isinstance(url, PageLocator):
            raise self.exception(self.messages.PAGE_TYPE_LOCATOR_ERROR)
        try:
            page.goto(url)
            return url
        except Exception as e:
            raise self.exception(self.messages.PAGE_LOCATOR_ERROR.format(msg=e.__str__()))

    def get_screenshot_page(
            self,
            page: PlayWrightPage,
            url: PageLocator,
            screen_save_path: ScreenSavePath,
            full_page: bool = True
    ) -> ScreenSavePath | NoReturn:
        """Метод получения скриншота страницы.

        Args:
            page: Инициализированная страница.
            url: Локатор страницы.
            screen_save_path: Пусть для сохранения скриншота.
            full_page: сохранить страницу целиком.

        Returns:
            Пусть до сохраненной страницы.
        """
        if not isinstance(page, PlayWrightPage):
            raise self.exception(self.messages.PAGE_TYPE_ERROR)
        self.goto_page(page, url)
        try:
            page.screenshot(path=screen_save_path, full_page=full_page)
            return screen_save_path
        except Exception as e:
            raise self.exception(self.messages.GET_SCREENSHOT_PAGE_ERROR.format(msg=e.__str__()))
