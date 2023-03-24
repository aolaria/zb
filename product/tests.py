from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from product.validators import ProductValidator
from account.models import User
from product.models import WatchRecord
from utils.tests import mock_user, mock_product


class ProductTestValidator(TestCase):
    def test_passing_empty_dict_return_error(self):
        with self.assertRaises(ValueError) as context:
            ProductValidator.validate({})
        self.assertEqual("empty payload", str(context.exception))

    def test_not_passing_name_return_error(self):
        with self.assertRaises(ValueError) as context:
            ProductValidator.validate({"brand": "foo", "price": 1})
        self.assertEqual(str({"name": ['required field']}), str(context.exception))

    def test_passing_wrong_typereturn_error(self):
        with self.assertRaises(ValueError) as context:
            ProductValidator.validate({"name": 12323, "brand": 8788, "price": "hgjhg"})
        self.assertTrue(isinstance(context.exception, ValueError))

    def test_passing_none_name_return_error(self):
        with self.assertRaises(ValueError) as context:
            ProductValidator.validate({"name": None, "brand": None, "price": None})
        self.assertTrue(isinstance(context.exception, ValueError))


class BrandViewTest(APITestCase):
    def setUp(self) -> None:
        self.url = '/brands/'
        self.data = {
            "name": "Super Exclusive & Expensive Brand & C.O",
        }
        self.user, _ = mock_user()
        

    def test_unauthorized_request_return_none(self):
        """
        not passing JWT token
        """
        response = self.client.post(
            self.url,
            self.data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_brand_return_none(self):
        """
        Successful creation of a brand instance
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url,
            self.data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_passing_empty_payload_return_none(self):
        """
        Passing Empty Payload
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url,
            {},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_passing_wrong_type_payload_return_none(self):
        """
        Passing wrong type payload
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url,
            {"name": 12323},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductDetailsTest(APITestCase):
    def setUp(self) -> None:
        self.url = "/products/%s/details/"
        self.product = mock_product()
        self.user = mock_user()
    
    def test_making_anonymous_request_return_none(self):
        """
        requesting an item as anonymous user
        """
        url = self.url % self.product.sku
        response = self.client.get(
            url,
            format="json"
        )

        watch_record = WatchRecord.objects.filter(product__sku=self.product.sku).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(watch_record.count, 1)

    def test_making_authenticated_request_return_none(self):
        """
        requesting an item as anonymous user
        """
        url = self.url % self.product.sku
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            url,
            format="json"
        )

        watch_record = WatchRecord.objects.filter(product__sku=self.product.sku).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(watch_record)