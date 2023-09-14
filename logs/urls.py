from django.urls import path

from logs.apps import LogsConfig
from logs.views import LoggingListView, LoggingDeleteView

app_name = LogsConfig.name

urlpatterns = [
    path(
        'list/',
        LoggingListView.as_view(),
        name='logs_list'
    ),
    path(
        'delete/<int:pk>',
        LoggingDeleteView.as_view(),
        name='delete_logs'
    ),
]
