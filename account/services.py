from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User
from account.serializers import (
    UserSerializer
)
from utils.custom_exceptions import NotAuthorizatedError


class LoginServices:
    """
    User's Services Module
    """
    @staticmethod
    def login(data: dict) -> dict:
        """
        Login's Services Module
        :param data: (dict) request's data
        :return: Serialized User's info with auth tokens
        """
        user = User.objects.filter(username=data.get("username", None)).first()

        if not user:
            raise ObjectDoesNotExist("User does not exists")

        if user.is_active is False:
            raise ValueError("user is inactive")

        if check_password(data.get("password"), user.password) is False:
            raise ValueError('Wrong password')

        refresh = RefreshToken.for_user(user)
        serialized_user = UserSerializer(user).data
        serialized_user["access"] = str(refresh.access_token)
        serialized_user["refresh"] = str(refresh)
        return serialized_user

    @staticmethod
    def refresh(refresh_token: dict) -> str:
        """
        Token's Refresh Function
        :param data: (dict)
        :return: Serialized Renewed Token
        """
        if not refresh_token:
            raise ValueError("empty payload")

        if not refresh_token["access"]:
            raise ValueError("valid cannot be empty")

        return RefreshToken(refresh_token['access'])


class AdminServices:
    """
    Creates/Updates/Destroy common non-staff-users
    """
    @staticmethod
    def create(data:dict) -> User:
        """
        creates an Admin instance/as the scope of the tasks demands, admin user
        must be able to CRUD products, the created under this method, will be able to 
        authenticate and to handle those instances but for security, it wont be a 'staff' user.
        """
        return User.objects.create_user(**data)

    @staticmethod
    def update(data:dict, pk:int) -> User:
        """
        updates an User instance
        """
        try:
            user = User.objects.get(id=pk)
            if user.is_staff or user.is_superuser:
                raise NotAuthorizatedError
            for key, value in data.items():
                if hasattr(user, key) and key in ['username', 'email', 'password']:
                    setattr(user, key, value)
            user.save()
        except ObjectDoesNotExist as error:
            raise error

    @staticmethod
    def destroy(pk:int):
        """
        destroys an User instance
        """
        try:
            user = User.objects.get(id=pk)
            if user.is_staff or user.is_superuser:
                raise NotAuthorizatedError
            user.delete()
        except ObjectDoesNotExist as error:
            raise error
