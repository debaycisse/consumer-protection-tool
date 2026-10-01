from rest_framework import serializers
from apps.consumer_protection.models.feedbacks import (
    Feedbacks,
    FeedbackResponse,
    FeedbackVerifications,
)
from apps.consumer_protection.models.users import Users
from apps.consumer_protection.models.items import Items


class FeedbacksSerializer(serializers.HyperlinkedModelSerializer):
    """
    so that the consumer who creates a feedback is known and the
    supplied ID is checked to ensure only exisiting users can
    create a feedback
    """

    consumer_id = serializers.HyperlinkedRelatedField(
        view_name="user-detail", queryset=Users.objects.all()
    )

    """
    so that the product against which a feedback is made can be
    identified and the supplied item or product id is validated
    """
    item_id = serializers.HyperlinkedRelatedField(
        view_name="item-detail", queryset=Items.objects.all()
    )

    url = serializers.HyperlinkedIdentityField(
        view_name="feedback-detail"
    )

    class Meta:
        model = Feedbacks
        fields = [
            "feedback_id",
            "consumer_id",
            "body",
            "item_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "feedback_id",
            "url",
            "created_at",
            "updated_at",
        ]


class FeedbackResponseSerializer(
    serializers.HyperlinkedModelSerializer
):
    """
    to ensure that the responder is a company and
    is validated against existed or known companies
    """

    responder_id = serializers.HyperlinkedRelatedField(
        view_name="user-detail",
        queryset=Users.objects.filter(user_type="producer"),
    )

    """
    to ensure that that the product or item on top of which the
    feedback is made, belongs to the responder
    """
    feedback_id = serializers.HyperlinkedRelatedField(
        view_name="feedback-detail",
        queryset=Feedbacks.objects.filter(
            item_id__producer_id=responder_id
        ),
    )

    url = serializers.HyperlinkedIdentityField(
        view_name="feedback-response-detail"
    )

    class Meta:
        model = FeedbackResponse
        fields = [
            "feedback_response_id",
            "responder_id",
            "feedback_id",
            "body",
            "url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "feedback_response_id",
            "url",
            "created_at",
            "updated_at",
        ]


class FeedbackVerificationSerializer(
    serializers.HyperlinkedModelSerializer
):
    feedback_id = serializers.HyperlinkedRelatedField(
        view_name="feedback-detail", queryset=Feedbacks.objects.all()
    )
    url = serializers.HyperlinkedIdentityField(
        view_name="feedback-verification-detail"
    )
    comments = serializers.HyperlinkedRelatedField(
        view_name="comment-list", read_only=True, many=True
    )

    class Meta:
        model = FeedbackVerifications
        fields = {
            "feedback_verification_id",
            "feedback_id",
            "genuine",
            "url",
            "comments",
            "created_at",
            "updated_at",
        }
        read_only_fields = [
            "feedback_verification_id",
            "url",
            "created_at",
            "updated_at",
            "comments",
        ]
