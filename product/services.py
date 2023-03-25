import string
import secrets

from django.core.exceptions import ObjectDoesNotExist

from account.models import User
from product.models import Brand, Product, WatchRecord
from product.validators import (
    ProductValidator
)
from .tasks import update_product_email


class BrandServices:
    """
    All Brand Related Services
    """
    @staticmethod
    def create(data:dict) -> Brand:
        """
        Creates Brand instance
        :param data: (dict) brand's details
        """
        if not data:
            raise ValueError("empty payload")
        return Brand.objects.create(name=data["name"].lower())


class ProductServices:
    """
    All Product Related Services
    """
    DEFAULT_RANDOM_STRING = 4

    @staticmethod
    def __create_random_string(length=DEFAULT_RANDOM_STRING) -> str:
        """
        Creates Random String, default length = 4
        """
        return ''.join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(length)
        )

    @staticmethod
    def __create_sku_code(b_n: str, p_n: str) -> str:
        """
        Product SKU Generator
        :param b_n: (str) base_name
        :param p_n: (str) product_name
        """
        return f"{b_n[:2]}{p_n[:2]}{ProductServices.__create_random_string()}".upper()

    @staticmethod
    def __upsert(data:dict) -> bool:
        """
        Updates or Create a product instance, this method prevents collitions or duplicates
        :param data: (dict) description of product instance
        :return: False/True
        """
        return Product.objects.update_or_create(**data)

    @staticmethod
    def __create_product_record(prod: Product) -> None:
        """
        Creates a WatchRecord related to an specified product
        """
        record = WatchRecord.objects.filter(product__sku=prod.sku).first()
        if not record:
            record = WatchRecord.objects.create(count=1, product=prod)
        else:
            record.count += 1
            record.save()

    @staticmethod
    def retrieve(sku:str, user:User=None) -> Product:
        """
        Retrieve a product instance
        :param sku: (str) product's SKU
        :return: Product instance
        """
        try:
            prod = Product.objects.get(sku=sku)
            if user and getattr(user, 'is_anonymous', False):
                ProductServices.__create_product_record(prod)
        except ObjectDoesNotExist as error:
            raise error
        return prod

    @staticmethod
    def _get_brand_by_name(name: str) -> Brand:
        """
        Get Brand instance by Name
        """
        brand = None
        if name and isinstance(name, str):
            brand = Brand.objects.filter(name=name.lower()).first()

        if not brand:
            raise ObjectDoesNotExist("Not existing brand")

        return brand

    @staticmethod
    def create(data:dict) -> None:
        """
        Product Creation service 
        """
        brand = ProductServices._get_brand_by_name(data["brand"])
        data["sku"] = ProductServices.__create_sku_code(b_n=brand.name, p_n=data["name"])
        data["brand"] = brand
        return ProductServices.__upsert(data=data)

    @staticmethod
    def update(sku:str, data:dict, user:User) -> None:
        """
        updates product instance
        :param sku: (str) SKU code
        :param data: (dict) data to be updated
        """
        if not sku:
            raise ValueError("SKU was not specified")

        if not data or len(data) == 0:
            raise ValueError("Empty Payload")

        product = ProductServices.retrieve(sku=sku)

        if "brand" in data.keys():
            brand = ProductServices._get_brand_by_name(data["brand"])
            data["brand"] = brand

        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        # send update email
        update_product_email(user=user, sku=sku, data=data)
    
    @staticmethod
    def destroy(sku:str) -> None:
        """
        deletes product instance
        :param sku: (str) SKU code
        """
        if not sku:
            raise ValueError("SKU was not specified")

        product = ProductServices.retrieve(sku=sku)
        product.delete()
