from rest_framework import serializers
from apps.consumer_protection.models.comments import Comments
from apps.consumer_protection.models.feedbacks import Feedbacks
from apps.consumer_protection.models.users import Users


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    """
    so that the feedback to which comment is made, is fetched and the
    supplied ID is validated against the existing feedback objects
    """

    feedback_id = serializers.HyperlinkedRelatedField(
        view_name="feedback-detail", queryset=Feedbacks.objects.all()
    )

    """
    so that only existing users can comment and the supplied ID is
    matched against the existing user objects
    """
    commenter_id = serializers.HyperlinkedRelatedField(
        view_name="user-detail", queryset=Users.objects.all()
    )
    url = serializers.HyperlinkedIdentityField(
        view_name="comment-detail"
    )

    class Meta:
        model = Comments
        fields = [
            "comment_id",
            "body",
            "feedback_id",
            "commenter_id",
            "url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["url", "created_at", "updated_at"]
