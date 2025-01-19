from unittest import TestCase
from unittest.mock import patch

from psd_tools import PSDImage

from app.base.common.general import merge_path_elements, get_current_path, remove_file_or_folder, is_file_exists
from app.base.common.image import Image, ImageCV
from app.base.types import Path, ImgPath, ImgMatrix, ImgSavePath, ImgSize


class TestImage(TestCase):

    def setUp(self) -> None:
        self.dir_data_path: Path = merge_path_elements([get_current_path(), "app", "tests", "data"])
        self.img_path: ImgPath = merge_path_elements([self.dir_data_path, "template_test.psd"])

        self.instance = Image()
        self.exception = self.instance.exception
        self.messages = self.instance.messages

    def test_open_image(self) -> None:
        with self.subTest("Open image"):
            self.assertIsInstance(self.instance.open_image( self.img_path), PSDImage)

        with self.subTest("Invalid image path"), self.assertRaises(self.exception) as e:
            _ = self.instance.open_image("test")
        self.assertEqual(self.messages.INVALID_IMG_PATH_ERROR, e.exception.message)

    def test_convert_format_image(self) -> None:
        img_path: ImgPath =  self.img_path
        save_img_path: ImgPath = img_path.replace(".psd", ".png")

        remove_file_or_folder(save_img_path)
        with self.subTest("Convert format from psd to png"):
            self.assertEqual(save_img_path, self.instance.convert_format_image(img_path))
        remove_file_or_folder(save_img_path)

        with self.subTest("Unknown from format"), self.assertRaises(self.exception) as e:
            _ = self.instance.convert_format_image(img_path, from_format="test")
        self.assertEqual(self.messages.UNKNOWN_FROM_FORMAT_ERROR, e.exception.message)

        with self.subTest("Unknown to format"), self.assertRaises(self.exception) as e:
            _ = self.instance.convert_format_image(img_path, to_format="test")
        self.assertEqual(self.messages.UNKNOWN_TO_FORMAT_ERROR, e.exception.message)

        with (
            self.subTest("Image composite error"),
            patch('psd_tools.PSDImage.composite', side_effect=Exception("Mocked composite error")),
            self.assertRaises(self.exception) as e,
        ):
            _ = self.instance.convert_format_image(img_path)
        self.assertIn(self.messages.IMG_COMPOSITE_ERROR[:-10], e.exception.message)


