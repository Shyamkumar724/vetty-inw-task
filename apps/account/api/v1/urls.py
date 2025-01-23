from django.urls import path
from apps.account.api.v1.views import SignUpView, LoginView, LogoutView

urlpatterns = [
    path("v1/register", SignUpView.as_view(), name="register_v1"),
    path("v1/login", LoginView.as_view(), name="login_v1"),
    path("v1/logout", LogoutView.as_view(), name="logout_v1"),
]
