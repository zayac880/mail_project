from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from mailing.forms import MailingForm, MailingSettingsForm
from mailing.models import Mailing, MailingSettings
from mailing.service import create_cron_jobs, remove_cron_jobs


class MailingCreateView(
    LoginRequiredMixin, CreateView
):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailings:list_mailing')

    permission_required = 'mailing.add_mailing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MailingFormset = inlineformset_factory(
            Mailing,
            MailingSettings,
            form=MailingSettingsForm,
            extra=1,
            can_delete=False
        )
        if self.request.method == 'POST':
            mailing_formset = MailingFormset(
                self.request.POST,
                instance=self.object
            )
        else:
            mailing_formset = MailingFormset(instance=self.object)

        context['mailing_formset'] = mailing_formset

        return context

    def form_valid(self, form):
        context_data = self.get_context_data()
        form.instance.user = self.request.user
        mailing_formset = context_data['mailing_formset']

        self.object = form.save(commit=False)
        self.object.save()

        mailing_formset.instance = self.object
        mailing_data = mailing_formset.save(commit=False)

        if mailing_data:
            mailing_settings_data = mailing_data[0]
        else:
            mailing_settings_data = MailingSettings()

        mailing_settings, created = MailingSettings.objects.get_or_create(
            mailing=self.object,
            defaults={
                'mailing_periods': mailing_settings_data.mailing_periods,
                'status': mailing_settings_data.status,
                'start_date': mailing_settings_data.start_date,
                'mailing_time': mailing_settings_data.mailing_time,
                'mailing_week_day_num': mailing_settings_data.mailing_week_day_num,
                'end_date': mailing_settings_data.end_date,
                'cron_setting': mailing_settings_data.cron_setting,
            }
        )
        self.object.setting = mailing_settings
        mailing_settings.save()

        return super().form_valid(form)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='manager').exists():
            queryset = queryset.all()
        else:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    success_url = reverse_lazy('mailings:detail_mailing')

    permission_required = 'mailing.view_mailing'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='manager').exists():
            queryset = queryset.filter(
                id=self.kwargs.get('pk'),
            )
        else:
            queryset = queryset.filter(
                id=self.kwargs.get('pk'),
                user=self.request.user
            )

        return queryset


class MailingUpdateView(
    LoginRequiredMixin, UpdateView
):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailings:list_mailing')

    def get_context_data(self, **kwargs):
        if self.request.user.groups.filter(name='manager').exists():
            raise Http404
        context = super().get_context_data(**kwargs)
        MailingFormset = inlineformset_factory(
            Mailing,
            MailingSettings,
            form=MailingSettingsForm,
            extra=1,
            can_delete=False
        )
        if self.request.method == 'POST':
            mailing_formset = MailingFormset(
                self.request.POST,
                instance=self.object
            )
        else:
            mailing_formset = MailingFormset(instance=self.object)

        context['mailing_formset'] = mailing_formset

        return context

    def form_valid(self, form):
        context_data = self.get_context_data()
        mailing_formset = context_data['mailing_formset']

        self.object = form.save(commit=False)
        if mailing_formset.is_valid():
            mailing_formset.instance = self.object
            mailing_formset.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class MailingDeleteView(
    LoginRequiredMixin, DeleteView
):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:list_mailing')

    def get_context_data(self, **kwargs):
        if self.request.user.groups.filter(name='manager').exists():
            raise Http404
        context = super().get_context_data(**kwargs)
        return context


def start_stop_mailing(request, *args, **kwargs):
    # TODO: реализовать механизм включения / выключения рассылки с
    #       удалением задачи из списка CRONJOBS и из crontab
    mailing_pk = kwargs.pop('pk')
    try:
        mailing = Mailing.objects.get(pk=mailing_pk)
    except Mailing.DoesNotExist:
        pass

    if mailing.setting.status == 'completed':
        if mailing.setting.start_date <= date.today() <= mailing.setting.end_date:
            mailing.setting.status = 'running'
            create_cron_jobs(mailing)
        else:
            print('mailing out of date')
    elif mailing.setting.status == 'running':
        mailing.setting.status = 'completed'
        remove_cron_jobs(mailing)
    mailing.setting.save()

    return redirect('mailings:list_mailing')
