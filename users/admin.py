from typing import Tuple

from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display: Tuple[str] = (
        'id',
        'first_name',
        'last_name',
        'email',
        'telephone',
        'country',
        'date_added',
        'last_modified',
        'is_staff',
        'is_active',
        'is_superuser',
        'is_verified',
    )

    list_display_links: Tuple[str] = ('first_name', 'last_name')

    list_filter: Tuple[str] = (
        'last_name',
        'is_staff',
        'is_active',
        'is_superuser',
        'date_added',
        'is_verified',
    )

    search_fields: Tuple[str] = (
        'first_name',
        'last_name',
        'email',
    )
