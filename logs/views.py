from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from logs.models import Logging


# Create your views here.


class LoggingListView(ListView):
    model = Logging
    template_name = 'logs/logs_detail.html'
    context_object_name = 'logs'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(mailing__user=self.request.user)
        return queryset


class LoggingDeleteView(DeleteView):
    model = Logging
    template_name = 'logs/logs_confirm_delete.html'
    success_url = reverse_lazy('logs:logs_list')
