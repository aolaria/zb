from django.db import models


class Brand(models.Model):
    """
    Brand's Model

    attrs:
        1. name
    """
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    """
    Product's Model
    
    attrs:
        1. SKU
        2. name
        3. price
        4. Brand
    """
    sku = models.CharField(primary_key=True, max_length=10, blank=False, null=False, unique=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.FloatField()
    brand = models.ForeignKey(Brand, null=False, blank=False, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.sku}-{self.name}"


class WatchRecord(models.Model):
    """
    Product's Watch Record

    attrs:
        1. count
        2. product FK
    """
    count = models.IntegerField()
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name}-{self.product.brand.name}"
