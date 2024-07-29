from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm as AuthPasswordChangeForm,
)
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
        user.email_verified = False  # Ensure the email is not verified yet
        if commit:
            user.save()
            self.send_verification_email(user)
        return user

    def send_verification_email(self, user):
        verification_code = "".join(
            random.choices(string.ascii_letters + string.digits, k=32)
        )
        user.verification_code = verification_code
        user.save()

        subject = "Activate your account"
        message = f"Hi {user.username},\n\nPlease use the following link to verify your email address:\n\n{settings.SITE_URL}/verify/{verification_code}/\n\nThank you!"
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = forms.HiddenInput()
        self.fields["username"].label = "Email"
        self.fields["username"].initial = self.data.get("email")


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
