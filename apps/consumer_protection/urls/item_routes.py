from rest_framework.urls import path
from apps.consumer_protection.views.items_views import (
    ItemListCreateView,
    ItemRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("items", ItemListCreateView.as_view(), name="item-list"),
    path(
        "items/<str:item_id>",
        ItemRetrieveUpdateDestroyView.as_view(),
        name="item-detail",
    ),
]
