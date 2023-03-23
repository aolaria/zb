from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status, mixins
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from account.services import (
    LoginServices
)
from account.validators import (
    LoginValidator
)
from utils.CustomResponse import ErrorResponse


class LoginView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    Login Class-View
    """
    permission_classes = [permissions.AllowAny]

    @action(methods=["post"], detail=False)
    def login(self, request):
        """
        Function to execute the login service
        :param request: request's data
        :return: login's info
        """
        try:
            LoginValidator.validate(request.data)
            user = LoginServices.login(request.data)
        except (ValueError, ObjectDoesNotExist)  as error:
            return ErrorResponse(str(error), status=status.HTTP_400_BAD_REQUEST)
        return Response(user, status=status.HTTP_200_OK)

    @action(methods=["put"], detail=False)
    def refresh(self, request):
        """
        refreshs JWT
        :param request: request's data
        :return: Refreshed Access token
        """
        try:
            token = LoginServices.refresh(request.data)
        except Exception as error:
            return ErrorResponse(str(error), status=status.HTTP_400_BAD_REQUEST)
        return Response({"access": str(token.access_token)}, status=status.HTTP_200_OK)
