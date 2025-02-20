from typing import NoReturn

import cv2 as cv
from easyocr import easyocr
from psd_tools import PSDImage

from app.libs.common.general import is_file_exists
from app.libs.constants import Language, FILL_TEXT_COLOR
from app.libs.exceptions import ImageException, ImageMessages, ImageCVMessages, ImageCVException
from app.libs.types import ImgPath, FromFormatImg, ToFormatImg, ImgMatrix, ImgSavePath, ImgSize


class Image:
    exception = ImageException
    messages = ImageMessages

    def open_image(self, img_path: ImgPath) -> PSDImage | NoReturn:
        """Метод открытия изображения.

        Args:
            img_path: Путь до изображения.

        Returns:
            Объект изображения.
        """
        if not (isinstance(img_path, str) and is_file_exists(img_path)):
            raise self.exception(self.messages.INVALID_IMG_PATH_ERROR)
        try:
            return PSDImage.open(img_path)
        except (FileNotFoundError, IsADirectoryError):
            raise self.exception(self.messages.INVALID_IMG_PATH_ERROR)
        except PermissionError:
            raise self.exception(self.messages.IMG_PERMISSION_ERROR)

    def convert_format_image(
            self,
            img_path: ImgPath,
            save_img_path: ImgPath | None = None,
            from_format: FromFormatImg = "psd",
            to_format: ToFormatImg = "png"
    ) -> ImgPath | NoReturn:
        """Метод конвертации формата изображения.

        Args:
            img_path: Путь до изображения.
            save_img_path: Пусть сохранения изображения.
            from_format: Конвертация из формата.
            to_format: Конвертация в формат.
        """
        if from_format not in ("psd", ):
            raise self.exception(self.messages.UNKNOWN_FROM_FORMAT_ERROR)
        if to_format not in ("png", ):
            raise self.exception(self.messages.UNKNOWN_TO_FORMAT_ERROR)

        if from_format == "psd" and to_format == "png":
            try:
                file: PSDImage = self.open_image(img_path)
                file: PSDImage = file.composite()
                if not save_img_path:
                    save_img_path = img_path.replace(img_path.split(".")[-1], to_format)
                file.save(save_img_path)
                return save_img_path
            except Exception as e:
                if "composite" in e.__str__():
                    raise self.exception(self.messages.IMG_COMPOSITE_ERROR.format(msg=e.__str__()))
                if "save" in e.__str__():
                    raise self.exception(self.messages.IMG_SAVE_ERROR.format(msg=e.__str__()))


