from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import DetailView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomLoginForm, CustomPasswordChangeForm
from .models import User

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Profile updated successfully.")
        return response

class CustomLoginView(auth_views.LoginView):
    form_class = CustomLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('profile')

class CustomPasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Password changed successfully.")
        return response

class CombinedPasswordResetView(auth_views.PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User not found")
            return self.get(request)

        new_password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
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
        return redirect(self.success_url)

class VerifyEmailView(View):
    def get(self, request, token, *args, **kwargs):
        try:
            user = User.objects.get(verification_token=token)
        except User.DoesNotExist:
            messages.error(request, "Invalid verification token.")
            return redirect('login')

        user.email_verified = True
        user.save()
        messages.success(request, "Email verified successfully.")
        return redirect('login')
