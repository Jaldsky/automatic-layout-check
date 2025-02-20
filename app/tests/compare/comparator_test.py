from unittest import TestCase
from unittest.mock import patch, Mock

from PIL import ImagePath

from app.libs.common.general import merge_path_elements, get_current_path
from app.libs.types import Path, ImgMatrix
from app.compare.comparator import Comparator, IsSimilar


class TestComparator(TestCase):

    def setUp(self) -> None:
        self.dir_data_path: Path = merge_path_elements([get_current_path(), "app", "tests", "data"])

        self.img_with_text_path: Path = merge_path_elements([self.dir_data_path, 'img_with_text.png'])
        self.img_with_text_hided_path: Path = merge_path_elements([self.dir_data_path, 'img_with_text_hided.png'])
        self.img_page_path: Path = merge_path_elements([self.dir_data_path, 'img_page.png'])

        with patch.object(Comparator, "_validate_params", new=Mock(return_value=None)):
            self.instance = Comparator(img_first=self.img_with_text_path, img_second=self.img_with_text_hided_path)
            self.exception = self.instance.exception
            self.messages = self.instance.messages

    def test__validate_img(self) -> None:
        with self.subTest("Valid img"):
            self.assertIsNone(self.instance._validate_img(img=self.img_with_text_path))

        with self.subTest("Invalid img"), self.assertRaises(self.exception) as e:
            self.instance._validate_img(img=None)
        self.assertEquals(e.exception.message, self.messages.INVALID_IMG_TYPE_ERROR)

    def test_get_image_matrix(self) -> None:
        with self.subTest("Get image matrix"):
            self.assertIsInstance(self.instance.get_image_matrix(self.img_with_text_path), ImgMatrix)

        with self.subTest("Invalid img type"), self.assertRaises(self.exception) as e:
            _ = self.instance.get_image_matrix(None)
        self.assertEqual(self.messages.PREPARE_IMG_TYPE_ERROR, e.exception.message)

    def test_prepare_images(self) -> None:
        img_first_path: ImagePath = self.img_with_text_path
        img_second_path: ImagePath = self.img_with_text_hided_path

        img_first_before: ImgMatrix = self.instance.get_image_matrix(img_first_path)
        img_second_before: ImgMatrix = self.instance.get_image_matrix(img_second_path)

        img_first_after, img_second_after = Comparator(
            img_first=img_first_path, img_second=img_second_path
        ).prepare_images()

        # check type
        self.assertIsInstance(img_first_after, ImgMatrix)
        self.assertIsInstance(img_second_after, ImgMatrix)

        # check grayscale
        self.assertEqual(3, len(img_first_before.shape))
        self.assertEqual(2, len(img_first_after.shape))
        self.assertEqual(3, len(img_second_before.shape))
        self.assertEqual(2, len(img_second_after.shape))

        # check size
        self.assertTrue(img_first_before.size != img_first_after.size)
        self.assertTrue(img_second_before.size != img_second_after.size)

    def test_compare_by_mean_squared_error(self):
        img_first_path: ImagePath = self.img_with_text_path
        img_second_path: ImagePath = self.img_with_text_hided_path
        img_third_path: ImagePath = self.img_page_path

        with self.subTest("Same images"):
            results = Comparator(img_first=img_first_path, img_second=img_first_path).compare_by_mean_squared_error()
            self.assertEqual(IsSimilar.YES, results["is_similar"])
            self.assertEqual(100.0, results["percent"])

        with self.subTest("Bit similar"):
            results = Comparator(img_first=img_first_path, img_second=img_second_path).compare_by_mean_squared_error()
            self.assertEqual(IsSimilar.YES, results["is_similar"])
            self.assertEqual(93.0, results["percent"])

        with self.subTest("Very different"):
            results = Comparator(img_first=img_first_path, img_second=img_third_path).compare_by_mean_squared_error()
            self.assertEqual(IsSimilar.NO, results["is_similar"])
            self.assertEqual(74.0, results["percent"])

    def test_compare_by_structural_similarity_index(self):
        img_first_path: ImagePath = self.img_with_text_path
        img_second_path: ImagePath = self.img_with_text_hided_path
        img_third_path: ImagePath = self.img_page_path

        with self.subTest("Same images"):
            results = Comparator(
                img_first=img_first_path, img_second=img_first_path
            ).compare_by_structural_similarity_index()
            self.assertEqual(IsSimilar.YES, results["is_similar"])
            self.assertEqual(100.0, results["percent"])

        with self.subTest("Bit similar"):
            results = Comparator(
                img_first=img_first_path, img_second=img_second_path
            ).compare_by_structural_similarity_index()
            self.assertEqual(IsSimilar.YES, results["is_similar"])
            self.assertTrue(results["percent"] > 55.0)

        with self.subTest("Very different"):
            results = Comparator(
                img_first=img_first_path, img_second=img_third_path
            ).compare_by_structural_similarity_index()
            self.assertEqual(IsSimilar.NO, results["is_similar"])
            self.assertTrue(results["percent"] < 55.0)

    def test_compare_by_neural_network_vgg16(self):
        img_first_path: ImagePath = self.img_with_text_path
        img_second_path: ImagePath = self.img_with_text_hided_path
        img_third_path: ImagePath = self.img_page_path

        with self.subTest("Same images"):
            results = Comparator(
                img_first=img_first_path, img_second=img_first_path
            ).compare_by_neural_network_vgg16()
            self.assertEqual(IsSimilar.YES, results["is_similar"])
            self.assertEqual(100.0, results["percent"])

        with self.subTest("Different images"):
            results = Comparator(
                img_first=img_first_path, img_second=img_second_path
            ).compare_by_neural_network_vgg16()
            self.assertEqual(IsSimilar.NO, results["is_similar"])
            self.assertTrue(results["percent"] < 85.0)

        with self.subTest("Very different"):
            results = Comparator(
                img_first=img_first_path, img_second=img_third_path
            ).compare_by_neural_network_vgg16()
            self.assertEqual(IsSimilar.NO, results["is_similar"])
            self.assertTrue(results["percent"] < 85.0)
