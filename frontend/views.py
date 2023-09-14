import random
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from blog.models import Posts
from contacts.models import ContactsList
from contacts.views import get_list_active_contacts
from mailing.models import Mailing


# Create your views here.


class IndexPageView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'frontend/index.html'
    context_object_name = 'mailings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.filter(name='manager').exists():
            context['total_mailings'] = Mailing.objects.filter(
            ).count()
            context['total_active_mailings'] = Mailing.objects.filter(
                setting__status='running'
            ).count()
        else:
            context['total_mailings'] = Mailing.objects.filter(
                user=self.request.user
            ).count()
            context['total_active_mailings'] = Mailing.objects.filter(
                user=self.request.user,
                setting__status='running'
            ).count()

        context['total_inactive_mailings'] = context['total_mailings'] - \
                                             context['total_active_mailings']

        list_of_contacts = ContactsList.objects.filter(
            list=self.kwargs.get('pk')
        )
        contact_activity_status = get_list_active_contacts(list_of_contacts)

        context['contact_activity_status'] = contact_activity_status

        current_date = datetime.now()
        thirty_days_ago = current_date - timedelta(days=30)
        random.seed(int(current_date.timestamp() * 1000))

        last_month_posts = list(
            Posts.objects.filter(
                creation_date__gte=thirty_days_ago,
                is_published=True
            ).all()
        )
        random_three_posts = random.sample(last_month_posts, 3)
        context['random_three_posts'] = random_three_posts
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            user=self.request.user,
            setting__status='running'
        )
        return queryset
