from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse

# Create your models here.


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'Email подтверждение для {self.user.email}'

    def send_verification_email(self):
        subject = f'Verification email for {self.user.username}'
        link = reverse('users:password-reset', kwargs={'pk': self.user.id, 'code': self.code})
        full_link = settings.DOMAIN_NAME + link
        message = 'Here the link for {}, go to the link to verify your email: {}'.format(self.user.email,
                                                                                         full_link)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )
