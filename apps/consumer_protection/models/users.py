from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from uuid import uuid4

# class ConsumersManager(BaseUserManager):
#     def create_user(self, **all_fields):
#         if not all_fields.get('email'):
#             raise ValidationError('email address cannot be blank')
#         if not all_fields.get('username'):
#             raise ValidationError("username cannot be blank")
#         if not all_fields.get('name'):
#             raise ValidationError('name cannot be blank')
#         if not all_fields.get('password'):
#             raise ValidationError('password cannot be blank')

#         email = self.normalize_email(all_fields.pop('email'))
#         password = all_fields.pop('password')
#         consumer = self.model(email=email, **all_fields)
#         consumer.set_password(password)
#         consumer.save(using=self._db)
#         return consumer


# class Consumers(AbstractBaseUser):
#     """
#     represents an instance of an end-user or consumer
#     """
#     consumer_id = models.UUIDField(
#         default=uuid4, primary_key=True, editable=False)
#     name = models.CharField(max_length=100, blank=False, null=False)
#     email = models.EmailField(unique=True, blank=False, null=False)
#     username = models.CharField(unique=True, blank=False, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     objects = ConsumersManager()

USER_TYPE = {"CONS": "consumer", "PROD": "producer"}


class UsersManager(BaseUserManager):
    def create_user(
        self,
        name=None,
        email=None,
        username=None,
        password=None,
        user_type=None,
        **other_fields
    ):
        if not email:
            raise ValidationError("email cannot be blank")
        if not username:
            raise ValidationError("username cannot be blank")
        if not name:
            raise ValidationError("name cannot be blank")
        if not password:
            raise ValidationError("password cannot be blank")

        if user_type == USER_TYPE["PROD"] and not other_fields.get(
            "rc_number"
        ):
            raise ValidationError("RC number is required")

        email = self.normalize_email(email)
        user = self.model(
            name, email, username, user_type, **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    user_id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    username = models.CharField(unique=True, blank=False, null=False)
    user_type = models.CharField(
        choices=USER_TYPE, default=USER_TYPE["CONS"]
    )
    rc_number = models.CharField(
        max_length=50, blank=True, null=False, default=""
    )
    hq_address = models.CharField(
        max_length=255, blank=True, null=False, default=""
    )
    phone = models.CharField(blank=True, null=False, max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name", "email"]

    objects = UsersManager()

    def __str__(self):
        return self.username
