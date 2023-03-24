from rest_framework.serializers import ModelSerializer
import serpy



class ProductSerializer(serpy.Serializer):
    """
    Serializer-Class for User's info
    """
    sku = serpy.Field()
    price = serpy.Field()
    name = serpy.Field()
    brand = serpy.MethodField()

    def get_brand(self, obj):
        """
        Brand serializer 
        """
        return BrandSerializer(obj.brand).data


class BrandSerializer(serpy.Serializer):
    """
    simplified brand serializer
    """
    name = serpy.Field()
