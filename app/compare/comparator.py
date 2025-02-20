from abc import ABC
from dataclasses import dataclass
from typing import Any

import numpy as np
from keras.src.applications.vgg16 import VGG16, preprocess_input
from skimage.metrics import structural_similarity
from sklearn.metrics.pairwise import cosine_similarity

from app.libs.common.general import setup_logging, StringEnum
from app.libs.common.image import ImageCV
from app.libs.exceptions import ComparatorException, ComparatorMessages
from app.libs.types import (
    ImgPath,
    Similarity,
    ImgMatrix,
    ComparatorResult,
    SimilarityResult,
    ImgSize,
    ToGrayscale,
    FeatureMatrix
)

class IsSimilar(StringEnum):
    YES: str = "yes"
    NO: str = "no"


@dataclass
class ComparatorData:
    """Класс с данными для класса Comparator."""
    img_first: ImgPath | ImgMatrix
    img_second: ImgPath | ImgMatrix


class ComparatorBase(ComparatorData, ABC):
    """Базовый класс сравнения."""
    exception = ComparatorException
    messages = ComparatorMessages

    def __init__(self, **kwargs: Any) -> None:
        """Инициализация параметров для запуска."""
        super().__init__(**kwargs)
        self._logger = setup_logging()
        self._validate_params()

    def _validate_params(self) -> None:
        self._validate_img(self.img_first)
        self._validate_img(self.img_second)

    def _validate_img(self, img: Any) -> None:
        """Метод для валидации значения изображения."""
        if not isinstance(img, (ImgPath, ImgMatrix)):
            raise self.exception(self.messages.INVALID_IMG_TYPE_ERROR)


