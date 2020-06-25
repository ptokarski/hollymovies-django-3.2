from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import (
    SignUpForm, SubmittableAuthenticationForm, SubmittablePasswordChangeForm
)
from hollymovies.mixins import SuccessMessagedFormMixin, TitleMixin


class SubmittableLoginView(TitleMixin, SuccessMessagedFormMixin, LoginView):
    title = 'Login'
    success_message = 'Successfully logged in!'
    form_class = SubmittableAuthenticationForm
    template_name = 'form.html'


class SubmittablePasswordChangeView(
    TitleMixin, SuccessMessagedFormMixin, PasswordChangeView
):
    title = 'Password Change'
    success_message = 'Password successfully changed!'
    form_class = SubmittablePasswordChangeForm
    template_name = 'form.html'
    success_url = reverse_lazy('index')


class SuccessMessagedLogoutView(LogoutView):
    def get_next_page(self):
        result = super().get_next_page()
        messages.success(self.request, 'Successfully logged out!')
        return result


class SignUpView(TitleMixin, SuccessMessagedFormMixin, CreateView):
    title = 'Sign Up'
    success_message = 'Successfully signed up!'
    template_name = 'form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')
