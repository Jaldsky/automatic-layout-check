from unittest import TestCase
from unittest.mock import Mock, patch

from playwright.sync_api import sync_playwright

from app.libs.common.general import remove_file_or_folder, is_file_exists, merge_path_elements, get_current_path
from app.libs.common.web_driver import PlayWrightAction, PlaywrightSettings
from app.libs.types import Browser, PlayWrightPage, PageLocator, ScreenSavePath, Path


class TestPlaywright(TestCase):

    def setUp(self) -> None:
        self.exception = PlayWrightAction.exception
        self.messages = PlayWrightAction.messages

    def test_browser(self):
        with self.subTest("Valid config args"), sync_playwright() as pwa:
            action = PlayWrightAction(pwa, PlaywrightSettings())
            self.assertIsInstance(action.browser, Browser)

        with (
            self.subTest("Browser not initialized"),
            sync_playwright() as pwa,
            self.assertRaises(self.exception) as e,
            patch.object(PlayWrightAction, 'initialize_browser', new=Mock(return_value=None))
        ):
            action = PlayWrightAction(pwa, PlaywrightSettings())
            _ = action.browser
        self.assertEqual(self.messages.INITIALIZE_BROWSER_ERROR, e.exception.message)

        with (
            self.subTest("Invalid config args"),
            sync_playwright() as pwa,
            self.assertRaises(self.exception) as e,
            PlayWrightAction(pwa, PlaywrightSettings(headless=0)),
        ):
            _ = pwa
        self.assertIn(self.messages.BROWSER_LAUNCH_ERROR[:-10], e.exception.message)

    def test_new_page(self):
        with (
            self.subTest("Get new page"),
            sync_playwright() as pwa,
        ):
            action = PlayWrightAction(pwa, PlaywrightSettings())
            self.assertIsInstance(action.new_page, PlayWrightPage)

        with (
            self.subTest("Browser not initialized for using page"),
            sync_playwright() as pwa,
            self.assertRaises(self.exception) as e,
            patch.object(PlayWrightAction, 'initialize_browser', new=Mock(return_value=None))
        ):
            action = PlayWrightAction(pwa, PlaywrightSettings())
            _ = action.new_page
        self.assertEqual(self.messages.INITIALIZE_BROWSER_ERROR, e.exception.message)

    def test_goto_page(self):
        with (
            self.subTest("Go to page"),
            sync_playwright() as pwa,
        ):
            action = PlayWrightAction(pwa, PlaywrightSettings())
            page = action.new_page
            url: PageLocator = "https://www.google.com/"
            self.assertEqual(url, action.goto_page(page, url))

        with (
            self.subTest("Invalid locator"),
            sync_playwright() as pwa,
            self.assertRaises(self.exception) as e
        ):
            action = PlayWrightAction(pwa, PlaywrightSettings())
            page = action.new_page
            _ = action.goto_page(page, "test")
        self.assertIn(self.messages.PAGE_LOCATOR_ERROR[:-10], e.exception.message)

        with (
            self.subTest("Invalid locator"),
            sync_playwright() as pwa,
            self.assertRaises(self.exception) as e
        ):
            action = PlayWrightAction(pwa, PlaywrightSettings())
            page = action.new_page
            _ = action.goto_page(page, "test")
        self.assertIn(self.messages.PAGE_LOCATOR_ERROR[:-10], e.exception.message)


    def test_get_screenshot_page(self):
        dir_tests_path: Path = merge_path_elements([get_current_path(), "app", "tests", "base", "common"])
        screen_save_path: ScreenSavePath = merge_path_elements([dir_tests_path, "screenshot.png"])
        url: PageLocator = "https://www.google.com/"

        with (
            self.subTest("Got screenshot page"),
            sync_playwright() as pwa,
        ):
            action = PlayWrightAction(pwa, PlaywrightSettings())
            page = action.new_page

            remove_file_or_folder(screen_save_path)
            self.assertEqual(screen_save_path, action.get_screenshot_page(page, url, screen_save_path))
            self.assertTrue(is_file_exists(screen_save_path))
            remove_file_or_folder(screen_save_path)

        with (
            self.subTest("Incorrect page type"),
            sync_playwright() as pwa,
            self.assertRaises(self.exception) as e

        ):
            action = PlayWrightAction(pwa, PlaywrightSettings())
            page = action.new_page.goto(url)

            _ = action.get_screenshot_page(page, url, screen_save_path)

        self.assertEqual(self.messages.PAGE_TYPE_ERROR, e.exception.message)
