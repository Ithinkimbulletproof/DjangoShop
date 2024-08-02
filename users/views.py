from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import View, CreateView

from .forms import (
    CustomLoginForm,
    CustomPasswordChangeForm,
    RegistrationForm,
)
from .models import User


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        self.send_verification_email(user)
        messages.success(
            self.request,
            "Registration successful. Please check your email to verify your account.",
        )
        return response

    def send_verification_email(self, user):
        verification_link = (
            f"{settings.SITE_URL}/users/verify/{user.verification_token}/"
        )
        subject = "Email Verification"
        message = render_to_string(
            "users/email_verification.html",
            {"user": user, "verification_link": verification_link},
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )


class VerifyEmailView(View):
    def get(self, request, token, *args, **kwargs):
        try:
            user = User.objects.get(verification_token=token)
            user.email_verified = True
            user.save()
            message = "Email verified successfully. You can now log in."
        except User.DoesNotExist:
            message = "Invalid verification token. Please try again."

        return render(request, "users/verify_email.html", {"message": message})


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "users/login.html"

    def form_valid(self, form):
        user = form.get_user()
        if not user.email_verified:
            form.add_error(None, "Email not verified. Please check your email.")
            return self.form_invalid(form)
        return super().form_valid(form)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "users/password_change_form.html"
    success_url = reverse_lazy("password_change_done")


class CustomPasswordResetView(PasswordResetView):
    template_name = "users/password_reset_form.html"
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
