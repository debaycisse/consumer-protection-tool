from rest_framework.urls import path
from apps.consumer_protection.views.users_views import (
    SignInView,
    SignOutView,
    RegistrationView,
    ListUsersView,
    RetrieveUpdateUserView,
)

urlpatterns = [
    path("users", ListUsersView.as_view(), name="user-list"),
    path("users/signin", SignInView.as_view(), name="sign-in"),
    path("users/signout", SignOutView.as_view(), name="sign-out"),
    path("users/register", RegistrationView.as_view(), name="register"),
    path(
        "users/<str:user_id>",
        RetrieveUpdateUserView.as_view(),
        name="user-detail",
    ),
]
