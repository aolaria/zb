import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from product.models import Brand
from product.services import (
    ProductServices,
    BrandServices
)
from product.serializers import (
    ProductSerializer,
    BrandSerializer
)
from product.validators import (
    ProductValidator,
    BrandValidator,
    ProductUpdateValidator
)
from utils.CustomResponse import ErrorResponse


logger = logging.getLogger(__name__)


class BrandViewSet(viewsets.ViewSet):
    """
    simplified brand view
    """
    def create(self, request) -> Brand:
        """
        creates brand instance
        """
        if not request.data:
            return ErrorResponse("Empty Payload", status=status.HTTP_400_BAD_REQUEST)
        try:
            BrandValidator.validate(request.data)
            brand = BrandServices.create(request.data)
        except Exception as error:
            return ErrorResponse(str(error), status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class ProductViewSet(viewsets.ViewSet):
    """
    Product's View/Controller
    """
    @action(detail=True, methods=['GET'], permission_classes=[AllowAny])
    def details(self, _, pk:str) -> Response:
        """
        Retriving Product Details
        """
        if not pk:
            return ErrorResponse("product SKU was not specified", status=status.HTTP_400_BAD_REQUEST)
        try:
            prod = ProductServices.retrieve(sku=pk)
        except ObjectDoesNotExist as error:
            return ErrorResponse(str(error), status=status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(prod).data, status=status.HTTP_200_OK)

    def create(self, request) -> Response:
        """
        POST Creates a Product instance
        :param request: (dict) request object, contains all of request's information
        :return: 201 HTTP status code
        """
        try:
            ProductValidator.validate(request.data)
            prod, _ = ProductServices.create(request.data)
        except Exception as error:
            return ErrorResponse(str(error), status=status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(prod).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None) -> Response:
        """
        PUT Updates a Product instance
        :param request: (dict) request object, contains all of request's information
        :param pk: SKU code
        :return: 204 HTTP status code
        """
        try:
            ProductUpdateValidator.validate(request.data)
            prod = ProductServices.update(sku=pk, data=request.data)
        except Exception as error:
            return ErrorResponse(str(error), status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, _, pk=None) -> Response:
        """
        DELETE Deletes a product instance
        :param pk: SKU code
        :return: 204 HTTP status code
        """
        try:
            ProductServices.destroy(sku=pk)
        except Exception as error:
            return ErrorResponse(str(error), status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
