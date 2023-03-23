from rest_framework import viewsets, status
from rest_framework.response import Response

from product.services import (
    ProductServices
)
from product.validators import (
    ProductValidator
)
from utils.CustomResponse import ErrorResponse


class ProductViewSet(viewsets.ViewSet):
    """
    Product's View/Controller
    """
    def post(self, request) -> Response:
        """
        POST Creates a Product instance
        :param request: (dict) request object, contains all of request's information
        :return: 201 HTTP status code
        """
        try:
            ProductValidator.validate(request.data)
            ProductServices.create_product(request.data)
        except ValueError as err:
            # TODO: log the value
            return ErrorResponse(err, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)
