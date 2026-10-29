from apps.consumer_protection.urls import comment_routes
from apps.consumer_protection.urls import feedback_routes
from apps.consumer_protection.urls import item_routes
from apps.consumer_protection.urls import leaderboard_routes
from apps.consumer_protection.urls import user_routes
from apps.consumer_protection.urls import api_root_route

urlpatterns = comment_routes.urlpatterns + feedback_routes.urlpatterns
urlpatterns += item_routes.urlpatterns + leaderboard_routes.urlpatterns
urlpatterns += user_routes.urlpatterns + api_root_route.urlpatterns
