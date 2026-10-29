from rest_framework.urls import path
from apps.consumer_protection.views.feedbacks_views import (
    FeedbackListCreateView,
    FeedbackRetrieveUpdateDestroyView,
    FeedbackResponseListCreateView,
    FeedbackResponseRetrieveUpdateDestroyView,
    FeedbackVerificationListCreateView,
    FeedbackVerificationRetrieveUpdateDestroyView,
)

urlpatterns = [
    path(
        "feedbacks",
        FeedbackListCreateView.as_view(),
        name="feedback-list",
    ),
    path(
        "feedbacks/<str:feedback_id>",
        FeedbackRetrieveUpdateDestroyView.as_view(),
        name="feedback-detail",
    ),
    path(
        "feedbackresponses",
        FeedbackResponseListCreateView.as_view(),
        name="feedback-response-list",
    ),
    path(
        "feedbackresponses/<str:feedback_response_id>",
        FeedbackResponseRetrieveUpdateDestroyView.as_view(),
        name="feedback-response-detail",
    ),
    path(
        "feedbackverifications",
        FeedbackVerificationListCreateView.as_view(),
        name="feedback-verification-list",
    ),
    path(
        "feedbackverifications/<str:feedback_verification_id>",
        FeedbackVerificationRetrieveUpdateDestroyView.as_view(),
        name="feedback-verification-detail",
    ),
]
