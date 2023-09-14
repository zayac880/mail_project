from django.urls import path

from contacts.apps import ContactsConfig
from contacts.views import (
    ContactCreateView, ContactListView,
    ContactDetailView, ContactUpdateView, ContactDeleteView,
    ListsCreateView, ListsListView,
    ListsDetailView, ListsUpdateView, ListsDeleteView
)

app_name = ContactsConfig.name

urlpatterns = [
    path(
        'create/',
        ContactCreateView.as_view(),
        name='create_contact'
    ),
    path(
        'list/',
        ContactListView.as_view(),
        name='list_contact'
    ),
    path(
        'detail/<int:pk>',
        ContactDetailView.as_view(),
        name='detail_contact'
    ),
    path(
        'update/<int:pk>',
        ContactUpdateView.as_view(),
        name='update_contact'
    ),
    path(
        'delete/<int:pk>',
        ContactDeleteView.as_view(),
        name='delete_contacts'
    ),
    path(
        'list/create/',
        ListsCreateView.as_view(),
        name='create_list'
    ),
    path(
        'list/view/',
        ListsListView.as_view(),
        name='list_list'
    ),
    path(
        'list/detail/<int:pk>',
        ListsDetailView.as_view(),
        name='detail_list'
    ),
    path(
        'list/update/<int:pk>',
        ListsUpdateView.as_view(),
        name='update_list'
    ),
    path(
        'list/delete/<int:pk>',
        ListsDeleteView.as_view(),
        name='delete_list'
    ),
]
