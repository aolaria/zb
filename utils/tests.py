from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User
from product.models import Brand, Product


def mock_user() -> tuple[User,RefreshToken]:
    """
    creates mock user
    """
    user = User.objects.create_user(**{
        "username": "Chester",
        "password": "superlongstrongsecurepassword"
    })
    user.is_active = True
    token = RefreshToken.for_user(user)
    return user, token


def mock_brand() -> Brand:
    """
    creates mock brand
    """
    brand = Brand.objects.create(**{
        "name": "Super Cool & Expensive Brand & C.O"
    })
    brand.save()
    return brand

def mock_product() -> Product:
    """
    creates mock product
    """
    brand = mock_brand()
    product = Product.objects.create(**{
        "sku": "SKUCODE",
        "name": "Super Cool Product",
        "brand": brand,
        "price": 599.99
    })
    product.save()
    return product
