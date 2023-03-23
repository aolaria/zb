import serpy


class UserSerializer(serpy.Serializer):
    """
    Serializer-Class for User's info
    """
    id = serpy.Field()
    username = serpy.Field()
