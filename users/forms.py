from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm as AuthPasswordChangeForm,
)
from .models import User


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
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"autofocus": True})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = forms.HiddenInput()
        self.fields["username"].label = "Email"


class PasswordChangeForm(AuthPasswordChangeForm):
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
