from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (
    MailingCreateView, MailingDeleteView,
    MailingListView, MailingUpdateView, MailingDetailView, start_stop_mailing
)

app_name = MailingConfig.name

urlpatterns = [
    path(
        'create/',
        MailingCreateView.as_view(),
        name='create_mailing'
    ),
    path(
        'list/',
        MailingListView.as_view(),
        name='list_mailing'
    ),
    path(
        'detail/<int:pk>',
        MailingDetailView.as_view(),
        name='detail_mailing'
    ),
    path(
        'update/<int:pk>',
        MailingUpdateView.as_view(),
        name='update_mailing'
    ),
    path(
        'delete/<int:pk>',
        MailingDeleteView.as_view(),
        name='delete_mailing'
    ),
    path('start/<int:pk>', start_stop_mailing, name='start_mailing'),
]
