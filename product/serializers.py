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


class ProductDetailSerializer(serpy.Serializer):
    """
    Serializer-Class for User's info
    """
    sku = serpy.Field()
    price = serpy.Field()
    name = serpy.Field()
    brand = serpy.MethodField()
    watch_record = serpy.MethodField()

    def get_brand(self, obj):
        """
        Brand serializer 
        """
        return BrandSerializer(obj.brand).data
    
    def get_watch_record(self, obj):
        """
        WatchRecord counter
        """
        if hasattr(obj, 'watchrecord'):
            return obj.watchrecord.count
        return 0


class BrandSerializer(serpy.Serializer):
    """
    simplified brand serializer
    """
    name = serpy.Field()
