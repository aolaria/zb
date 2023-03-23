from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


from account.validators import LoginValidator
from account.models import User



class LoginValidatorTestCase(TestCase):
    """
    Login Validator Test Case
    """
    def setUp(self):
        pass

    def test_passing_empty_dict_return_error(self):
        """
        Passing empty payload
        """
        with self.assertRaises(ValueError) as context:
            LoginValidator.validate({})
        self.assertEqual("empty payload", str(context.exception))

    def test_not_passing_username_return_error(self):
        """
        Not passing 'username'
        """
        with self.assertRaises(ValueError) as context:
            LoginValidator.validate({"password": "1234"})
        self.assertEqual(str({"username": ['required field']}), str(context.exception))

    def test_not_passing_password_return_error(self):
        """
        Not passing 'password'
        """
        with self.assertRaises(ValueError) as context:
            LoginValidator.validate({"username": "1234"})
        self.assertEqual(str({"password": ['required field']}), str(context.exception))

    def test_passing_username_wrong_type_return_error(self):
        """
        Passing wrong type
        """
        with self.assertRaises(ValueError) as context:
            LoginValidator.validate({"username": 1234, "password": "1234"})
        self.assertEqual(str({"username": ['must be of string type']}), str(context.exception))

    def test_passing_wrong_password_type_return_error(self):
        """
        Passing wrong type
        """
        with self.assertRaises(ValueError) as context:
            LoginValidator.validate({"username": "1234", "password": 1234})
        self.assertEqual(str({"password": ['must be of string type']}), str(context.exception))


class LoginTestCase(APITestCase):
    """
    Login's Test Suit
    """
    def setUp(self) -> None:
        self.url = reverse('login')
        self.username = "chester"
        self.password = "tester"
        self.data = {
            'username': self.username,
            'password': self.password
        }

    def test_succesful_login_return_none(self):
        """
        Making an empty request to /login/
        """
        user = User.objects.create_user(**self.data)
        user.is_active = True
        user.save()

        response = self.client.post(
            self.url,
            self.data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.keys()), ["id","username","access","refresh"])

    def test_wrong_password_login_return_none(self):
        """
        Making an empty request to /login/
        """
        user = User.objects.create_user(**self.data)
        user.is_active = True
        user.save()

        obj = self.data
        obj["password"] = "wrongpassword"

        response = self.client.post(
            self.url,
            obj,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"]["msg"], "Wrong password")
    
    def test_not_existing_user_login_return_none(self):
        """
        Making an empty request to /login/
        """
        user = User.objects.create_user(**self.data)
        user.is_active = True
        user.save()

        obj = self.data
        obj["username"] = "wronguser"

        response = self.client.post(
            self.url,
            obj,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"]["msg"], "User does not exists")


class RefreshTokenTestCase(APITestCase):
    """
    Refresh Token Test Case
    """
    def setUp(self) -> None:
        self.url = reverse('refresh')
        self.username = "chester"
        self.password = "tester"
        self.data = {
            'username': self.username,
            'password': self.password
        }

    def test_succesful_token_refresh_return_none(self):
        """
        Successful Token Refresh
        """
        user = User.objects.create_user(**self.data)
        user.is_active = True
        user.save()

        user_token = RefreshToken.for_user(user)

        response = self.client.put(
            self.url,
            {"access": str(user_token)},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_passing_access_token_return_none(self):
        """
        Not passing access token
        """
        response = self.client.put(
            self.url,
            {"access": ""},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