class Comparator(ComparatorBase):
    """Класс сравнения.
    Для начала сравнения двух изображений необходимо:
    1. Представить изображения в виде попиксельной матрицы.
    2. Преобразовать цветные изображения в черно-белые.
    3. Привести изображения к одному и тому же размеру.
    После этого уже проводить сравнения.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Инициализация параметров для запуска."""
        super().__init__(**kwargs)
        self.image_cv: ImageCV = ImageCV()

    def get_image_matrix(self, img: ImgPath | ImgMatrix) -> ImgMatrix:
        """Метод выполнения основной логики сравнения двух изображений на схожесть.

        Args:
            img: Путь до изображения или матрица изображения.

        Returns:
            Матрица изображения.
        """
        if not isinstance(img, (ImgPath, ImgMatrix)):
            raise self.exception(self.messages.PREPARE_IMG_TYPE_ERROR)
        return self.image_cv.read_image(img) if isinstance(img, ImgPath) else img

    def normalize_image_size(self, img_matrix_first, img_matrix_second) -> tuple[ImgMatrix, ImgMatrix]:
        """Метод нормализации размера изображений.

        Args:
            img_matrix_first: Матрица первого изображения.
            img_matrix_second: Матрица второго изображения.

        Returns:
            Кортеж с матрицей первого нормализированного изображения и второго.
        """
        img_first_shape = img_matrix_first.shape
        img_second_shape = img_matrix_first.shape
        if img_first_shape[0] * img_first_shape[1] < img_second_shape[0] * img_second_shape[1]:
            img_matrix_second = self.image_cv.resize_image(img_matrix_second, (img_first_shape[1], img_first_shape[0]))
        else:
            img_matrix_first = self.image_cv.resize_image(img_matrix_first, (img_second_shape[1], img_second_shape[0]))
        return img_matrix_first, img_matrix_second

    def prepare_images(
            self,
            img_shape: ImgSize | None = None,
            to_grayscale: ToGrayscale = True
    ) -> tuple[ImgMatrix, ImgMatrix]:
        """Метод подготовки изображений для сравнения.

        Args:
            img_shape: Размер изображения.
            to_grayscale: Преобразовать изображения в черно-белые.

        Returns:
            Кортеж с матрицей первого и второго изображений.
        """
        self._logger.info(self.messages.PREPARE_IMG)
        # transformation into matrix
        img_matrix_first: ImgMatrix = self.get_image_matrix(self.img_first)
        img_matrix_second: ImgMatrix = self.get_image_matrix(self.img_second)

        if to_grayscale:
            # convert to grayscale
            img_matrix_first: ImgMatrix = self.image_cv.convert_image_to_grayscale(img_matrix_first)
            img_matrix_second: ImgMatrix = self.image_cv.convert_image_to_grayscale(img_matrix_second)

        # normalize size
        if img_shape:
            img_matrix_first = self.image_cv.resize_image(img_matrix_first, img_shape)
            img_matrix_second = self.image_cv.resize_image(img_matrix_second, img_shape)
            return img_matrix_first, img_matrix_second

        if img_matrix_first.shape[0] * img_matrix_first.shape[1] < img_matrix_second.shape[0] * img_matrix_second.shape[1]:
            img_matrix_second = self.image_cv.resize_image(img_matrix_second, (img_matrix_first.shape[1], img_matrix_first.shape[0]))
        else:
            img_matrix_first = self.image_cv.resize_image(img_matrix_first, (img_matrix_second.shape[1], img_matrix_second.shape[0]))

        return img_matrix_first, img_matrix_second

    def return_comparison_results(self, result: SimilarityResult, similarity: Similarity) -> ComparatorResult:
        """Метод форматирования результатов сравнения.

        Args:
            result: Результат сравнения.
            similarity: Порог схожести.

        Returns:
            Результат сравнения в виде словаря.
        """
        percent: float = result * 100
        is_similar: str = IsSimilar.YES if result >= similarity else IsSimilar.NO
        results: ComparatorResult = {"is_similar": is_similar, "percent": percent}
        self._logger.info(self.messages.RESULT_COMPARATOR.format(percent=percent))
        return results

    def compare_by_mean_squared_error(self, similarity: Similarity = 0.85) -> ComparatorResult:
        """Метод определения схожести изображений по методу среднеквадратичной ошибки (Mean Squared Error - MSE).

        Args:
            similarity: Порог схожести.

        Returns:
            Результат сравнения в виде словаря.
        """
        img_first, img_second = self.prepare_images()
        if self.image_cv.is_images_the_same_pixels(img_first, img_second):
            return {"is_similar": IsSimilar.YES, "percent": 100.0}

        error = np.sum((img_first.astype("float") - img_second.astype("float")) ** 2)
        error /= float(img_first.shape[0] * img_first.shape[1])
        result: SimilarityResult = round(1 - error / 255**2, 2).item()

        return self.return_comparison_results(result, similarity)

    def compare_by_structural_similarity_index(self, similarity: Similarity = 0.55) -> ComparatorResult:
        """Метод определения схожести изображений по методу измерения индекса структурного сходства
        (Structural Similarity Index Measure - SSIM).

        Args:
            similarity: Порог схожести.

        Returns:
            Результат сравнения в виде словаря.
        """
        img_first, img_second = self.prepare_images()
        if self.image_cv.is_images_the_same_pixels(img_first, img_second):
            return {"is_similar": IsSimilar.YES, "percent": 100.0}

        result: np.float64 | float = structural_similarity(img_first, img_second)
        result: SimilarityResult = round(result, 2).item() if not isinstance(result, float) else result

        return self.return_comparison_results(result, similarity)

    def compare_by_neural_network_vgg16(self, similarity: Similarity = 0.85) -> ComparatorResult:
        """Метод определения схожести изображений на основе сверточной нейросети VGG16).

        Args:
            similarity: Порог схожести.

        Returns:
            Результат сравнения в виде словаря.
        """
        img_first, img_second = self.prepare_images(img_shape=(224, 224), to_grayscale=False)
        if self.image_cv.is_images_the_same_pixels(img_first, img_second):
            return {"is_similar": IsSimilar.YES, "percent": 100.0}

        img_first: ImgMatrix = np.expand_dims(img_first, axis=0)
        img_second: ImgMatrix = np.expand_dims(img_second, axis=0)

        img_first: ImgMatrix = preprocess_input(img_first)
        img_second: ImgMatrix = preprocess_input(img_second)

        model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

        img_first_feature: FeatureMatrix = model.predict(img_first).reshape(1, -1)
        img_second_feature: FeatureMatrix = model.predict(img_second).reshape(1, -1)

        result: SimilarityResult = cosine_similarity(img_first_feature, img_second_feature)[0][0]

        return self.return_comparison_results(result, similarity)