class ImageCV:
    exception = ImageCVException
    messages = ImageCVMessages

    def read_image(self, img_path: ImgPath) -> ImgMatrix | NoReturn:
        """Метод считывания изображения.

        Args:
            img_path: Путь до изображения.

        Returns:
            Объект изображения в виде попиксельной матрицы.
        """
        if not (isinstance(img_path, str) and is_file_exists(img_path)):
            raise self.exception(self.messages.INVALID_IMG_PATH_ERROR)
        try:
            return cv.imread(img_path)
        except (FileNotFoundError, IsADirectoryError):
            raise self.exception(self.messages.INVALID_IMG_PATH_ERROR)
        except PermissionError:
            raise self.exception(self.messages.IMG_PERMISSION_ERROR)
        except Exception as e:
            raise self.exception(self.messages.IMG_READ_ERROR.format(msg=e.__str__()))

    def save_image(self, img_matrix: ImgMatrix, save_path: ImgSavePath) -> ImgSavePath | NoReturn:
        """Метод сохранения изображения.

        Args:
            img_matrix: Объект изображения в виде попиксельной матрицы.
            save_path: Путь сохранения изображения.

        Returns:
            Путь с сохраненным изображением.
        """
        if img_matrix is None or not isinstance(img_matrix, ImgMatrix):
            raise self.exception(self.messages.IMG_MATRIX_TYPE_ERROR)
        if save_path is None or not isinstance(save_path, ImgSavePath):
            raise self.exception(self.messages.INVALID_IMG_SAVE_PATH_ERROR)

        try:
            cv.imwrite(save_path, img_matrix)
            return save_path
        except (FileNotFoundError, IsADirectoryError):
            raise self.exception(self.messages.INVALID_IMG_PATH_ERROR)
        except PermissionError:
            raise self.exception(self.messages.IMG_PERMISSION_ERROR)
        except Exception as e:
            raise self.exception(self.messages.IMG_SAVE_ERROR.format(msg=e.__str__()))

    def resize_image(self, img_matrix: ImgMatrix, img_size: ImgSize) -> ImgMatrix | NoReturn:
        """Метод изменения разрешения изображения.

        Args:
            img_matrix: Объект изображения в виде попиксельной матрицы.
            img_size: Размер изображения.

        Returns:
            Объект изображения в виде попиксельной матрицы с измененным размером.
        """
        if not isinstance(img_matrix, ImgMatrix):
            raise self.exception(self.messages.IMG_MATRIX_TYPE_ERROR)
        if img_size is None or not isinstance(img_size, tuple):
            raise self.exception(self.messages.IMG_SIZE_TYPE_ERROR)

        try:
            return cv.resize(img_matrix, img_size)
        except Exception as e:
            raise self.exception(self.messages.IMG_RESIZE_ERROR.format(msg=e.__str__()))

    def convert_image_to_rgb(self, img_matrix: ImgMatrix) -> ImgMatrix | NoReturn:
        """Метод конвертации изображения к RGB-формату.

        Args:
            img_matrix: Объект изображения в виде попиксельной матрицы.

        Returns:
            Объект изображения в виде попиксельной матрицы приведенный к RGB-формату.
        """
        if not isinstance(img_matrix, ImgMatrix):
            raise self.exception(self.messages.IMG_MATRIX_TYPE_ERROR)

        try:
            return cv.cvtColor(img_matrix, cv.COLOR_BGR2RGB)
        except Exception as e:
            raise self.exception(self.messages.IMG_CONVERT_RGB_ERROR.format(msg=e.__str__()))

    def convert_image_to_grayscale(self, img_matrix: ImgMatrix) -> ImgMatrix | NoReturn:
        """Метод конвертации изображения к черно-белому формату.

        Args:
            img_matrix: Объект изображения в виде попиксельной матрицы.

        Returns:
            Объект изображения в виде попиксельной матрицы приведенный к черно-белому формату.
        """
        if not isinstance(img_matrix, ImgMatrix):
            raise self.exception(self.messages.IMG_MATRIX_TYPE_ERROR)
        try:
            return cv.cvtColor(img_matrix, cv.COLOR_BGR2GRAY)
        except Exception as e:
            raise self.exception(self.messages.IMG_CONVERT_GRAYSCALE_ERROR.format(msg=e.__str__()))

    def is_images_the_same_pixels(
            self,
            img_first: ImgPath | ImgMatrix,
            img_second: ImgPath | ImgMatrix
    ) -> bool | NoReturn:
        """Метод для проверки двух изображений на схожесть методом попиксельного сравнения.

        Args:
            img_first: Путь до первого изображения или матрица.
            img_second: Путь до второго изображения или матрица.

        Returns:
            Утверждение схожи ли два изображения.
        """
        if not isinstance(img_first, (ImgPath, ImgMatrix)):
            raise self.exception(self.messages.IMG_IS_SAME_TYPE_ERROR)
        if not isinstance(img_second, (ImgPath, ImgMatrix)):
            raise self.exception(self.messages.IMG_IS_SAME_TYPE_ERROR)

        img_matrix_first = self.read_image(img_first) if isinstance(img_first, ImgPath) else img_first
        img_matrix_second = self.read_image(img_second) if isinstance(img_second, ImgPath) else img_second

        difference = cv.subtract(img_matrix_first, img_matrix_second)
        colors_decomposition = cv.split(difference)
        if len(colors_decomposition) == 1:
            if cv.countNonZero(colors_decomposition[0]) == 0:
                return True
            return False

        blue, green, red = colors_decomposition

        if cv.countNonZero(blue) == 0 and cv.countNonZero(green) == 0 and cv.countNonZero(red) == 0:
            return True
        return False

    def found_and_hide_text_on_image(
            self,
            img_path: ImgPath,
            save_path: ImgSavePath | None = None,
            languages: list[Language] = (Language.RUSSIAN, Language.ENGLISH)
    ) -> ImgSavePath | NoReturn:
        """Метод для происка и скрытия текста на изображении.

        Args:
            img_path: Путь до изображения.
            save_path: Путь сохранения изображения.
            languages: Языки текста на изображении.
        """
        img_matrix: ImgMatrix = self.read_image(img_path)

        if not save_path:
            file_name: str = img_path.split("/")[-1].split(".")[0]
            save_path = img_path.replace(file_name, f"{file_name}_text_hided")

        try:
            reader = easyocr.Reader(languages)
            results = reader.readtext(img_matrix)

            for result in results:
                box = result[0]
                x1, y1 = int(box[0][0]), int(box[0][1])
                x2, y2 = int(box[2][0]), int(box[2][1])
                cv.rectangle(img_matrix, (x1, y1), (x2, y2), FILL_TEXT_COLOR, cv.FILLED)
        except Exception as e:
            raise self.exception(self.messages.IMG_FOUND_AND_HIDE_TEXT_ERROR.format(msg=e.__str__()))
        return self.save_image(img_matrix, save_path)
