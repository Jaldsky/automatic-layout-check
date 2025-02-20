from unittest import TestCase
from unittest.mock import patch

from django.test import Client

from app.utils.common import setup_environment
from app.views import UserRegistrationView

setup_environment()

from app.forms import UserRegistrationForm


class TestUserRegistrationView(TestCase):
    def setUp(self):
        self.client = Client()
        self.endpoint = '/register/'

    def test_post_with_valid_data(self):
        with (
            patch.object(UserRegistrationForm, 'is_valid', return_value=True),
            patch.object(UserRegistrationForm, 'save') as mock
        ):
            data = {'username': 'testuser', 'password': 'testpassword'}
            response = self.client.post(self.endpoint, data)

            self.assertTrue(mock.called)
            self.assertEqual(response.status_code, 302)

    def test_post_with_invalid_data(self):
        with patch.object(UserRegistrationForm, 'is_valid', return_value=False):
            data = {'username': 'testuser', 'password': ''}
            response = self.client.post(self.endpoint, data)

            self.assertEqual(response.status_code, 200)
            # we give 200 and write that the data is incorrect

    def test_method_not_allowed(self):
        response = self.client.put(self.endpoint)
        self.assertEqual(response.status_code, 405)
        self.assertIn(UserRegistrationView.METHOD_NOT_ALLOWED_ERROR, response.json()['error'])
