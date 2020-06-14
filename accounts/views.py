from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy

from accounts.forms import (
    SubmittableAuthenticationForm, SubmittablePasswordChangeForm
)


class SubmittableLoginView(LoginView):
    form_class = SubmittableAuthenticationForm
    template_name = 'form.html'


class SubmittablePasswordChangeView(PasswordChangeView):
    form_class = SubmittablePasswordChangeForm
    template_name = 'form.html'
    success_url = reverse_lazy('index')
