from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser
from apps.consumer_protection.models.users import Users


class IsProducer(permissions.BasePermission):
    """
    to confirm if user is a producer of a product (service) or not
    """

    def has_permission(self, request, view):
        user = request.user
        if isinstance(user, AnonymousUser):
            return False
        user_qs = Users.objects.filter(user_name=user.user_name)
        return user_qs.user_type == "producer"