class TestImageCV(TestCase):

    def setUp(self) -> None:
        self.dir_data_path: Path = merge_path_elements([get_current_path(), "app", "tests", "data"])
        self.img_with_text_path = merge_path_elements([self.dir_data_path, 'img_page_test.png'])

        self.instance = ImageCV()
        self.exception = self.instance.exception
        self.messages = self.instance.messages

    def test_open_image(self) -> None:
        with self.subTest("Read image"):
            self.assertIsInstance(self.instance.read_image(self.img_with_text_path), ImgMatrix)

        with self.subTest("Invalid image path"), self.assertRaises(self.exception) as e:
            _ = self.instance.read_image("test")
        self.assertEqual(self.messages.INVALID_IMG_PATH_ERROR, e.exception.message)

    def test_save_image(self) -> None:
        save_path: Path = merge_path_elements([self.dir_data_path, 'test_img.png'])
        img_matrix: ImgMatrix = self.instance.read_image(self.img_with_text_path)

        remove_file_or_folder(save_path)
        with self.subTest("Save image"):
            self.assertIsInstance(self.instance.save_image(img_matrix, save_path), ImgSavePath)
        remove_file_or_folder(save_path)

        with self.subTest("Image type error"), self.assertRaises(self.exception) as e:
            _ = self.instance.save_image("test", save_path)
        self.assertEqual(self.messages.IMG_MATRIX_TYPE_ERROR, e.exception.message)

        with self.subTest("Image save path error"), self.assertRaises(self.exception) as e:
            _ = self.instance.save_image(img_matrix, None)
        self.assertEqual(self.messages.INVALID_IMG_SAVE_PATH_ERROR, e.exception.message)

    def test_resize_image(self) -> None:
        img_matrix: ImgMatrix = self.instance.read_image(self.img_with_text_path)
        img_size: ImgSize = (500, 500)

        with self.subTest("Resize image"):
            old_size = img_matrix.shape
            new_size = self.instance.resize_image(img_matrix, img_size).shape
            self.assertTrue(old_size != new_size)

        with self.subTest("Image type error"), self.assertRaises(self.exception) as e:
            _ = self.instance.resize_image(None, img_size)
        self.assertEqual(self.messages.IMG_MATRIX_TYPE_ERROR, e.exception.message)

        with self.subTest("Size error"), self.assertRaises(self.exception) as e:
            _ = self.instance.resize_image(img_matrix, None)
        self.assertEqual(self.messages.IMG_SIZE_TYPE_ERROR, e.exception.message)

    def test_convert_image_to_grayscale(self) -> None:
        img_matrix: ImgMatrix = self.instance.read_image(self.img_with_text_path)

        with self.subTest("Convert image to white-black format"):
            img_grayscale = self.instance.convert_image_to_grayscale(img_matrix)
            self.assertEqual(2, len(img_grayscale.shape))

        with self.subTest("Image type error"), self.assertRaises(self.exception) as e:
            _ = self.instance.convert_image_to_rgb("test")
        self.assertEqual(self.messages.IMG_MATRIX_TYPE_ERROR, e.exception.message)

    def test_convert_image_to_rgb(self) -> None:
        img_matrix: ImgMatrix = self.instance.read_image(self.img_with_text_path)

        img_grayscale = self.instance.convert_image_to_grayscale(img_matrix)
        with self.subTest("Convert image to RGB-format"):
            self.assertEqual(2, len(img_grayscale.shape))

            img_rgb = self.instance.convert_image_to_rgb(img_grayscale)
            self.assertEqual(3, len(img_rgb.shape))

        with self.subTest("Image type error"), self.assertRaises(self.exception) as e:
            _ = self.instance.convert_image_to_rgb("test")
        self.assertEqual(self.messages.IMG_MATRIX_TYPE_ERROR, e.exception.message)

    def test_is_images_the_same_pixels(self):
        img_text_path: Path = merge_path_elements([self.dir_data_path, 'img_with_text_test.png'])
        img_text_hided_path: Path = merge_path_elements([self.dir_data_path, 'img_with_text_hided.png'])

        img_text_matrix: ImgMatrix = self.instance.read_image(img_text_path)
        img_text_hided_matrix: ImgMatrix = self.instance.read_image(img_text_hided_path)

        with self.subTest("The same images, matrix"):
            self.assertTrue(self.instance.is_images_the_same_pixels(img_text_matrix, img_text_matrix))

        with self.subTest("Different images, matrix"):
            self.assertFalse(self.instance.is_images_the_same_pixels(img_text_matrix, img_text_hided_matrix))

        with self.subTest("The same images, path"):
            self.assertTrue(self.instance.is_images_the_same_pixels(img_text_path, img_text_path))

        with self.subTest("Different images, path"):
            self.assertFalse(self.instance.is_images_the_same_pixels(img_text_path, img_text_hided_path))

        with self.subTest("Incorrect image type"), self.assertRaises(self.exception) as e:
            _ = self.instance.is_images_the_same_pixels(None, img_text_path)
        self.assertEqual(self.messages.IMG_IS_SAME_TYPE_ERROR, e.exception.message)

    def test_found_and_hide_text_on_image(self):
        with self.subTest("Found and hide text on image"):
            img_path_before: Path = self.img_with_text_path
            img_path_after: Path = merge_path_elements([self.dir_data_path, 'img_page_test_text_hided.png'])

            self.instance.found_and_hide_text_on_image(img_path_before, save_path=img_path_after)
            self.assertTrue(is_file_exists(img_path_after))

            img_matrix_before: ImgMatrix = self.instance.read_image(img_path_before)
            img_matrix_after: ImgMatrix = self.instance.read_image(img_path_after)

            self.assertFalse(self.instance.is_images_the_same_pixels(img_matrix_before, img_matrix_after))
