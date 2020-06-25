from django.urls import path

from accounts.views import (
    SignUpView, SubmittableLoginView, SubmittablePasswordChangeView,
    SuccessMessagedLogoutView
)

app_name = 'accounts'
urlpatterns = [
    path('login/', SubmittableLoginView.as_view(), name='login'),
    path('logout/', SuccessMessagedLogoutView.as_view(), name='logout'),
    path(
        'password-change/', SubmittablePasswordChangeView.as_view(),
        name='password_change'
    ),
    path('sign-up/', SignUpView.as_view(), name='sign_up')
]
