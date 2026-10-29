from django.contrib import admin
from django.urls import path, include
from apps.consumer_protection import urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(urls)),
]
