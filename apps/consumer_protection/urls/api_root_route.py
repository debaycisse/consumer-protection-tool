from rest_framework.urls import path
from apps.consumer_protection.views.api_root import APIViewRoot

urlpatterns = [path("", APIViewRoot.as_view(), name="api-root")]
