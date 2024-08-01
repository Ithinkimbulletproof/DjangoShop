from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegistrationView, VerifyEmailView, CustomLoginView, CustomPasswordChangeView, CustomPasswordResetView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("verify/<token>/", VerifyEmailView.as_view(), name="verify_email"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    path("password_change/", CustomPasswordChangeView.as_view(), name="password_change"),
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
