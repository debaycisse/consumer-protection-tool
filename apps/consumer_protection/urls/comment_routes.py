from rest_framework.urls import path
from apps.consumer_protection.views.comment_views import (
    CommentListCreateView,
    CommentRetrieveUpdateDestroyView,
)

urlpatterns = [
    path(
        "comments", CommentListCreateView.as_view(), name="comment-list"
    ),
    path(
        "comments/<str:comment_id>",
        CommentRetrieveUpdateDestroyView.as_view(),
        name="comment-detail",
    ),
]
