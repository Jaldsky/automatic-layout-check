from typing import NoReturn

from django.apps import apps
from django.db.models import Model

from app.libs.exceptions import ModelManagerException, ModelManagerMessages
from app.libs.types import ModelName, RecordArgs


class ModelManager:
    exception = ModelManagerException
    messages = ModelManagerMessages

    def get_model_by_name(self, model_name: ModelName) -> Model | NoReturn:
        """Метод получения модели по названию.

        Args:
            model_name: Название модели, начиная с названия проекта (например, app.mymodel).

        Returns:
            Объект модели.
        """
        if not isinstance(model_name, ModelName):
            raise self.exception(self.messages.INVALID_MODEL_NAME_TYPE_ERROR)
        try:
            return apps.get_model(model_name)
        except Exception:
            raise self.exception(self.messages.GET_MODEL_ERROR)

    def delete_model_record(self, model_name: ModelName, **kwargs: RecordArgs) -> None | NoReturn:
        """Метод удаления записи из таблицы.
        Пример использования: get_or_create_record("app.AuthUser", username="test").

        Args:
            model_name: Название модели, начиная с названия проекта (например, app.mymodel).
            **kwargs: Аргументы поиска записи в таблице в формате словаря.
        """
        model: Model = self.get_model_by_name(model_name)
        if not kwargs:
            raise self.exception(self.messages.EMPTY_KWARGS_ERROR)
        try:
            model.objects.filter(**kwargs).delete()
        except Exception as e:
            raise self.exception(self.messages.DELETE_RECORD_ERROR.format(msg=e.__str__()))

    def get_or_create_model_record(self, model_name: ModelName, **kwargs: RecordArgs | None) -> Model | NoReturn:
        """Метод получения/создания записи в таблице.

        Args:
            model_name: Название модели, начиная с названия проекта (например, app.mymodel).
            **kwargs: Аргументы поиска записи в таблице в формате словаря.
        """
        model: Model = self.get_model_by_name(model_name)
        if not kwargs:
            raise self.exception(self.messages.EMPTY_KWARGS_ERROR)
        try:
            record = model.objects.get(**kwargs)
            return record
        except model.DoesNotExist:
            return model.objects.create(**kwargs)
        except Exception as e:
            raise self.exception(self.messages.GET_OR_CREATE_RECORD_ERROR.format(msg=e.__str__()))

    def get_all_model_records(self, model_name: ModelName) -> list[Model] | NoReturn:
        """Метод получения всех записей в таблице.

        Args:
            model_name: Название модели, начиная с названия проекта (например, app.mymodel).

        Returns:
            Список всех записей в таблице.
        """
        model: Model = self.get_model_by_name(model_name)
        try:
            return list(model.objects.all())
        except Exception as e:
            raise self.exception(self.messages.GET_ALL_RECORDS_ERROR.format(msg=e.__str__()))
