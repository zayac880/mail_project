from typing import Tuple

from django.contrib import admin

from contacts.models import ContactsList, Lists, Contacts


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display: Tuple[str] = (
        'id',
        'email',
        'telephone',
        'status',
        'user',
        'date_added',
    )

    list_display_links: Tuple[str] = ('email',)

    list_filter: Tuple[str] = (
        'status',
        'date_added',
    )

    search_fields: Tuple[str] = ('email', 'telephone', 'users',)


@admin.register(Lists)
class ListsAdmin(admin.ModelAdmin):
    list_display: Tuple[str] = (
        'id',
        'name',
        'date_added',
    )

    list_display_links: Tuple[str] = ('name',)

    list_filter: Tuple[str] = (
        'date_added',
    )

    search_fields: Tuple[str] = ('name',)


@admin.register(ContactsList)
class ContactsListAdmin(admin.ModelAdmin):
    list_display: Tuple[str] = (
        'id',
        'contact',
        'list',
    )

    list_display_links: Tuple[str] = ('contact',)

    list_filter: Tuple[str] = (
        'contact',
        'list',
    )

    search_fields: Tuple[str] = ('contact', 'list',)
