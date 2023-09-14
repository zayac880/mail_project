from django.urls import path

from frontend.apps import FrontendConfig
from frontend.views import IndexPageView

app_name = FrontendConfig.name

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
]
