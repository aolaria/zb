from product import models as product_models
from product.validators import (
    ProductValidator
)


class ProductServices:
    """
    All Product Related Services
    """
    @staticmethod
    def __create_sku_code():
        """
        Product SKU Generator
        """
        return "HR87029P"

    @staticmethod
    def create_product(data:dict) -> None:
        """
        Product Creation service 
        """
        data["sku"] = ProductServices.__create_sku_code()
        product_models.Product(**data).save()

    @staticmethod
    def update_product(data:dict) -> None:
        """
        updates product instance
        """
