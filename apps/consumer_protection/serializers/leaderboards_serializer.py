from rest_framework import serializers

from apps.consumer_protection.models.leaderboards import Leaderboard
from apps.consumer_protection.models.users import Users


class LeaderboardSerializer(serializers.HyperlinkedModelSerializer):
    producer_id = serializers.HyperlinkedRelatedField(
        view_name="user-detail",
        queryset=Users.objects.filter(user_type="producer"),
    )
    url = serializers.HyperlinkedIdentityField(
        view_name="leaderboard-detail"
    )

    class Meta:
        model = Leaderboard
        fields = ["leaderboard_id", "producer_id", "score", "url"]
        read_only_fields = ["leaderboard_id", "url"]
