from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from users.forms import RegisterUserForm
from .models import Subscription

User = get_user_model()

admin.site.register(Subscription)

@admin.register(User)
class UsersAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'avatar'),
        }),
    )
    add_form = RegisterUserForm
