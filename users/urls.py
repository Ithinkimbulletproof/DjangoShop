from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    UserProfileView,
    RegistrationView,
    UserUpdateView,
    CustomPasswordChangeView,
    CombinedPasswordResetView,
    CustomLoginView,
    VerifyEmailView,
    LoginView,
)

urlpatterns = [
    path("verify/<token>/", VerifyEmailView.as_view(), name="verify_email"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("profile/edit/", UserUpdateView.as_view(), name="user_update"),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/", CustomPasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", CombinedPasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
