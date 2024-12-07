from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = [
        (
            None,
            {
                'fields': (
                    'username',
                    'password',
                    'is_moderator',
                    'is_admin',
                    'category',
                    'ranking',
                    'street_address',
                    'city',
                    'state',
                    'postal_code',
                    'country',
                )
            },
        )
    ]


admin.site.register(CustomUser, CustomUserAdmin)
