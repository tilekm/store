from django.contrib.auth.views import LogoutView, login_required
from django.urls import path

from users.views import (EmailVerificationView, UserLoginView,
                         UserPasswordChangeDoneView, UserPasswordChangeView,
                         UserPasswordResetDoneView, UserPasswordResetView,
                         UserProfileView, UserRegistrationView)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', login_required(UserProfileView.as_view()), name='profile'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='verification'),

    # Password Reset Email Send
    path('password/reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    # Password Reset
    path('password/change/<uidb64>/<token>/', UserPasswordChangeView.as_view(), name='password_reset_confirm'),
    path('password/change/done/', UserPasswordChangeDoneView.as_view(), name='password_reset_complete'),
]
