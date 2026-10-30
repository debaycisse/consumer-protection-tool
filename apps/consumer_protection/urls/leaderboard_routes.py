from rest_framework.urls import path
from apps.consumer_protection.views.leaderboards_views import (
    LeaderboardListCreateView,
    LeaderboardRetrieveUpdateDestroyView,
)

urlpatterns = [
    path(
        "leaderboards",
        LeaderboardListCreateView.as_view(),
        name="leaderboard-list",
    ),
    path(
        "leaderboard/<str:leaderboard_id>",
        LeaderboardRetrieveUpdateDestroyView.as_view(),
        name="leaderboard-detail",
    ),
]
