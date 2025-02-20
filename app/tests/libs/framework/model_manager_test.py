from unittest import TestCase

from django.db.models.base import ModelBase
from django.db.models import Model
from app.libs.framework.model_manager import ModelManager


class TestModelManager(TestCase):

    def setUp(self) -> None:
        self.instance = ModelManager()
        self.exception = self.instance.exception
        self.messages = self.instance.messages

        self.table_name = "app.AuthUser"

    def test_get_model_by_name(self) -> None:
        table_name = self.table_name

        with self.subTest("Get model by name"):
            self.assertTrue(issubclass(type(self.instance.get_model_by_name(table_name)), ModelBase))

        with self.subTest("Invalid model name, non-existent table"), self.assertRaises(self.exception) as e:
            _ = self.instance.get_model_by_name("test")
        self.assertEqual(self.messages.GET_MODEL_ERROR, e.exception.message)

        with self.subTest("Invalid model name, unknown type"), self.assertRaises(self.exception) as e:
            _ = self.instance.get_model_by_name(None)
        self.assertEqual(self.messages.INVALID_MODEL_NAME_TYPE_ERROR, e.exception.message)

    def test_delete_model_records(self):
        table_name = self.table_name

        with self.subTest("Delete table record, record not exist"):
            self.assertIsNone(self.instance.delete_model_record(table_name, email="test"))

        with self.subTest("Delete table record, record exist"):
            self.instance.get_or_create_model_record("app.AuthUser", username="test")
            self.instance.delete_model_record(table_name, username="test")

        with self.subTest("Empty kwargs"), self.assertRaises(self.exception) as e:
            self.instance.delete_model_record(table_name)
        self.assertEqual(self.messages.EMPTY_KWARGS_ERROR, e.exception.message)

    def test_get_or_create_record(self):
        table_name = self.table_name

        with self.subTest("Create table record"):
            self.instance.delete_model_record(table_name, username="test")
            record = self.instance.get_or_create_model_record(table_name, username="test")
            self.assertEqual("test", record.username)

        with self.subTest("Empty kwargs"), self.assertRaises(self.exception) as e:
            self.instance.delete_model_record(table_name)
        self.assertEqual(self.messages.EMPTY_KWARGS_ERROR, e.exception.message)

    def test_get_all_model_records(self):
        table_name = self.table_name

        with self.subTest("Get all records from table"):
            records = self.instance.get_all_model_records(table_name)
            self.assertTrue(records)
            for record in records:
                self.assertIsInstance(record, Model)
