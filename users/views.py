from django.contrib.auth.views import (LoginView, PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from users.forms import (UserLoginForm, UserPasswordResetForm,
                         UserPasswordSetForm, UserProfileForm,
                         UserRegistrationForm)
from users.models import EmailVerification, User

# Create your views here.


class UserRegistrationView(SuccessMessageMixin, TitleMixin, CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    title = 'Store - Регистрация'
    success_message = 'Вы успешно зарегистрировались!'
    success_url = reverse_lazy('users:login')


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Профиль'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.object.id])


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.filter(email=kwargs['email']).last()
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and now() < email_verification.last().expiration:
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'


# Password Reset and Change
class UserPasswordResetView(TitleMixin, PasswordResetView):
    template_name = 'users/password-reset.html'
    title = 'Восстановление пароля'
    form_class = UserPasswordResetForm
    from_email = 'project.python@yandex.ru'
    email_template_name = 'users/password_reset_email_subject.html'
    extra_context = {
        'domain': '127.0.0.1:8000',
        'site_name': 'Store',
    }
    extra_email_context = {
        'domain': '127.0.0.1:8000',
        'site_name': 'Store',
    }
    success_url = reverse_lazy('users:password_reset_done')


class UserPasswordResetDoneView(TitleMixin, PasswordResetDoneView):
    template_name = 'users/password-reset-done.html'
    title = 'Восстановление пароля'


class UserPasswordChangeView(TitleMixin, PasswordResetConfirmView):
    template_name = 'users/password-reset-confirm.html'
    form_class = UserPasswordSetForm
    success_url = reverse_lazy('users:password_reset_complete')


class UserPasswordChangeDoneView(TitleMixin, PasswordResetCompleteView):
    template_name = 'users/password-reset-confirm-done.html'
