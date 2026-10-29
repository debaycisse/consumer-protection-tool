from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from apps.consumer_protection.views.utils import CommonViewAttributes
from apps.consumer_protection.models.users import Users
from apps.consumer_protection.serializers.users_serializer import (
    UserSerializer,
)
from apps.consumer_protection.permissions.owner_permission import (
    IsAccountOwner,
)


class SignInView(CommonViewAttributes, APIView):
    """
    View to process login request from users
    """

    def post(self, request, format=None):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        # authenticate
        user_obj = authenticate(
            request=request, username=username, password=password
        )

        if user_obj:
            generated_token, _ = Token.objects.get_or_create(
                user=user_obj
            )

            data = {"token": generated_token.key}

            return Response({"data": data}, status=status.HTTP_200_OK)

        raise AuthenticationFailed()


class SignOutView(CommonViewAttributes, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user_token = request.auth

        self.check_object_permissions(request, user_token)

        user_token.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RegistrationView(CommonViewAttributes, APIView):
    def post(self, request, format=None):
        request_data = request.data
        new_user = Users.objects.create(**request_data)

        user_serializer = UserSerializer(data=new_user)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        response_data = {"data": user_serializer.data}

        return Response(response_data, status=status.HTTP_201_CREATED)


class ListUsersView(CommonViewAttributes, APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        user_objects = Users.objects.all()

        self.check_object_permissions(request, user_objects)

        users_serializer = UserSerializer(user_objects, many=True)

        response_data = {"data": users_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)


class RetrieveUpdateUserView(CommonViewAttributes, APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAccountOwner]

    def get_object(self, user_id=None):
        return Users.objects.get(user_id=user_id)

    def get(self, request, user_id=None, format=None):
        user_object = self.get_object(user_id)

        self.check_object_permissions(request, user_object)

        user_serializer = UserSerializer(user_object)

        response_data = {"data": user_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def patch(self, request, user_id=None, format=None):
        user_object = self.get_object(user_id)

        self.check_object_permissions(request, user_object)

        request_data = request.data

        user_serializer = UserSerializer(
            user_object, data=request_data, partial=True
        )
        user_serializer.is_valid(raise_exception=True)

        response_data = {"data": user_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request, user_id=None, format=None):
        user_object = self.get_object(user_id)

        self.check_object_permissions(request, user_object)

        user_object.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
