from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm as AuthPasswordChangeForm,
)
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from .models import User
import random
import string


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "phone",
            "country",
            "avatar",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.email_verified = False
        if commit:
            user.save()
            self.send_verification_email(user)
        return user

    def send_verification_email(self, user):
        verification_code = user.verification_token
        subject = "Activate your account"
        message = (f"Hi {user.username},\n\nPlease use the following "
                   f"link to verify your email address:\n\n{settings.SITE_URL}/verify/{verification_code}/\n\nThank you!")
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )


class CustomLoginForm(AuthenticationForm):
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"autofocus": True})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = forms.HiddenInput()
        self.fields["username"].label = "Email"
        self.fields["username"].initial = self.data.get("email")

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': 'email'},
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class CustomPasswordChangeForm(AuthPasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Old Password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    new_password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Confirm New Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        new_password_confirm = cleaned_data.get("new_password_confirm")

        if (
            new_password
            and new_password_confirm
            and new_password != new_password_confirm
        ):
            raise forms.ValidationError("New passwords do not match")

        return cleaned_data
