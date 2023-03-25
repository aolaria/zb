import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework import viewsets, status, mixins
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from account.services import (
    LoginServices,
    AdminServices
)
from account.serializers import (
    UserSerializer
)
from account.validators import (
    LoginValidator,
    AdminValidator,
    AdminValidatorUpdate,
)
from utils.custom_response import ErrorResponse
from utils.custom_exceptions import NotAuthorizatedError
from utils.error_messages import ErrorMessages as e


logger = logging.getLogger(__name__)


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
            logging.error(error)
            return ErrorResponse(e.SOMETHING_WENT_WRONG, status=status.HTTP_400_BAD_REQUEST)
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
            logging.error(error)
            return ErrorResponse(e.SOMETHING_WENT_WRONG, status=status.HTTP_400_BAD_REQUEST)
        return Response({"access": str(token.access_token)}, status=status.HTTP_200_OK)


class AdminViewSet(viewsets.ViewSet):
    """
    'admin' or users who can-authenticate
    """
    def create(self, request):
        try:
            AdminValidator.validate(request.data)
            user = AdminServices.create(request.data)
        except IntegrityError as error:
            logging.error(error)
            return ErrorResponse("username already taken", status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            logging.error(error)
            return ErrorResponse(e.SOMETHING_WENT_WRONG, status=status.HTTP_400_BAD_REQUEST)
        return Response(UserSerializer(user).data,status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            if not request.data:
                return ErrorResponse(e.EMPTY_PAYLOAD, status=status.HTTP_400_BAD_REQUEST)
            AdminValidatorUpdate.validate(request.data)
            AdminServices.update(data=request.data, pk=pk)
        except NotAuthorizatedError:
            return ErrorResponse(e.NOT_AUTHORIZED,status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            logging.error(error)
            return ErrorResponse(e.SOMETHING_WENT_WRONG, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, _, pk=None):
        try:
            if not pk:
                return ErrorResponse("admin id was not specified", status=status.HTTP_400_BAD_REQUEST)
            AdminServices.destroy(pk=pk)
        except NotAuthorizatedError:
            return ErrorResponse(e.NOT_AUTHORIZED,status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            logging.error(error)
            return ErrorResponse(e.SOMETHING_WENT_WRONG, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
