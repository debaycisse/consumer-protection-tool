from rest_framework import serializers
from apps.consumer_protection.models.items import Items
from apps.consumer_protection.models.users import Users


class ItemsSerializer(serializers.HyperlinkedModelSerializer):
    """
    so that the item which could either be a product or
    service is mapped to its manufacturer or producer
    """

    producer_id = serializers.HyperlinkedRelatedField(
        view_name="user-detail",
        queryset=Users.objects.filter(user_type="producer"),
    )

    url = serializers.HyperlinkedIdentityField(view_name="item-detail")

    class Meta:
        model = Items
        fields = [
            "item_id",
            "name",
            "producer_id",
            "leaderboard_score",
            "category",
            "url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "item_id",
            "url",
            "created_at",
            "updated_at",
            "leaderboard_score",
        ]
