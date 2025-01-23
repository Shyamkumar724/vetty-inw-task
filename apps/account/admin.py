from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.account.models import Account

# Register your models here.


@admin.register(Account)
class AccountAdmin(UserAdmin):
    pass
