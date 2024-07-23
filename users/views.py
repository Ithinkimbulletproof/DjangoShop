from django.views.generic import CreateView, DetailView, UpdateView, View
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import RegistrationForm, PasswordChangeForm
from .models import User
import random


class UserProfileView(DetailView):
    model = User
    template_name = 'users/user_profile.html'
    context_object_name = 'user'


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        send_mail(
            'Welcome to our site',
            'Thank you for registering.',
            'from@example.com',
            [form.instance.email],
            fail_silently=False,
        )
        return response


class CustomLoginView(LoginView):
    template_name = 'users/login.html'


class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return self.request.user


class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return super().form_valid(form)


class CombinedPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error'] = self.request.session.get('error')
        return context

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            request.session['error'] = 'User not found'
            return self.get(request)

        new_password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        user.set_password(new_password)
        user.save()

        send_mail(
            'Password Reset',
            f'Your new password is {new_password}',
            'from@example.com',
            [email],
            fail_silently=False,
        )

        request.session['success'] = 'New password sent to your email'
        return super().post(request, *args, **kwargs)
