from rest_framework import serializers
from apps.consumer_protection.models.users import Users


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = [
            "user_id",
            "email",
            "username",
            "user_type",
            "rc_number",
            "hq_address",
            "phone",
            "url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "user_id",
            "url",
            "created_at",
            "updated_at",
        ]
