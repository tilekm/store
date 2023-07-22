from django.contrib import admin

from products.admin import BasketAdmin
from users.models import EmailVerification, User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']
    inlines = [BasketAdmin]


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'expiration']
    fields = ['code', 'user', 'expiration', 'created_timestamp']
    readonly_fields = ['created_timestamp']
