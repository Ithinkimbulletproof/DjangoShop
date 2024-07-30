from django.views.generic import CreateView, DetailView, UpdateView, View
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.contrib.auth import update_session_auth_hash, login
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.template.loader import render_to_string
from .forms import RegistrationForm, CustomPasswordChangeForm, CustomLoginForm
from .models import User
import random
import string

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/user_profile.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user

class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("home")

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
        verification_link = f"{settings.SITE_URL}/users/verify/{user.verification_token}/"
        subject = "Email Verification"
        message = render_to_string(
            "users/email_verification.html",
            {
                "user": user,
                "verification_link": verification_link,
            },
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
        except User.DoesNotExist:
            messages.error(request, "Invalid verification token.")
            return redirect("login")

        user.email_verified = True
        user.save()
        messages.success(request, "Email verified successfully.")
        return redirect("login")


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("profile")

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(CustomLoginView, self).form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "avatar",
        "phone",
        "country",
    ]
    template_name = "users/user_update.html"
    success_url = reverse_lazy("user_profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Profile updated successfully.")
        return response

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "users/password_change.html"
    success_url = reverse_lazy("password_change_done")

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, "Password changed successfully.")
        return super().form_valid(form)

class CombinedPasswordResetView(PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    subject_template_name = "users/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["error"] = self.request.session.get("error")
        return context

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            request.session["error"] = "User not found"
            return self.get(request)

        new_password = "".join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )
        user.set_password(new_password)
        user.save()

        send_mail(
            "Password Reset",
            f"Your new password is {new_password}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        messages.success(request, "New password sent to your email.")
        return super().post(request, *args, **kwargs)
